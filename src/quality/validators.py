from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd
from src.models.schemas import QualityReport
from src.utils.logger import setup_logger

logger = setup_logger("quality.validators")


def validate_dataset(
    df: pd.DataFrame,
    name: str,
    required_columns: List[str],
    numeric_ranges: Dict[str, Tuple[float, float]] = None,
) -> QualityReport:
    total_rows = len(df)

    missing_cols = [c for c in required_columns if c not in df.columns]
    if missing_cols:
        logger.error(f"[{name}] Columnas faltantes: {missing_cols}")

    null_count = {}
    for col in df.columns:
        nulls = int(df[col].isna().sum())
        if nulls > 0:
            null_count[col] = nulls

    duplicate_count = int(df.duplicated().sum())

    out_of_range = {}
    if numeric_ranges:
        for col, (min_val, max_val) in numeric_ranges.items():
            if col not in df.columns:
                continue
            invalid = int(((df[col] < min_val) | (df[col] > max_val)).sum())
            if invalid > 0:
                out_of_range[col] = invalid

    total_issues = sum(null_count.values()) + duplicate_count + sum(out_of_range.values())
    max_issues = total_rows * len(df.columns)
    quality_score = round((1 - total_issues / max_issues) * 100, 2) if max_issues > 0 else 100

    valid_rows = total_rows - duplicate_count

    report = QualityReport(
        dataset_name=name,
        total_rows=total_rows,
        valid_rows=valid_rows,
        null_count=null_count,
        duplicate_count=duplicate_count,
        out_of_range=out_of_range,
        quality_score=quality_score,
        timestamp=datetime.now().isoformat(),
    )

    logger.info(
        f"[{name}] Calidad: {quality_score}% | "
        f"Filas: {total_rows} | Nulls: {sum(null_count.values())} | "
        f"Duplicados: {duplicate_count} | Fuera de rango: {sum(out_of_range.values())}"
    )

    return report
