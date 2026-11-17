---
id: computing-software.software-engineering.typer.typer-progress-bars
name: typer-progress-bars
category: computing-software
field: software-engineering
product: typer
tags: [typer, progress-bar, rich, spinner, progressbar, cli]
level: practitioner
status: docs-checked
description: "Show progress in a Typer CLI with Rich track() and spinners, or the built-in typer.progressbar with length, label and manual update()."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/progressbar.md
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial004_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial005_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/progressbar/tutorial006_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Progress bars and spinners in Typer

For long operations, tell the user something is happening.

## Rich (preferred)

Wrap the iterable in Rich's `track()` and iterate over that:

```python
@app.command()
def main():
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")
```

It renders a colored bar with percent and time.

For unknown duration use a spinner. Rich's `Progress` can show several spinners at once, e.g. "Processing..." and "Preparing...". See Rich's Progress Display docs.

```python
from rich.progress import Progress, SpinnerColumn, TextColumn


@app.command()
def main():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        progress.add_task(description="Preparing...", total=None)
        time.sleep(5)
    print("Done!")
```

## typer.progressbar (when Rich is unavailable or disabled)

Use it in a `with` statement and iterate over the object it yields; iterating updates the bar. Note the two nested blocks (`with`, then `for`):

```python
@app.command()
def main():
    total = 0
    with typer.progressbar(range(100)) as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.01)
            total += 1
    print(f"Processed {total} things.")
```

### length

The bar is sized from the iterable's length. If the length is unavailable (for example a generator fetching IDs from a web API), pass it explicitly. A generator is a function using `yield`, iterable in a `for` loop.

```python
def iterate_user_ids():
    # Let's imagine this is a web API, not a range()
    for i in range(100):
        yield i


with typer.progressbar(iterate_user_ids(), length=100) as progress:
    for value in progress:
        ...
```

### label

Pass `label="Processing"` to show a text prefix: `typer.progressbar(range(100), label="Processing")`.

### Manual updates

For irregular progress pass only a `length` (no iterable) and call `.update()` on the object from the `with`:

```python
total = 1000
with typer.progressbar(length=total) as progress:
    for batch in range(4):
        # Fake processing time
        time.sleep(1)
        # Increment by 250 on each loop iteration
        progress.update(250)
print(f"Processed {total} things in batches.")
```

The first examples finish with `Processed 100 things.`; the length example prints `Processed 100 user IDs.`

## Checked

2026-11-07. Read in full against progressbar.md and docs_src progressbar examples 1-6 (Typer docs repository checkout). Confirmed: track(), spinners with Progress, typer.progressbar with length, label and update(). Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
