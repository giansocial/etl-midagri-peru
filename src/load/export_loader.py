from pathlib import Path
import pandas as pd
from src.load.base_loader import BaseLoader
from src.config.settings import WAREHOUSE_DIR


class ExportLoader(BaseLoader):
    def __init__(self):
        super().__init__("export")

    def load(self, df: pd.DataFrame, table_name: str) -> int:
        return self.to_csv(df, f"{table_name}.csv")

    def to_csv(self, df: pd.DataFrame, filename: str) -> int:
        filepath = self._get_path(filename)
        df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"Exportado CSV: {filepath} ({len(df)} filas)")
        return len(df)

    def to_parquet(self, df: pd.DataFrame, filename: str) -> int:
        filepath = self._get_path(filename)
        df.to_parquet(filepath, index=False)
        self.logger.info(f"Exportado Parquet: {filepath} ({len(df)} filas)")
        return len(df)

    def to_excel(self, df: pd.DataFrame, filename: str) -> int:
        filepath = self._get_path(filename)
        df.to_excel(filepath, index=False, engine="openpyxl")
        self.logger.info(f"Exportado Excel: {filepath} ({len(df)} filas)")
        return len(df)

    def _get_path(self, filename: str) -> Path:
        WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
        return WAREHOUSE_DIR / filename
