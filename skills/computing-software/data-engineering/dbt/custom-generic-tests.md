---
id: computing-software.data-engineering.dbt.custom-generic-tests
name: custom-generic-tests
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-tests, custom-generic-test, test-block, generic-tests, model-argument, column-name-argument, reusable-tests, tests-generic-folder]
level: advanced
status: verified
description: "Write reusable dbt generic tests: {% test %} blocks in tests/generic, model/column_name arguments, extra parameters with defaults, default configs, and overriding built-in tests."
sources:
  - https://docs.getdbt.com/best-practices/writing-custom-generic-tests
  - https://docs.getdbt.com/docs/build/data-tests#generic-data-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom generic tests

**Goal:** a rule you check on many models becomes one parameterised test applied in YAML.

## Define
```sql
-- tests/generic/not_negative.sql
{% test not_negative(model, column_name, allow_null=true) %}
    {{ config(severity='error') }}
    select {{ column_name }} as failing_value
    from {{ model }}
    where {{ column_name }} < 0
    {% if not allow_null %} or {{ column_name }} is null {% endif %}
{% endtest %}
```
- `model` is the relation under test; `column_name` is passed when the test is attached to a column.
- Extra arguments need defaults if optional.
- Returns failing rows, like any test.
Location: `tests/generic/` or `macros/` (per the dbt data-tests docs; both definitions here ran from `tests/generic/`). The `arguments:` block needs dbt 1.10.5+; older versions put arguments directly under the test name.

## Model-level test (no column)
```sql
{% test row_count_within(model, compare_model, tolerance_pct=5) %}
with a as (select count(*) c from {{ model }}),
     b as (select count(*) c from {{ compare_model }})
select a.c, b.c from a, b
where abs(a.c - b.c) > b.c * {{ tolerance_pct }} / 100.0
{% endtest %}
```

## Apply
```yaml
models:
  - name: fct_payments
    data_tests:
      - row_count_within:
          arguments: {compare_model: ref('stg_payments'), tolerance_pct: 1}
    columns:
      - name: amount
        data_tests:
          - not_negative:
              arguments: {allow_null: false}
              config: {where: "created_at >= current_date - 30"}
```
`where`, `severity`, `store_failures` configs work automatically (dbt wraps the test query; `where` applied above). A `config(severity=...)` inside the test definition takes precedence over a project-level `data_tests: +severity: warn` (the `not_negative` test still failed as an error).

## Overriding a built-in
Define `{% test unique(model, column_name) %}` in your project to replace the built-in (e.g. adapter-optimised version). Packages like dbt_utils and dbt-expectations follow the same pattern; prefer them before writing your own.

## Tips
- Keep tests cross-database with `{{ dbt.dateadd(...) }}`, `{{ dbt.type_string() }}` macros.
- Document the test in a macro properties file (`macros:` block with `description`) so it appears in docs.

## Verify
- [ ] `dbt test -s fct_payments` runs the custom tests and passes on good data.
- [ ] Injecting a negative amount in dev causes a failure with the value returned.
