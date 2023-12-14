#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import locale

#Función calculadora UF
def get_ufs(date_last_uf, last_uf_day_9, ipc_day_9):
    # Validador de la fecha objetivo sea 9
    if date_last_uf.day != 9:
        raise ValueError("Error: La función solo admite el día 9 del mes.")

    # Obtener el último día del mes actual
    ultimo_dia_mes_actual = date_last_uf.replace(day=1) + timedelta(days=calendar.monthrange(date_last_uf.year, date_last_uf.month)[1])

    # Calcular la cantidad total de días en el mes de la última UF conocida
    dias_en_mes = calendar.monthrange(date_last_uf.year, date_last_uf.month)[1]

    # Calcular la diferencia de días entre el 9 de diciembre y el último día del mes actual
    diferencia_dias = (ultimo_dia_mes_actual.replace(day=9) - date_last_uf.replace(day=9)).days

    # Inicializar el diccionario de resultados
    uf_values = {}

    # Calcular el valor de la UF para cada día desde la fecha inicial hasta el 9 del siguiente mes
    for i in range(0, diferencia_dias + 1):
        fecha_actual = date_last_uf + timedelta(days=i)
        valor_uf_objetivo = round(last_uf_day_9 * (1 + ipc_day_9) ** (i / dias_en_mes), 2)
        uf_values[fecha_actual.strftime('%d-%m-%Y')] = valor_uf_objetivo

    return uf_values