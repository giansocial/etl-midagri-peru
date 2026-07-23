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


class TestGetCampanaAgricola:
    def test_agosto_inicia_campana(self):
        assert get_campana_agricola(2023, 8) == "2023-2024"

    def test_diciembre_misma_campana(self):
        assert get_campana_agricola(2023, 12) == "2023-2024"

    def test_enero_campana_anterior(self):
        assert get_campana_agricola(2024, 1) == "2023-2024"

    def test_julio_campana_anterior(self):
        assert get_campana_agricola(2024, 7) == "2023-2024"

    def test_mes_cero_retorna_vacio(self):
        assert get_campana_agricola(2023, 0) == ""

    def test_mes_invalido_retorna_vacio(self):
        assert get_campana_agricola(2023, 13) == ""


class TestEpocas:
    @pytest.mark.parametrize("mes", [8, 9, 10, 11, 12, 1])
    def test_meses_siembra(self, mes):
        assert es_epoca_siembra(mes) is True

    @pytest.mark.parametrize("mes", [2, 3, 4, 5, 6, 7])
    def test_meses_no_siembra(self, mes):
        assert es_epoca_siembra(mes) is False

    @pytest.mark.parametrize("mes", [3, 4, 5, 6, 7])
    def test_meses_cosecha(self, mes):
        assert es_epoca_cosecha(mes) is True

    @pytest.mark.parametrize("mes", [1, 2, 8, 9, 10, 11, 12])
    def test_meses_no_cosecha(self, mes):
        assert es_epoca_cosecha(mes) is False


class TestGetNombreMes:
    def test_enero(self):
        assert get_nombre_mes(1) == "Enero"

    def test_diciembre(self):
        assert get_nombre_mes(12) == "Diciembre"

    def test_mes_invalido(self):
        assert get_nombre_mes(13) == ""

    def test_mes_cero(self):
        assert get_nombre_mes(0) == ""


class TestTrimestre:
    def test_primer_trimestre(self):
        assert get_trimestre(1) == 1
        assert get_trimestre(3) == 1

    def test_cuarto_trimestre(self):
        assert get_trimestre(10) == 4
        assert get_trimestre(12) == 4


class TestSemestre:
    def test_primer_semestre(self):
        assert get_semestre(1) == 1
        assert get_semestre(6) == 1

    def test_segundo_semestre(self):
        assert get_semestre(7) == 2
        assert get_semestre(12) == 2


class TestGenerarRangoMeses:
    def test_mismo_anio(self):
        resultado = generar_rango_meses(2023, 1, 2023, 3)
        assert resultado == [(2023, 1), (2023, 2), (2023, 3)]

    def test_cruce_anio(self):
        resultado = generar_rango_meses(2023, 11, 2024, 2)
        assert resultado == [(2023, 11), (2023, 12), (2024, 1), (2024, 2)]

    def test_un_solo_mes(self):
        resultado = generar_rango_meses(2023, 5, 2023, 5)
        assert resultado == [(2023, 5)]
