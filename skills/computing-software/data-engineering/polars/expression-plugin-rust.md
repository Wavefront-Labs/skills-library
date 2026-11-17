---
id: computing-software.data-engineering.polars.expression-plugin-rust
name: expression-plugin-rust
category: computing-software
field: data-engineering
product: polars
tags: [polars-expr-plugins, plugin, rust, pyo3-polars, polars-expr, register-plugin-function, maturin, kwargs]
level: advanced
status: docs-checked
description: "Build a Rust expression plugin for Polars with pyo3-polars: polars_expr macro, register_plugin_function, kwargs via serde, and output_type_func."
sources:
  - https://docs.pola.rs/user-guide/plugins/expr_plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression plugins

Preferred way to write user-defined functions: compile Rust, register it as an expression; Polars dynamically links it at runtime. No Python/GIL contention, with optimisation, parallelism and Rust performance.

## Setup
`Cargo.toml`: `[lib] name = "expression_lib"`, `crate-type = ["cdylib"]`; dependencies `polars`, `pyo3` (features `extension-module`, `abi3-py310`), `pyo3-polars` (feature `derive`), `serde` (feature `derive`). The Python package folder must be named like `lib.name` (`expression_lib/__init__.py`), next to `src/` (`lib.rs`, `expressions.rs`), `Cargo.toml`, `pyproject.toml`.

## Rust side
Add `#[polars_expr(output_type=DataType)]`; the function's first argument must be `inputs: &[Series]`.
```rust
#[polars_expr(output_type=String)]
fn pig_latinnify(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_into_string_amortized(pig_latin_str);
    Ok(out.into_series())
}
```
Use `apply_into_string_amortized` rather than `apply_values` to avoid allocating a string per row. For multi-input elementwise String outputs see `binary_elementwise_into_string_amortized` in `polars::prelude::arity`.

## Python side
```python
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent

def pig_latinnify(expr: IntoExpr) -> pl.Expr:
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="pig_latinnify",
        args=expr,
        is_elementwise=True,
    )
```
`function_name` must match the Rust name exactly or Polars cannot resolve it. `is_elementwise=True` lets Polars run the expression in batches (not allowed for sort or slice). Compile with `maturin develop --release`, then `df.with_columns(pig_latin=pig_latinnify("convert"))`. Alternatively register a custom namespace for `pl.col("x").language.pig_latinnify()`.

## kwargs
Define a struct deriving `serde::Deserialize` and take it as the second argument: `fn append_kwargs(input: &[Series], kwargs: MyKwargs)`. In Python pass `kwargs={...}` to `register_plugin_function`.

## Dynamic output dtype
Use `#[polars_expr(output_type_func=my_fn)]` where `fn(input_fields: &[Field]) -> PolarsResult<Field>`, e.g. `FieldsMapper::new(input_fields).map_to_float_dtype()` (from `polars_plan::dsl::FieldsMapper`). Raise unsupported types with `polars_bail!(InvalidOperation: ...)`.

The page links an example repo and a tutorial.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
