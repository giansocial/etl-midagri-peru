from pathlib import Path
from typing import Optional, List
import pandas as pd
from src.extract.base_extractor import BaseExtractor


class CsvExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("csv")

    def extract(
        self,
        filepath: Path,
        encoding: str = "utf-8",
        separator: str = ",",
        columns: Optional[List[str]] = None,
        skiprows: Optional[int] = None,
    ) -> pd.DataFrame:
        self.logger.info(f"Leyendo archivo: {filepath}")

        try:
            df = pd.read_csv(
                filepath,
                encoding=encoding,
                sep=separator,
                skiprows=skiprows,
                low_memory=False,
            )
        except UnicodeDecodeError:
            self.logger.warning(f"Error con encoding {encoding}, intentando latin-1")
            df = pd.read_csv(
                filepath,
                encoding="latin-1",
                sep=separator,
                skiprows=skiprows,
                low_memory=False,
            )

        if columns:
            missing = [c for c in columns if c not in df.columns]
            if missing:
                self.logger.warning(f"Columnas faltantes: {missing}")
            available = [c for c in columns if c in df.columns]
            df = df[available]

        self.validate_output(df)
        return df

    def extract_excel(
        self,
        filepath: Path,
        sheet_name: Optional[str] = None,
        skiprows: Optional[int] = None,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        self.logger.info(f"Leyendo Excel: {filepath}")

        df = pd.read_excel(
            filepath,
            sheet_name=sheet_name or 0,
            skiprows=skiprows,
            engine="openpyxl",
        )

        if columns:
            available = [c for c in columns if c in df.columns]
            df = df[available]

        self.validate_output(df)
        return df
