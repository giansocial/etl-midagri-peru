# ETL - Ministerio de Desarrollo Agrario y Riego (MIDAGRI) - Perú

¿Sabías que Perú es el primer exportador mundial de arándanos y el segundo de paltas, pero un agricultor en Huancavelica produce la mitad de papa por hectárea que uno en Ica? Esa brecha le cuesta al país más de USD 850 millones cada año. Y lo más frustrante: toda la data para detectarlo ya existe, publicada por el propio ministerio. Pero nadie la había conectado.

Soy Gian Cruz. Mientras exploraba la plataforma SIEA del MIDAGRI, descubrí que Perú tiene 5 fuentes oficiales con datos de producción agrícola, valor bruto, precios en chacra, comercio exterior e indicadores productivos de 24 departamentos. El problema: cada fuente vive aislada en su propio dashboard de Power BI. No puedes cruzar cuánto produce Puno en quinua con cuánto se exporta a Estados Unidos ni con el precio que paga el mercado mayorista de Lima. Toda esa información existe pero fragmentada, y sin un modelo que la conecte, no sirve para tomar decisiones.

Lo que hice fue construir un pipeline ETL que extrae esas 5 fuentes oficiales (4,700,000+ registros reales), las limpia, normaliza, enriquece con métricas calculadas como campaña agrícola y rendimiento por hectárea, valida la calidad con scoring automático y las carga en un Data Warehouse con esquema estrella. En lugar de 5 dashboards que no se hablan, ahora hay un modelo unificado donde cada pregunta de negocio tiene respuesta directa.

El resultado: análisis cruzados que antes no existían. Cuantifiqué que cada evento El Niño le cuesta al agro entre S/. 2,800 y 4,200 millones. Identifiqué que el arándano creció 93x en 8 años (de USD 15M a USD 1,400M) y que si el ritmo se mantiene, las agroexportaciones superarían USD 15,000M al 2026. Detecté un diferencial de precios estacional del 45-70% en papa que representa una oportunidad concreta para programas de almacenamiento que hoy no existen a escala.

Este proyecto no es un ejercicio académico. Está construido con las mismas prácticas que se usan en producción: arquitectura medallion (Bronze/Silver/Gold), 63 tests automatizados, validación de calidad de datos, esquema estrella normalizado y un pipeline reproducible que se ejecuta con un solo comando. Todo sobre data real y verificable del ministerio.

Si te interesa ver cómo se construye un pipeline de datos de principio a fin sobre fuentes oficiales, el código está aquí. Si quieres hablar sobre cómo la ingeniería de datos puede transformar información pública en decisiones estratégicas, escríbeme.

## Datos: 5 fuentes oficiales, 4,700,000+ registros

| Archivo | Fuente MIDAGRI | Registros | Contenido |
|---------|---------------|-----------|-----------|
| SISAGRI.xlsx | SISAGRI | 4,282,786 | Producción agrícola por distrito, departamento, cultivo |
| DATA_VBP.xlsx | SIEA | 372,018 | Valor Bruto de Producción mensual por departamento y producto (2000-2026) |
| SISCOMEX.xlsx | SUNAT/MIDAGRI | 64,372 | Importaciones y exportaciones agrícolas FOB/CIF por país y producto |
| SISAP.xlsx | SISAP | 4,415 | Precios por kilogramo en chacra por variedad de cultivo (2010-2026) |
| SISAGRI_OTROS_CULTIVOS.xlsx | SISAGRI | 8,686 | Arándano, caña de azúcar, palma aceitera: producción, cosecha, siembra, precios |

Fuente única: [SIEA - MIDAGRI](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) > Perfil Productivo de los Principales Cultivos > Descargar datos

## Período de análisis: 2015-2023

| Período | Evento | Impacto medible |
|---------|--------|-----------------|
| 2015-2019 | Boom agroexportador | Perú se posicionó como primer exportador mundial de arándanos. USD 7,800M en agroexportaciones al 2019 |
| 2017 | Fenómeno El Niño costero | 120,000 hectáreas afectadas en costa norte. Pérdidas estimadas: S/. 3,150 millones |
| 2020 | COVID-19 | Caída del 3.4% en superficie cosechada. Disrupción logística en mercados mayoristas |
| 2021-2023 | Recuperación y expansión | Agroexportaciones superaron USD 10,000M por primera vez |

## Arquitectura

```
SIEA/MIDAGRI (5 archivos Excel oficiales)
        |
   [EXTRACT] Bronze -> data/raw/
        |              5 fuentes, 4.7M+ registros
        |
  [TRANSFORM] Silver -> data/processed/
        |              - Limpieza y deduplicación
        |              - Normalización de departamentos y cultivos
        |              - Enriquecimiento: campaña agrícola, rendimiento, variación interanual
        |              - Validación de calidad con scoring automático
        |
     [LOAD] Gold -> PostgreSQL (Star Schema)
                    - 4 tablas de hechos (producción, precios, comercio exterior, VBP)
                    - 4 dimensiones (cultivo, ubicación, tiempo, mercado)
                    - Vistas analíticas precalculadas
```

## Hallazgos cruzados

Estos resultados solo son posibles porque el pipeline unifica las 5 fuentes en un solo modelo:

**Brechas de rendimiento (oportunidad de USD 850M+):**
La papa en Costa rinde 17,000 kg/ha; en Sierra, 9,500 kg/ha. Cerrar esa brecha al 75% en los 8 departamentos serranos con mayor superficie agregaría 2.1 millones de toneladas anuales. Cruce: SISAGRI (producción) x DATA_VBP (valor económico).

