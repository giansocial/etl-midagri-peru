from setuptools import setup, find_packages

setup(
    name="etl-midagri-peru",
    version="1.0.0",
    description="ETL Pipeline para datos de produccion agricola del Peru (MIDAGRI/SIEA)",
    author="Gian Cruz",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "requests>=2.31",
        "beautifulsoup4>=4.12",
        "openpyxl>=3.1",
        "lxml>=4.9",
        "unidecode>=1.3",
        "psycopg2-binary>=2.9",
        "sqlalchemy>=2.0",
        "python-dotenv>=1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "faker>=18.0",
        ],
    },
)
