---
id: computing-software.software-engineering.python.generics-typevar-and-paramspec
name: generics-typevar-and-paramspec
category: computing-software
field: software-engineering
product: python
tags: [python, python-typing, typevar, paramspec, pep-695, generics, type-parameters, typevartuple, concatenate, variance, self-type, py-typing-core]
level: advanced
status: verified
description: "Write generic Python functions, classes and decorators: PEP 695 syntax, bounds vs constraints, variance, ParamSpec for decorators, and Self."
sources: ["https://peps.python.org/pep-0695/", "https://peps.python.org/pep-0612/", "https://typing.python.org/en/latest/spec/generics.html", "https://docs.python.org/3/library/typing.html#typing.ParamSpec"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Generics: TypeVar, PEP 695 and ParamSpec

**Goal:** preserve the caller's types through containers, helpers and decorators
instead of degrading everything to `Any`.

## PEP 695 syntax (Python 3.12+)
```python
def first[T](items: Sequence[T]) -> T:
    return items[0]

class Box[T]:
    def __init__(self, item: T) -> None: self.item = item

def largest[T: SupportsLessThan](xs: Iterable[T]) -> T: ...   # bound (upper bound)
def concat[S: (str, bytes)](a: S, b: S) -> S: ...             # constrained: exactly str or bytes

type Json = dict[str, Json] | list[Json] | str | int | float | bool | None   # type alias
```
Older versions: `T = TypeVar("T", bound=...)` and `class Box(Generic[T])`.
Variance is inferred automatically with PEP 695; with old TypeVars declare
`covariant=True` for read-only containers.

## Bound vs constraints
- Bound `T: Base` accepts any subtype and returns that same subtype.
- Constraints `S: (str, bytes)` mean S is solved to exactly one listed type, so mixing
  `str` and `bytes` is rejected.

## Decorators with ParamSpec
```python
def retry[**P, R](times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def deco(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for i in range(times):
                try: return fn(*args, **kwargs)
                except TransientError:
                    if i == times - 1: raise
            raise AssertionError
        return wrapper
    return deco
```
Without ParamSpec, decorated functions lose their parameter types. Use
`Concatenate[Request, P]` when the decorator injects or strips a leading argument.

## Self
`def with_name(self, n: str) -> Self:` (typing.Self, 3.11+) makes fluent/builder methods
return the subclass type.

## Gotchas
- A TypeVar used once in a signature is pointless (`def f[T](x: T) -> None`); use `object`.
- `list[Derived]` is not a `list[Base]` (invariance); accept `Sequence[Base]` for read-only.
- Runtime: generic parameters are erased; `Box[int](...)` does no checking.

## Verify
- [ ] `reveal_type(first([1, 2]))` shows `int` under mypy/pyright.
- [ ] Decorated functions keep their signatures in IDE hover and checker output.

## Checked
- mypy (current pip release) on Python 3.14.0: PEP 695 `first`, bound `largest`, constrained `concat` (mixing str/bytes rejected), `retry[**P, R]` preserved `def (url: str, n: int =) -> bytes` and rejected a wrong argument, `Self` revealed `D`, `list[B]` rejected for `list[A]` (invariance, suggests `Sequence`), inferred covariance accepted `RO[B]` for `RO[A]`; at runtime `Box[int]('x')` is unchecked and the `type Json` alias evaluates. Single-use TypeVar was not flagged by mypy (a style rule; checkers differ).
