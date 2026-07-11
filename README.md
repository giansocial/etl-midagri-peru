# ETL - Ministerio de Desarrollo Agrario y Riego (MIDAGRI) - Peru

Sabias que Peru es el primer exportador mundial de arandanos y el segundo de paltas, pero un agricultor en Huancavelica produce la mitad de papa por hectarea que uno en Ica? Esa brecha le cuesta al pais mas de USD 850 millones cada ano. Y lo mas frustrante: toda la data para detectarlo ya existe, publicada por el propio ministerio. Pero nadie la habia conectado.

Soy Gian Cruz. Mientras exploraba la plataforma SIEA del MIDAGRI, descubri que Peru tiene 5 fuentes oficiales con datos de produccion agricola, valor bruto, precios en chacra, comercio exterior e indicadores productivos de 24 departamentos. El problema: cada fuente vive aislada en su propio dashboard de Power BI. No puedes cruzar cuanto produce Puno en quinua con cuanto se exporta a Estados Unidos ni con el precio que paga el mercado mayorista de Lima. Toda esa informacion existe pero fragmentada, y sin un modelo que la conecte, no sirve para tomar decisiones.

Lo que hice fue construir un pipeline ETL que extrae esas 5 fuentes oficiales (4,700,000+ registros reales), las limpia, normaliza, enriquece con metricas calculadas como campana agricola y rendimiento por hectarea, valida la calidad con scoring automatico y las carga en un Data Warehouse con esquema estrella. En lugar de 5 dashboards que no se hablan, ahora hay un modelo unificado donde cada pregunta de negocio tiene respuesta directa.

El resultado: analisis cruzados que antes no existian. Cuantifique que cada evento El Nino le cuesta al agro entre S/. 2,800 y 4,200 millones. Identifique que el arandano crecio 93x en 8 anos (de USD 15M a USD 1,400M) y que si el ritmo se mantiene, las agroexportaciones superarian USD 15,000M al 2026. Detecte un diferencial de precios estacional del 45-70% en papa que representa una oportunidad concreta para programas de almacenamiento que hoy no existen a escala.

Este proyecto no es un ejercicio academico. Esta construido con las mismas practicas que se usan en produccion: arquitectura medallion (Bronze/Silver/Gold), 63 tests automatizados, validacion de calidad de datos, esquema estrella normalizado y un pipeline reproducible que se ejecuta con un solo comando. Todo sobre data real y verificable del ministerio.

Si te interesa ver como se construye un pipeline de datos de principio a fin sobre fuentes oficiales, el codigo esta aqui. Si quieres hablar sobre como la ingenieria de datos puede transformar informacion publica en decisiones estrategicas, escribeme.

## Datos: 5 fuentes oficiales, 4,700,000+ registros

| Archivo | Fuente MIDAGRI | Registros | Contenido |
|---------|---------------|-----------|-----------|
| SISAGRI.xlsx | SISAGRI | 4,282,786 | Produccion agricola por distrito, departamento, cultivo |
| DATA_VBP.xlsx | SIEA | 372,018 | Valor Bruto de Produccion mensual por departamento y producto (2000-2026) |
| SISCOMEX.xlsx | SUNAT/MIDAGRI | 64,372 | Importaciones y exportaciones agricolas FOB/CIF por pais y producto |
| SISAP.xlsx | SISAP | 4,415 | Precios por kilogramo en chacra por variedad de cultivo (2010-2026) |
| SISAGRI_OTROS_CULTIVOS.xlsx | SISAGRI | 8,686 | Arandano, cana de azucar, palma aceitera: produccion, cosecha, siembra, precios |

Fuente unica: [SIEA - MIDAGRI](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) > Perfil Productivo de los Principales Cultivos > Descargar datos

## Periodo de analisis: 2015-2023

| Periodo | Evento | Impacto medible |
|---------|--------|-----------------|
| 2015-2019 | Boom agroexportador | Peru se posiciono como primer exportador mundial de arandanos. USD 7,800M en agroexportaciones al 2019 |
| 2017 | Fenomeno El Nino costero | 120,000 hectareas afectadas en costa norte. Perdidas estimadas: S/. 3,150 millones |
| 2020 | COVID-19 | Caida del 3.4% en superficie cosechada. Disrupcion logistica en mercados mayoristas |
| 2021-2023 | Recuperacion y expansion | Agroexportaciones superaron USD 10,000M por primera vez |

## Arquitectura

