from typing import Dict
import pandas as pd
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger("quality.profiler")


def profile_dataset(df: pd.DataFrame, name: str) -> Dict:
    profile = {
        "nombre": name,
        "filas": len(df),
        "columnas": len(df.columns),
        "memoria_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        "columnas_detalle": {},
    }

    for col in df.columns:
        col_info = {
            "tipo": str(df[col].dtype),
            "nulls": int(df[col].isna().sum()),
            "nulls_pct": round(df[col].isna().mean() * 100, 2),
            "unicos": int(df[col].nunique()),
        }

        if pd.api.types.is_numeric_dtype(df[col]):
            serie = df[col].dropna()
            if len(serie) > 0:
                col_info["min"] = float(serie.min())
                col_info["max"] = float(serie.max())
                col_info["media"] = round(float(serie.mean()), 2)
                col_info["mediana"] = round(float(serie.median()), 2)
                col_info["desv_std"] = round(float(serie.std()), 2)
                col_info["p25"] = round(float(serie.quantile(0.25)), 2)
                col_info["p75"] = round(float(serie.quantile(0.75)), 2)
                col_info["iqr"] = round(col_info["p75"] - col_info["p25"], 2)
                col_info["coef_variacion"] = (
                    round(float(serie.std() / serie.mean() * 100), 2)
                    if serie.mean() != 0 else 0
                )
                col_info["asimetria"] = round(float(serie.skew()), 2)
                col_info["curtosis"] = round(float(serie.kurtosis()), 2)

        if pd.api.types.is_string_dtype(df[col]):
            top_values = df[col].value_counts().head(5)
            col_info["top_valores"] = top_values.to_dict()

        profile["columnas_detalle"][col] = col_info

    logger.info(
        f"[{name}] Perfil: {profile['filas']} filas, "
        f"{profile['columnas']} columnas, "
        f"{profile['memoria_mb']} MB"
    )

    return profile


def detect_outliers_iqr(df: pd.DataFrame, col: str, factor: float = 1.5) -> pd.Series:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return (df[col] < lower) | (df[col] > upper)


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    return df[numeric_cols].corr().round(3)
