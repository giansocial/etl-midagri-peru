import pandas as pd
from unidecode import unidecode
from src.transform.base_transformer import BaseTransformer
from src.models.enums import DEPARTAMENTO_REGION, CULTIVO_CATEGORIA


class DataNormalizer(BaseTransformer):
    def __init__(self):
        super().__init__("normalizer")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.normalize_text_columns(df)
        return df

    def normalize_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        str_columns = df.select_dtypes(include=["object"]).columns
        for col in str_columns:
            df[col] = df[col].apply(
                lambda x: self._normalize_text(x) if isinstance(x, str) else x
            )
        return df

    def normalize_departamento(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        mapping = self._build_departamento_mapping()
        df[col] = df[col].map(mapping).fillna(df[col])
        return df

    def add_region_natural(self, df: pd.DataFrame, depto_col: str) -> pd.DataFrame:
        df["region_natural"] = df[depto_col].map(
            lambda x: DEPARTAMENTO_REGION.get(x, "").value
            if x in DEPARTAMENTO_REGION else ""
        )
        unmapped = df[df["region_natural"] == ""][depto_col].unique()
        if len(unmapped) > 0:
            self.logger.warning(f"Departamentos sin region natural: {unmapped}")
        return df

    def add_categoria_cultivo(self, df: pd.DataFrame, cultivo_col: str) -> pd.DataFrame:
        df["categoria"] = df[cultivo_col].str.lower().map(
            lambda x: CULTIVO_CATEGORIA.get(x, "").value
            if x in CULTIVO_CATEGORIA else "Otros"
        )
        return df

    def _normalize_text(self, text: str) -> str:
        text = text.strip()
        text = " ".join(text.split())
        return text.title()

    def _build_departamento_mapping(self) -> dict:
        mapping = {}
        for depto in DEPARTAMENTO_REGION:
            mapping[depto.lower()] = depto
            mapping[depto.upper()] = depto
            mapping[unidecode(depto).lower()] = depto
            mapping[unidecode(depto).upper()] = depto
        return mapping
