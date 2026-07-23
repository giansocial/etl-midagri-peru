from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from src.transform.base_transformer import BaseTransformer


class DataCleaner(BaseTransformer):
    def __init__(self):
        super().__init__("cleaner")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = self.remove_duplicates(df)
        df = self.strip_whitespace(df)
        self.log_changes(before, len(df))
        return df

    def remove_duplicates(
        self,
        df: pd.DataFrame,
        subset: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates(subset=subset, keep="first")
        duplicates = before - len(df)
        if duplicates > 0:
            self.logger.info(f"{duplicates} duplicados eliminados")
        return df

    def strip_whitespace(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        str_columns = df.select_dtypes(include=["object"]).columns
        for col in str_columns:
            df[col] = df[col].str.strip()
        return df

    def fill_nulls(
        self,
        df: pd.DataFrame,
        fill_map: Dict[str, any],
    ) -> pd.DataFrame:
        df = df.copy()
        for col, value in fill_map.items():
            if col in df.columns:
                null_count = df[col].isna().sum()
                if null_count > 0:
                    df[col] = df[col].fillna(value)
                    self.logger.info(f"{col}: {null_count} nulls rellenados con {value}")
        return df

    def convert_types(
        self,
        df: pd.DataFrame,
        type_map: Dict[str, str],
    ) -> pd.DataFrame:
        df = df.copy()
        for col, dtype in type_map.items():
            if col not in df.columns:
                continue
            try:
                if dtype == "float":
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                elif dtype == "int":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif dtype == "date":
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                elif dtype == "str":
                    df[col] = df[col].astype(str)
            except Exception as e:
                self.logger.warning(f"Error convirtiendo {col} a {dtype}: {e}")
        return df

    def remove_out_of_range(
        self,
        df: pd.DataFrame,
        ranges: Dict[str, tuple],
    ) -> pd.DataFrame:
        before = len(df)
        for col, (min_val, max_val) in ranges.items():
            if col not in df.columns:
                continue
            mask = (df[col] >= min_val) & (df[col] <= max_val)
            invalid = (~mask).sum()
            if invalid > 0:
                self.logger.warning(f"{col}: {invalid} valores fuera de rango [{min_val}, {max_val}]")
                df = df[mask | df[col].isna()]
        self.log_changes(before, len(df))
        return df
