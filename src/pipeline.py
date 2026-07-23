import argparse
import sys
from datetime import datetime
from pathlib import Path

from src.config.settings import RAW_DIR, PROCESSED_DIR, WAREHOUSE_DIR
from src.extract.midagri_extractor import MidagriExtractor
from src.transform.cleaner import DataCleaner
from src.transform.normalizer import DataNormalizer
from src.transform.enricher import DataEnricher
from src.transform.aggregator import DataAggregator
from src.quality.validators import validate_dataset
from src.quality.reporter import save_quality_report, print_quality_summary
from src.load.export_loader import ExportLoader
from src.utils.logger import setup_logger
from src.utils.file_handler import ensure_directories

logger = setup_logger("pipeline")


class ETLPipeline:
    def __init__(self):
        self.extractor = MidagriExtractor()
        self.cleaner = DataCleaner()
        self.normalizer = DataNormalizer()
        self.enricher = DataEnricher()
        self.aggregator = DataAggregator()
        self.exporter = ExportLoader()
        self.datasets = {}
        self.start_time = None

    def run(self, steps: str = "full") -> None:
        self.start_time = datetime.now()
        logger.info(f"Pipeline iniciado: {self.start_time.isoformat()}")
        ensure_directories(RAW_DIR, PROCESSED_DIR, WAREHOUSE_DIR)

        try:
            if steps in ("full", "extract"):
                self._extract()

            if steps in ("full", "transform"):
                self._transform()

            if steps in ("full", "load"):
                self._load()

            elapsed = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"Pipeline completado en {elapsed:.1f} segundos")

        except Exception as e:
            logger.error(f"Pipeline fallido: {e}")
            raise

    def _extract(self) -> None:
        logger.info("ETAPA 1: Extraccion (Bronze)")

        excel_files = list(RAW_DIR.glob("*.xlsx"))
        csv_files = list(RAW_DIR.glob("*.csv"))
        raw_files = excel_files + csv_files

        if not raw_files:
            logger.warning(
                "No hay archivos en data/raw/. "
                "Descarga los datos desde SIEA/MIDAGRI."
            )
            return

        for filepath in raw_files:
            file_type = self.extractor.identify_file(filepath)
            if not file_type:
                logger.warning(f"Archivo no reconocido: {filepath.name}")
                continue

            logger.info(f"Procesando {filepath.name} como {file_type}")

            extractors = {
                "vbp": self.extractor.extract_vbp,
                "siscomex": self.extractor.extract_siscomex,
                "sisap": self.extractor.extract_sisap,
                "sisagri_otros": self.extractor.extract_sisagri_otros,
                "sisagri": self.extractor.extract_sisagri,
            }

            df = extractors[file_type](filepath)
            if df.empty:
                continue

            self.datasets[file_type] = df

            report = validate_dataset(df, name=f"bronze_{file_type}", required_columns=[])
            save_quality_report(report)
            print_quality_summary(report)

        logger.info(f"Extraccion completada: {len(self.datasets)} datasets cargados")

    def _transform(self) -> None:
        logger.info("ETAPA 2: Transformacion (Silver)")

        if not self.datasets:
            self._load_from_raw()

        for name, df in self.datasets.items():
            logger.info(f"Transformando: {name} ({len(df)} filas)")

            df = self.cleaner.transform(df)

            if "departamento" in df.columns:
                df = self.normalizer.normalize_departamento(df, "departamento")
                df = self.normalizer.add_region_natural(df, "departamento")

            if "cultivo" in df.columns:
                df = self.normalizer.add_categoria_cultivo(df, "cultivo")

            if "anio" in df.columns and "mes" in df.columns:
                df = self.enricher.add_campana_agricola(df, "anio", "mes")

            if "produccion_toneladas" in df.columns and "superficie_cosechada" in df.columns:
                df = self.enricher.calculate_rendimiento(
                    df, "produccion_toneladas", "superficie_cosechada"
                )

            if "precio_chacra_soles" in df.columns and "departamento" in df.columns:
                df = self.enricher.calculate_variacion_precio(
                    df, "precio_chacra_soles", ["departamento", "cultivo"], "anio"
                )

            numeric_ranges = {}
            if "produccion_toneladas" in df.columns:
                numeric_ranges["produccion_toneladas"] = (0, 50_000_000)
            if "precio_kg_soles" in df.columns:
                numeric_ranges["precio_kg_soles"] = (0, 5_000)
            if "valor_fob_miles_usd" in df.columns:
                numeric_ranges["valor_fob_miles_usd"] = (0, 10_000_000)

            report = validate_dataset(
                df, name=f"silver_{name}", required_columns=[], numeric_ranges=numeric_ranges
            )
            save_quality_report(report)

            self.datasets[name] = df
            self.exporter.to_csv(df, f"{name}_processed.csv")
            logger.info(f"{name}: {len(df)} filas procesadas y exportadas")

    def _load(self) -> None:
        logger.info("ETAPA 3: Carga (Gold)")

        processed_files = list(PROCESSED_DIR.glob("*_processed.csv"))
        if not processed_files and self.datasets:
            processed_files = [WAREHOUSE_DIR / f"{name}_processed.csv" for name in self.datasets]

        if not processed_files:
            logger.warning("No hay archivos procesados para cargar")
            return

        for filepath in processed_files:
            if filepath.exists():
                logger.info(f"Listo para carga: {filepath.name}")

        logger.info(
            "Archivos procesados en data/warehouse/. "
            "Para cargar a PostgreSQL, ejecuta los scripts SQL."
        )

    def _load_from_raw(self) -> None:
        logger.info("Cargando datasets desde data/raw/")
        for filepath in RAW_DIR.glob("*.xlsx"):
            file_type = self.extractor.identify_file(filepath)
            if not file_type:
                continue
            extractors = {
                "vbp": self.extractor.extract_vbp,
                "siscomex": self.extractor.extract_siscomex,
                "sisap": self.extractor.extract_sisap,
                "sisagri_otros": self.extractor.extract_sisagri_otros,
                "sisagri": self.extractor.extract_sisagri,
            }
            df = extractors[file_type](filepath)
            if not df.empty:
                self.datasets[file_type] = df


def main():
    parser = argparse.ArgumentParser(
        description="ETL Pipeline - Produccion Agricola del Peru (MIDAGRI)"
    )
    parser.add_argument(
        "--step",
        choices=["full", "extract", "transform", "load"],
        default="full",
        help="Etapa del pipeline a ejecutar",
    )
    args = parser.parse_args()

    pipeline = ETLPipeline()
    pipeline.run(steps=args.step)


if __name__ == "__main__":
    main()
