---
id: computing-software.software-engineering.typer.typer-custom-type-parser
name: typer-custom-type-parser
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, custom-types, parser, argument, option]
level: practitioner
status: docs-checked
description: "Use the parser callable on typer.Argument or typer.Option to turn the raw input string into your own Python type."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/custom-types.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/custom_types/tutorial001_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer custom parameter types with `parser`

Typer lets you use your own classes as CLI parameter types. You give `typer.Argument` or `typer.Option` a `parser`: a function or other callable that parses the input into your own type.

## How it works

- The callable passed as `parser` receives the input value as a string.
- It must return the parsed value, an instance of your own custom type.
- Both `typer.Argument(parser=...)` and `typer.Option(parser=...)` accept it.

## Example

```python
from typing import Annotated

import typer


class CustomClass:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"<CustomClass: value={self.value}>"


def parse_custom_class(value: str):
    return CustomClass(value * 2)


app = typer.Typer()


@app.command()
def main(
    custom_arg: Annotated[CustomClass, typer.Argument(parser=parse_custom_class)],
    custom_opt: Annotated[CustomClass, typer.Option(parser=parse_custom_class)] = "Foo",
):
    print(f"custom_arg is {custom_arg}")
    print(f"--custom-opt is {custom_opt}")


if __name__ == "__main__":
    app()
```

Annotate the function parameter with your custom type and put the parser in the `typer.Option()` or `typer.Argument()` metadata.

## Tips

- The parser can be a function or any other callable, as in the example.
- The same `parser=` mechanism works on both arguments and options.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/custom-types.md with its example file. Removed or trimmed: the contrast with type plugins and two tips that went beyond the page.

Method: documentation only; no commands were run.
