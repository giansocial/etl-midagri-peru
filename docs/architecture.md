# Arquitectura del Pipeline ETL

## Patron Medallion

El pipeline sigue la arquitectura Medallion con tres capas de procesamiento:

### Bronze (Extraccion)
- Lectura de 5 fuentes Excel descargadas del portal SIEA/MIDAGRI
- Identificacion automatica del tipo de archivo por nombre
- Mapeo de columnas crudas a nombres normalizados del modelo
- Almacenamiento en formato crudo en `data/raw/`

### Silver (Transformacion)
- Limpieza: eliminacion de duplicados, espacios en blanco, valores nulos
- Normalizacion: estandarizacion de nombres de departamentos y cultivos
- Enriquecimiento: calculo de campana agricola, rendimiento, variaciones de precio
- Validacion de calidad con rangos numericos definidos por dominio
- Almacenamiento procesado en `data/processed/`

### Gold (Carga)
- Agregaciones por region, cultivo y periodo temporal
- Carga a PostgreSQL en esquema estrella
- Exportacion a CSV/Parquet para analisis externo

## Fuentes de Datos

| Dataset | Registros | Contenido |
|---------|-----------|-----------|
| SISAGRI | 4,282,786 | Produccion agricola mensual por distrito |
| DATA_VBP | 372,018 | Valor Bruto de Produccion agricola |
| SISCOMEX | 64,372 | Comercio exterior agroexportador |
| SISAP | 4,415 | Precios en mercados mayoristas |
| SISAGRI_OTROS | 8,686 | Cultivos complementarios (formato pivotado) |

## Esquema Estrella (Star Schema)

```
                    dim_tiempo
                        |
dim_cultivo --- fact_produccion --- dim_ubicacion

dim_cultivo --- fact_precios_mercado --- dim_mercado
                        |
                    dim_tiempo

                    dim_tiempo
                        |
dim_cultivo --- fact_comercio_exterior
                        |
                    (pais, producto)

                    dim_tiempo
                        |
dim_cultivo --- fact_vbp --- dim_ubicacion
```

### Tablas de Hechos

**fact_produccion**: metricas de produccion agricola mensual
- superficie_sembrada_ha, superficie_cosechada_ha
- produccion_toneladas, rendimiento_kg_ha, precio_chacra_soles

**fact_precios_mercado**: precios en mercados mayoristas
- precio_promedio, precio_minimo, precio_maximo
- volumen_toneladas, variacion_pct

**fact_comercio_exterior**: operaciones de importacion y exportacion
- tipo_operacion, cod_arancel, producto, pais
- peso_neto_tm, peso_bruto_tm, valor_fob_miles_usd, valor_cif_miles_usd

**fact_vbp**: valor bruto de la produccion agricola
- produccion_toneladas, precio_base_2007, vbp_millones

### Dimensiones

- **dim_cultivo**: codigo, nombre, categoria, exportabilidad
- **dim_ubicacion**: departamento, provincia, distrito, region natural, ubigeo
- **dim_mercado**: nombre, ciudad, departamento, tipo
- **dim_tiempo**: anio, mes, trimestre, semestre, campana agricola, epocas

## Patrones de Diseno

### Abstract Factory (Extractores)
- `BaseExtractor` define la interfaz comun
- `MidagriExtractor` implementa metodos especificos por fuente (extract_vbp, extract_siscomex, etc.)
- `CsvExtractor` maneja archivos CSV genericos

### Template Method (Transformadores)
- `BaseTransformer` define el flujo transform() -> log_changes()
- `DataCleaner`, `DataNormalizer`, `DataEnricher` implementan logica especifica

### Strategy (Loaders)
- `BaseLoader` define la interfaz de carga
- `WarehouseLoader` (PostgreSQL) y `ExportLoader` (archivos) son intercambiables

## Validacion de Calidad

Cada etapa genera un `QualityReport` con:
- Conteo de nulos por columna
- Conteo de duplicados
- Valores fuera de rango
- Score de calidad (0-100%)
- Perfil estadistico por columna (media, mediana, asimetria, curtosis, IQR)
