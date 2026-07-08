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
| precio_chacra_soles | DECIMAL(10,2) | Precio en chacra en soles por kilogramo |

## fact_precios_mercado

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| cultivo_id | INT | FK a dim_cultivo |
| mercado_id | INT | FK a dim_mercado |
| tiempo_id | INT | FK a dim_tiempo |
| precio_promedio | DECIMAL(10,2) | Precio promedio en soles/kg |
| precio_minimo | DECIMAL(10,2) | Precio minimo registrado |
| precio_maximo | DECIMAL(10,2) | Precio maximo registrado |
| volumen_toneladas | DECIMAL(12,2) | Volumen comercializado en toneladas |
| variacion_pct | DECIMAL(6,2) | Variacion porcentual respecto al periodo anterior |

## fact_comercio_exterior

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| tiempo_id | INT | FK a dim_tiempo |
| tipo_operacion | VARCHAR(20) | EXPORTACIONES o IMPORTACIONES |
| cod_arancel | VARCHAR(20) | Codigo arancelario del producto |
| producto | VARCHAR(200) | Descripcion del producto |
| pais | VARCHAR(100) | Pais de destino u origen |
| peso_neto_tm | DECIMAL(14,6) | Peso neto en toneladas metricas |
| peso_bruto_tm | DECIMAL(14,6) | Peso bruto en toneladas metricas |
| valor_fob_miles_usd | DECIMAL(14,6) | Valor FOB en miles de dolares |
| valor_cif_miles_usd | DECIMAL(14,6) | Valor CIF en miles de dolares |

## fact_vbp

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| cultivo_id | INT | FK a dim_cultivo |
| ubicacion_id | INT | FK a dim_ubicacion |
| tiempo_id | INT | FK a dim_tiempo |
| produccion_toneladas | DECIMAL(14,2) | Produccion en toneladas metricas |
| precio_base_2007 | DECIMAL(12,6) | Precio base ano 2007 para calculo de VBP |
| vbp_millones | DECIMAL(14,6) | Valor Bruto de Produccion en millones de soles |

## dim_cultivo

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| codigo | VARCHAR(20) | Codigo del cultivo |
| nombre | VARCHAR(100) | Nombre del cultivo |
| categoria | VARCHAR(50) | Categoria (Cereales, Frutas, Tuberculos, etc.) |
| subcategoria | VARCHAR(50) | Subcategoria opcional |
| es_exportable | BOOLEAN | Si el cultivo tiene potencial exportador |
| campana_inicio_mes | INT | Mes de inicio de campana para este cultivo |
| campana_fin_mes | INT | Mes de fin de campana para este cultivo |

## dim_ubicacion

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| ubigeo | VARCHAR(6) | Codigo UBIGEO de INEI |
| departamento | VARCHAR(50) | Nombre del departamento |
| provincia | VARCHAR(80) | Nombre de la provincia |
| distrito | VARCHAR(100) | Nombre del distrito |
| region_natural | VARCHAR(20) | Region natural (Costa, Sierra, Selva) |
| altitud_msnm | INT | Altitud en metros sobre el nivel del mar |
| latitud | DECIMAL(10,7) | Coordenada de latitud |
| longitud | DECIMAL(10,7) | Coordenada de longitud |

## dim_mercado

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| nombre | VARCHAR(100) | Nombre del mercado mayorista |
| ciudad | VARCHAR(50) | Ciudad donde se ubica |
| departamento | VARCHAR(50) | Departamento |
| tipo | VARCHAR(30) | Tipo de mercado (Mayorista por defecto) |

## dim_tiempo

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | SERIAL | Identificador unico |
| fecha | DATE | Fecha completa |
| anio | INT | Ano |
| mes | INT | Mes (1-12) |
| trimestre | INT | Trimestre (1-4) |
| semestre | INT | Semestre (1-2) |
| nombre_mes | VARCHAR(20) | Nombre del mes |
| campana_agricola | VARCHAR(20) | Campana agricola (ej: 2023-2024) |
| es_epoca_siembra | BOOLEAN | Si es epoca de siembra (ago-ene) |
| es_epoca_cosecha | BOOLEAN | Si es epoca de cosecha (mar-jul) |

## Campos Calculados (Silver Layer)

| Campo | Formula | Descripcion |
|-------|---------|-------------|
| rendimiento_calculado | produccion_toneladas * 1000 / superficie_cosechada | Rendimiento en kg/ha |
| campana_agricola | f(anio, mes) | Agosto-Julio del siguiente ano |
| es_epoca_siembra | mes in (8,9,10,11,12,1) | Meses de siembra |
| es_epoca_cosecha | mes in (3,4,5,6,7) | Meses de cosecha |
| variacion_pct | (precio_actual - precio_anterior) / precio_anterior * 100 | Variacion porcentual |
| volatilidad | std(precio, window=12) | Desviacion estandar movil de 12 periodos |
| region_natural | mapping(departamento) | Costa, Sierra o Selva |
| categoria | mapping(cultivo) | Categoria del cultivo |
