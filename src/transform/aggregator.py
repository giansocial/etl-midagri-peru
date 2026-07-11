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
        agg = df.groupby(depto_col).agg(
            produccion_total=("produccion_toneladas", "sum"),
            superficie_total=("superficie_cosechada_ha", "sum"),
            rendimiento_promedio=("rendimiento_kg_ha", "mean"),
            precio_promedio=("precio_chacra_soles", "mean"),
            num_cultivos=("cultivo", "nunique"),
        ).reset_index()

        agg = agg.round(2)
        self.logger.info(f"Agregacion por region: {len(agg)} departamentos")
        return agg

    def aggregate_by_cultivo(
        self,
        df: pd.DataFrame,
        cultivo_col: str = "cultivo",
    ) -> pd.DataFrame:
        agg = df.groupby(cultivo_col).agg(
            produccion_total=("produccion_toneladas", "sum"),
            superficie_total=("superficie_cosechada_ha", "sum"),
            rendimiento_promedio=("rendimiento_kg_ha", "mean"),
            precio_min=("precio_chacra_soles", "min"),
            precio_max=("precio_chacra_soles", "max"),
            precio_promedio=("precio_chacra_soles", "mean"),
            num_departamentos=("departamento", "nunique"),
        ).reset_index()

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
