# Arquitectura del Pipeline ETL

## Patron Medallion

El pipeline sigue la arquitectura Medallion con tres capas de procesamiento:

### Bronze (Extraccion)
- Lectura de archivos CSV y Excel descargados del SIEA/MIDAGRI
- Validacion inicial de estructura y completitud
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

## Esquema Estrella (Star Schema)

```
                    dim_tiempo
                        |
dim_cultivo --- fact_produccion --- dim_ubicacion
                        
dim_cultivo --- fact_precios_mercado --- dim_mercado
                        |
                    dim_tiempo
```

### Tablas de Hechos

**fact_produccion**: metricas de produccion agricola mensual
- superficie_sembrada_ha
- superficie_cosechada_ha
- produccion_toneladas
- rendimiento_kg_ha
- precio_chacra_soles

**fact_precios_mercado**: metricas de precios en mercados mayoristas
- precio_promedio
- precio_minimo
- precio_maximo
- volumen_toneladas
- variacion_pct

### Dimensiones

- **dim_cultivo**: codigo, nombre, categoria, exportabilidad
- **dim_ubicacion**: departamento, region natural
- **dim_mercado**: nombre, ciudad, departamento, tipo
- **dim_tiempo**: anio, mes, trimestre, semestre, campana agricola

## Patrones de Diseno

### Abstract Factory (Extractores)
- `BaseExtractor` define la interfaz comun
- `CsvExtractor`, `ApiExtractor`, `WebExtractor` implementan estrategias especificas

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
- Perfil estadistico por columna
