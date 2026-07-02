import pytest
from unittest.mock import patch, MagicMock
from src.pipeline import ETLPipeline


@pytest.fixture
def pipeline():
    return ETLPipeline()


class TestETLPipeline:
    def test_pipeline_init(self, pipeline):
        assert pipeline.extractor is not None
        assert pipeline.cleaner is not None
        assert pipeline.normalizer is not None
        assert pipeline.enricher is not None
        assert pipeline.exporter is not None

    def test_run_extract_only(self, pipeline):
        with patch.object(pipeline, "_extract") as mock_extract:
            with patch.object(pipeline, "_transform") as mock_transform:
                with patch.object(pipeline, "_load") as mock_load:
                    pipeline.run(steps="extract")
                    mock_extract.assert_called_once()
                    mock_transform.assert_not_called()
                    mock_load.assert_not_called()

    def test_run_transform_only(self, pipeline):
        with patch.object(pipeline, "_extract") as mock_extract:
            with patch.object(pipeline, "_transform") as mock_transform:
                with patch.object(pipeline, "_load") as mock_load:
                    pipeline.run(steps="transform")
                    mock_extract.assert_not_called()
                    mock_transform.assert_called_once()
                    mock_load.assert_not_called()

    def test_run_full(self, pipeline):
        with patch.object(pipeline, "_extract") as mock_extract:
            with patch.object(pipeline, "_transform") as mock_transform:
                with patch.object(pipeline, "_load") as mock_load:
                    pipeline.run(steps="full")
                    mock_extract.assert_called_once()
                    mock_transform.assert_called_once()
                    mock_load.assert_called_once()
