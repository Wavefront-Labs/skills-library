---
id: computing-software.systems-network-administration.bash.terminal-session-recording-script
name: terminal-session-recording-script
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, script-command, scriptreplay, session-recording, asciinema, audit, change-record]
level: practitioner
status: docs-checked
description: "Record terminal sessions for change records or training with script (timing files, -q, -f, -c) and replay with scriptreplay, with a note on tlog for central recording."
sources:
  - https://man7.org/linux/man-pages/man1/script.1.html
  - https://man7.org/linux/man-pages/man1/scriptreplay.1.html
  - https://github.com/Scribery/tlog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording sessions with script

## Record
```bash
script -q -f --log-timing chg-1234.tm chg-1234.log        # -q quiet, -f flush after each write, --log-timing timing file
script -q -f -t 2>chg-1234.tm chg-1234.log                 # deprecated -t: timing on stderr
script -q -c 'ansible-playbook site.yml' run.log           # record a single command
exit                                                        # end recording (or Ctrl+D)
```
Name files with the change ticket and date; store with the change record.

## Replay
```bash
scriptreplay --log-timing chg-1234.tm chg-1234.log          # real-time playback
scriptreplay -t chg-1234.tm -O chg-1234.log -d 4            # 4x speed (-d is the divisor; -s is a deprecated alias of -O)
```

## Alternatives
- **tlog** (https://github.com/Scribery/tlog) sends recorded sessions to a logging service (syslog or journald) as JSON instead of a local file.

## Gotchas
- The log holds all terminal output; logging input (`--log-in`, `--log-io`) also records passwords typed with echo off. Protect the files like credentials.
- scriptreplay is only guaranteed to work on the same type of terminal the typescript was recorded on.
- Users can just exit `script`: it is a record-keeping convenience, not an audit control.
- `-f` flushes after each write at some performance cost.

## Checked
2026-11-01. Confirmed against script(1), scriptreplay(1) man pages (man7.org) and the tlog README: `-q`, `-f`, `-c`,
`--log-timing`, deprecated `-t`, scriptreplay `-t`/`-O`/`-d`, replay caveats, input-logging warning, tlog output to syslog/journald.
Removed: asciinema, sudoreplay, version number, less/col helpers, RHEL/SSSD claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Replay shows the full session; the file is stored with restricted permissions next to the change ticket.
