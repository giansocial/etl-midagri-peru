import pandas as pd
from src.utils.logger import setup_logger


class BaseTransformer:
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"transform.{name}")

    def log_changes(self, before: int, after: int):
        removed = before - after
        if removed > 0:
            self.logger.info(f"[{self.name}] {removed} filas eliminadas ({before} -> {after})")
