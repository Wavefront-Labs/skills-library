---
id: computing-software.cloud-infrastructure-engineering.netdata.text-logs-to-journal
name: text-logs-to-journal
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, log2journal, systemd-cat-native, journal-namespace]
level: advanced
status: docs-checked
description: "Turn plain text log files into systemd journal entries Netdata can explore using log2journal and systemd-cat-native, or the OpenTelemetry file_log route."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/logs/text-files-to-journals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Choose a bridge:
- log2journal: you use `journalctl`, journal-aware tooling or a SIEM reading journal files.
- OpenTelemetry Collector: you want Netdata's indexed store with its own retention and S3 archiving.
- Both can run in parallel without interfering.

log2journal: describe the format in a YAML file of PCRE2 patterns (stock configs such as `nginx-combined` ship with Netdata), then:

```
tail -F -n 0 /var/log/nginx/access.log \
  | log2journal -c nginx-combined \
  | systemd-cat-native --namespace=nginx
```

Gotchas:
- The `nginx` namespace must already exist, with its `systemd-journald@nginx` socket units active (they start on demand). A unit with `LogNamespace=nginx` creates it, and needs no `--namespace`.
- Without a namespace, drop the option to write to the system journal.
- In the Logs tab entries appear as `namespace-nginx` under the `systemd-journal` source.
- `systemd-cat-native --url` sends to a remote `systemd-journal-remote` over HTTP/HTTPS; log2journal needs no systemd, so it can convert locally on non-systemd distributions.

OpenTelemetry route: configure the `file_log` receiver (globs, multiline, JSON parsing, persistent offsets), forward to Netdata's OTLP endpoint, and set `service.namespace` and `service.name`. Logs appear under `otel-logs`.

## Checked

2026-11-04. Confirmed against the Netdata Text Files to Journals page: the bridge choice table, parallel use, PCRE2 YAML configs and nginx-combined, the tail | log2journal | systemd-cat-native pipeline, namespace requirements and LogNamespace note, the namespace-nginx display, the --url remote option, and the file_log receiver, service.namespace, service.name and otel-logs source. Nothing removed.

Method: documentation only; no commands were run.
