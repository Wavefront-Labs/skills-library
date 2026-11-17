---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.relabel-actions-reference
name: relabel-actions-reference
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, relabeling, relabel-configs, relabel-actions, labelmap-action, hashmod-action, keepequal, dropequal, replace-action, keep-action, drop-action, labeldrop, labelkeep, lowercase, uppercase, separator, regex-anchoring, relabel-debugging, pca]
level: practitioner
status: verified
description: "Every relabel_config action (replace, keep, drop, keepequal, hashmod, labelmap, labeldrop, case) with examples, ordering, anchoring, and debugging."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config", "https://relabeler.promlabs.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# relabel_config actions

**Goal:** know what each action does to the label set, in which order, so you can write a
rule once and predict its output without trial and error.

## 1. Mechanics common to all actions
- `source_labels` are concatenated with `separator` (default `;`) into one string.
- `regex` (default `(.*)`) is **fully anchored**: `^(?:regex)$`. `foo` does not match `foobar`.
- `replacement` (default `$1`) may use `$1`, `${1}`, `${name}` capture groups.
- Rules run in order; each sees the labels as left by the previous one. Labels starting
  with `__` are removed **after** the whole `relabel_configs` list (so you can use temp
  labels like `__tmp_x` between rules).
- In `relabel_configs` the inputs are SD `__meta_*` labels plus `__address__`,
  `__scheme__`, `__metrics_path__`, `__param_*`; `job` is pre-set from `job_name`
  and `instance` is set from `__address__` if still empty at the end. In `metric_relabel_configs` the inputs are the
  scraped series' labels plus `__name__`.

## 2. Actions
| Action | Effect |
|---|---|
| `replace` (default) | if `regex` matches the joined source, set `target_label` = `replacement`; if no match, **do nothing** (label unchanged) |
| `keep` | keep the target/series only if `regex` matches |
| `drop` | drop the target/series if `regex` matches |
| `keepequal` | keep only if joined `source_labels` == `target_label`'s value |
| `dropequal` | drop if joined `source_labels` == `target_label`'s value |
| `hashmod` | `target_label` = `hash(joined source) % modulus` — for sharding |
| `labelmap` | for every **label name** matching `regex`, copy its value to the name given by `replacement` |
| `labeldrop` | remove every label whose **name** matches `regex` |
| `labelkeep` | remove every label whose name does **not** match |
| `lowercase` / `uppercase` | `target_label` = lowercased/uppercased joined source |

```yaml
relabel_configs:
  # replace: build address from IP + annotation port
  - source_labels: [__meta_kubernetes_pod_ip, __meta_kubernetes_pod_annotation_prometheus_io_port]
    regex: (.+);(\d+)
    replacement: $1:$2
    target_label: __address__
  # keep: opt-in only
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  # labelmap: all pod labels → plain labels (prefix stripped)
  - regex: __meta_kubernetes_pod_label_(.+)
    action: labelmap
  # labeldrop: then remove the noisy ones
  - regex: pod_template_hash|controller_revision_hash
    action: labeldrop
  # lowercase: normalise env from a tag
  - source_labels: [__meta_ec2_tag_Env]
    action: lowercase
    target_label: env
  # hashmod: 3-way sharding across Prometheus replicas
  - source_labels: [__address__]
    modulus: 3
    action: hashmod
    target_label: __tmp_shard
  - source_labels: [__tmp_shard]
    regex: "1"          # this replica's shard
    action: keep
  # keepequal: only scrape the port named in an annotation
  - source_labels: [__meta_kubernetes_pod_container_port_number]
    action: keepequal
    target_label: __meta_kubernetes_pod_annotation_prometheus_io_port
```
`metric_relabel_configs` examples:
```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: go_gc_.*|go_memstats_.*
    action: drop
  - source_labels: [__name__, le]        # rename a metric
    regex: old_metric_bucket;(.*)
    replacement: new_metric_bucket
    target_label: __name__
```

## 3. Debugging a rule
- `/service-discovery` page: "Discovered labels" (before) vs "Target labels" (after) per target.
- `promtool check config` catches syntax, missing files and regexes RE2 cannot compile (lookahead `(?=` is
  rejected), not logic; use the Relabeler web tool (promlabs) to paste labels and rules and step through them.
- A `replace` that "does nothing": the regex didn't match (anchoring, or an empty source
  label because the meta label does not exist). Add `regex: (.+)` style guards consciously.
- A `keep` that drops everything: matching is case-sensitive (`"True"` does not match `true`), so
  lowercase first. An unquoted `regex: true` works (it loads as the string `true`).

## Gotchas
- `labelmap` `replacement` is applied to the **name**, and `$1` refers to the name's
  capture; it does not touch values.
- In `relabel_configs`, `labeldrop` of `__address__` stops the target being created (log: `no address`);
  dropping `job` leaves the series without a `job` label; dropping `instance` is undone (it is refilled
  from `__address__`). In `metric_relabel_configs`, `labeldrop` of `__name__` fails the whole scrape
  (`missing metric name (__name__ label)`, `up == 0`).
- `hashmod` uses the raw joined string; include `__address__` only, not labels that differ
  per Prometheus replica, or shards disagree.
- `separator` matters when a source label value legitimately contains `;`.
- `modulus` without `action: hashmod` is ignored silently; `hashmod` without `modulus` is rejected at load.

## Verify
- [ ] `/service-discovery` shows the intended "Target labels" for one target of each job.
- [ ] `count by (job) (up)` matches expectations after a `keep`/`drop` change.
- [ ] No series carries `__meta_*`, `__tmp_*` or `pod_template_hash` labels.
