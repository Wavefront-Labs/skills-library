---
id: computing-software.digital-forensics-incident-response.log-analysis.writing-vql-queries
name: writing-vql-queries
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [vql, velociraptor, query-language, threat-hunting, artifact-development, dfir]
level: advanced
status: draft
description: "Write Velociraptor Query Language (VQL): SELECT syntax, plugins and functions, LET, foreach, parsing files and registry, and testing queries in notebooks before hunting."
sources: ["https://docs.velociraptor.app/docs/vql/", "https://docs.velociraptor.app/vql_reference/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing VQL queries

**Goal:** express collection and detection logic in VQL so it runs on endpoints at scale.

## Syntax essentials
```sql
-- plugins produce rows; functions transform values
SELECT Name, Pid, Ppid, CommandLine, Exe
FROM pslist()
WHERE Exe =~ '(?i)\\\\(temp|appdata|programdata)\\\\'

-- LET defines stored or lazy queries; foreach iterates rows
LET users = SELECT Name, Directory FROM Artifact.Windows.Sys.Users()
SELECT * FROM foreach(row=users, query={
  SELECT OSPath, Size, Mtime FROM glob(globs=Directory + '/AppData/Roaming/**/*.exe')
})
```
- Regex match operator `=~` (case-sensitive unless `(?i)`); `!~` negation.
- Paths: `glob(globs=..., accessor='ntfs')` for raw NTFS (locked files), `accessor='registry'`
  for live registry, `'raw_reg'` for offline hive files.
- Parsing: `parse_evtx(filename=...)`, `parse_csv`, `parse_json`, `read_file`,
  `parse_binary` with profiles, `yara(rules=..., files=...)`, `hash(path=...)`,
  `authenticode(filename=...)`.

## Examples
```sql
-- Services with ImagePath in user-writable paths
SELECT Key.OSPath AS Key, ImagePath FROM read_reg_key(
  globs='HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\*')
WHERE ImagePath =~ '(?i)(users|programdata|temp)'

-- 4698 scheduled task creation events
SELECT System.TimeCreated.SystemTime AS Time, EventData.TaskName, EventData.TaskContent
FROM parse_evtx(filename=expand(path='%SystemRoot%/System32/winevt/Logs/Security.evtx'))
WHERE System.EventID.Value = 4698
```

## Develop safely
Test in a **notebook** against one client (`collect_client()` or the client's shell),
check CPU/IO with `rate`/`ops_per_second` limits, then wrap into an artifact and hunt.

## Gotchas
- Backslash escaping in VQL strings and regex (double escaping) is the commonest bug.
- Unbounded globs (`C:/**`) on every endpoint are slow; constrain paths and depth.

## Verify
Query returns expected rows on a test host where you planted a known artefact, and returns
nothing on a clean baseline host.
