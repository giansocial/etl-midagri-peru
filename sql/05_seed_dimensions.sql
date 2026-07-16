INSERT INTO dim_cultivo (codigo, nombre, categoria, es_exportable) VALUES
    ('ARR', 'Arroz', 'Cereales', FALSE),
    ('PAP', 'Papa', 'Tuberculos', FALSE),
    ('MAD', 'Maiz Amarillo Duro', 'Cereales', FALSE),
    ('MAA', 'Maiz Amilaceo', 'Cereales', FALSE),
    ('TRI', 'Trigo', 'Cereales', FALSE),
    ('CEB', 'Cebada Grano', 'Cereales', FALSE),
    ('CAF', 'Cafe', 'Estimulantes', TRUE),
    ('CAC', 'Cacao', 'Estimulantes', TRUE),
    ('QUI', 'Quinua', 'Cereales', TRUE),
    ('ESP', 'Esparrago', 'Hortalizas', TRUE),
    ('UVA', 'Uva', 'Frutas', TRUE),
    ('PAL', 'Palta', 'Frutas', TRUE),
    ('MAN', 'Mango', 'Frutas', TRUE),
    ('ARA', 'Arandano', 'Frutas', TRUE),
    ('MDR', 'Mandarina', 'Frutas', TRUE),
    ('PLT', 'Platano', 'Frutas', FALSE),
    ('YUC', 'Yuca', 'Tuberculos', FALSE),
    ('CDA', 'Cana de Azucar', 'Industriales', FALSE),
    ('ALG', 'Algodon', 'Industriales', TRUE),
    ('ACE', 'Aceituna', 'Frutas', TRUE)
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO dim_ubicacion (departamento, region_natural) VALUES
    ('Amazonas', 'Selva'),
    ('Ancash', 'Costa'),
    ('Apurimac', 'Sierra'),
    ('Arequipa', 'Costa'),
    ('Ayacucho', 'Sierra'),
    ('Cajamarca', 'Sierra'),
    ('Cusco', 'Sierra'),
    ('Huancavelica', 'Sierra'),
    ('Huanuco', 'Sierra'),
    ('Ica', 'Costa'),
    ('Junin', 'Sierra'),
    ('La Libertad', 'Costa'),
    ('Lambayeque', 'Costa'),
    ('Lima', 'Costa'),
    ('Loreto', 'Selva'),
    ('Madre de Dios', 'Selva'),
    ('Moquegua', 'Costa'),
    ('Pasco', 'Sierra'),
    ('Piura', 'Costa'),
    ('Puno', 'Sierra'),
    ('San Martin', 'Selva'),
    ('Tacna', 'Costa'),
    ('Tumbes', 'Costa'),
    ('Ucayali', 'Selva')
ON CONFLICT DO NOTHING;

INSERT INTO dim_mercado (nombre, ciudad, departamento, tipo) VALUES
    ('Gran Mercado Mayorista de Lima', 'Lima', 'Lima', 'Mayorista'),
    ('Mercado Mayorista de Arequipa', 'Arequipa', 'Arequipa', 'Mayorista'),
    ('Mercado Mayorista Moshoqueque', 'Chiclayo', 'Lambayeque', 'Mayorista'),
    ('Mercado Mayorista de Huancayo', 'Huancayo', 'Junin', 'Mayorista'),
    ('Mercado Mayorista de Trujillo', 'Trujillo', 'La Libertad', 'Mayorista')
ON CONFLICT (nombre) DO NOTHING;
