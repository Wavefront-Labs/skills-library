---
id: computing-software.cybersecurity-defensive.splunk.file-monitor-inputs
name: file-monitor-inputs
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, monitor-input, inputs-conf, crcsalt, initcrclength, fishbucket, universal-forwarder, log-rotation]
level: practitioner
status: draft
description: "Configure Splunk file monitor inputs that survive log rotation: whitelist/blacklist, crcSalt vs initCrcLength, fishbucket behaviour, and diagnosing files that never index."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Data/Monitorfilesanddirectorieswithinputs.conf", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Inputsconf", "https://docs.splunk.com/Documentation/Splunk/latest/Data/Howlogfilerotationishandled"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File monitor inputs

## Stanza
```
[monitor:///var/log/nginx/]
whitelist = (access|error)\.log$
blacklist = \.(gz|bz2|zip)$
index = web
sourcetype = nginx:plus:kv
disabled = false
ignoreOlderThan = 7d
```
Windows: `[monitor://<IIS_LOG_DIR>\W3SVC1\*.log]` (the IIS log folder on the system drive).
- `whitelist`/`blacklist` are regexes on the full path, not globs.
- `...` in the path recurses; `*` matches one path segment.
- `ignoreOlderThan` skips files by modtime at first discovery; a file skipped once is not
  revisited later even if it changes.

## How Splunk recognises a file (fishbucket)
The forwarder hashes the first 256 bytes (CRC) plus a seek pointer and stores it in
`$SPLUNK_HOME/var/lib/splunk/fishbucket`. Consequences:
- Files with an identical header (e.g. a CSV header or a banner line) look like the same file:
  only one is indexed. Fix with `initCrcLength = 1024` (hash more bytes) or `crcSalt = <SOURCE>`
  (add the path to the hash).
- `crcSalt = <SOURCE>` re-indexes rotated files that are renamed (app.log -> app.log.1) because
  the path changed. Use it only when files are never renamed.
- Rotated-and-compressed files are skipped automatically when the CRC matches one already read.

## Re-indexing a file on purpose
`splunk cmd btprobe -d $SPLUNK_HOME/var/lib/splunk/fishbucket/splunk_private_db --file <path> --reset`
then restart. Never delete the whole fishbucket on a production forwarder: everything re-indexes.

## Diagnose a file that never shows up
1. `splunk list inputstatus` (or REST `/services/admin/inputstatus/TailingProcessor:FileStatus`)
   shows each file: "finished reading", "ignored file (crc conflict)", "binary file", "older than".
2. `index=_internal host=<fwd> source=*splunkd.log (TailReader OR WatchedFile OR TailingProcessor)`.
3. Permissions: on Linux the forwarder user needs read on the file and execute on every parent
   directory; check `ls -l` and `getfacl`. Running UF as root to "fix" this is a hardening regression.
4. Binary detection: files with NUL bytes are skipped; set `NO_BINARY_CHECK = true` in props for
   the source if it is really text.

## Gotchas
- Hundreds of thousands of files in a monitored tree exhaust file descriptors; narrow the path
  or archive old logs.
- Changing `sourcetype` or `index` on an existing input only affects new data.
- Network shares are unreliable for tailing; forward from the host that writes the log.

## Verify
`| tstats latest(_time) as last where index=web by host source` shows every file and its freshness.
