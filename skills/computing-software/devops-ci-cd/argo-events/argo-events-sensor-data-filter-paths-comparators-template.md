---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-data-filter-paths-comparators-template
name: argo-events-sensor-data-filter-paths-comparators-template
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, data-filter, gjson, comparator, regex, template, sprig, multipaths]
level: practitioner
status: docs-checked
description: "Write Sensor data filters: path, type, comparator, regex string values, gjson multipaths and sprig templates such as b64dec."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/data.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor data filter paths comparators template

Data filters apply to the `data` section of the CloudEvent (for a webhook: `data.header` and `data.body`). Fields:

```yaml
filters:
  dataLogicalOperator: or     # and (default) | or, lower case
  data:
    - path: body.value
      type: number
      comparator: ">"
      value:
        - "50.0"
```

Filters are evaluated in declaration order, and any error (such as a missing path) counts as false.

Comparators: `>=`, `>`, `=`, `!=`, `<`, `<=`. For type `string` the value may be an exact string or a regex, and is always evaluated as a regex; for `bool` or `float` give exact values.

Multipaths (gjson syntax) combine several paths into one string, so a string regex can match combinations, for example the path `body.action,body.labels.#(name=="Webhook").name` yielding `"opened","Webhook"`; list the acceptable resulting strings under `value`.

`template` runs the extracted value through a sprig template before matching, with the data treated as a string first and cast to `type` afterwards:

```yaml
- path: body.message
  type: string
  value: ["hello world"]
  template: "{{ b64dec .Input }}"
```

This matches the message `{"message":"aGVsbG8gd29ybGQ="}`.

## Checked

2026-11-04. Confirmed against the Data Filter page: the fields, declaration-order evaluation, errors counting as false, `dataLogicalOperator` values (lower case, empty means `and`), the six comparators, string-as-regex and exact `bool`/`float` values, gjson multipaths with the `"opened","Webhook"` result, and the sprig `template` with `b64dec` and its string-then-cast note. The multipath path in the skill is a shortened form of the page's example. Nothing removed.
Method: documentation only; no commands were run.
