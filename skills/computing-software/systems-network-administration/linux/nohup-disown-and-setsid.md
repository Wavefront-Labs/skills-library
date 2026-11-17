---
id: computing-software.systems-network-administration.linux.nohup-disown-and-setsid
name: nohup-disown-and-setsid
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nohup, disown, setsid, systemd-run, background-process, sighup, logout, process-groups, sessions, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Keep a long job running after you disconnect: nohup, disown, setsid, systemd-run --user/--unit, and why logind KillUserProcesses can still kill them."
sources:
  - https://github.com/coreutils/coreutils/blob/master/doc/coreutils.texi
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/setsid.1.adoc
  - https://github.com/systemd/systemd/blob/main/man/logind.conf.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd-run.xml
  - https://github.com/systemd/systemd/blob/main/man/loginctl.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Survive logout: nohup, disown, setsid, systemd-run

**Goal:** start (or rescue) a long-running command over SSH so it keeps going when the
connection drops, with its output captured.

## 1. Why things die
Closing the terminal sends SIGHUP to the session; bash forwards SIGHUP to its jobs (and with
`shopt -s huponexit` on exit) (gated: unconfirmed, source is paywalled or blocked). The bash manual on gnu.org returned HTTP 429 and bash is not mirrored on GitHub.

## 2. Options, best first
```bash
# A. Transient systemd unit: logged, restartable, survives everything
systemd-run --unit=reindex --property=Nice=10 /usr/local/bin/reindex.sh   # root: system manager
systemd-run --user --unit=sync rsync -a src/ dst/      # user manager (needs linger to survive logout)
journalctl -u reindex -f;  systemctl status reindex

# B. tmux/screen — when you want to re-attach interactively (see tmux skill)

# C. nohup: ignore SIGHUP, redirect output
nohup ./long-job.sh > job.log 2>&1 &
# if stdout is a terminal, output is appended to ./nohup.out, else $HOME/nohup.out, else the command is not run

# D. setsid: new session, no controlling terminal at all
setsid -f ./long-job.sh > job.log 2>&1 < /dev/null   # -f: always fork; setsid runs the program in a new session

# E. Already started in the foreground and forgot?
Ctrl-Z           # stop it
bg               # resume in background
disown -h %1     # keep in job table but don't send it SIGHUP  (plain `disown %1` removes it) (gated: unconfirmed, source is paywalled or blocked)
```
`disown` doesn't redirect output; redirect at start if the job will write to the terminal.

## 3. The logind trap
`KillUserProcesses=yes` in `/etc/systemd/logind.conf` (the default is chosen at build time) terminates the session scope
and every process in it at logout, so nohup, setsid and disown do not help; `KillExcludeUsers=` and `KillOnlyUsers=` adjust it.
Escape hatches: `systemd-run --user` services with `loginctl enable-linger`, or `systemd-run --scope` for tools such as tmux.

## Gotchas
- `&` alone is not enough: background jobs can still get SIGHUP from the shell (gated: unconfirmed, source is paywalled or blocked).
- `setsid` forks only if the caller is a process group leader; `-f` always forks, `-w` waits and returns the exit status.

## Verify
- [ ] After disconnecting and reconnecting, `pgrep -a long-job` (or `systemctl status <unit>`) shows it running.
- [ ] The log file keeps growing after logout.

## Checked

2026-10-26. coreutils manual (nohup.out fallback order), util-linux master (last commit 2026-10-26) setsid(1) (-f, -w and fork behaviour), systemd logind.conf (KillUserProcesses=, KillExcludeUsers=, build-time default), loginctl enable-linger, systemd-run --scope and --unit. The bash behaviours (SIGHUP forwarding, huponexit, disown -h) could not be confirmed and carry the gated marker. Removed the reptyr, sudo-in-background and EIO remarks.

Method: documentation only; no commands were run.
