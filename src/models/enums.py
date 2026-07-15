from enum import Enum


class CategoriasCultivo(str, Enum):
    CEREALES = "Cereales"
    TUBERCULOS = "Tuberculos"
    LEGUMINOSAS = "Leguminosas"
    FRUTAS = "Frutas"
    HORTALIZAS = "Hortalizas"
    INDUSTRIALES = "Industriales"
    ESTIMULANTES = "Estimulantes"
    FORRAJES = "Forrajes"


class RegionNatural(str, Enum):
    COSTA = "Costa"
    SIERRA = "Sierra"
    SELVA = "Selva"


DEPARTAMENTO_REGION = {
    "Tumbes": RegionNatural.COSTA,
    "Piura": RegionNatural.COSTA,
    "Lambayeque": RegionNatural.COSTA,
    "La Libertad": RegionNatural.COSTA,
    "Ancash": RegionNatural.COSTA,
    "Lima": RegionNatural.COSTA,
    "Lima Metropolitana": RegionNatural.COSTA,
    "Ica": RegionNatural.COSTA,
    "Arequipa": RegionNatural.COSTA,
    "Moquegua": RegionNatural.COSTA,
    "Tacna": RegionNatural.COSTA,
    "Cajamarca": RegionNatural.SIERRA,
    "Huanuco": RegionNatural.SIERRA,
    "Huánuco": RegionNatural.SIERRA,
    "Pasco": RegionNatural.SIERRA,
    "Junin": RegionNatural.SIERRA,
    "Junín": RegionNatural.SIERRA,
    "Huancavelica": RegionNatural.SIERRA,
    "Ayacucho": RegionNatural.SIERRA,
    "Apurimac": RegionNatural.SIERRA,
    "Apurímac": RegionNatural.SIERRA,
    "Cusco": RegionNatural.SIERRA,
    "Puno": RegionNatural.SIERRA,
    "Amazonas": RegionNatural.SELVA,
    "San Martin": RegionNatural.SELVA,
    "San Martín": RegionNatural.SELVA,
    "Loreto": RegionNatural.SELVA,
    "Ucayali": RegionNatural.SELVA,
    "Madre De Dios": RegionNatural.SELVA,
    "Madre de Dios": RegionNatural.SELVA,
}

CULTIVO_CATEGORIA = {
    "arroz": CategoriasCultivo.CEREALES,
    "maiz amarillo duro": CategoriasCultivo.CEREALES,
    "maiz amilaceo": CategoriasCultivo.CEREALES,
    "trigo": CategoriasCultivo.CEREALES,
    "cebada grano": CategoriasCultivo.CEREALES,
    "quinua": CategoriasCultivo.CEREALES,
    "papa": CategoriasCultivo.TUBERCULOS,
    "yuca": CategoriasCultivo.TUBERCULOS,
    "cafe": CategoriasCultivo.ESTIMULANTES,
    "cacao": CategoriasCultivo.ESTIMULANTES,
    "esparrago": CategoriasCultivo.HORTALIZAS,
    "uva": CategoriasCultivo.FRUTAS,
    "palta": CategoriasCultivo.FRUTAS,
    "mango": CategoriasCultivo.FRUTAS,
    "arandano": CategoriasCultivo.FRUTAS,
    "mandarina": CategoriasCultivo.FRUTAS,
    "platano": CategoriasCultivo.FRUTAS,
    "cana de azucar": CategoriasCultivo.INDUSTRIALES,
    "algodón": CategoriasCultivo.INDUSTRIALES,
    "aceituna": CategoriasCultivo.FRUTAS,
}
