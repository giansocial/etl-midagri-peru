# Diccionario de Datos

## fact_produccion

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| cultivo_id | INT | FK a dim_cultivo |
| ubicacion_id | INT | FK a dim_ubicacion |
| tiempo_id | INT | FK a dim_tiempo |
| superficie_sembrada_ha | DECIMAL(12,2) | Superficie sembrada en hectareas |
| superficie_cosechada_ha | DECIMAL(12,2) | Superficie cosechada en hectareas |
| produccion_toneladas | DECIMAL(14,2) | Produccion en toneladas metricas |
| rendimiento_kg_ha | DECIMAL(10,2) | Rendimiento en kilogramos por hectarea |
| precio_chacra_soles | DECIMAL(8,2) | Precio en chacra en soles por kilogramo |

## fact_precios_mercado

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| cultivo_id | INT | FK a dim_cultivo |
| mercado_id | INT | FK a dim_mercado |
| tiempo_id | INT | FK a dim_tiempo |
| precio_promedio | DECIMAL(8,2) | Precio promedio en soles/kg |
| precio_minimo | DECIMAL(8,2) | Precio minimo registrado |
| precio_maximo | DECIMAL(8,2) | Precio maximo registrado |
| volumen_toneladas | DECIMAL(12,2) | Volumen comercializado en toneladas |
| variacion_pct | DECIMAL(6,2) | Variacion porcentual respecto al periodo anterior |

## dim_cultivo

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| codigo | VARCHAR(5) | Codigo del cultivo (ej: ARR, PAP) |
| nombre | VARCHAR(100) | Nombre del cultivo |
| categoria | VARCHAR(50) | Categoria (Cereales, Frutas, Tuberculos, etc.) |
| es_exportable | BOOLEAN | Si el cultivo tiene potencial exportador |

## dim_ubicacion

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| departamento | VARCHAR(50) | Nombre del departamento |
| region_natural | VARCHAR(20) | Region natural (Costa, Sierra, Selva) |

## dim_mercado

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| nombre | VARCHAR(100) | Nombre del mercado mayorista |
| ciudad | VARCHAR(50) | Ciudad donde se ubica |
| departamento | VARCHAR(50) | Departamento |
| tipo | VARCHAR(20) | Tipo de mercado |

## dim_tiempo

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| anio | INT | Ano |
| mes | INT | Mes (1-12) |
| trimestre | INT | Trimestre (1-4) |
| semestre | INT | Semestre (1-2) |
| nombre_mes | VARCHAR(20) | Nombre del mes |
| campana_agricola | VARCHAR(10) | Campana agricola (ej: 2023-2024) |
| es_epoca_siembra | BOOLEAN | Si es epoca de siembra |
| es_epoca_cosecha | BOOLEAN | Si es epoca de cosecha |

## Campos Calculados (Silver Layer)

| Campo | Formula | Descripcion |
|-------|---------|-------------|
| rendimiento_calculado | produccion_toneladas * 1000 / superficie_cosechada_ha | Rendimiento en kg/ha |
| campana_agricola | f(anio, mes) | Agosto-Julio del siguiente ano |
| es_epoca_siembra | mes in (8,9,10,11,12,1) | Meses de siembra |
| es_epoca_cosecha | mes in (3,4,5,6,7) | Meses de cosecha |
| variacion_pct | (precio_actual - precio_anterior) / precio_anterior * 100 | Variacion porcentual |
| volatilidad | std(precio, window=12) | Desviacion estandar movil |
| region_natural | mapping(departamento) | Costa, Sierra o Selva |
| categoria | mapping(cultivo) | Categoria del cultivo |
