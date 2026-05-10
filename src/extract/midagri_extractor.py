from pathlib import Path
from typing import Optional
import pandas as pd
from src.extract.base_extractor import BaseExtractor


COLUMN_MAPS = {
    "DATA_VBP": {
        "TXT_ANIO": "anio",
        "COD_DEPARTAMENTO": "cod_departamento",
        "DEPARTAMENTO": "departamento",
        "PRODUCTO": "cultivo",
        "MES": "mes_nombre",
        "PRODUCCION": "produccion_toneladas",
        "PRECIO 2007": "precio_base_2007",
        "VBP": "vbp_millones",
        "TIPO": "tipo_producto",
    },
    "SISCOMEX": {
        "TIPO": "tipo_operacion",
        "COD_ARANCEL": "cod_arancel",
        "TXT_NARANCEL": "producto",
        "TEX_PAIS_DESTINO": "pais",
        "COD_ANIO": "anio",
        "COD_MES": "mes",
        "CAN_PNETO": "peso_neto_tm",
        "CAN_PBRUTO": "peso_bruto_tm",
        "VALOR_FOB": "valor_fob_miles_usd",
        "VALOR_CIF": "valor_cif_miles_usd",
    },
    "SISAP": {
        "COD_GENERO": "cod_cultivo",
        "COD_ANIO": "anio",
        "TXT_DSCGENERO": "cultivo",
        "TXT_DSCVARIEDAD": "variedad",
        "PRECIO_KG": "precio_kg_soles",
    },
    "SISAGRI_OTROS_CULTIVOS": {
        "CULTIVO": "cultivo",
        "Dpto": "departamento",
        "Año": "anio",
        "MES": "mes",
        "Valores": "indicador",
        "Total": "valor",
    },
}

MES_NOMBRE_A_NUMERO = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

SISAGRI_COLUMNS = [
    "anio", "mes", "cod_ubigeo", "departamento", "provincia",
    "distrito", "cod_cultivo", "cultivo", "superficie_sembrada",
    "superficie_cosechada", "produccion_toneladas", "rendimiento_kg_ha",
    "precio_chacra_soles",
]


class MidagriExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("midagri")

    def extract_vbp(self, filepath: Path) -> pd.DataFrame:
        self.logger.info(f"Extrayendo VBP: {filepath.name}")
        df = pd.read_excel(filepath, engine="openpyxl")
        df = df.rename(columns=COLUMN_MAPS["DATA_VBP"])

        df["mes"] = df["mes_nombre"].str.lower().map(MES_NOMBRE_A_NUMERO)
        df = df.dropna(subset=["mes"])
        df["mes"] = df["mes"].astype(int)
        df["anio"] = df["anio"].astype(int)

        df = df[df["tipo_producto"] == "AGRÍCOLA"]
        df = df.drop(columns=["mes_nombre"], errors="ignore")

        self.logger.info(f"VBP extraido: {len(df)} registros agricolas")
        self.validate_output(df)
        return df

    def extract_siscomex(self, filepath: Path) -> pd.DataFrame:
        self.logger.info(f"Extrayendo SISCOMEX: {filepath.name}")
        df = pd.read_excel(filepath, engine="openpyxl")
        df = df.rename(columns=COLUMN_MAPS["SISCOMEX"])

        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
        df = df.dropna(subset=["anio", "mes"])
        df["anio"] = df["anio"].astype(int)
        df["mes"] = df["mes"].astype(int)

        for col in ["peso_neto_tm", "peso_bruto_tm", "valor_fob_miles_usd", "valor_cif_miles_usd"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        self.logger.info(f"SISCOMEX extraido: {len(df)} registros")
        self.validate_output(df)
        return df

    def extract_sisap(self, filepath: Path) -> pd.DataFrame:
        self.logger.info(f"Extrayendo SISAP: {filepath.name}")
        df = pd.read_excel(filepath, engine="openpyxl")
        df = df.rename(columns=COLUMN_MAPS["SISAP"])

        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df["precio_kg_soles"] = pd.to_numeric(df["precio_kg_soles"], errors="coerce")
        df = df.dropna(subset=["anio", "precio_kg_soles"])
        df["anio"] = df["anio"].astype(int)

        self.logger.info(f"SISAP extraido: {len(df)} registros de precios")
        self.validate_output(df)
        return df

    def extract_sisagri_otros(self, filepath: Path) -> pd.DataFrame:
        self.logger.info(f"Extrayendo SISAGRI otros cultivos: {filepath.name}")
        df = pd.read_excel(filepath, engine="openpyxl")
        df = df.rename(columns=COLUMN_MAPS["SISAGRI_OTROS_CULTIVOS"])

        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
        df = df.dropna(subset=["anio", "mes"])
        df["anio"] = df["anio"].astype(int)
        df["mes"] = df["mes"].astype(int)

        pivoted = df.pivot_table(
            index=["cultivo", "departamento", "anio", "mes"],
            columns="indicador",
            values="valor",
            aggfunc="first",
        ).reset_index()

        column_remap = {
            "PRODUCCION (t)": "produccion_toneladas",
            "COSECHA (ha)": "superficie_cosechada",
            "SIEMBRA (ha)": "superficie_sembrada",
            "PRECIO_(Soles x kg)": "precio_chacra_soles",
            "PRODXPRECIO_": "valor_produccion",
        }
        pivoted = pivoted.rename(columns=column_remap)
        pivoted.columns.name = None

        self.logger.info(f"SISAGRI otros pivoteado: {len(pivoted)} registros")
        self.validate_output(pivoted)
        return pivoted

    def extract_sisagri(self, filepath: Path) -> pd.DataFrame:
        self.logger.info(f"Extrayendo SISAGRI principal: {filepath.name}")

        wb_sheets = pd.ExcelFile(filepath, engine="openpyxl").sheet_names
        self.logger.info(f"Hojas encontradas: {wb_sheets}")

        frames = []
        for sheet in wb_sheets:
            df = pd.read_excel(filepath, sheet_name=sheet, engine="openpyxl", header=None)
            if df.empty or len(df.columns) < 8:
                continue

            first_row = df.iloc[0].tolist()
            if all(v is None or str(v).strip() == "" for v in first_row[1:]):
                df = df.iloc[1:]

            if len(df.columns) >= 13:
                df.columns = SISAGRI_COLUMNS
            else:
                self.logger.warning(f"Hoja {sheet}: {len(df.columns)} columnas, esperadas 13")
                continue

            df = df.dropna(subset=["departamento", "cultivo"], how="all")
            frames.append(df)

        if not frames:
            self.logger.warning("SISAGRI: ninguna hoja con datos validos")
            return pd.DataFrame()

        result = pd.concat(frames, ignore_index=True)

        for col in ["anio", "mes"]:
            result[col] = pd.to_numeric(result[col], errors="coerce")
        result = result.dropna(subset=["anio"])
        result["anio"] = result["anio"].astype(int)
        result["mes"] = pd.to_numeric(result["mes"], errors="coerce").fillna(0).astype(int)

        for col in ["superficie_sembrada", "superficie_cosechada", "produccion_toneladas",
                     "rendimiento_kg_ha", "precio_chacra_soles"]:
            if col in result.columns:
                result[col] = pd.to_numeric(result[col], errors="coerce").fillna(0)

        self.logger.info(f"SISAGRI extraido: {len(result)} registros")
        self.validate_output(result)
        return result

    def identify_file(self, filepath: Path) -> Optional[str]:
        name = filepath.stem.upper()
        if "VBP" in name:
            return "vbp"
        if "SISCOMEX" in name:
            return "siscomex"
        if "SISAP" in name:
            return "sisap"
        if "OTROS" in name:
            return "sisagri_otros"
        if "SISAGRI" in name:
            return "sisagri"
        return None
