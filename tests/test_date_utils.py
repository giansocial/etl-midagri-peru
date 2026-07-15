import pytest
from src.utils.date_utils import (
    get_campana_agricola,
    es_epoca_siembra,
    es_epoca_cosecha,
    get_nombre_mes,
    get_trimestre,
    get_semestre,
    generar_rango_meses,
)


def test_agosto_inicia_campana():
    assert get_campana_agricola(2023, 8) == "2023-2024"


def test_diciembre_misma_campana():
    assert get_campana_agricola(2023, 12) == "2023-2024"


def test_enero_campana_anterior():
    assert get_campana_agricola(2024, 1) == "2023-2024"


def test_julio_campana_anterior():
    assert get_campana_agricola(2024, 7) == "2023-2024"


def test_mes_cero_retorna_vacio():
    assert get_campana_agricola(2023, 0) == ""


def test_mes_invalido_retorna_vacio():
    assert get_campana_agricola(2023, 13) == ""


@pytest.mark.parametrize("mes", [8, 9, 10, 11, 12, 1])
def test_meses_siembra(mes):
    assert es_epoca_siembra(mes) is True


@pytest.mark.parametrize("mes", [2, 3, 4, 5, 6, 7])
def test_meses_no_siembra(mes):
    assert es_epoca_siembra(mes) is False


@pytest.mark.parametrize("mes", [3, 4, 5, 6, 7])
def test_meses_cosecha(mes):
    assert es_epoca_cosecha(mes) is True


@pytest.mark.parametrize("mes", [1, 2, 8, 9, 10, 11, 12])
def test_meses_no_cosecha(mes):
    assert es_epoca_cosecha(mes) is False


def test_get_nombre_mes_enero():
    assert get_nombre_mes(1) == "Enero"


def test_get_nombre_mes_diciembre():
    assert get_nombre_mes(12) == "Diciembre"


def test_get_nombre_mes_invalido():
    assert get_nombre_mes(13) == ""


def test_get_nombre_mes_cero():
    assert get_nombre_mes(0) == ""


def test_primer_trimestre():
    assert get_trimestre(1) == 1
    assert get_trimestre(3) == 1


def test_cuarto_trimestre():
    assert get_trimestre(10) == 4
    assert get_trimestre(12) == 4


def test_primer_semestre():
    assert get_semestre(1) == 1
    assert get_semestre(6) == 1


def test_segundo_semestre():
    assert get_semestre(7) == 2
    assert get_semestre(12) == 2


def test_rango_mismo_anio():
    resultado = generar_rango_meses(2023, 1, 2023, 3)
    assert resultado == [(2023, 1), (2023, 2), (2023, 3)]


def test_rango_cruce_anio():
    resultado = generar_rango_meses(2023, 11, 2024, 2)
    assert resultado == [(2023, 11), (2023, 12), (2024, 1), (2024, 2)]


def test_rango_un_solo_mes():
    resultado = generar_rango_meses(2023, 5, 2023, 5)
    assert resultado == [(2023, 5)]
