import pandas as pd
import numpy as np
from src.transform.base_transformer import BaseTransformer
from src.utils.date_utils import get_campana_agricola, es_epoca_siembra, es_epoca_cosecha


class DataEnricher(BaseTransformer):
    def __init__(self):
        super().__init__("enricher")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def add_campana_agricola(
        self,
        df: pd.DataFrame,
        anio_col: str,
        mes_col: str,
    ) -> pd.DataFrame:
        df["campana_agricola"] = df.apply(
            lambda row: get_campana_agricola(int(row[anio_col]), int(row[mes_col])),
            axis=1,
        )
        df["es_epoca_siembra"] = df[mes_col].apply(lambda m: es_epoca_siembra(int(m)))
        df["es_epoca_cosecha"] = df[mes_col].apply(lambda m: es_epoca_cosecha(int(m)))
        self.logger.info("Campana agricola y epocas calculadas")
        return df

    def calculate_rendimiento(
        self,
        df: pd.DataFrame,
        produccion_col: str,
        superficie_col: str,
    ) -> pd.DataFrame:
        mask = df[superficie_col] > 0
        df.loc[mask, "rendimiento_calculado"] = (
            df.loc[mask, produccion_col] * 1000 / df.loc[mask, superficie_col]
        )
        df.loc[~mask, "rendimiento_calculado"] = 0
        return df

    def calculate_variacion_precio(
        self,
        df: pd.DataFrame,
        precio_col: str,
        group_cols: list,
        sort_col: str,
    ) -> pd.DataFrame:
        df = df.sort_values(group_cols + [sort_col])
        df["precio_anterior"] = df.groupby(group_cols)[precio_col].shift(1)
        mask = df["precio_anterior"] > 0
        df.loc[mask, "variacion_pct"] = (
            (df.loc[mask, precio_col] - df.loc[mask, "precio_anterior"])
            / df.loc[mask, "precio_anterior"]
            * 100
        ).round(2)
        df.loc[~mask, "variacion_pct"] = 0
        df = df.drop(columns=["precio_anterior"])
        self.logger.info("Variacion de precios calculada")
        return df

    def calculate_volatilidad(
        self,
        df: pd.DataFrame,
        precio_col: str,
        group_cols: list,
        window: int = 12,
    ) -> pd.DataFrame:
        df = df.sort_values(group_cols + ["anio", "mes"])
        df["volatilidad"] = (
            df.groupby(group_cols)[precio_col]
            .transform(lambda x: x.rolling(window=window, min_periods=3).std())
            .round(2)
        )
        self.logger.info(f"Volatilidad calculada (ventana={window} periodos)")
        return df
