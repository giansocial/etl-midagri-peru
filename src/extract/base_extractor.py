import pandas as pd
from src.utils.logger import setup_logger


class BaseExtractor:
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"extract.{name}")

    def validate_output(self, df: pd.DataFrame) -> bool:
        if df.empty:
            self.logger.warning(f"[{self.name}] Extraccion vacia")
            return False
        self.logger.info(f"[{self.name}] {len(df)} filas extraidas")
        return True
