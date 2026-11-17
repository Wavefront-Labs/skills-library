---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-troubleshooting-telegraf
name: telegraf-troubleshooting-telegraf
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [troubleshooting, debug, pprof, apparmor, dns, errors]
level: practitioner
status: docs-checked
description: "Collects Telegraf diagnostics: debug logging, a file output to inspect metrics, pprof profiling, AppArmor denials and common errors such as context deadline exceeded."
sources: ["https://docs.influxdata.com/telegraf/v1/administer/troubleshoot/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Telegraf

## Techniques

1. `--test` to validate collection; `--once` to test the full path.
2. Add `[[outputs.file]] files = ["stdout"]` to see what is sent when data does not reach the destination.
3. Set `debug = true` in `[agent]`. Startup logs then show `Loaded inputs`, `Loaded outputs` and connection attempts for each output.

## pprof

Profiling is off by default:

```bash
telegraf --config telegraf.conf --pprof-addr localhost:6060
go tool pprof http://localhost:6060/debug/pprof/heap
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

Browse `http://localhost:6060/debug/pprof/`. For memory bugs, generate heap images a few moments after start and again later, and attach them to bug reports.

## AppArmor

Denials depend on plugins used and the profile. Telegraf does not control your profiles: read the operation and mask in the message (for example `ptrace` with `read`), decide whether to allow it, and adjust the profile. More denials may follow each change.

## Common errors

- `context deadline exceeded (Client.Timeout while awaiting headers)`: usually a transient network, DNS, proxy or firewall issue; Telegraf normally recovers without data loss.
- `no such host` for names other programs resolve: Go uses a pure Go resolver by default. Set `GODEBUG=netdns=cgo` (in `/etc/default/telegraf` for the service).
- Windows service error 1067: relative config path at install; use an absolute path.

## Checked

Method: docs-checked 2026-11-09 against the Troubleshoot Telegraf page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed.
