from datetime import date

class FixedCoupon:
    def __init__(self, amortizacion: float, interes: float, saldo_residual: float, fecha_inicio: date, fecha_fin: date):
        self._validate_value("amortizacion", amortizacion)
        self._validate_value("interes", interes)
        self._validate_value("saldo_residual", saldo_residual)

        self.amortizacion = float(amortizacion)
        self.interes = float(interes)
        self.saldo_residual = float(saldo_residual)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cupon = self.calculate_cupon()

    def _validate_value(self, name: str, value: float):
        if not isinstance(value, float) or value < 0 or value > 100:
            raise ValueError(f"{name.capitalize()} debe ser un número no negativo y menor a 100.")

    def calculate_cupon(self):
        days_to_coupon = (self.fecha_fin - self.fecha_inicio).days
        return (self.amortizacion + self.interes) / ((1 + self.interes) ** (days_to_coupon / 365))
