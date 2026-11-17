---
id: computing-software.cloud-infrastructure-engineering.ansible.math-and-random-filters
name: math-and-random-filters
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, math-filters, random-filter, shuffle, seed, human-readable]
level: practitioner
status: docs-checked
description: "Do arithmetic and set maths in templates (int, round, min, max, sum, log, pow, human_readable) and generate stable per-host randomness with random and shuffle seeded by hostname."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Math and random filters

## Arithmetic
Facts and inventory values are often strings — cast first:
```yaml
workers: "{{ (ansible_facts.processor_vcpus | int) * 2 }}"
heap_mb: "{{ ((ansible_facts.memtotal_mb | int) * 0.5) | int }}"
pct: "{{ (used / total * 100) | round(1) }}"          # round(precision, method='common'|'ceil'|'floor')
pages: "{{ (items | length / 20) | round(0, 'ceil') | int }}"
```
`round` returns a float; add `| int` for integer output. Operators: `+ - * / // % **`.

## Aggregates and sets
```yaml
"{{ [3, 9, 1] | max }}"                 "{{ list_of_dicts | max(attribute='size') }}"
"{{ disks | map(attribute='size') | sum }}"
"{{ a | union(b) }}" / intersect / difference / symmetric_difference / unique
```

## Other math
`log` (natural log by default, `| log(10)` for another base), `pow` (`| pow(2)`), `root` (square root by default, `| root(3)`), and Jinja's `abs`.
`human_readable` (`1232345345 | human_readable` → `1.15 GB`; `unit='M'` forces a unit), `human_to_bytes`
(`'4G' | human_to_bytes` → bytes; `default_unit` for inputs without a unit) — useful for sizing from facts.

## Random
```yaml
"{{ 60 | random }}"                                   # 0 up to 59 (upper bound exclusive)
"{{ 101 | random(start=10, step=10) }}"          # 10, 20, ... 100
"{{ ['a','b','c'] | random }}"
"{{ my_list | shuffle }}"
```
Non-deterministic values make tasks non-idempotent (cron minute changes every run!). Seed with
something stable per host:
```yaml
- ansible.builtin.cron:
    name: nightly report
    minute: "{{ 60 | random(seed=inventory_hostname) }}"
    hour: "{{ 24 | random(seed=inventory_hostname ~ 'h') }}"
    job: /usr/local/bin/report
```
`seed` makes the selection pseudo-random but repeatable, so the same host gets the same value each run while different hosts spread out. `shuffle` also accepts `seed`.

Passwords: `lookup('ansible.builtin.password', '/dev/null length=24 chars=ascii_letters,digits')` generates a new password on each call without storing it (using `/dev/null` as the path); give a real path to persist it. Do not use `random` for secrets.

## Gotchas
- `/` is true division (float) in Jinja2; `//` for integer division.
- Arithmetic on undefined values is an error, and facts or variables given as strings need `| int` or `| float` first.
- `random` without a seed in a templated file changes the output, and so reports `changed`, on each run.
- `random` with a number returns a value from 0 (inclusive) up to the number (exclusive).

## Verify
- [ ] Running a `debug` task with `msg: "{{ 60 | random(seed=inventory_hostname) }}"` twice prints identical values per host.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Filters (playbooks_filters.rst), ansible-core plugins/filter docs, Templating now() page, Jinja filters.py; password lookup source.
Confirmed:
- random: number input is an exclusive upper bound, start, step and seed arguments; shuffle seed; log default base e; root default 2; human_readable and human_to_bytes arguments and example output.
- password lookup: /dev/null path generates without storing.
- Corrected the 59 | random range and cron minute and hour examples to use 60 and 24.

Method: documentation only; no commands were run.
