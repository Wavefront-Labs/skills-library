---
id: computing-software.software-engineering.typer.typer-number-ranges
name: typer-number-ranges
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, int, float, min-max, clamp, count]
level: practitioner
status: docs-checked
description: "Validate int and float Typer parameters with min and max, clamp out-of-range values, and build -vvv style counters with count=True."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/number.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/number/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/number/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/number/tutorial003_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer number validation, clamping and counters

## min and max

`int` and `float` parameters accept `min` and `max` in `typer.Argument()` and `typer.Option()`. Give one or both.

```python
@app.command()
def main(
    ID: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"ID is {ID}")
    print(f"--age is {age}")
    print(f"--score is {score}")
```

Help shows the ranges: `--age <int range>  [default: 20; x>=18]` and `--score <float range>  [default: 0; x<=100]`.

Errors name the range, for example `Error: Invalid value for '--age': 15 is not in the range x>=18.` and `Error: Invalid value for 'ID': 1002 is not in the range 0<=x<=1000.` Only the bound you set is enforced, so `--score -5` is accepted when there is no minimum.

## clamp

Set `clamp=True` to use the nearest valid value instead of raising:

```python
ID: Annotated[int, typer.Argument(min=0, max=1000)],
rank: Annotated[int, typer.Option(max=10, clamp=True)] = 0,
score: Annotated[float, typer.Option(min=0, max=100, clamp=True)] = 0,
```

`python main.py 5 --rank 11 --score -5` prints `--rank is 10` and `--score is 0`. A parameter without `clamp` (like the argument `ID`) still errors when out of range.

## Counter options

`count=True` makes an option a flag whose function value is how many times it appeared:

```python
@app.command()
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0):
    print(f"Verbose level is {verbose}")
```

Verify: no flag gives `Verbose level is 0`; `-v` gives 1; `--verbose --verbose --verbose`, `-v -v -v` and `-vvv` all give 3 (short names can be combined).

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/number.md with its three example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
