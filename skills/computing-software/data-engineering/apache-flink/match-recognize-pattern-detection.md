---
id: computing-software.data-engineering.apache-flink.match-recognize-pattern-detection
name: match-recognize-pattern-detection
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, match-recognize, cep, pattern-detection, complex-event-processing, row-pattern]
level: advanced
status: docs-checked
description: "Detect event sequences in Flink SQL with MATCH_RECOGNIZE: PARTITION BY/ORDER BY, PATTERN quantifiers, DEFINE, MEASURES, WITHIN, AFTER MATCH and state growth."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/match_recognize/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/libs/cep/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MATCH_RECOGNIZE pattern detection

SQL row pattern recognition (SQL:2016) backed by Flink CEP. Example: three failed logins followed by a success within 10 minutes.

```sql
SELECT *
FROM logins
MATCH_RECOGNIZE (
  PARTITION BY user_id
  ORDER BY ts                          -- first ORDER BY column must be an ascending time attribute (event or processing time)
  MEASURES
    FIRST(F.ts) AS first_fail,
    LAST(F.ts)  AS last_fail,
    S.ts        AS success_ts,
    COUNT(F.ip) AS fails,
    LAST(F.ip)  AS ip
  ONE ROW PER MATCH
  AFTER MATCH SKIP PAST LAST ROW
  PATTERN (F{3,} S) WITHIN INTERVAL '10' MINUTE
  DEFINE
    F AS F.status = 'FAIL',
    S AS S.status = 'OK'
) AS m;
```

## Pieces
- `PARTITION BY`: per-key matching (like keyBy). Without it the clause becomes a non-parallel operator.
- `ORDER BY` time attribute: with event time, rows are sorted before they reach the pattern state machine, so results are correct regardless of arrival order. The time attribute must be the first `ORDER BY` column, ascending.
- `PATTERN`: regex over variables: `A B` (strict contiguity), quantifiers `*`, `+`, `?`, `{n}`, `{n,}`, `{n,m}`, `{,m}`, greedy by default or reluctant. Not supported: pattern groups, alternation `|`, `PERMUTE`, anchors, exclusion, the reluctant optional quantifier `A??`, and patterns that can produce an empty match (such as `A*`).
- `DEFINE`: conditions; a variable without a definition matches every row. Conditions can navigate earlier rows, e.g. `LAST(B.price, 1)`.
- `MEASURES`: output columns, with `FIRST`, `LAST`, aggregates over a variable's rows (`DISTINCT` aggregations are not supported), `MATCH_ROWTIME()` and `MATCH_PROCTIME()` for output time attributes.
- `AFTER MATCH` strategies: `SKIP PAST LAST ROW`, `SKIP TO NEXT ROW`, `SKIP TO FIRST variable`, `SKIP TO LAST variable`.
- `ONE ROW PER MATCH` is the only supported output mode (`ALL ROWS PER MATCH` is not). The clause applies only to append tables and always produces an append table.

## State and performance
- **Use `WITHIN`** (a non-standard Flink SQL extension) so a pattern finishes within a time bound; the docs encourage it for streaming to bound state.
- A greedy quantifier cannot be used on the last variable of a pattern (`(A B*)` is not allowed); work around it with an artificial final variable, e.g. `PATTERN (A B* C)` with `C` defined as the negation of `B`.
- High-cardinality partitions with many partial matches use a lot of state; monitor state size.

## DataStream CEP
For logic SQL cannot express (custom conditions with state, timeouts emitting partial matches), use the `flink-cep` library: `Pattern.<Event>begin("fail").where(...).timesOrMore(3).next("ok").where(...).within(Duration.ofMinutes(10))` and `CEP.pattern(stream, pattern).process(...)`; a `PatternProcessFunction` that implements `TimedOutPartialMatchHandler` receives timed-out partial matches.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the MATCH_RECOGNIZE page (supported and unsupported features, output mode, `ORDER BY` time attribute rule, greedy and reluctant quantifiers, `WITHIN`, AFTER MATCH strategies, `MATCH_ROWTIME`/`MATCH_PROCTIME`, append-table restriction) and the CEP library page (`timesOrMore`, `within`, `CEP.pattern`, `TimedOutPartialMatchHandler`). Corrected the unsupported-feature list and the last-variable greedy rule; removed unconfirmed late-row and RocksDB claims.

Method: documentation only; no commands were run.

## Verify
- [ ] Unit test with a scripted event sequence (match, near-miss, overlapping) and expected rows.
- [ ] State size stable over days (WITHIN effective).
