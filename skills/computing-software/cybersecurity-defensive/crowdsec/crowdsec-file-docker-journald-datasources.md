---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-file-docker-journald-datasources
name: crowdsec-file-docker-journald-datasources
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [file-datasource, docker-datasource, journald, inotify, swarm, glob]
level: practitioner
status: docs-checked
description: "Configure the file, docker and journald datasources, including globbing, inotify polling, container name matching and journalctl filters."
sources: ["https://docs.crowdsec.net/docs/log_processor/data_sources/file", "https://docs.crowdsec.net/docs/log_processor/data_sources/docker", "https://docs.crowdsec.net/docs/log_processor/data_sources/journald"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## File

Reads text files in streaming or one-shot mode, and `.gz` files in one-shot only.

```yaml
source: file
filenames:
  - /tmp/foo/*.log
  - /var/log/syslog
labels:
  type: syslog
```

`filename` is a single path, `filenames` a list; both support globs. `exclude_regexps` removes files from a glob (for example everything except `*.log.gz`). By default CrowdSec uses inotify; `force_inotify` forces a watch on the folder even if it is empty. `poll_without_inotify: true` polls with `os.Stat`, for network shares, at significantly higher CPU per open file (this was not the default up to 1.4.6). `discovery_poll_enable` periodically rescans the patterns for files not yet tailed, useful when the filesystem emits no create events such as NFS; `discovery_poll_interval` defaults to 30s.

## Docker

```yaml
source: docker
container_name_regexp:
  - .*nginx*
labels:
  type: nginx
```

Select by `container_name`, `container_id` or their `_regexp` variants. For Swarm use `service_name`, `service_id` and the regexp variants, and do not mix container and swarm options because that duplicates logs. `use_container_labels` lets a single datasource take the log type from each container's labels.

## journald

```yaml
source: journalctl
journalctl_filter:
  - "_SYSTEMD_UNIT=ssh.service"
labels:
  type: syslog
```

Instead of one entry per unit you can filter by `_TRANSPORT` (`journal`, `syslog`, `stdout` or `kernel`).

## Checked

2026-11-03. Confirmed against the file, docker and journald datasource pages: gz in one-shot only, exclude_regexps, force_inotify, poll_without_inotify (os.Stat, higher CPU, not default up to 1.4.6), discovery_poll_enable and the 30s interval, swarm options and the duplicate-logs warning, use_container_labels, _TRANSPORT filters. Removed: nothing.

Method: documentation only; no commands were run.
