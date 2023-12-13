### main entregable 3 Derivados renta fija: Tomás Barría, Francisco Gorigoitía, Lucas Laragit config --global user.name "FIRST_NAME LAST_NAME"

# si no funciona usar tal cual: (incluido el punto)
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
print(valor_uf["09-01-2024"])