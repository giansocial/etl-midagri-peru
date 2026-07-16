import pytest
import pandas as pd
import numpy as np
from src.transform.cleaner import DataCleaner
from src.transform.normalizer import DataNormalizer
from src.transform.enricher import DataEnricher
from src.transform.aggregator import DataAggregator


@pytest.fixture
def cleaner():
    return DataCleaner()


@pytest.fixture
def normalizer():
    return DataNormalizer()


@pytest.fixture
def enricher():
    return DataEnricher()


@pytest.fixture
def aggregator():
    return DataAggregator()


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "departamento": ["  Arequipa  ", "Lima", "Cusco", "Lima", "Cusco"],
        "cultivo": ["Arroz", "Papa ", " Quinua", "Papa ", " Quinua"],
        "produccion_toneladas": [100.0, 200.0, 50.0, 200.0, 50.0],
        "superficie_cosechada_ha": [10.0, 15.0, 25.0, 15.0, 25.0],
        "anio": [2023, 2023, 2023, 2023, 2023],
        "mes": [3, 4, 8, 4, 8],
    })


class TestDataCleaner:
    def test_remove_duplicates(self, cleaner, sample_df):
        result = cleaner.remove_duplicates(sample_df)
        assert len(result) == 3

    def test_strip_whitespace(self, cleaner, sample_df):
        result = cleaner.strip_whitespace(sample_df)
        assert result["departamento"].iloc[0] == "Arequipa"
        assert result["cultivo"].iloc[2] == "Quinua"

    def test_transform_removes_duplicates_and_strips(self, cleaner, sample_df):
        result = cleaner.transform(sample_df)
        assert len(result) == 3
        assert result["departamento"].iloc[0] == "Arequipa"

    def test_fill_nulls(self, cleaner):
        df = pd.DataFrame({
            "precio": [1.5, None, 3.0, None],
            "cantidad": [10, 20, None, 40],
        })
        result = cleaner.fill_nulls(df, {"precio": 0.0, "cantidad": 0})
        assert result["precio"].isna().sum() == 0
        assert result["cantidad"].isna().sum() == 0

    def test_convert_types(self, cleaner):
        df = pd.DataFrame({
            "precio": ["1.5", "2.0", "abc", "4.0"],
            "anio": ["2023", "2024", "2025", "2026"],
        })
        result = cleaner.convert_types(df, {"precio": "float", "anio": "int"})
        assert result["precio"].dtype == float
        assert pd.isna(result["precio"].iloc[2])

    def test_remove_out_of_range(self, cleaner):
        df = pd.DataFrame({
            "produccion": [100, 200, -10, 500000, 300],
        })
        result = cleaner.remove_out_of_range(df, {"produccion": (0, 400000)})
        assert len(result) == 3


class TestDataNormalizer:
    def test_transform_strips_and_title_cases(self, normalizer):
        df = pd.DataFrame({
            "cultivo": ["  ARROZ  ", "  papa  ", "quinua"],
        })
        result = normalizer.transform(df)
        assert result["cultivo"].iloc[0] == "Arroz"
        assert result["cultivo"].iloc[1] == "Papa"
        assert result["cultivo"].iloc[2] == "Quinua"


class TestDataEnricher:
    def test_add_campana_agricola(self, enricher):
        df = pd.DataFrame({
            "anio": [2023, 2023, 2024],
            "mes": [9, 3, 1],
        })
        result = enricher.add_campana_agricola(df, "anio", "mes")
        assert "campana_agricola" in result.columns
        assert result["campana_agricola"].iloc[0] == "2023-2024"
        assert result["campana_agricola"].iloc[1] == "2022-2023"

    def test_calculate_rendimiento(self, enricher):
        df = pd.DataFrame({
            "produccion_toneladas": [100.0, 200.0],
            "superficie_cosechada_ha": [10.0, 0.0],
        })
        result = enricher.calculate_rendimiento(
            df, "produccion_toneladas", "superficie_cosechada_ha"
        )
        assert "rendimiento_calculado" in result.columns
        assert result["rendimiento_calculado"].iloc[0] == 10000.0
        assert result["rendimiento_calculado"].iloc[1] == 0
