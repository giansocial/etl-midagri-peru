# Fuentes de Datos

## SIEA - Sistema Integrado de Estadisticas Agrarias

**URL**: https://siea.midagri.gob.pe

**Institucion**: Ministerio de Desarrollo Agrario y Riego (MIDAGRI)

## Datasets Utilizados

### 1. SISAGRI - Produccion Agricola Principal
- **Archivo**: SISAGRI.xlsx
- **Registros**: 4,282,786
- **Descripcion**: Estadisticas mensuales de produccion agricola por distrito
- **Variables**: superficie sembrada/cosechada, produccion (t), rendimiento (kg/ha), precio chacra (S/./kg)
- **Granularidad**: Mensual, por distrito, provincia y departamento
- **Periodo**: 2000-2023
- **Particularidad**: Archivo multi-hoja, sin encabezados. El extractor asigna columnas por posicion (13 columnas esperadas)

### 2. DATA_VBP - Valor Bruto de Produccion
- **Archivo**: DATA_VBP.xlsx
- **Registros**: 372,018
- **Descripcion**: VBP agricola a precios constantes base 2007
- **Variables**: producto, departamento, mes, produccion, precio base 2007, VBP en millones
- **Granularidad**: Mensual, por departamento y cultivo
- **Periodo**: 2007-2023
- **Particularidad**: Incluye tipo AGRICOLA y PECUARIO; el extractor filtra solo AGRICOLA. Meses en texto (Enero, Febrero...) convertidos a numeros

### 3. SISCOMEX - Comercio Exterior Agrario
- **Archivo**: SISCOMEX.xlsx
- **Registros**: 64,372
- **Descripcion**: Operaciones de importacion y exportacion de productos agrarios
- **Variables**: tipo operacion, codigo arancelario, producto, pais, peso neto/bruto (TM), valor FOB/CIF (miles USD)
- **Granularidad**: Mensual, por producto y pais
- **Periodo**: 2015-2023

### 4. SISAP - Precios en Mercados Mayoristas
- **Archivo**: SISAP.xlsx
- **Registros**: 4,415
- **Descripcion**: Precios de productos agricolas en mercados mayoristas
- **Variables**: codigo genero, cultivo, variedad, precio por kg en soles
- **Granularidad**: Por producto y variedad
- **Periodo**: Variable

### 5. SISAGRI_OTROS - Cultivos Complementarios
- **Archivo**: SISAGRI_OTROS_CULTIVOS.xlsx
- **Registros**: 8,686
- **Descripcion**: Produccion de cultivos no incluidos en SISAGRI principal
- **Variables**: cultivo, departamento, anio, mes, indicador (produccion/cosecha/siembra/precio), valor
- **Granularidad**: Mensual, por departamento
- **Particularidad**: Formato largo (indicador/valor). El extractor pivotea a formato ancho con columnas separadas por indicador

## Mercados Mayoristas de Referencia

| Mercado | Ciudad | Departamento |
|---------|--------|-------------|
| Gran Mercado Mayorista de Lima | Lima | Lima |
| Mercado Mayorista de Arequipa | Arequipa | Arequipa |
| Mercado Mayorista Moshoqueque | Chiclayo | Lambayeque |
| Mercado Mayorista de Huancayo | Huancayo | Junin |
| Mercado Mayorista de Trujillo | Trujillo | La Libertad |

## Cultivos Principales

**Cereales**: Arroz, Maiz Amarillo Duro, Maiz Amilaceo, Trigo, Cebada, Quinua

**Frutas**: Uva, Palta, Mango, Arandano, Mandarina, Platano, Aceituna

**Tuberculos**: Papa, Yuca

**Industriales**: Cana de Azucar, Algodon

**Estimulantes**: Cafe, Cacao

**Hortalizas**: Esparrago

## Descarga de Datos

1. Ir a https://siea.midagri.gob.pe
2. Navegar a los dashboards Power BI del SIEA
3. En cada dashboard, usar la opcion de exportar datos
4. Descargar los archivos Excel correspondientes
5. Colocar los archivos en `data/raw/` con los nombres originales

## Consideraciones

- Los datos son publicados con un desfase de 2-3 meses
- SISAGRI principal puede contener datos preliminares que se revisan en publicaciones posteriores
- El VBP usa precios base 2007 para comparabilidad temporal
- SISCOMEX reporta valores FOB para exportaciones y CIF para importaciones
