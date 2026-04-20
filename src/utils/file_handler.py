from pathlib import Path
from typing import Optional
import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger("utils.file_handler")


def save_dataframe(
    df: pd.DataFrame,
    directory: Path,
    filename: str,
    format: str = "csv",
) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename

    if format == "csv":
        df.to_csv(filepath, index=False, encoding="utf-8")
    elif format == "parquet":
        df.to_parquet(filepath, index=False)
    elif format == "excel":
        df.to_excel(filepath, index=False, engine="openpyxl")
    else:
        raise ValueError(f"Formato no soportado: {format}")

    logger.info(f"Archivo guardado: {filepath} ({len(df)} filas)")
    return filepath


def load_dataframe(
    filepath: Path,
    format: Optional[str] = None,
) -> pd.DataFrame:
    if format is None:
        format = filepath.suffix.lstrip(".")

    if format == "csv":
        return pd.read_csv(filepath, encoding="utf-8")
    elif format == "parquet":
        return pd.read_parquet(filepath)
    elif format in ("xlsx", "xls", "excel"):
        return pd.read_excel(filepath, engine="openpyxl")
    else:
        raise ValueError(f"Formato no soportado: {format}")


def ensure_directories(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
