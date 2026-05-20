import pytest
import pandas as pd
from pathlib import Path
from src.extract.csv_extractor import CsvExtractor


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def extractor():
    return CsvExtractor()


class TestCsvExtractor:
    def test_extract_csv(self, extractor):
        filepath = FIXTURES_DIR / "sample_data.csv"
        df = extractor.extract(filepath)
        assert not df.empty
        assert "departamento" in df.columns
        assert "produccion_toneladas" in df.columns
        assert len(df) == 15

    def test_extract_csv_with_columns(self, extractor):
        filepath = FIXTURES_DIR / "sample_data.csv"
        df = extractor.extract(filepath, columns=["departamento", "cultivo"])
        assert list(df.columns) == ["departamento", "cultivo"]

    def test_extract_csv_missing_columns_handled(self, extractor):
        filepath = FIXTURES_DIR / "sample_data.csv"
        df = extractor.extract(
            filepath,
            columns=["departamento", "columna_inexistente"],
        )
        assert "departamento" in df.columns
        assert "columna_inexistente" not in df.columns

    def test_extract_csv_data_types(self, extractor):
        filepath = FIXTURES_DIR / "sample_data.csv"
        df = extractor.extract(filepath)
        assert df["produccion_toneladas"].dtype == float
        assert df["anio"].dtype == int