**Agroexportación (CAGR 12.5%):**
Arándano pasó de USD 15M (2015) a USD 1,400M (2023). Palta de USD 306M a USD 1,100M. Cruce: SISCOMEX (exportaciones) x SISAGRI_OTROS (producción de arándano por departamento).

**Vulnerabilidad climática cuantificada:**
En campañas con El Niño, la producción de arroz en Piura cae 25-40% mientras los precios en chacra suben 35-60%. Cruce: SISAGRI (producción) x SISAP (precios) x DATA_VBP (valor perdido).

**Estacionalidad de precios (arbitraje 45-70%):**
Los precios de papa tocan fondo en mayo-junio y su máximo en enero-febrero. Cruce: SISAP (precios por variedad) x SISAGRI (producción mensual).

## Stack tecnológico

| Componente | Tecnología |
|-----------|------------|
| Lenguaje | Python 3.9+ |
| Procesamiento | pandas, numpy |
| Extracción | openpyxl, requests |
| Base de datos | PostgreSQL + SQLAlchemy |
| Calidad de datos | Validadores con scoring, profiling estadístico (IQR, asimetría, curtosis) |
| Testing | pytest (63 tests) |
| Visualización | matplotlib, seaborn |

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración de base de datos

```bash
cp .env.example .env

psql -U postgres -c "CREATE DATABASE produccion_agricola;"
psql -U postgres -d produccion_agricola -f sql/01_create_dimensions.sql
psql -U postgres -d produccion_agricola -f sql/02_create_facts.sql
psql -U postgres -d produccion_agricola -f sql/03_create_indexes.sql
psql -U postgres -d produccion_agricola -f sql/04_create_views.sql
psql -U postgres -d produccion_agricola -f sql/05_seed_dimensions.sql
```

## Ejecución

```bash
python -m src.pipeline                   # Pipeline completo
python -m src.pipeline --step extract    # Solo extracción (Bronze)
python -m src.pipeline --step transform  # Solo transformación (Silver)
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
│   ├── config/          # Conexión a BD, rutas, variables de entorno
│   ├── extract/         # Extractores especializados por fuente MIDAGRI
│   ├── transform/       # Limpieza, normalización, enriquecimiento, agregación
│   ├── quality/         # Validación, profiling estadístico, reportes de calidad
│   ├── load/            # Carga a PostgreSQL y exportación a archivos
│   ├── models/          # Dataclasses del dominio agrícola y enums
│   ├── utils/           # Logger, manejo de archivos, utilidades de fechas
│   └── pipeline.py      # Orquestador principal del ETL
├── sql/                 # DDL del Data Warehouse (dimensiones, hechos, vistas, índices)
├── tests/               # 63 tests unitarios y de integración
├── notebooks/           # Análisis exploratorio de datos (EDA)
├── data/                # Datos por capa (raw, processed, warehouse, quality)
├── docs/                # Arquitectura, diccionario de datos, documentación de fuentes
└── requirements.txt
```

## Fuentes oficiales

Todos los datos provienen del Ministerio de Desarrollo Agrario y Riego:

| Dataset | Sistema origen | Período | URL de descarga |
|---------|---------------|---------|-----------------|
| SISAGRI | Sistema Integrado de Estadística Agraria | 2015-2026 | [SIEA - Estadística Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| DATA_VBP | Valor Bruto de la Producción Agropecuaria | 2000-2026 | [SIEA - Estadística Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISCOMEX | Comercio Exterior Agropecuario (SUNAT) | 2015-2026 | [SIEA - Estadística Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAP | Sistema de Abastecimiento y Precios | 2010-2026 | [SIEA - Estadística Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAGRI_OTROS | Cultivos emergentes (arándano, palma, caña) | 2015-2026 | [SIEA - Estadística Agropecuaria](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |

| Descarga directa | Archivo Excel consolidado (Google Drive) | 2015-2026 | [Descargar datos MIDAGRI](https://drive.usercontent.google.com/download?id=1ajmiK9uIYlvPZwseRXh1ko3ivHKHufKm&export=download&authuser=0) |

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

The result: cross-dataset analyses that did not exist before. I quantified that each El Niño event costs agriculture between PEN 2,800 and 4,200 million. I identified that blueberry exports grew 93x in 8 years (from USD 15M to USD 1,400M) and that if the pace holds, agro-exports would surpass USD 15B by 2026. I detected a seasonal price spread of 45-70% in potato that represents a concrete opportunity for storage programs that do not yet exist at scale.

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
During El Niño campaigns, rice production in Piura drops 25-40% while farmgate prices surge 35-60%. Cross: SISAGRI (production) x SISAP (prices) x DATA_VBP (lost value).

## Official sources

All data comes from Peru's Ministry of Agrarian Development and Irrigation:

| Dataset | Source system | Period | Download |
|---------|-------------|--------|----------|
| SISAGRI | Integrated Agricultural Statistics | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| DATA_VBP | Gross Agricultural Production Value | 2000-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISCOMEX | Agricultural Foreign Trade (SUNAT) | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAP | Supply and Pricing System | 2010-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |
| SISAGRI_OTROS | Emerging crops (blueberry, palm, cane) | 2015-2026 | [SIEA Portal](https://siea.midagri.gob.pe/index.php/herramientas/estadistica-agropecuarias) |

| Direct download | Consolidated Excel file (Google Drive) | 2015-2026 | [Download MIDAGRI data](https://drive.usercontent.google.com/download?id=1ajmiK9uIYlvPZwseRXh1ko3ivHKHufKm&export=download&authuser=0) |

Portal: https://siea.midagri.gob.pe

## License

MIT License - see [LICENSE](LICENSE)

## Author

Gian Cruz
