---
id: computing-software.cybersecurity-defensive.security-operations.osquery-endpoint-investigation
name: osquery-endpoint-investigation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [osquery-investigation, osquery, osquery-manager, elastic-security, fleetdm, live-query, endpoint-investigation, sql, dfir]
level: practitioner
status: docs-checked
description: "Investigate endpoints with osquery SQL: process, network, persistence and user tables, running live queries via Elastic Osquery Manager or Fleet, and reading results safely."
sources: ["https://osquery.readthedocs.io/en/stable/introduction/using-osqueryi/", "https://osquery.io/schema/", "https://www.elastic.co/docs/solutions/security/investigate/osquery", "https://www.elastic.co/docs/solutions/security/investigate/run-osquery-from-alerts", "https://www.elastic.co/docs/solutions/security/investigate/use-placeholder-fields-in-osquery-queries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# osquery for endpoint investigation

osquery exposes the OS as SQL tables. Run it interactively (`osqueryi`) on one host, or fleet-wide
through the Elastic Osquery Manager integration or another osquery manager.

## Running queries
- Local: `osqueryi --json "SELECT ..."`.
- Elastic: add the Osquery Manager integration to an Elastic Agent policy, open **Osquery** from the
  navigation menu and click **Run query** (9.4+) or **New live query** (9.0-9.3), then select agents or
  groups. From an alert open the alert details flyout and use **Take action > Run Osquery**, where
  placeholder fields such as `{{host.name}}` insert alert data into the query.
- Results are stored in the `logs-osquery_manager.result-<namespace>` data stream; packs can be scheduled for recurring collection.

## Core investigation queries
Processes whose binary is no longer on disk (`on_disk` is 1 yes, 0 no, -1 unknown):
```sql
SELECT pid, name, path, cmdline FROM processes WHERE on_disk = 0;
```
Listening ports with owning process:
```sql
SELECT p.name, p.path, l.port, l.address, l.protocol
FROM listening_ports l JOIN processes p USING (pid) WHERE l.address NOT IN ('127.0.0.1','::1');
```
Established connections:
```sql
SELECT p.name, s.remote_address, s.remote_port FROM process_open_sockets s
JOIN processes p USING (pid) WHERE s.state = 'ESTABLISHED';
```
Persistence:
- Windows (`autoexec`, `scheduled_tasks`, `services` are Windows tables): `SELECT * FROM autoexec;` `SELECT name, action, path FROM scheduled_tasks WHERE enabled=1;`
  `SELECT * FROM services WHERE start_type='AUTO_START' AND path NOT LIKE '%system32%';`
- Linux (`systemd_units` is Linux only; `crontab`, `authorized_keys` and `last` also work on macOS): `SELECT * FROM crontab;` `SELECT * FROM systemd_units WHERE active_state='active';`
  `SELECT * FROM authorized_keys;`
- macOS: `SELECT * FROM launchd WHERE run_at_load=1;`
Hash a suspicious file: `SELECT path, sha256 FROM hash WHERE path = '/tmp/x';`
Users and logins: `SELECT * FROM logged_in_users;` `SELECT * FROM last;`

## Hunting fleet-wide
Run the same query across all hosts and stack the results (group by path/hash) in the SIEM;
singletons are the leads.

## Gotchas
- Some tables need root/SYSTEM; the agent normally runs privileged, `osqueryi` as a user does not.
- Large tables (`file` with wildcards, `hash` over directories) can spike CPU; constrain paths.
- Live queries have a timeout (Elastic: default and minimum 60 seconds, maximum 900); results arrive only from agents online during the window.
- osquery reads current state; it is not a forensic image. Collect volatile evidence first if the
  case may go to court.

## Verify
Run a known-good query (`SELECT version FROM osquery_info;`) across the target group and check the
response count equals the expected online hosts before trusting negative results.

## Checked

Checked 2026-10-25 against the osquery table specs (osquery/osquery master `specs/`, last pushed 2026-10-23), the osqueryi documentation and the Elastic documentation source (elastic/docs-content, Osquery pages). Confirmed: tables and columns used (`processes.on_disk`, `listening_ports`, `process_open_sockets.state`, `autoexec`, `scheduled_tasks`, `services.start_type` values, `crontab`, `systemd_units.active_state`, `authorized_keys`, `launchd.run_at_load`, `hash` requiring a `path`, `logged_in_users`, `last`, `osquery_info.version`), `osqueryi --json`, Elastic live query navigation (Run query from 9.4, New live query 9.0-9.3), Take action > Run Osquery, `{{host.name}}` placeholders, the `logs-osquery_manager.result-<namespace>` data stream, the 60/900 second timeout. Corrected: Elastic navigation text and data stream name. Removed the FleetDM and Kolide names and the malware prevalence remark.

Method: documentation only; no commands were run.
