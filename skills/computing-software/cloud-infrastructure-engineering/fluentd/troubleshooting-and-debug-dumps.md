---
id: computing-software.cloud-infrastructure-engineering.fluentd.troubleshooting-and-debug-dumps
name: troubleshooting-and-debug-dumps
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, troubleshooting, verbose-logging, sigdump, sigcont, high-cpu, perf]
level: practitioner
status: docs-checked
description: "Diagnose a misbehaving Fluentd: enable trace logging per install type, dump internal state with SIGCONT, investigate high CPU and silent crashes."
sources:
  - https://docs.fluentd.org/deployment/trouble-shooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd troubleshooting basics
1. **Read the logs** first. For td-agent packages: `/var/log/td-agent/td-agent.log`.
2. **Verbose logging**: set `log_level trace` in `<system>`, or add `-vv`.
   - td-agent/calyptia-fluentd under systemd: add a unit file override under `/etc/systemd/system/` with `[Service] ExecStart=...existing options... -vv`.
   - td-agent init.d: add `-vv` to `TD_AGENT_OPTIONS` in `/etc/init.d/td-agent` (does not work under systemd, which ignores other options).
   - gem install: `fluentd .. -vv`.
3. **Dump internals** (thread dump, object allocation) with SIGDUMP: send `SIGCONT` to the Fluentd parent and child processes, e.g. on a hang. On Windows use `fluent-ctl`.
4. **High CPU**: possible causes are a plugin race condition, gem bugs, a regular expression on broken data, or system-call bugs such as `inotify` with many files. Use Linux `perf`; `pid2line.rb` helps find the offending call.
5. **Unexpected exit** (non-zero code, e.g. `process finished code=6`): Ruby-level crashes are not fully logged when daemonized. Run in the foreground to see everything; for td-agent the page uses `LD_PRELOAD` of jemalloc with `/usr/sbin/td-agent -c ... --user td-agent --group td-agent`.

Also see `troubleshooting-guide-common-problems`.

## Checked

2026-11-04. Confirmed against the Fluentd Trouble Shooting page (docs.fluentd.org/deployment/trouble-shooting): log location, verbose logging per install type, SIGDUMP via SIGCONT, fluent-ctl on Windows, high CPU causes and perf/pid2line.rb, the foreground td-agent command. Nothing removed.

Method: documentation only; no commands were run.
