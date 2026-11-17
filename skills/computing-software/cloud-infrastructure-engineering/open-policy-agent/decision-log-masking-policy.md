---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.decision-log-masking-policy
name: decision-log-masking-policy
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [decision-logs, masking, data-system-log-mask, json-pointer, pii-redaction]
level: advanced
status: docs-checked
description: "Redact sensitive input and result fields from OPA decision logs with a data.system.log.mask policy using JSON Pointers, remove and upsert operations, and limits."
sources:
  - https://www.openpolicyagent.org/docs/management-decision-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep passwords and personal data out of decision logs.

Before encoding and uploading a log (or calling a custom decision log plugin), OPA queries `data.system.log.mask`. The whole log event is the policy input, so the original query input is at `input.input`. The query returns a set of JSON Pointers to erase.

```rego
package system.log

mask contains "/input/password" if {
    input.input.resource == "user"
}

# unconditional: omit the body
mask contains "/input/ssn"
```

Erased paths are recorded on the event as `erased` (for example `["/input/password", "/input/ssn"]`).

Restrictions:
- Pointers must start with `/input`, `/result` or `/nd_builtin_cache`.
- Pointers to undefined data are ignored (`/input/name/first` when `name` is a string).
- Pointers may index arrays, either mid-path or as the last element: `/input/users/0/name` and `/input/users/0` are both valid.

To modify rather than erase, return objects with `op` and `path`, plus `value` for upserts:
- `"remove"`: deletes the path; `value` is ignored
- `"upsert"`: sets `value` at the path, overwriting if present or adding if not

Performance warning from the docs: the mask policy runs for every logged decision, so avoid expensive work such as crypto operations in its body.

Modified fields are listed in the event's `masked` array.

Check: send a query containing `password`, then confirm the logged event has no `/input/password` and lists it under `erased`.

## Checked

2026-11-04. Confirmed against the OPA docs Decision Logs page, section Masking Sensitive Data: data.system.log.mask queried before encoding or calling custom plugins, whole event as input (input.input), JSON Pointers, unconditional mask rules, the erased and masked event fields, the three allowed pointer prefixes, undefined pointers ignored, array indexes, remove and upsert operations, and the performance note. Nothing removed.

Method: documentation only; no commands were run.
