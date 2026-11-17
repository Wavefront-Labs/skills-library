---
id: computing-software.software-engineering.typer.typer-enum-choices
name: typer-enum-choices
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, enum, choices, literal, case-insensitive]
level: practitioner
status: docs-checked
description: "Restrict a Typer CLI parameter to predefined choices with enum.Enum, case_sensitive=False, lists of Enum values, or Literal."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/enum.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/enum/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/enum/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/enum/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/enum/tutorial004_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer choices with Enum and Literal

To limit a parameter to a fixed set of values, annotate it with a standard Python `enum.Enum`.

```python
from enum import Enum

import typer


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


app = typer.Typer()


@app.command()
def main(network: NeuralNetwork = NeuralNetwork.simple):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    app()
```

The parameter arrives as an `Enum` member, not a `str`. Use `network.value` to get the string.

Help shows `--network <simple|conv|lstm>  [default: simple]`. Verify: `--network conv` prints `Training neural network of type: conv`; `--network capsule` gives `Error: Invalid value for '--network': 'capsule' is not one of 'simple', 'conv', 'lstm'.`

## Case sensitivity

Enum choices are case sensitive by default (`CONV` is rejected). Set `case_sensitive=False` on `typer.Option()` to accept lower, upper or mixed case:

```python
@app.command()
def main(
    network: Annotated[
        NeuralNetwork, typer.Option(case_sensitive=False)
    ] = NeuralNetwork.simple,
):
    print(f"Training neural network of type: {network.value}")
```

Then `--network CONV` and `--network LsTm` work and print `Training neural network of type: conv` and `lstm`.

## List of Enum values

Annotate with `list[Enum]` and give a list default:

```python
class Food(str, Enum):
    food_1 = "Eggs"
    food_2 = "Bacon"
    food_3 = "Cheese"


@app.command()
def main(groceries: Annotated[list[Food], typer.Option()] = [Food.food_1, Food.food_3]):
    print(f"Buying groceries: {', '.join([f.value for f in groceries])}")
```

Help shows `--groceries <Eggs|Bacon|Cheese>  [default: Eggs, Cheese]`. With no option it prints `Buying groceries: Eggs, Cheese`; `--groceries "Eggs" --groceries "Bacon"` prints `Buying groceries: Eggs, Bacon`.

## Literal choices

Use `Literal` instead of an Enum, with the same help and error output:

```python
@app.command()
def main(
    network: Annotated[Literal["simple", "conv", "lstm"], typer.Option()] = "simple",
):
    print(f"Training neural network of type: {network}")
```

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/enum.md with its four example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
