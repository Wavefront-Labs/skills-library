---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-options
name: tetragon-policy-options
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [policy-options, tetragon, kprobe-multi, heap-size]
level: advanced
status: docs-checked
description: "Pass per-spec options to Tetragon kprobe, uprobe, fentry and lsm hooks, such as disabling multi-link attach or sizing dedicated heap maps."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/options/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon tracing policy options

Goal: tune how hooks in one policy file attach or allocate memory, without changing global daemon settings.

Options are a name/value array in the spec. Each hook that supports options processes them; support exists for kprobe, uprobe, fentry and lsm hooks.

```yaml
spec:
  options:
    - name: "option-1"
      value: "True"
    - name: "option-2"
      value: "10"
```

## Kprobe

- `disable-kprobe-multi`: attach all kprobes in the spec through the standard kprobe interface instead of kprobe multi link. Boolean, default false. Other spec files keep multi link. Example value `"1"`.

## Uprobe

- `disable-uprobe-multi`: same idea for uprobes; boolean, default false.
- `uprobe-heap-size`: positive integer; max entries for the heap maps `process_call_heap`, `ratelimit_heap`, `string_postfix_maps_heap`, `string_prefix_maps_heap`, `string_maps_heap`, `buffer_heap_map`, used by uprobe and usdt sensors. Applies to both `uprobes` and `usdts` in the spec. When unset, these maps are shared globally across policies and sized by the `--uprobe-heap-size` daemon flag (default `32768`); setting the option gives the spec dedicated maps of that size.

```yaml
  options:
    - name: "uprobe-heap-size"
      value: "65536"
```

## Fentry

- `fentry-heap-size`: same six maps, used by the fentry sensor, covering all `fentries` including return (fexit) probes. Global default from `--fentry-heap-size` (`32768`).

## Lsm

- `lsm-heap-size`: same six maps, for all `lsmhooks` in the spec. Global default from `--lsm-heap-size` (`32768`).

Both take a positive integer, e.g. `value: "65536"`.

## Checked

2026-11-08. Read the options page in full (raw docs markdown). Checked option names, defaults, heap map list and daemon flags against it; no claims removed.

Method: documentation only; no commands were run.
