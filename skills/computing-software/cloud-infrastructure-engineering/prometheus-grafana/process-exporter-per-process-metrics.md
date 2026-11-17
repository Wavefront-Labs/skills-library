---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.process-exporter-per-process-metrics
name: process-exporter-per-process-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [process-exporter, per-process-metrics, exporters, node-exporter, linux, resource-usage]
level: practitioner
status: docs-checked
description: "Monitor CPU, memory, I/O and counts of named process groups on hosts with process-exporter, including grouping config and cardinality limits."
sources: ["https://github.com/ncabatoff/process-exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# process-exporter

node_exporter reports host totals, not per-process usage. process-exporter reads `/proc` and aggregates processes into
named groups; every metric is attached to a group (label `groupname`).

## Config
```yaml
# /etc/process-exporter/config.yml
process_names:
  - comm: [sshd, nginx]          # name defaults to {{.ExeBase}}
  - name: "java-{{.Matches.app}}"
    exe: [java]
    cmdline: ['-Dapp=(?P<app>\S+)']
```
Run: `process-exporter -config.path /etc/process-exporter/config.yml` (metrics on port 9256).
- Each item needs at least one selector (`comm`, `exe` or `cmdline`); with several, all must match.
- `comm` is the executable base name truncated at 15 characters; `exe` is argv[0] (a bare name matches the basename,
  a path with slashes must match exactly); `cmdline` is a list of Go regexps that must all match, and captures must be
  named (`?P<name>`) to appear in `.Matches`.
- Performance tip from the README: add an `exe` or `comm` selector next to any `cmdline` so the regexp only runs for
  matching executables.
- Name template fields include `{{.Comm}}`, `{{.ExeBase}}`, `{{.ExeFull}}`, `{{.Username}}`, `{{.Matches}}`, `{{.PID}}`,
  `{{.StartTime}}` and `{{.Cgroups}}`.

## Metrics
All start with `namedprocess_namegroup_`: `num_procs`, `cpu_seconds_total` (user and system time), `read_bytes_total`,
`write_bytes_total`, `memory_bytes{memtype="resident|virtual|swapped"}`, `open_filedesc`, `worst_fd_ratio`,
`oldest_start_time_seconds`, `num_threads`, `states`, page-fault and context-switch counters. Thread metrics add a
`threadname` label; the `-threads` flag can disable them.
`read_bytes_total` and `write_bytes_total` read `/proc/[pid]/io`, which is readable only by the process's own user: run
the exporter as that user or root, or the metric stays 0.

## Queries
```promql
topk(5, sum by (groupname) (rate(namedprocess_namegroup_cpu_seconds_total[5m])))
namedprocess_namegroup_num_procs{groupname="sshd"} == 0              # process missing
namedprocess_namegroup_memory_bytes{memtype="resident"} > 4e9
```

## Gotchas
- `{{.PID}}` in the name makes each group contain a single process: one series set per process, so cardinality grows
  with process churn.
- In a container, mount the host `/proc` and pass `--procfs`, as the README's Docker example does
  (`-v /proc:/host/proc ... --procfs /host/proc`).
- Overhead grows with the number of processes and the rate new ones appear; regexps and templates run once per
  process unless `-recheck` is set.

## Verify
- [ ] Each critical daemon has a `num_procs == 0` alert.

## Checked
2026-10-31. Confirmed against the process-exporter README (config format and selectors, comm truncation, name template
fields, metric names, `memtype` values, `/proc/[pid]/io` permission note, `-threads`, `-recheck`, port 9256 and
Docker `--procfs` example). Removed: first-match-wins ordering, the `mode` label on `cpu_seconds_total`, Kubernetes
cAdvisor advice, node_exporter comparison details and the `hostPID` setting (not on the cited page).
Method: documentation only; no commands were run.
