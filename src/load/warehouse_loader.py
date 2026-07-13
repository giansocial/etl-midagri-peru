from typing import List, Optional
import pandas as pd
from sqlalchemy import text
from src.load.base_loader import BaseLoader
from src.config.database import get_engine


class WarehouseLoader(BaseLoader):
    def __init__(self):
        super().__init__("warehouse")

    def load(self, df: pd.DataFrame, table_name: str) -> int:
        engine = get_engine()
        rows = df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )
        count = rows if rows else len(df)
        self.logger.info(f"{count} filas cargadas en {table_name}")
        return count

    def upsert_dimension(
        self,
        df: pd.DataFrame,
        table_name: str,
        key_columns: List[str],
    ) -> int:
        engine = get_engine()
        inserted = 0

        with engine.begin() as conn:
            for _, row in df.iterrows():
                where_clause = " AND ".join(
                    [f"{col} = :{col}" for col in key_columns]
                )
                check_query = text(
                    f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}"
                )
                params = {col: row[col] for col in key_columns}
                result = conn.execute(check_query, params).scalar()

                if result == 0:
                    row_dict = row.to_dict()
                    columns = ", ".join(row_dict.keys())
                    placeholders = ", ".join([f":{k}" for k in row_dict.keys()])
                    insert_query = text(
                        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    )
                    conn.execute(insert_query, row_dict)
                    inserted += 1

        self.logger.info(f"{inserted} nuevos registros en {table_name}")
        return inserted

    def truncate_and_load(self, df: pd.DataFrame, table_name: str) -> int:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        return self.load(df, table_name)

    def execute_sql_file(self, filepath: str) -> None:
        engine = get_engine()
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()
        with engine.begin() as conn:
            for statement in sql.split(";"):
                statement = statement.strip()
                if statement:
                    conn.execute(text(statement))
        self.logger.info(f"Script SQL ejecutado: {filepath}")
