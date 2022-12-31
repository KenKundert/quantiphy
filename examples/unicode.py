from quantiphy import Quantity
import textwrap

Quantity.set_prefs(
    map_sf = Quantity.map_sf_to_sci_notation,
    spacer = Quantity.non_breaking_space
)
constants = [
    Quantity('h'),
    Quantity('hbar'),
    Quantity('k'),
    Quantity('q'),
    Quantity('c'),
    Quantity('0C'),
    Quantity('eps0'),
    Quantity('mu0'),
]
sentences = [f'{q.desc.capitalize()} is {q}.' for q in constants]
print(textwrap.fill('  '.join(sentences)))
