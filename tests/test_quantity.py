# encoding: utf8

from parametrize_from_file import parametrize, Namespace
import pytest
from functools import partial
from voluptuous import Schema, Optional, Required

from quantiphy import Quantity
Quantity.reset_prefs()

def name_from_dict_keys(cases):
    return [{**v, 'name': k} for k,v in cases.items()]

parametrize_from_file = partial(parametrize, preprocess=name_from_dict_keys)

with_quantiphy = Namespace('from quantiphy import Quantity')

# Schema for test cases
# Errors are indicated by a lack of a tests field.
schema = Schema({
    Required('name'): str,
    Required('given'): str,
    Optional('prefs', default='{}'): eval,
    Optional('tests', default={}): {str: {str:str}},
    Optional('error', default=''): str,
})

@parametrize_from_file(schema=schema)
def test_number_recognition(name, given, prefs, tests, error):
    with Quantity.prefs(**prefs):
        try:
            defined = with_quantiphy.exec(given)
        except (ValueError, KeyError) as e:
            assert not tests, name
            assert str(e) == error, name
            return

        for id, test in tests.items():
            result = eval(test['evaluate'], {}, defined)
            expected = eval(test['expected'], {}, defined)
            assert result == pytest.approx(expected, abs=0, nan_ok=True), f'{name} {id}'
