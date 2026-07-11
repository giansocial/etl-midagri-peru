from datetime import datetime, date
from typing import List, Tuple


def get_campana_agricola(anio: int, mes: int) -> str:
    if mes >= 8:
        return f"{anio}-{anio + 1}"
    return f"{anio - 1}-{anio}"


def es_epoca_siembra(mes: int) -> bool:
    return mes in (8, 9, 10, 11, 12, 1)


def es_epoca_cosecha(mes: int) -> bool:
    return mes in (3, 4, 5, 6, 7)


def get_nombre_mes(mes: int) -> str:
    nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    }
    return nombres.get(mes, "")


def get_trimestre(mes: int) -> int:
    return (mes - 1) // 3 + 1


def get_semestre(mes: int) -> int:
    return 1 if mes <= 6 else 2


def generar_rango_meses(
    anio_inicio: int,
    mes_inicio: int,
    anio_fin: int,
    mes_fin: int,
) -> List[Tuple[int, int]]:
    resultado = []
    anio, mes = anio_inicio, mes_inicio
    while (anio, mes) <= (anio_fin, mes_fin):
        resultado.append((anio, mes))
        mes += 1
        if mes > 12:
            mes = 1
            anio += 1
    return resultado