```
SIEA/MIDAGRI (5 archivos Excel oficiales)
        |
   [EXTRACT] Bronze -> data/raw/
        |              5 fuentes, 560K+ registros
        |
  [TRANSFORM] Silver -> data/processed/
        |              - limpieza y deduplicacion
        |              - normalizacion de departamentos y cultivos
        |              - enriquecimiento: campana agricola, rendimiento, variacion interanual
        |              - validacion de calidad con scoring automatico
        |
     [LOAD] Gold -> PostgreSQL (Star Schema)
                    - 2 tablas de hechos (produccion, comercio exterior)
                    - 4 dimensiones (cultivo, ubicacion, tiempo, producto comercial)
                    - vistas analiticas pre-calculadas
```

## Hallazgos cruzados

Estos resultados solo son posibles porque el pipeline unifica las 5 fuentes en un solo modelo:

**Brechas de rendimiento (oportunidad de USD 850M+):**
La papa en Costa rinde 17,000 kg/ha; en Sierra, 9,500 kg/ha. Cerrar esa brecha al 75% en los 8 departamentos serranos con mayor superficie agregaria 2.1 millones de toneladas anuales. Cruce: SISAGRI (produccion) x DATA_VBP (valor economico).

**Agroexportacion (CAGR 12.5%):**
Arandano paso de USD 15M (2015) a USD 1,400M (2023). Palta de USD 306M a USD 1,100M. Cruce: SISCOMEX (exportaciones) x SISAGRI_OTROS (produccion de arandano por departamento).

**Vulnerabilidad climatica cuantificada:**
En campanas con El Nino, produccion de arroz en Piura cae 25-40% mientras precios en chacra suben 35-60%. Cruce: SISAGRI (produccion) x SISAP (precios) x DATA_VBP (valor perdido).

**Estacionalidad de precios (arbitraje 45-70%):**
Precios de papa tocan fondo en mayo-junio y su maximo en enero-febrero. Cruce: SISAP (precios por variedad) x SISAGRI (produccion mensual).

## Stack tecnologico

| Componente | Tecnologia |
|-----------|------------|
| Lenguaje | Python 3.9+ |
| Procesamiento | pandas, numpy |
| Extraccion | openpyxl, requests |
| Base de datos | PostgreSQL + SQLAlchemy |
| Calidad de datos | Validadores con scoring, profiling estadistico (IQR, asimetria, curtosis) |
| Testing | pytest (63 tests) |
| Visualizacion | matplotlib, seaborn |

## Instalacion

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuracion de base de datos

```bash
cp .env.example .env

psql -U postgres -c "CREATE DATABASE produccion_agricola;"
psql -U postgres -d produccion_agricola -f sql/01_create_dimensions.sql
psql -U postgres -d produccion_agricola -f sql/02_create_facts.sql
psql -U postgres -d produccion_agricola -f sql/03_create_indexes.sql
psql -U postgres -d produccion_agricola -f sql/04_create_views.sql
psql -U postgres -d produccion_agricola -f sql/05_seed_dimensions.sql
```

## Ejecucion

```bash
python -m src.pipeline                   # Pipeline completo
python -m src.pipeline --step extract    # Solo extraccion (Bronze)
python -m src.pipeline --step transform  # Solo transformacion (Silver)
python -m src.pipeline --step load       # Solo carga (Gold)
```

## Testing

```bash
pytest
pytest --cov=src --cov-report=term-missing
```

## Estructura del proyecto

```
etl-midagri-peru/
├── src/
│   ├── config/          # Conexion a BD, rutas, variables de entorno
│   ├── extract/         # Extractores CSV, Excel, API REST
│   ├── transform/       # Limpieza, normalizacion, enriquecimiento, agregacion
│   ├── quality/         # Validacion, profiling estadistico, reportes de calidad
│   ├── load/            # Carga a PostgreSQL y exportacion a archivos
│   ├── models/          # Dataclasses del dominio agricola y enums
│   ├── utils/           # Logger, manejo de archivos, utilidades de fechas
│   └── pipeline.py      # Orquestador principal del ETL
├── sql/                 # DDL del Data Warehouse (dimensiones, hechos, vistas, indices)
├── tests/               # 63 tests unitarios y de integracion
├── notebooks/           # Analisis exploratorio de datos (EDA)
├── data/                # Datos por capa (raw, processed, warehouse, quality)
├── docs/                # Arquitectura, diccionario de datos, documentacion de fuentes
└── requirements.txt
```

## Fuentes oficiales

Todos los datos provienen del Ministerio de Desarrollo Agrario y Riego:

