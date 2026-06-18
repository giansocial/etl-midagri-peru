import json
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from src.models.schemas import QualityReport
from src.config.settings import QUALITY_DIR
from src.utils.logger import setup_logger

logger = setup_logger("quality.reporter")


def save_quality_report(report: QualityReport) -> Path:
    QUALITY_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quality_{report.dataset_name}_{timestamp}.json"
    filepath = QUALITY_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)

    logger.info(f"Reporte de calidad guardado: {filepath}")
    return filepath


def print_quality_summary(report: QualityReport) -> None:
    print(f"\n  REPORTE DE CALIDAD: {report.dataset_name}")
    print(f"  {'-' * 40}")
    print(f"  Fecha:         {report.timestamp}")
    print(f"  Total filas:   {report.total_rows:,}")
    print(f"  Filas validas: {report.valid_rows:,}")
    print(f"  Duplicados:    {report.duplicate_count:,}")
    print(f"  Score:         {report.quality_score}%")

    if report.null_count:
        print(f"\n  Campos con nulls:")
        for col, count in sorted(report.null_count.items(), key=lambda x: -x[1]):
            pct = round(count / report.total_rows * 100, 1) if report.total_rows > 0 else 0
            print(f"    {col}: {count:,} ({pct}%)")

    if report.out_of_range:
        print(f"\n  Valores fuera de rango:")
        for col, count in report.out_of_range.items():
            print(f"    {col}: {count:,}")

    print()
