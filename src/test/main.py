### main entregable 3 Derivados renta fija: Tomás Barría, Francisco Gorigoitía, Lucas Laragit config --global user.name "FIRST_NAME LAST_NAME"

## ejemplos para entregable 3:

# si no funciona, usar tal cual: (incluido el punto)
# pip install .

from datetime import date
from datetime import datetime
from mypackage.funcs.functions import get_ufs

# Ejemplo uf diciembre 9 2023 al 9 de enero 2024
last_uf_day_9 = 36607.69  # El valor de la UF para el día 9 del último mes
ipc_day_9 = 0.007  # El IPC para el día 9 del último mes
date_last_uf = datetime(2023, 12, 9)  # Fecha inicial

# Calcular los valores de la UF hasta el próximo 9 del proximo mes:
valor_uf = get_ufs(date_last_uf, last_uf_day_9, ipc_day_9)
print(f"El valor de la UF es: $ {valor_uf['09-01-2024']}")

## ejemplos para el entregable 4:

from mypackage.fixedincome.clbonds import CLBond
from mypackage.fixedincome.fixedcoupon import FixedCoupon
from datetime import date

# Crear instancias de FixedCoupon con fechas de inicio y fin
coupon1 = FixedCoupon(amortizacion=99.0, interes=0.009, saldo_residual=95.0, fecha_inicio=date(2022, 1, 1), fecha_fin=date(2022, 12, 31))
coupon2 = FixedCoupon(amortizacion=70.0, interes=0.006, saldo_residual=11.0, fecha_inicio=date(2022, 1, 1), fecha_fin=date(2022, 12, 31))

# Crear lista de cupones fijos
fixed_coupons_list = [coupon1, coupon2]

# Crear instancia de CLBond
cl_bond = CLBond(cupones_fijos=fixed_coupons_list)

# Imprimir el valor de la "tera"
print("Tera:", cl_bond.tera)

# Imprimir el valor del bono para un notional, tasa y fecha dados
notional_value = 1000000.0
interest_rate = 0.05
valuation_date = date(2023, 1, 1)

bond_value = cl_bond.obtener_valor(notional_value, interest_rate, valuation_date)
print("Valor del bono:", bond_value)