from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ProduccionRecord:
    cultivo: str
    categoria: str
    departamento: str
    provincia: str
    anio: int
    mes: int
    superficie_sembrada_ha: float
    superficie_cosechada_ha: float
    produccion_toneladas: float
    rendimiento_kg_ha: float
    precio_chacra_soles: float


@dataclass
class PrecioMercadoRecord:
    producto: str
    mercado: str
    ciudad: str
    fecha: date
    precio_minimo: float
    precio_maximo: float
    precio_promedio: float
    unidad: str
    volumen_toneladas: Optional[float] = None


@dataclass
class QualityReport:
    dataset_name: str
    total_rows: int
    valid_rows: int
    null_count: dict
    duplicate_count: int
    out_of_range: dict
    quality_score: float
    timestamp: str
