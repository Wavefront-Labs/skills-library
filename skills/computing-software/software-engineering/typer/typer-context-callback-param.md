---
id: computing-software.software-engineering.typer.typer-context-callback-param
name: typer-context-callback-param
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, context, callback, callbackparam, validation]
level: advanced
status: docs-checked
description: "Access typer.Context and typer.CallbackParam in option callbacks, check resilient_parsing, and raise typer.BadParameter to validate input."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/reference/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer Context and CallbackParam

Every Typer app has an internal object tracking state relevant to the script's execution. For advanced cases you can reach it by declaring a function parameter of type `typer.Context`.

If one callback is shared by several CLI parameters and must know which one fired, declare a parameter typed `typer.CallbackParam`.

## Callback example

```python
from typing import Annotated

import typer

app = typer.Typer()


def name_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if ctx.resilient_parsing:
        return
    print(f"Validating param: {param.name}")
    if value != "Rick":
        raise typer.BadParameter("Only Rick is allowed")
    return value


@app.command()
def main(name: Annotated[str | None, typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
```

## How it works

- Attach the callback with `typer.Option(callback=...)`.
- Typer passes `ctx` (`typer.Context`), `param` (`typer.CallbackParam`) and `value` based on the parameter annotations.
- `param.name` identifies which CLI parameter triggered the callback.
- Raise `typer.BadParameter("message")` to reject a value.
- The example returns the value.

## Gotcha

The page's example checks `ctx.resilient_parsing` first and returns early, before printing or validating. The page does not explain why.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/reference/context.md. Removed or trimmed: the unexplained claim about resilient parsing having no side effects, and the claim that the returned value may be transformed.

Method: documentation only; no commands were run.
