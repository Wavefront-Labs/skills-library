---
id: computing-software.systems-network-administration.linux.pgrep-pkill-killall
name: pgrep-pkill-killall
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pgrep, pkill, killall, pidof, signals, process-selection, lpic-1, rhcsa, sysadmin]
level: practitioner
status: verified
description: "Find and signal processes by name, user, parent, terminal or age with pgrep/pkill/killall/pidof — with dry runs so you don't kill the wrong thing."
sources:
  - https://manpages.debian.org/trixie/procps/pgrep.1.en.html
  - https://manpages.debian.org/trixie/psmisc/killall.1.en.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# pgrep, pkill, killall, pidof

**Goal:** select processes precisely by attribute and signal them, previewing the selection
first.

## 1. pgrep / pkill (procps — same selection options)
```bash
pgrep -a nginx                 # PID + full command line (-a/--list-full; preview!)
pgrep -l -u www-data           # by effective user; -U real user
pgrep -f 'python3 .*worker.py' # match the whole command line, not just the 15-char name
pgrep -x sshd                  # exact name match (not "sshd-session")
pgrep -P 1234                  # children of PID 1234
pgrep -t pts/3                 # on a terminal
pgrep -n / -o rsync            # newest / oldest only
pgrep --older 3600 -f backup   # running longer than 3600 s
pgrep -c httpd                 # count
pkill -HUP -x rsyslogd         # same selectors, sends the signal (default TERM)
pkill -KILL -u baduser         # everything a user runs
pkill -t pts/3                 # log out a terminal session
pkill -e -f 'stuck-job'        # -e echoes what it killed
```
Workflow: run the `pgrep -a` form, eyeball the list, then swap `pgrep -a` for `pkill`.

## 2. killall (psmisc)
```bash
killall -i nginx           # interactive confirm per process
killall -u alice           # all processes of a user
killall -w -TERM app       # wait until they've all died
killall -o 2h script.sh    # older than 2 hours (-y younger)
```
Matches process names (`-r` for a POSIX extended regex). The manual warns that `killall name` may not have the desired effect on non-Linux systems,
especially as a privileged user — never type it from habit elsewhere.

## 3. pidof
`pidof` prints PIDs for a program name (see pidof(1) for `-s` and `-x`). Mostly for init
scripts; pgrep is more flexible.

## Gotchas
- Name matching is limited to the 15 characters shown in `/proc/PID/stat`; long names need `-f`.
- `pkill -f` with a loose pattern can hit your own SSH session or editor; always preview.
- Exit status: 0 one or more matched, 1 none matched, 2 syntax error, 3 fatal error — useful in health checks (`pgrep -x app >/dev/null || alert`).
- For systemd services prefer `systemctl kill --signal=HUP unit` — scoped to the unit's cgroup.

## Verify
- [ ] `pgrep -a <selection>` lists only the intended processes before you pkill.
- [ ] Afterwards `pgrep -c <selection>` returns 0 (or the expected survivors).

## Checked
2026-10-27. Checked against the Debian trixie pages for pgrep(1) (procps 4.0.4), killall(1) (psmisc 23.7) and the procps pidof page was not reachable, so only its existence is stated. Confirmed: pgrep -a, -l, -u (effective user), -U (real user), -f, -x, -P, -t, -n, -o, --older, -c; pkill -e and the default SIGTERM; the 15-character name limit and -f; exit status 0 to 3; killall -i, -u, -w, -o and -y with unit suffixes, -r POSIX extended regex, and the non-Linux warning. Removed: the procps version gate for --older, the Solaris and AIX wording (the manual gives a general warning), the self-match remark and the pidof option details. The man7.org links in sources were replaced because man7.org does not host these pages.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (procps 4.0.4, psmisc 23.7): pgrep -a/-l/-x/-f/-n/-o/-c/-P/-t/--older, the 15-character name limit (pgrep refuses a longer name and points to -f), exit codes 0, 1 and 2, pkill -e and -f, killall -w/-r/-i/-o/-y and the default signal, pidof -s/-x. Not run: exit status 3, -U real-user selection, systemctl kill.
