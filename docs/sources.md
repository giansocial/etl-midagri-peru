# Fuentes de Datos

## SIEA - Sistema Integrado de Estadisticas Agrarias

**URL**: https://siea.midagri.gob.pe

**Institucion**: Ministerio de Desarrollo Agrario y Riego (MIDAGRI)

### Datasets Disponibles

#### Produccion Agricola
- **Descripcion**: Estadisticas mensuales de produccion agricola por departamento
- **Variables**: superficie sembrada, superficie cosechada, produccion (toneladas), rendimiento (kg/ha), precio en chacra (S/./kg)
- **Granularidad**: Mensual, por departamento y cultivo
- **Periodo**: 2000 - presente
- **Formato**: Excel (.xlsx), CSV

#### Precios en Mercados Mayoristas
- **Descripcion**: Precios de productos agricolas en los principales mercados mayoristas
- **Variables**: precio promedio, precio minimo, precio maximo, volumen
- **Granularidad**: Diaria/Semanal, por mercado y producto
- **Formato**: Excel (.xlsx)

### Mercados Mayoristas Incluidos

| Mercado | Ciudad | Departamento |
|---------|--------|-------------|
| Gran Mercado Mayorista de Lima | Lima | Lima |
| Mercado Mayorista de Arequipa | Arequipa | Arequipa |
| Mercado Mayorista Moshoqueque | Chiclayo | Lambayeque |
| Mercado Mayorista de Huancayo | Huancayo | Junin |
| Mercado Mayorista de Trujillo | Trujillo | La Libertad |

### Cultivos Principales

**Cereales**: Arroz, Maiz Amarillo Duro, Maiz Amilaceo, Trigo, Cebada, Quinua

**Frutas**: Uva, Palta, Mango, Arandano, Mandarina, Platano, Aceituna

**Tuberculos**: Papa, Yuca

**Industriales**: Cana de Azucar, Algodon

**Estimulantes**: Cafe, Cacao

**Hortalizas**: Esparrago

### Descarga de Datos

1. Ir a https://siea.midagri.gob.pe
2. Navegar a "Estadistica Agricola" > "Produccion Agricola"
3. Seleccionar los filtros deseados (departamento, cultivo, periodo)
4. Descargar en formato Excel o CSV
5. Colocar los archivos descargados en `data/raw/`

### Consideraciones

- Los datos son publicados con un desfase de 2-3 meses
- Algunas series pueden tener datos preliminares que se actualizan posteriormente
- Los archivos Excel del SIEA pueden contener filas de encabezado adicionales que el extractor maneja automaticamente con el parametro `skiprows`
