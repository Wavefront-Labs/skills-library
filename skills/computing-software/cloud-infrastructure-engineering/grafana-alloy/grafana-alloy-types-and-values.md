---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-types-and-values
name: grafana-alloy-types-and-values
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [types, secret, capsule, raw-strings, duration, convertnonsensitive, objects]
level: intro
status: docs-checked
description: "Alloy value types (number, string, bool, array, object, null), duration strings, raw strings, and the secret and capsule special types."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/expressions/types_and_values.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy types and values

Value types: `number` (integers and floats are one type, so `5.0 == (10 / 2)`), `string`, `bool`, `array` (zero-indexed), `object`, `function` and `null`. Reference docs also use `any`, `map(T)`, `list(T)` and `duration`.

- **duration**: a string with units `h`, `m`, `s`, `ms`, `ns`; units combine, so `"1h30m"` equals `"90m"`.
- **Strings** use double quotes with escapes (`\n`, `\t`, `\xNN`, `\uNNNN`). **Raw strings** use backticks, have no escapes, can span lines, and cannot contain a backtick (concatenate `"` + backtick with `+`).
- **Arrays**: `[0, 1, 2]`; a trailing comma is required when the closing bracket is on a different line.
- **Objects**: `{ first_name = "John" }`; wrap keys that are not valid identifiers in quotes, for example `"app.kubernetes.io/name" = "mysql"`. Objects need commas between pairs; blocks do not use commas.
- Functions cannot be constructed, only called (standard library or exported by a component).

## Secret
A `secret` is a string Alloy never displays; the UI shows `(secret)` in the graph, Arguments, Exports and Debug info. A string can be assigned to a secret attribute but not the reverse, and components cannot export a secret as a string. Call `convert.nonsensitive` to expose it as plain text, which reveals it in the UI.

## Capsule
A `capsule("prometheus.Receiver")` represents an internal type. You cannot construct one, and capsule types are not interchangeable: `prometheus.remote_write.default.receiver` fits `forward_to` of `prometheus.scrape`, which expects an array of that capsule.

## Checked

2026-11-08. Read the Types and values page in full. Confirmed: the seven value types, the reference-doc names (any, map(T), list(T), duration) and duration units, single number type, string escapes, raw string rules, array trailing comma rule, object key quoting and the object-versus-block comma note, function and null, secret redaction in the UI and the assignment rules, `convert.nonsensitive`, and capsule behaviour with the remote_write example. Removed the unread selector example.

Method: documentation only; no commands were run.
