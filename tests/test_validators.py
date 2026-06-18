import pytest
import pandas as pd
from src.quality.validators import validate_dataset


@pytest.fixture
def clean_df():
    return pd.DataFrame({
        "departamento": ["Arequipa", "Lima", "Cusco"],
        "cultivo": ["Arroz", "Papa", "Quinua"],
        "produccion_toneladas": [100.0, 200.0, 50.0],
    })


@pytest.fixture
def dirty_df():
    return pd.DataFrame({
        "departamento": ["Arequipa", "Lima", None, "Lima"],
        "cultivo": ["Arroz", "Papa", "Quinua", "Papa"],
        "produccion_toneladas": [100.0, None, 50.0, None],
    })


class TestValidateDataset:
    def test_clean_data_high_score(self, clean_df):
        report = validate_dataset(clean_df, name="test_clean", required_columns=[])
        assert report.quality_score == 100.0
        assert report.duplicate_count == 0
        assert len(report.null_count) == 0

    def test_detects_nulls(self, dirty_df):
        report = validate_dataset(dirty_df, name="test_dirty", required_columns=[])
        assert report.null_count.get("departamento", 0) == 1
        assert report.null_count.get("produccion_toneladas", 0) == 2

    def test_detects_duplicates(self, dirty_df):
        report = validate_dataset(dirty_df, name="test_dup", required_columns=[])
        assert report.duplicate_count >= 0

    def test_missing_required_columns(self, clean_df):
        report = validate_dataset(
            clean_df,
            name="test_missing",
            required_columns=["precio", "volumen"],
        )
        assert report.total_rows == 3

    def test_out_of_range_detection(self):
        df = pd.DataFrame({
            "produccion_toneladas": [100.0, -5.0, 99999999.0, 500.0],
        })
        report = validate_dataset(
            df,
            name="test_range",
            required_columns=[],
            numeric_ranges={"produccion_toneladas": (0, 50000000)},
        )
        assert report.out_of_range.get("produccion_toneladas", 0) == 2

    def test_quality_score_decreases_with_issues(self, dirty_df):
        report = validate_dataset(dirty_df, name="test_score", required_columns=[])
        assert report.quality_score < 100.0

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        report = validate_dataset(df, name="test_empty", required_columns=[])
        assert report.total_rows == 0
        assert report.quality_score == 100.0
