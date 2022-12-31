from quantiphy import Quantity
Quantity.set_prefs(
    show_label = True,
    show_desc = True,
    label_fmt = '{n} = {v}',
    label_fmt_full = '{V:<18}  # {d}',
)

T = Quantity(300, 'T K ambient temperature')
# T = Quantity(27, 'T C ambient temperature', scale='K')
k = Quantity('k')
q = Quantity('q')
Vt = Quantity(k*T/q, f'Vt V thermal voltage at {T:q}')

print(T, k, q, Vt, sep='\n')