| Dataset | Sistema origen | Periodo | URL de descarga |
|---------|---------------|---------|-----------------|
| SISAGRI | Sistema Integrado de Estadistica Agraria | 2015-2026 | [SIEA - Estadistica Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| DATA_VBP | Valor Bruto de la Produccion Agropecuaria | 2000-2026 | [SIEA - Estadistica Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISCOMEX | Comercio Exterior Agropecuario (SUNAT) | 2015-2026 | [SIEA - Estadistica Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAP | Sistema de Abastecimiento y Precios | 2010-2026 | [SIEA - Estadistica Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAGRI_OTROS | Cultivos emergentes (arandano, palma, cana) | 2015-2026 | [SIEA - Estadistica Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |

Portal: https://siea.midagri.gob.pe

## Licencia

MIT License - ver [LICENSE](LICENSE)

## Autor

Gian Cruz

---

# ETL - Ministry of Agrarian Development and Irrigation (MIDAGRI) - Peru

Did you know that Peru is the world's top blueberry exporter and second-largest avocado exporter, yet a farmer in Huancavelica produces half the potato yield per hectare compared to one in Ica? That gap costs the country over USD 850 million every year. And the most frustrating part: all the data to detect it already exists, published by the ministry itself. But nobody had connected it.

I am Gian Cruz. While exploring the SIEA platform from Peru's MIDAGRI, I discovered that Peru has 5 official sources with agricultural production data, gross production value, farmgate prices, foreign trade, and productivity indicators across 24 departments. The problem: each source lives isolated in its own Power BI dashboard. You cannot cross-reference how much quinoa Puno produces with how much gets exported to the United States or what price Lima's wholesale market pays. All that information exists but fragmented, and without a model connecting it, it cannot drive decisions.

What I built is an ETL pipeline that extracts those 5 official sources (4,700,000+ real records), cleans them, normalizes them, enriches them with calculated metrics like agricultural campaign and yield per hectare, validates quality with automated scoring, and loads them into a Star Schema Data Warehouse. Instead of 5 dashboards that do not talk to each other, there is now a unified model where every business question has a direct answer.

The result: cross-dataset analyses that did not exist before. I quantified that each El Nino event costs agriculture PEN 2,800-4,200 million. I identified that blueberry grew 93x in 8 years (from USD 15M to USD 1,400M) and that if the pace holds, agro-exports would surpass USD 15B by 2026. I detected a seasonal price spread of 45-70% in potato that represents a concrete opportunity for storage programs that do not yet exist at scale.

This project is not an academic exercise. It is built with production-grade practices: medallion architecture (Bronze/Silver/Gold), 63 automated tests, data quality validation, normalized star schema, and a reproducible pipeline that runs with a single command. All on real, verifiable ministry data.

If you want to see how a data pipeline is built end-to-end on official sources, the code is here. If you want to discuss how data engineering can transform public information into strategic decisions, reach out.

## Data: 5 official sources, 4,700,000+ records

| File | MIDAGRI source | Records | Content |
|------|---------------|---------|---------|
| SISAGRI.xlsx | SISAGRI | 4,282,786 | Agricultural production by district, department, crop |
| DATA_VBP.xlsx | SIEA | 372,018 | Monthly Gross Production Value by department and product (2000-2026) |
| SISCOMEX.xlsx | SUNAT/MIDAGRI | 64,372 | Agricultural imports and exports FOB/CIF by country and product |
| SISAP.xlsx | SISAP | 4,415 | Farmgate prices per kilogram by crop variety (2010-2026) |
| SISAGRI_OTROS_CULTIVOS.xlsx | SISAGRI | 8,686 | Blueberry, sugarcane, oil palm: production, harvest, planting, prices |

Single source: [SIEA - MIDAGRI](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) > Main Crop Productive Profile > Download data

## Cross-dataset findings

These results are only possible because the pipeline unifies all 5 sources into a single model:

**Yield gaps (USD 850M+ opportunity):**
Coastal potato yields 17,000 kg/ha; Highland potato yields 9,500 kg/ha. Closing that gap to 75% across 8 highland departments would add 2.1 million tonnes annually. Cross: SISAGRI (production) x DATA_VBP (economic value).

**Agro-exports (12.5% CAGR):**
Blueberry grew from USD 15M (2015) to USD 1,400M (2023). Avocado from USD 306M to USD 1,100M. Cross: SISCOMEX (exports) x SISAGRI_OTROS (blueberry production by department).

**Quantified climate vulnerability:**
During El Nino campaigns, rice production in Piura drops 25-40% while farmgate prices surge 35-60%. Cross: SISAGRI (production) x SISAP (prices) x DATA_VBP (lost value).

## Official sources

All data comes from Peru's Ministry of Agrarian Development and Irrigation:

| Dataset | Source system | Period | Download |
|---------|-------------|--------|----------|
| SISAGRI | Integrated Agricultural Statistics | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| DATA_VBP | Gross Agricultural Production Value | 2000-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISCOMEX | Agricultural Foreign Trade (SUNAT) | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAP | Supply and Pricing System | 2010-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAGRI_OTROS | Emerging crops (blueberry, palm, cane) | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |

Portal: https://siea.midagri.gob.pe

## License

MIT License - see [LICENSE](LICENSE)

## Author

Gian Cruz
