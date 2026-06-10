CREATE TABLE IF NOT EXISTS fact_produccion (
    id SERIAL PRIMARY KEY,
    cultivo_id INT NOT NULL REFERENCES dim_cultivo(id),
    ubicacion_id INT NOT NULL REFERENCES dim_ubicacion(id),
    tiempo_id INT NOT NULL REFERENCES dim_tiempo(id),
    superficie_sembrada_ha DECIMAL(12,2),
    superficie_cosechada_ha DECIMAL(12,2),
    produccion_toneladas DECIMAL(14,2),
    rendimiento_kg_ha DECIMAL(10,2),
    precio_chacra_soles DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cultivo_id, ubicacion_id, tiempo_id)
);

CREATE TABLE IF NOT EXISTS fact_precios_mercado (
    id SERIAL PRIMARY KEY,
    cultivo_id INT NOT NULL REFERENCES dim_cultivo(id),
    mercado_id INT NOT NULL REFERENCES dim_mercado(id),
    tiempo_id INT NOT NULL REFERENCES dim_tiempo(id),
    precio_minimo DECIMAL(10,2),
    precio_maximo DECIMAL(10,2),
    precio_promedio DECIMAL(10,2),
    volumen_toneladas DECIMAL(12,2),
    variacion_pct DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cultivo_id, mercado_id, tiempo_id)
);

CREATE TABLE IF NOT EXISTS fact_comercio_exterior (
    id SERIAL PRIMARY KEY,
    tiempo_id INT NOT NULL REFERENCES dim_tiempo(id),
    tipo_operacion VARCHAR(20) NOT NULL,
    cod_arancel VARCHAR(20),
    producto VARCHAR(200) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    peso_neto_tm DECIMAL(14,6),
    peso_bruto_tm DECIMAL(14,6),
    valor_fob_miles_usd DECIMAL(14,6),
    valor_cif_miles_usd DECIMAL(14,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_vbp (
    id SERIAL PRIMARY KEY,
    cultivo_id INT NOT NULL REFERENCES dim_cultivo(id),
    ubicacion_id INT NOT NULL REFERENCES dim_ubicacion(id),
    tiempo_id INT NOT NULL REFERENCES dim_tiempo(id),
    produccion_toneladas DECIMAL(14,2),
    precio_base_2007 DECIMAL(12,6),
    vbp_millones DECIMAL(14,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cultivo_id, ubicacion_id, tiempo_id)
);
