CREATE TABLE IF NOT EXISTS dim_cultivo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    subcategoria VARCHAR(50),
    es_exportable BOOLEAN DEFAULT FALSE,
    campana_inicio_mes INT,
    campana_fin_mes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_ubicacion (
    id SERIAL PRIMARY KEY,
    ubigeo VARCHAR(6) UNIQUE,
    departamento VARCHAR(50) NOT NULL,
    provincia VARCHAR(80),
    distrito VARCHAR(100),
    region_natural VARCHAR(20),
    altitud_msnm INT,
    latitud DECIMAL(10,7),
    longitud DECIMAL(10,7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_mercado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    tipo VARCHAR(30) DEFAULT 'Mayorista',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_tiempo (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    anio INT NOT NULL,
    trimestre INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes VARCHAR(20) NOT NULL,
    semestre INT NOT NULL,
    campana_agricola VARCHAR(20),
    es_epoca_siembra BOOLEAN DEFAULT FALSE,
    es_epoca_cosecha BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
