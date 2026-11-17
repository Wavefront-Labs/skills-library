---
id: computing-software.software-engineering.python.clis-with-argparse
name: clis-with-argparse
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, argparse, python-cli, subcommands, exit-codes, command-line, py-cli-config]
level: practitioner
status: verified
description: "Build robust command-line tools with argparse: positional vs optional args, types and choices, subcommands, mutually exclusive groups, exit codes and testing."
sources:
  - https://docs.python.org/3/library/argparse.html
  - https://docs.python.org/3/howto/argparse.html
  - https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CLIs with argparse

**Goal:** a CLI with clear help, validated input, conventional exit codes and tests, using only the standard library.

## 1. Skeleton
```python
import argparse, sys
from pathlib import Path

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="report", description="Generate usage reports.")
    p.add_argument("input", type=Path, help="CSV file to read")
    p.add_argument("-o", "--output", type=Path, default=Path("report.html"))
    p.add_argument("--since", type=date.fromisoformat, help="YYYY-MM-DD")   # from datetime import date
    p.add_argument("--format", choices=["html", "csv", "json"], default="html")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--version", action="version", version="%(prog)s 1.4.0")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.input.exists():
        print(f"report: {args.input}: no such file", file=sys.stderr)
        return 2
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```
`type=` accepts any callable; it raising `ValueError`/`ArgumentTypeError` becomes a clean usage error (exit 2).

## 2. Subcommands
```python
sub = p.add_subparsers(dest="command", required=True)
run = sub.add_parser("run", help="run a job")
run.add_argument("job")
run.set_defaults(func=cmd_run)
ls = sub.add_parser("list", aliases=["ls"])
ls.set_defaults(func=cmd_list)
args = p.parse_args(); return args.func(args)
```

## 3. Groups and validation
```python
g = p.add_mutually_exclusive_group(required=True)
g.add_argument("--all", action="store_true")
g.add_argument("--id", action="append", type=int)     # repeatable
```
Cross-argument rules: check after parsing and call `p.error("...")` (prints usage, exits 2).

## 4. Conventions
- stdout for results, stderr for diagnostics; exit 0 success, 1 failure, 2 usage error.
- Support `-` for stdin/stdout where it makes sense.
- Env var defaults: `default=os.environ.get("REPORT_TOKEN")`, never take secrets as flags (visible in `ps`).
- Expose via `[project.scripts] report = "report.cli:main"` in pyproject.

## 5. Testing
```python
def test_bad_date(capsys):
    with pytest.raises(SystemExit) as e:
        main(["in.csv", "--since", "nope"])
    assert e.value.code == 2
    assert "invalid fromisoformat value" in capsys.readouterr().err
```
Passing `argv` explicitly keeps `main` testable without patching `sys.argv`.

## Gotchas
- `type=bool` treats any non-empty string as True; use `store_true` or `BooleanOptionalAction` (`--color/--no-color`).
- Defaults with `action="append"` are appended to, not replaced; default to `None` and handle it.
- Prefix matching: `--out` matches `--output` unless `allow_abbrev=False`; abbreviations break when new flags are added.
- For large CLIs, click/typer give composable commands and better help, at the cost of a dependency.

## Verify
- `report --help` is readable, invalid inputs exit 2 with one-line errors, and the test suite covers each subcommand via `main([...])`.

## Checked
- Python 3.14.0: the `build_parser` skeleton parses `-vv --dry-run --since 2026-01-02` into the expected namespace; an invalid `--since` (via `date.fromisoformat`), a bad `--format` choice and a missing positional exit with code 2 and usage-style messages; `--version` prints `report 1.4.0` and exits 0; `ArgumentTypeError` becomes `argument --k: must be ok`; a required subparser, an alias (`ls`), a required mutually exclusive group (none and both rejected), repeatable `--id` with `action="append"`, and `p.error()` exiting 2 with usage. The pytest `capsys` test and `[project.scripts]` wiring were not run.
