---
id: computing-software.cybersecurity-defensive.system-hardening.osquery-fim
name: osquery-fim
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [osquery-fim, osquery, file-integrity-monitoring, file-events, fleetdm, ntfs-journal-events]
level: practitioner
status: docs-checked
description: "Use osquery for file integrity monitoring: file_paths configuration, file_events and es_process_file_events tables, hashing, scheduled queries, exclusions and shipping to a SIEM."
sources: ["https://github.com/osquery/osquery/blob/master/docs/wiki/deployment/file-integrity-monitoring.md", "https://github.com/osquery/osquery/blob/master/docs/wiki/deployment/configuration.md", "https://github.com/osquery/osquery/blob/master/docs/wiki/deployment/logging.md", "https://github.com/osquery/osquery/blob/master/specs/posix/file_events.table", "https://github.com/osquery/osquery/blob/master/specs/darwin/es_process_file_events.table", "https://github.com/osquery/osquery/blob/master/specs/linux/process_file_events.table"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# osquery file events (FIM)

osquery exposes the OS as SQL tables. Its FIM uses inotify (Linux `file_events`), FSEvents (macOS `file_events`) or the NTFS journal
(Windows, `ntfs_journal_events`) to record changes in configured paths, queried on a schedule. FIM is disabled by default: events must be enabled (`--disable_events=false`) and the table's flag set (`--enable_file_events=true`).

## Configuration (osquery.conf)
```json
{
  "options": { "disable_events": "false", "enable_file_events": "true" },
  "file_paths": {
    "etc": ["/etc/%%"],
    "binaries": ["/usr/bin/%%", "/usr/sbin/%%", "/usr/local/bin/%%"],
    "ssh": ["/root/.ssh/%%", "/home/%/.ssh/%%"],
    "web": ["/var/www/%%"]
  },
  "exclude_paths": { "etc": ["/etc/mtab", "/etc/ld.so.cache"] },
  "file_accesses": ["ssh"],
  "schedule": {
    "fim": {
      "query": "SELECT target_path, category, action, md5, sha256, uid, time FROM file_events;",
      "interval": 300, "removed": false
    }
  }
}
```
- `%` matches one directory level, `%%` recursive.
- `file_accesses` lists `file_paths` categories for which file reads are also recorded (Linux, via inotify; explicit opt-in because of overhead; hashes are not computed for access events).
- md5, sha1 and sha256 are calculated when the event occurs if possible (`hashed` is 1 if hashed, 0 if not, -1 if hashing failed).
- You cannot match recursively inside a path (`/Users/%%/x.conf` is invalid); applications that replace a file instead of editing it require osquery to be restarted unless you monitor the containing directory.
- Windows: `--enable_ntfs_event_publisher=true` and query `ntfs_journal_events`.
- macOS: `es_process_file_events` (EndpointSecurity) returns FIM events with process context; osquery may need Full Disk Access.

## Attribute changes to the "who"
Linux `file_events` (inotify) does not record the process. Linux `process_file_events` uses the Audit subsystem and needs `--disable_audit=false`, `--audit_allow_fim_events=true` and, for osquery to install the audit rules, `--audit_allow_config=true`. osquery cannot share the Audit subsystem with `auditd`; use another FIM source or stop auditd.

## Operations
- Events are always recorded as they happen; the query interval only controls how often buffered events are logged. Ship results with a logger plugin (`filesystem` is the default; `tls`, `syslog`, `kinesis`, `firehose` and `kafka_producer` are available, several can be combined with a comma-separated `--logger_plugin`); build SIEM
  alerts for changes to critical paths outside change windows.
- Very busy directories (logs, caches) should be excluded, and `file_paths_query` can derive paths from a query.
- Run osqueryd as root and check SELinux or AppArmor are not blocking it; `--verbose` shows warnings.

## Gotchas
- Events only exist after the daemon was running; it is not a baseline comparer like AIDE. For "what changed
  since the golden state" use scheduled snapshot queries (`"snapshot": true` returns the full result set each interval instead of differentials).
- inotify limits (`fs.inotify.max_user_watches`, `max_user_instances`, `max_queued_events`) bound how many files can be monitored.

## Verify
Touch a file in `/etc` on a test host and see a `file_events` row with sha256 in the SIEM within the schedule
interval, and `osqueryd --verbose` output shows no FIM errors.

## Checked
Checked 2026-10-25 against the osquery documentation and table specs (osquery/osquery, last commit 2026-10-23: deployment/file-integrity-monitoring.md, configuration.md, logging.md, and the file_events, process_file_events and es_process_file_events table files). Confirmed: `file_paths` and `exclude_paths` with `%` (one level) and `%%` (recursive), `file_accesses`, `file_paths_query`, `--disable_events=false`, `--enable_file_events=true`, `--enable_ntfs_event_publisher=true`, `file_events` columns (target_path, category, action, md5, sha1, sha256, hashed, uid, time), logger plugin names, `snapshot` queries, inotify sysctl names, and that Linux process attribution comes from `process_file_events` (Audit) which cannot share with auditd. Removed unconfirmed: `hash_file_events`, `--events_expiry`/`--events_max`, the `hash JOIN file` ad hoc query, the ES entitlement remark and the `osquery_events` verification. The Fleet documentation was dropped from sources (not read).

Method: documentation only; no commands were run.
