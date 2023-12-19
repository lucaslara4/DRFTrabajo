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
    
    def obtener_cupon_actual(self, date: date) -> FixedCoupon: # necesario para ver el cupon que vamos a trabajar e ir cambiando
        for current in self.cupones_fijos:
            if current.fecha_inicio <= date and current.fecha_fin > date:
                return current

     def obtener_interes_acumulado(self, date: date, interes_acumulado) -> float:
        interes_acumulado = self.interes_acumulado if interes_acumulado is None else interes_acumulado
        cupon_actual = self.obtener_cupon_actual(date)
        
        if date >= cupon_actual.fecha_fin or date <= self.fecha_emision:
            return interes_acumulado
        
        interes_acumulado += cupon_actual.obtener_interes_acumulado(date, self.tera)
        return interes_acumulado

    # valor par
     def obtener_valor_par(self,date: date) -> float:
        cupon_actual = self.obtener_cupon_actual(date)
        dias_a_vencimiento = (cupon_actual.fecha_fin - date).days
        factor_de_descuento = 1/((1+self.tera) ** (dias_a_vencimiento/360))
        valor_par = cupon_actual.saldo_residual * factor_de_descuento
        return round(valor_par)
    
     #valor presente
    def obtener_valor_presente(self, date: date, tera: float) -> float:
        valores_presente = 0
        for coupon in self.cupones_fijos:
            if coupon.fecha_fin > date:
                dias_a_vencimiento = (coupon.fecha_fin - date).days
                factor_de_descuento = 1 / ((1 + tera) ** (dias_a_vencimiento / 360))
                valores_presente += coupon.flujo * factor_de_descuento
        return valores_presente
        
    #precio
    def obtener_precio(self, date: date) -> float: # depende del valor presente
        vp = self.obtener_valor_presente(date)
        valor_par = self.obtener_valor_par(date)
        precio = round(100 * vp/valor_par)
        return precio

    def obtener_valor(self, nominal: float, tasa: float, fecha: date) -> float: # depende de valor par y precio
        precio = self.obtener_precio(date)
        valor_par = self.obtener_valor_par(date)
        return nominal * precio * valor_par / 10000

    def obtener_dv01(self, nominal: float) -> float: # depende de valor presente
       vp = self.obtener_valor_presente(date)
       vp_r = self.obtener_valor_presente(self.fecha_emision,self.tera)
       r_mas_01 = self.tera + 0.0001
       vp_por_r_mas_01 = self.obtener_valor_presente(self.fecha_emision,r_mas_01)
       dv_01 = vp_por_r_mas_01 - vp_r
       return dv_01