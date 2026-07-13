import pandas as pd
from src.utils.logger import setup_logger


class BaseLoader:
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"load.{name}")
