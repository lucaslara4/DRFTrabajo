from datetime import date
from typing import List
from math import isclose
from scipy.optimize import newton

class FixedCoupon:
    def __init__(self, amortizacion: float, interes: float, saldo_residual: float):
        self._validate_value("amortizacion", amortizacion)
        self._validate_value("interes", interes)
        self._validate_value("saldo_residual", saldo_residual)
        
        self.amortizacion = float(amortizacion)
        self.interes = float(interes)
        self.saldo_residual = float(saldo_residual)
        self.cupon = self.calculate_cupon()

    def _validate_value(self, name: str, value: float):
        if not isinstance(value, float) or value < 0 or value > 100:
            raise ValueError(f"{name.capitalize()} debe ser un número no negativo y menor a 100.")

    def calculate_cupon(self):
        return self.amortizacion + self.interes

class CLBond:
    def __init__(self, cupones_fijos: List[FixedCoupon], tera=None):
        self.cupones_fijos = cupones_fijos
        self.tera = tera if tera is not None else self.calcular_tera()

    def calcular_tera(self):
        suposicion_inicial = sum(cupon.amortizacion + cupon.interes for cupon in self.cupones_fijos) / len(self.cupones_fijos)
        tera = newton(lambda tasa: sum((cupon.amortizacion + cupon.interes) / ((1 + tasa) ** self.obtener_fraccion_temporal(cupon.fecha_inicio, cupon.fecha_fin)) for cupon in self.cupones_fijos) - 1, x0=suposicion_inicial)
        return tera

    def establecer_tera(self):
        nueva_tera = self.calcular_tera()
        if nueva_tera is not None and not isclose(self.tera, nueva_tera):
            self.tera = nueva_tera

    def obtener_valor(self, nominal: float, tasa: float, fecha: date) -> float:
        return nominal * sum((cupon.amortizacion + cupon.interes) / ((1 + tasa) ** ((cupon.fecha_fin - fecha).days / 365)) for cupon in self.cupones_fijos)

    def obtener_dv01(self, nominal: float) -> float:
        return nominal * sum((cupon.amortizacion + cupon.interes) * ((cupon.fecha_fin - cupon.fecha_inicio).days / 365) / ((1 + self.tera) ** ((cupon.fecha_fin - cupon.fecha_inicio).days / 365 + 1)) for cupon in self.cupones_fijos)

    def obtener_wf(self, tasa: float, fecha_inicio: date, fecha_fin: date) -> float:
        fraccion_temporal = (fecha_fin - fecha_inicio).days / 365
        return (1 + tasa) ** fraccion_temporal

    def obtener_fraccion_temporal(self, fecha_inicio: date, fecha_fin: date) -> float:
        return (fecha_fin - fecha_inicio).days / 365

    def obtener_derivada_npv(self, tasa, cupon):
        return -cupon.amortizacion * ((cupon.fecha_fin - cupon.fecha_inicio).days / 365) * (1 + tasa) ** (((cupon.fecha_fin - cupon.fecha_inicio).days / 365) - 1)

    def _obtener_wf_desde_tasa_compuesta(self, valor_tasa: float, fecha_inicio: date, fecha_fin: date) -> float:
        fraccion_temporal = (fecha_fin - fecha_inicio).days / 365
        return (1 + valor_tasa) ** fraccion_temporal

