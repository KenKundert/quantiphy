from typing import Any, Callable, Sequence

class QuantiPhyError(Exception):
    args: tuple
    kwargs: dict

    def render(self, template: str) -> str:
        ...

class ExpectedQuantity(QuantiPhyError, ValueError):
    ...

class IncompatibleUnits(QuantiPhyError, TypeError):
    ...

class InvalidNumber(QuantiPhyError, ValueError, TypeError):
    ...

class InvalidRecognizer(QuantiPhyError, KeyError):
    ...

class MissingName(QuantiPhyError, NameError):
    ...

class UnknownConversion(QuantiPhyError, KeyError):
    ...

class UnknownFormatKey(QuantiPhyError, KeyError):
    ...

class UnknownPreference(QuantiPhyError, KeyError):
    ...

class UnknownScaleFactor(QuantiPhyError, ValueError):
    ...

class UnknownUnitSystem(QuantiPhyError, KeyError):
    ...

class IncompatiblePreferences(QuantiPhyError, ValueError):
    ...


__released__: str
__version__: str

class Quantity(float):
    units: str
    name: str
    desc: str
    non_breaking_space: str
    narrow_non_breaking_space: str
    thin_space: str
    plus_sign: str
    minus_sign: str
    infinity_symbol: str
    all_sf: str

    def __new__(
        cls,
        value: float | str | Quantity,
        model: str | Quantity = ...,
        *,
        units: str = ...,
        scale: str | float | tuple[float | Quantity, str] | Callable = ...,
        name: str = ...,
        desc: str = ...,
        ignore_sf: bool = ...,
        binary: bool = ...,
        params: Any = ...,
    ) -> Quantity:
        ...

    @classmethod
    def reset_prefs(cls) -> None:
        ...

    @classmethod
    def set_prefs(cls, **kwargs) -> None:
        ...

    @classmethod
    def get_pref(cls, name: str):
        ...

    @classmethod
    def prefs(cls, **kwargs):
        ...

    def __getattr__(self, name: str) -> Any:
        ...

    def is_infinite(self) -> str | None:
        ...

    def is_nan(self) -> str | None:
        ...

    def as_tuple(self) -> tuple[float, str]:
        ...

    def scale(
        self,
        scale: str | float | tuple[float | Quantity, str] | Callable,
        cls: type = ...
    ) -> Quantity:
        ...

    def add(
        self,
        addend: float | Quantity,
        check_units: bool = ...,
    ):
        ...

    def render(
        self,
        form: str = ...,
        show_units: bool = ...,
        prec: int = ...,
        show_label: bool = ...,
        strip_zeros:bool = ...,
        strip_radix: bool = ...,
        scale: str | float | tuple[float | Quantity, str] | Callable = ...,
        negligible: float = ...,
    ) -> str:
        ...

    def fixed(
        self,
        show_units: bool = ...,
        prec: int = ...,
        show_label: bool = ...,
        show_commas: bool = ...,
        strip_zeros: bool = ...,
        strip_radix: bool = ...,
        scale: str | float | tuple[float | Quantity, str] | Callable = ...,
    ) -> str:
        ...

    def binary(
        self,
        show_units: bool = ...,
        prec: int = ...,
        show_label: bool = ...,
        strip_zeros: bool = ...,
        strip_radix: bool = ...,
        scale: str | float | tuple[float | Quantity, str] | Callable = ...,
    ) -> str:
        ...

    def is_close(
        self,
        other: float | str | Quantity,
        reltol: float = ...,
        abstol: float = ...,
        check_units: bool = ...,
    ):
        ...

    def format(self, template: str) -> str:
        ...

    def __format__(self, template: str) -> str:
        ...

    @classmethod
    def extract(
        cls,
        text: str,
        predefined: dict = ...,
        **kwargs,
    ):
        ...

    @staticmethod
    def map_sf_to_sci_notation(sf: str):
        ...

    @staticmethod
    def map_sf_to_greek(sf: str) -> str | tuple[str, bool]:
        ...

    @classmethod
    def all_from_conv_fmt(
        cls,
        text: str,
        only_e_notation: bool = ...,
        **kwargs,
    ):
        ...

    @classmethod
    def all_from_si_fmt(
        cls,
        text:str,
        **kwargs
    ):
        ...

class UnitConversion:

    def __init__(
        self,
        to_units: str | Quantity | Sequence[str],
        from_units: str | Quantity | Sequence[str],
        slope: float | Callable = ...,
        intercept: float | Callable = ...,
    ) -> None:
        ...

    def activate(self) -> None:
        ...

    def convert(
        self,
        value: float | str | Quantity = ...,
        from_units: str = ...,
        to_units: str = ...,
        as_tuple: bool = ...,
    ):
        ...

    @staticmethod
    def fixture(converter_func):
        ...

    def clear_all(self) -> None:
        ...

def set_unit_system(unit_system: str) -> None:
    ...

def add_constant(
    value: Quantity | str,
    alias: str = ...,
    unit_systems: str | Sequence[str] = ...,
) -> None:
    ...

def as_real(
    value: float | str | Quantity,
    model: str | Quantity = ...,
    *,
    units: str = ...,
    scale: str | float | tuple[float | Quantity, str] | Callable = ...,
    name: str = ...,
    desc: str = ...,
    ignore_sf: bool = ...,
    binary: bool = ...,
    params: Any = ...
) -> float:
    ...

def as_tuple(
    value: float | str | Quantity,
    model: str | Quantity = ...,
    *,
    units: str = ...,
    scale: str | float | tuple[float | Quantity, str] | Callable = ...,
    name: str = ...,
    desc: str = ...,
    ignore_sf: bool = ...,
    binary: bool = ...,
    params: Any = ...
) -> tuple[float, str]:
    ...

def render(
    value: float,
    units: str,
    form: str = ...,
    show_units: bool = ...,
    prec: int = ...,
    show_label: bool = ...,
    strip_zeros:bool = ...,
    strip_radix: bool = ...,
    scale: str | float | tuple[float | Quantity, str] | Callable = ...,
    negligible: float = ...,
) -> str:
    ...

def fixed(
    value: float,
    units: str,
    show_units: bool = ...,
    prec: int = ...,
    show_label: bool = ...,
    show_commas: bool = ...,
    strip_zeros: bool = ...,
    strip_radix: bool = ...,
    scale: str | float | tuple[float | Quantity, str] | Callable = ...,
) -> str:
    ...

def binary(
    value: float,
    units: str,
    show_units: bool = ...,
    prec: int = ...,
    show_label: bool = ...,
    strip_zeros: bool = ...,
    strip_radix: bool = ...,
    scale: str | float | tuple[float | Quantity, str] | Callable = ...,
) -> str:
    ...

