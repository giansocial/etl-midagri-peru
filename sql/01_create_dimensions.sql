-- todo: evaluar si particionamos dim_tiempo por anio cuando crezca
CREATE TABLE IF NOT EXISTS dim_cultivo (
    id SERIAL PRIMARY KEY,
    codigo varchar(20) UNIQUE NOT NULL,
    nombre varchar(100) NOT NULL,
    categoria varchar(50) NOT NULL,
    subcategoria varchar(50),
    es_exportable BOOLEAN DEFAULT FALSE,
    campana_inicio_mes INT,
    campana_fin_mes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_ubicacion (
    id SERIAL PRIMARY KEY,
    ubigeo varchar(6) UNIQUE,
    departamento varchar(50) NOT NULL,
    provincia varchar(80),
    distrito varchar(100),
    region_natural varchar(20),
    altitud_msnm INT,
    latitud DECIMAL(10,7),
    longitud DECIMAL(10,7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_mercado (
    id SERIAL PRIMARY KEY,
    nombre varchar(100) UNIQUE NOT NULL,
    ciudad varchar(50) NOT NULL,
    departamento varchar(50) NOT NULL,
    tipo varchar(30) DEFAULT 'Mayorista',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_tiempo (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    anio INT NOT NULL,
    trimestre INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes varchar(20) NOT NULL,
    semestre INT NOT NULL,
    campana_agricola varchar(20),
    es_epoca_siembra BOOLEAN DEFAULT FALSE,
    es_epoca_cosecha BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
