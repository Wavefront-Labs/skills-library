---
id: computing-software.data-engineering.dbt.unit-testing-incremental-models
name: unit-testing-incremental-models
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-unit-tests, incremental-unit-tests, is-incremental, this-relation, overrides, incremental-models]
level: advanced
status: verified
description: "Unit test both branches of a dbt incremental model: override is_incremental, mock {{ this }} with existing rows, and assert only the new or changed rows are emitted."
sources:
  - https://docs.getdbt.com/docs/build/unit-tests#unit-testing-incremental-models
  - https://docs.getdbt.com/reference/resource-properties/unit-test-overrides
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit testing incremental models

**Goal:** prove the incremental filter and merge-input logic is right (no missed late rows, no full re-emits) without running against prod data.

## Model under test
```sql
-- models/marts/fct_events.sql
{{ config(materialized='incremental', unique_key='event_id') }}
select event_id, user_id, event_ts, payload
from {{ ref('stg_events') }}
{% if is_incremental() %}
where event_ts > (select coalesce(max(event_ts), '1900-01-01') from {{ this }}) - interval '2 hours'
{% endif %}
```

## Test the incremental branch
```yaml
unit_tests:
  - name: fct_events_incremental_picks_new_and_late_rows
    model: fct_events
    overrides:
      macros:
        is_incremental: true
    given:
      - input: ref('stg_events')
        rows:
          - {event_id: 1, user_id: 10, event_ts: "2026-10-17 08:00:00"}   # old, already loaded
          - {event_id: 2, user_id: 10, event_ts: "2026-10-17 11:30:00"}   # late, within 2h lookback
          - {event_id: 3, user_id: 11, event_ts: "2026-10-17 13:00:00"}   # new
      - input: this
        rows:
          - {event_id: 1, user_id: 10, event_ts: "2026-10-17 08:00:00"}
          - {event_id: 9, user_id: 12, event_ts: "2026-10-17 12:00:00"}   # current max
    expect:
      rows:
        - {event_id: 2}
        - {event_id: 3}
```
The `expect` is the **SELECT output** (rows that would be merged), not the final table after merge. dbt does not simulate the merge.

## Test the full-refresh branch
```yaml
  - name: fct_events_full_refresh_emits_all
    model: fct_events
    overrides:
      macros: {is_incremental: false}
    given:
      - input: ref('stg_events')
        rows: [{event_id: 1}, {event_id: 2}]
    expect:
      rows: [{event_id: 1}, {event_id: 2}]
```

## Tips
- Only specify columns the logic uses; others default to null.
- `input: this` is how you mock the existing target. Without it in the incremental test, the subquery has nothing to read.
- Override other macros or vars the model depends on (`overrides: {vars: {lookback_hours: 2}}`, `env_vars`).
- Run: `dbt test --select "fct_events,test_type:unit"` or `dbt build` (unit tests run before the model builds).

## Gotchas
- Unit tests need dbt 1.8 or later. The upstream relations and the incremental model's own relation must exist (at least empty): without them the test fails with a "Not able to get columns" error; `dbt run -s +fct_events --empty` created them and the tests then passed (dbt 1.12.6, DuckDB).
- Timestamps given as strings were cast to the column type (DuckDB).

## Verify
- [ ] Both unit tests pass; mutating the lookback (e.g. to 0) makes the late-row test fail (checked: `FAIL 1`).
- [ ] CI runs unit tests on every PR touching the model.
