from datetime import date
from typing import List
from math import isclose
from scipy.optimize import newton

from .fixedcoupon import FixedCoupon

class CLBond:
    def __init__(self, cupones_fijos: List[FixedCoupon], tera=None):
        self.cupones_fijos = cupones_fijos
        self.tera = tera if tera is not None else self.calcular_tera()
        self.fecha_emision = self.cupones_fijos[0].fecha_inicio #para hacer que no sea 0.5 siempre el yf

    def calcular_tera(self):
        suposicion_inicial = 0.04 
        tera = newton(lambda tasa: sum((cupon.flujo) / ((1 + tasa) ** self.obtener_fraccion_temporal(self.fecha_emision, cupon.fecha_fin)) for cupon in self.cupones_fijos) - 1, x0=suposicion_inicial)
        return tera 

    def establecer_tera(self):
        nueva_tera = self.calcular_tera()
        if nueva_tera is not None and not isclose(self.tera, nueva_tera):
            self.tera = nueva_tera

    def obtener_fraccion_temporal(self, fecha_inicio: date, fecha_fin: date) -> float:
        return (fecha_fin - fecha_inicio).days / 360

    # valor par
     def obtener_valor_par(self, )  

     #valor presente
    def obtener_valor_presente(self, )
        
    #precio
    def obtener_precio(self, ) # depende del valor presente

    def obtener_valor(self, nominal: float, tasa: float, fecha: date) -> float: # depende de valor par, valor presente y precio
        return nominal * sum((cupon.amortizacion + cupon.interes) / ((1 + tasa) ** ((cupon.fecha_fin - fecha).days / 360)) for cupon in self.cupones_fijos)

    def obtener_dv01(self, nominal: float) -> float: # depende de valor presente
        return nominal * sum((cupon.amortizacion + cupon.interes) * ((cupon.fecha_fin - cupon.fecha_inicio).days / 360) / ((1 + self.tera) ** ((cupon.fecha_fin - cupon.fecha_inicio).days / 360 + 1)) for cupon in self.cupones_fijos)
