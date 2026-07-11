SIEA_BASE_URL = "https://siea.midagri.gob.pe"

PRODUCCION_URLS = {
    "agricola_mensual": f"{SIEA_BASE_URL}/portal/publicaciones/datos-abiertos",
}

PRECIOS_URLS = {
    "mercado_mayorista_lima": "https://sistemas.midagri.gob.pe/sisap/portal2/mayorista/",
}

BOLETIN_URLS = {
    "boletin_estadistico": f"{SIEA_BASE_URL}/portal/publicaciones/boletin-estadistico-mensual",
}

CULTIVOS_PRINCIPALES = [
    "arroz",
    "papa",
    "maiz amarillo duro",
    "maiz amilaceo",
    "trigo",
    "cebada grano",
    "cafe",
    "cacao",
    "quinua",
    "esparrago",
    "uva",
    "palta",
    "mango",
    "arandano",
    "mandarina",
    "platano",
    "yuca",
    "cana de azucar",
    "algodón",
    "aceituna",
]

DEPARTAMENTOS = [
    "Amazonas", "Ancash", "Apurimac", "Arequipa", "Ayacucho",
    "Cajamarca", "Cusco", "Huancavelica", "Huanuco", "Ica",
    "Junin", "La Libertad", "Lambayeque", "Lima", "Loreto",
    "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno",
    "San Martin", "Tacna", "Tumbes", "Ucayali",
]

MERCADOS_MAYORISTAS = [
    {"nombre": "Gran Mercado Mayorista de Lima", "ciudad": "Lima", "departamento": "Lima"},
    {"nombre": "Mercado Mayorista de Arequipa", "ciudad": "Arequipa", "departamento": "Arequipa"},
    {"nombre": "Mercado Mayorista Moshoqueque", "ciudad": "Chiclayo", "departamento": "Lambayeque"},
    {"nombre": "Mercado Mayorista de Huancayo", "ciudad": "Huancayo", "departamento": "Junin"},
    {"nombre": "Mercado Mayorista de Trujillo", "ciudad": "Trujillo", "departamento": "La Libertad"},
]
