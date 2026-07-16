CREATE INDEX IF NOT EXISTS idx_fact_prod_cultivo ON fact_produccion(cultivo_id);
CREATE INDEX IF NOT EXISTS idx_fact_prod_ubicacion ON fact_produccion(ubicacion_id);
CREATE INDEX IF NOT EXISTS idx_fact_prod_tiempo ON fact_produccion(tiempo_id);
CREATE INDEX IF NOT EXISTS idx_fact_prod_cultivo_tiempo ON fact_produccion(cultivo_id, tiempo_id);

CREATE INDEX IF NOT EXISTS idx_fact_precios_cultivo ON fact_precios_mercado(cultivo_id);
CREATE INDEX IF NOT EXISTS idx_fact_precios_mercado ON fact_precios_mercado(mercado_id);
CREATE INDEX IF NOT EXISTS idx_fact_precios_tiempo ON fact_precios_mercado(tiempo_id);
CREATE INDEX IF NOT EXISTS idx_fact_precios_cultivo_tiempo ON fact_precios_mercado(cultivo_id, tiempo_id);

CREATE INDEX IF NOT EXISTS idx_dim_ubicacion_depto ON dim_ubicacion(departamento);
CREATE INDEX IF NOT EXISTS idx_dim_tiempo_anio_mes ON dim_tiempo(anio, mes);
CREATE INDEX IF NOT EXISTS idx_dim_tiempo_campana ON dim_tiempo(campana_agricola);
CREATE INDEX IF NOT EXISTS idx_dim_cultivo_categoria ON dim_cultivo(categoria);

CREATE INDEX IF NOT EXISTS idx_fact_comex_tiempo ON fact_comercio_exterior(tiempo_id);
CREATE INDEX IF NOT EXISTS idx_fact_comex_tipo ON fact_comercio_exterior(tipo_operacion);
CREATE INDEX IF NOT EXISTS idx_fact_comex_pais ON fact_comercio_exterior(pais);
CREATE INDEX IF NOT EXISTS idx_fact_comex_producto ON fact_comercio_exterior(producto);

CREATE INDEX IF NOT EXISTS idx_fact_vbp_cultivo ON fact_vbp(cultivo_id);
CREATE INDEX IF NOT EXISTS idx_fact_vbp_ubicacion ON fact_vbp(ubicacion_id);
CREATE INDEX IF NOT EXISTS idx_fact_vbp_tiempo ON fact_vbp(tiempo_id);
