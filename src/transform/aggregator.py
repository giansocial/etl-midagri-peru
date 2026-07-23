import pandas as pd
from src.transform.base_transformer import BaseTransformer


class DataAggregator(BaseTransformer):
    def __init__(self):
        super().__init__("aggregator")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def aggregate_by_region(
        self,
        df: pd.DataFrame,
        depto_col: str = "departamento",
    ) -> pd.DataFrame:
        agg_cols = {
            "produccion_total": ("produccion_toneladas", "sum"),
            "num_cultivos": ("cultivo", "nunique"),
        }

        superficie_col = (
            "superficie_cosechada_ha" if "superficie_cosechada_ha" in df.columns
            else "superficie_cosechada"
        )
        if superficie_col in df.columns:
            agg_cols["superficie_total"] = (superficie_col, "sum")

        rendimiento_col = (
            "rendimiento_kg_ha" if "rendimiento_kg_ha" in df.columns
            else "rendimiento_calculado"
        )
        if rendimiento_col in df.columns:
            agg_cols["rendimiento_promedio"] = (rendimiento_col, "mean")

        if "precio_chacra_soles" in df.columns:
            agg_cols["precio_promedio"] = ("precio_chacra_soles", "mean")

        agg = df.groupby(depto_col).agg(**agg_cols).reset_index()

        agg = agg.round(2)
        self.logger.info(f"Agregacion por region: {len(agg)} departamentos")
        return agg

    def aggregate_by_cultivo(
        self,
        df: pd.DataFrame,
        cultivo_col: str = "cultivo",
    ) -> pd.DataFrame:
        agg_cols = {
            "produccion_total": ("produccion_toneladas", "sum"),
        }

        superficie_col = (
            "superficie_cosechada_ha" if "superficie_cosechada_ha" in df.columns
            else "superficie_cosechada"
        )
        if superficie_col in df.columns:
            agg_cols["superficie_total"] = (superficie_col, "sum")

        rendimiento_col = (
            "rendimiento_kg_ha" if "rendimiento_kg_ha" in df.columns
            else "rendimiento_calculado"
        )
        if rendimiento_col in df.columns:
            agg_cols["rendimiento_promedio"] = (rendimiento_col, "mean")

        if "precio_chacra_soles" in df.columns:
            agg_cols["precio_min"] = ("precio_chacra_soles", "min")
            agg_cols["precio_max"] = ("precio_chacra_soles", "max")
            agg_cols["precio_promedio"] = ("precio_chacra_soles", "mean")

        if "departamento" in df.columns:
            agg_cols["num_departamentos"] = ("departamento", "nunique")

        agg = df.groupby(cultivo_col).agg(**agg_cols).reset_index()

        agg = agg.round(2)
        self.logger.info(f"Agregacion por cultivo: {len(agg)} cultivos")
        return agg

    def aggregate_temporal(
        self,
        df: pd.DataFrame,
        time_cols: list,
        value_cols: dict,
    ) -> pd.DataFrame:
        agg = df.groupby(time_cols).agg(**value_cols).reset_index()
        agg = agg.round(2)
        self.logger.info(f"Agregacion temporal: {len(agg)} periodos")
        return agg
