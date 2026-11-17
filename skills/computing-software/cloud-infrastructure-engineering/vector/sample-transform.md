---
id: computing-software.cloud-infrastructure-engineering.vector.sample-transform
name: sample-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [sample, transform, ratio, rate, group-by, cost-reduction, vector]
level: practitioner
status: docs-checked
description: "Reduce volume with the sample transform using rate or ratio, grouping and exclusions."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/sample/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`sample` forwards a subset of events. It is stable and stateless and accepts logs and traces. Exactly one of `rate` or `ratio` must be set:

- `rate`: forward 1 out of N events (`rate: 1500` forwards one in 1500).
- `ratio`: forward a fraction, for example `ratio: 0.13` for 13%. This gives more precise control and supports values above 1/2.

```yaml
transforms:
  sampler:
    type: sample
    inputs: [parsed]
    ratio: 0.13
    group_by: "{{ service }}"
    exclude: '.severity == "error"'
```

Options:

- `exclude`: a condition; matching events skip sampling and are always forwarded.
- `group_by`: a template that places events in separate buckets sampled independently, so a noisy service does not starve a quiet one.
- `key_field`: hash this field's value so related events (for example one request ID) are kept or dropped together.
- `rate_field` / `ratio_field`: take the rate or ratio per event from a field.
- `sample_rate_key` (default `sample_rate`): the key where the rate is written on the event; set to an empty string to omit it. Downstream tools can use it to weight counts.
- `max_state_bytes` (default 128 MiB): cap on per-group state.

Sample after parsing so `exclude` and `group_by` can use extracted fields, and exclude errors so they are never lost.

Verify the output volume against the configured ratio over a representative window.

## Checked

2026-11-03. Read transforms/sample. Confirmed: stable, stateless, logs and traces; exactly one of `rate` or `ratio`; the 1500 and 0.13 examples; `exclude`; `group_by`; `key_field` hashing; `rate_field` and `ratio_field`; `sample_rate_key` and its empty-string behaviour; `max_state_bytes` of 134217728 (128 MiB). Nothing removed.

Method: documentation only; no commands were run.
