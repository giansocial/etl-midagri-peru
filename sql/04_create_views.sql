CREATE OR REPLACE VIEW v_produccion_por_departamento AS
SELECT
    u.departamento,
    u.region_natural,
    c.nombre AS cultivo,
    c.categoria,
    t.anio,
    t.nombre_mes,
    f.superficie_cosechada_ha,
    f.produccion_toneladas,
    f.rendimiento_kg_ha,
    f.precio_chacra_soles
FROM fact_produccion f
JOIN dim_cultivo c ON f.cultivo_id = c.id
JOIN dim_ubicacion u ON f.ubicacion_id = u.id
JOIN dim_tiempo t ON f.tiempo_id = t.id;

CREATE OR REPLACE VIEW v_top_cultivos_por_region AS
SELECT
    u.departamento,
    u.region_natural,
    c.nombre AS cultivo,
    SUM(f.produccion_toneladas) AS produccion_total,
    AVG(f.rendimiento_kg_ha) AS rendimiento_promedio,
    AVG(f.precio_chacra_soles) AS precio_promedio,
    RANK() OVER (
        PARTITION BY u.departamento
        ORDER BY SUM(f.produccion_toneladas) DESC
    ) AS ranking
FROM fact_produccion f
JOIN dim_cultivo c ON f.cultivo_id = c.id
JOIN dim_ubicacion u ON f.ubicacion_id = u.id
JOIN dim_tiempo t ON f.tiempo_id = t.id
GROUP BY u.departamento, u.region_natural, c.nombre;

CREATE OR REPLACE VIEW v_precios_tendencia AS
SELECT
    c.nombre AS cultivo,
    c.categoria,
    m.nombre AS mercado,
    m.ciudad,
    t.anio,
    t.mes,
    t.nombre_mes,
    p.precio_promedio,
    p.precio_minimo,
    p.precio_maximo,
    p.variacion_pct,
    p.volumen_toneladas
FROM fact_precios_mercado p
JOIN dim_cultivo c ON p.cultivo_id = c.id
JOIN dim_mercado m ON p.mercado_id = m.id
JOIN dim_tiempo t ON p.tiempo_id = t.id;

CREATE OR REPLACE VIEW v_resumen_anual AS
SELECT
    t.anio,
    c.categoria,
    COUNT(DISTINCT c.id) AS num_cultivos,
    COUNT(DISTINCT u.departamento) AS num_departamentos,
    SUM(f.superficie_cosechada_ha) AS superficie_total_ha,
    SUM(f.produccion_toneladas) AS produccion_total_tn,
    AVG(f.rendimiento_kg_ha) AS rendimiento_promedio,
    AVG(f.precio_chacra_soles) AS precio_promedio
FROM fact_produccion f
JOIN dim_cultivo c ON f.cultivo_id = c.id
JOIN dim_ubicacion u ON f.ubicacion_id = u.id
JOIN dim_tiempo t ON f.tiempo_id = t.id
GROUP BY t.anio, c.categoria
ORDER BY t.anio, c.categoria;

CREATE OR REPLACE VIEW v_exportaciones_por_producto AS
SELECT
    t.anio,
    ce.producto,
    ce.pais,
    SUM(ce.peso_neto_tm) AS peso_total_tm,
    SUM(ce.valor_fob_miles_usd) AS valor_fob_total,
    COUNT(*) AS num_operaciones
FROM fact_comercio_exterior ce
JOIN dim_tiempo t ON ce.tiempo_id = t.id
WHERE ce.tipo_operacion = 'EXPORTACIONES'
GROUP BY t.anio, ce.producto, ce.pais
ORDER BY t.anio, valor_fob_total DESC;

CREATE OR REPLACE VIEW v_vbp_por_departamento AS
SELECT
    u.departamento,
    u.region_natural,
    c.nombre AS cultivo,
    t.anio,
    SUM(v.produccion_toneladas) AS produccion_total,
    SUM(v.vbp_millones) AS vbp_total,
    AVG(v.precio_base_2007) AS precio_base_promedio
FROM fact_vbp v
JOIN dim_cultivo c ON v.cultivo_id = c.id
JOIN dim_ubicacion u ON v.ubicacion_id = u.id
JOIN dim_tiempo t ON v.tiempo_id = t.id
GROUP BY u.departamento, u.region_natural, c.nombre, t.anio
ORDER BY t.anio, vbp_total DESC;
