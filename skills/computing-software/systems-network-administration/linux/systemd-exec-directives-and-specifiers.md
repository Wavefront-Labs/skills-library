---
id: computing-software.systems-network-administration.linux.systemd-exec-directives-and-specifiers
name: systemd-exec-directives-and-specifiers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, unit-file, execstart, execstartpre, execstartpost, execreload, execstop, unit-specifiers, template-units, environmentfile, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Write ExecStart/ExecStartPre/ExecReload/ExecStop lines that systemd actually parses as intended: no shell, prefixes (- @ + !), environment expansion and %i/%n specifiers."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Specifiers
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exec directives and specifiers

**Goal:** command lines in units that start, reload and stop the service correctly, and
template units that reuse one file for many instances.

## 1. The rules systemd applies
- **No shell.** Pipes, `&&`, redirection, globbing and `$(...)` don't work. If you need them:
  `ExecStart=/bin/sh -c 'exec /usr/bin/app >>/var/log/app.log 2>&1'` (keep `exec` so the
  main PID is the app, not sh).
- The first word is an absolute path or a plain file name that systemd resolves through a fixed search path (`ExecSearchPath=` in `systemd.exec`); it cannot be a variable.
- Variables: `${VAR}` expands to one argument, `$VAR` splits on whitespace into several.
  Source them with `Environment=` or `EnvironmentFile=-/etc/sysconfig/app` (`-` = optional).
- `%` must be written `%%` and literal `$` as `$$`.

## 2. Which directive runs when
| Directive | Runs | Notes |
|---|---|---|
| `ExecStartPre=` | before main process, in order | failure aborts start (unless `-` prefix) |
| `ExecStart=` | main process | exactly one, except `Type=oneshot` (many allowed) |
| `ExecStartPost=` | after start is considered done | for notify/forking, after READY/fork |
| `ExecReload=` | `systemctl reload` | e.g. `/bin/kill -HUP $MAINPID` (a bare signal is asynchronous: no completion notification) |
| `ExecStop=` | `systemctl stop` | omitted → SIGTERM (KillSignal=) to the cgroup |
| `ExecStopPost=` | after stop, even on failure | cleanup; sees `$SERVICE_RESULT`, `$EXIT_STATUS` |
| `ExecCondition=` | before Pre; exit 1-254 skips start cleanly | systemd ≥ 243 |

## 3. Prefixes
`-` ignore failure · `@` second word is argv[0] · `+` run with full privileges (ignores `User=`, `Group=`, capability and namespace restrictions) · `!` like `+` but only ignores `User=`, `Group=` and `SupplementaryGroups=` · `:` do not expand environment variables.

## 4. Override a list in a drop-in
`ExecStart=` is additive in drop-ins; clear it first:
```ini
# systemctl edit app.service
[Service]
ExecStart=
ExecStart=/usr/bin/app --config /etc/app/prod.yaml
```

## 5. Templates and specifiers
`app@.service` → instances `app@blue.service`, `app@green.service`:
```ini
[Service]
EnvironmentFile=/etc/app/%i.env
ExecStart=/usr/bin/app --name %i --state %S/app/%i
```
Useful specifiers: `%i` instance (escaped) / `%I` unescaped, `%n` full unit name, `%p`
prefix, `%H` hostname, `%t` runtime dir (`/run` or `$XDG_RUNTIME_DIR`), `%S` state dir,
`%C` cache dir, `%h` user home (user units), `%u` user. Escape paths with
`systemd-escape --path /dev/sdb1` → `dev-sdb1`.

## Gotchas
- `ExecReload=` that only sends a signal returns instantly; the reload may still fail later.
- `Type=forking` + `ExecStart=` that daemonises needs `PIDFile=` or systemd may track the wrong PID.

## Verify
- [ ] `systemd-analyze verify app.service` reports no errors.
- [ ] `systemctl show -p ExecStart app` displays the parsed argv you intended.
- [ ] `systemctl reload app` then `journalctl -u app -n 20` shows the reload took effect.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: no shell syntax; `${VAR}` expands to one argument and `$VAR` splits words; `$$` for a literal dollar and `%%` as a specifier; `ExecCondition=` (exit 1-254 skips cleanly, v243 NEWS), `ExecStartPre/Post`, `ExecReload`, `ExecStop` (omitted means the kill signal), `ExecStopPost` with `$SERVICE_RESULT`; exactly one `ExecStart=` unless `Type=oneshot`; prefixes `@ - : + !` and `|`; the specifier table in `systemd.unit` (`%i %I %n %N %p %H %t %S %C %h %u`); empty assignment resets a list. Removed the shell-quoting remark, the prefix-combination example and the version gate on PATH search.

Method: documentation only; no commands were run.
