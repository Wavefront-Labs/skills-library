---
id: computing-software.systems-network-administration.linux.auditd-rules-and-log-review
name: auditd-rules-and-log-review
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, auditd, audit-rules, audit-log, auditctl, ausearch, aureport, audit-rules-d, augenrules, syscall-audit, file-watch, immutable-rules, audit-backlog, audit-key, cis-audit, stig-audit, pam-tty-audit, lpic-2, security, compliance, sysadmin, auditd-conf, max-log-file, audisp-remote]
level: advanced
status: docs-checked
description: "Configure the Linux audit subsystem: persistent rules.d file watches and syscall rules, CIS/STIG baseline, ausearch/aureport queries, log sizing and rotation, and performance limits."
sources:
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/auditctl.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/audit.rules.7
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/auditd.conf.5
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/auditd.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/augenrules.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/aureport.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/auditd-plugins.5
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# auditd — record who touched what, and be able to answer the question later

**Goal:** a kernel-level audit trail of privileged actions, config changes and sensitive
file access, with rules that survive reboot, logs that don't fill the disk, and queries
you can run in an incident.

## 1. Service and config
```bash
# install your distribution's auditd package, then:
systemctl enable --now auditd
auditctl -s                        # kernel status: enabled flag, failure mode, auditd pid (0 = not running), backlog, lost (events lost)
```
`/etc/audit/auditd.conf` essentials:
```
log_file = /var/log/audit/audit.log
max_log_file = 50                # size of one log file in MB
num_logs = 10
max_log_file_action = ROTATE     # keep_logs rotates without using num_logs, so logs accumulate (ship them off-box)
space_left = 500                 # MiB free; a number followed by % is also accepted
space_left_action = SYSLOG       # warn; EMAIL/EXEC for serious environments
admin_space_left_action = SUSPEND   # SUSPEND stops logging; HALT shuts the machine down (see auditd.conf(5))
disk_full_action = SUSPEND
flush = INCREMENTAL_ASYNC
freq = 50
```
Keep `/var/log/audit` on its own filesystem and size `max_log_file` and `num_logs` to it so a full audit partition cannot fill the root filesystem. Ship logs to a central collector with an auditd plugin (plugins live in `/etc/audit/plugins.d` and each has an `active` setting; the `audisp-remote` plugin forwards to another auditd; see auditd-plugins(5)).

## 2. Rules (persistent in `/etc/audit/rules.d/*.rules`, compiled by `augenrules`)
```
# /etc/audit/rules.d/10-base.rules
-D                              # delete all
-b 8192                         # backlog buffer
-f 1                            # on failure: 1 = printk (the default), 2 = panic, 0 = silent
--backlog_wait_time 60000

# /etc/audit/rules.d/30-watches.rules   (-w path -p rwxa -k key)
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers
-w /etc/ssh/sshd_config -p wa -k sshd
-w /etc/ssh/sshd_config.d/ -p wa -k sshd
-w /var/log/sudo.log -p wa -k sudo_log
-w /etc/selinux/ -p wa -k mac-policy
-w /etc/audit/ -p wa -k audit-config
-w /sbin/insmod -p x -k modules
-w /sbin/modprobe -p x -k modules

# /etc/audit/rules.d/40-syscalls.rules   (-a action,list -F filters -S syscalls -k key)
-a always,exit -F arch=b64 -S execve -F euid=0 -F auid>=1000 -F auid!=unset -k rootcmd       # commands run as root by real users
-a always,exit -F arch=b64 -S adjtimex,settimeofday,clock_settime -k time-change
-a always,exit -F arch=b64 -S sethostname,setdomainname -k system-locale
-a always,exit -F arch=b64 -S chmod,fchmod,fchmodat,chown,fchown,lchown,fchownat,setxattr,lsetxattr,fsetxattr,removexattr -F auid>=1000 -F auid!=unset -k perm_mod
-a always,exit -F arch=b64 -S open,openat,openat2,creat,truncate -F exit=-EACCES -F auid>=1000 -F auid!=unset -k access
-a always,exit -F arch=b64 -S open,openat,openat2,creat,truncate -F exit=-EPERM  -F auid>=1000 -F auid!=unset -k access
-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=unset -k mounts
-a always,exit -F arch=b64 -S unlink,unlinkat,rename,renameat -F auid>=1000 -F auid!=unset -k delete
-a always,exit -F arch=b64 -S init_module,finit_module,delete_module -k modules
-a always,exit -F arch=b64 -F path=/usr/bin/sudo -F perm=x -F auid>=1000 -F auid!=unset -k privileged
-a always,exit -F arch=b64 -F path=/usr/bin/passwd -F perm=x -F auid>=1000 -F auid!=unset -k privileged

# /etc/audit/rules.d/99-finalize.rules
-e 2                            # lock the configuration: it can only be changed by rebooting
```
```bash
augenrules --load                # compile rules.d → /etc/audit/audit.rules and load
auditctl -l                      # loaded rules
auditctl -w /etc/hosts -p wa -k hosts   # ad-hoc, non-persistent
```
- `auid` = the login UID, which survives `sudo`/`su` — the whole point of audit vs syslog.
  `auid>=1000 -F auid!=unset` excludes daemons and the unset (-1/4294967295) UID.
- Duplicate the `arch=b64` syscall rules with `arch=b32` on hosts that run 32-bit binaries; syscall names and availability differ per architecture (for example `open` is absent on some). Watch rules (`-w`) are arch-independent.
- `-e 2` makes any configuration change require a reboot; keep it last in the rules and test rules before enabling it.
- Rules are evaluated in order, so put any exclusion rules above the rules they should exempt.
- High-volume syscall rules (`open*` on busy hosts) cost CPU; use `-F dir=` / `-F exit=` filters
  and raise `-b` if `auditctl -s` shows `lost` increasing.

## 3. Querying
```bash
ausearch -k identity --start today -i               # -i interprets uids/syscalls
aureport -l --failed --start this-week               # failed logins
ausearch -ul alice --start recent                    # by login uid (auid); -ua matches any of uid, euid and auid
ausearch -x /usr/bin/passwd -i
ausearch -m AVC -ts recent                           # SELinux denials (same log)
ausearch -c sshd --raw | aureport -i -f              # file report for a process
aureport -au --summary; aureport -x --summary; aureport -k --summary   # auth, executables, keys
aureport --failed; aureport -i -l                    # failures, logins
ausearch -i -a 1234567                               # all records of one event id
```
Each event is several records (SYSCALL, CWD, PATH, PROCTITLE) sharing a serial; `-i` makes
them human-readable. 
## 4. Extras
- `aureport --tty` reports TTY input recorded by the audit system.
- Add `audit=1` to the kernel command line so processes started before auditd are marked auditable (auditd(8) notes some processes cannot otherwise be audited).

## Failure modes
- Rule changes are denied (and audited) while the configuration is locked with `-e 2`: reboot to change it.
- Rule load errors are reported by auditctl; its `-c` option continues loading after an error and exits non-zero if any rule failed.
- Audit log fills `/`: no separate partition, or `max_log_file_action` set so that logs accumulate.
- SELinux hosts: `ausearch -m avc` is also where you find why a service can't read a file.

## Verify
- [ ] `auditctl -s` shows enabled 1 (or 2 when locked) and `lost 0`; `auditctl -l` matches your rules.d.
- [ ] `sudo touch /etc/sudoers.d/test && rm` produces `ausearch -k sudoers` events with your `auid`.
- [ ] After reboot the rules are loaded and the log rotates under `max_log_file` with disk usage bounded.

## Checked
Checked 2026-10-25 against the audit-userspace man pages on GitHub (linux-audit/audit-userspace docs/, master, last commit 2026-10-10). Confirmed: auditctl `-b` (kernel default 64), `--backlog_wait_time`, `-D`, `-e 0|1|2` (2 locks the configuration until reboot), `-f 0|1|2` (default 1 printk, 2 panic), `-s` status fields, rule syntax `-w`, `-a always,exit`, `-F path= perm= arch= exit= dir= auid!=unset`, `-k`; auid unsigned and 4294967295 when unset; `openat2` in the open-family examples; auditd.conf keys `max_log_file`, `num_logs`, `max_log_file_action` (ROTATE, KEEP_LOGS), `space_left` (MiB or %), `space_left_action`, `admin_space_left_action`, `disk_full_action`, `flush` (INCREMENTAL_ASYNC), `freq`, actions SUSPEND and HALT; `audit=1` boot parameter; plugins in `/etc/audit/plugins.d` with `active`; `augenrules` merging `/etc/audit/rules.d`; ausearch `-k -i -m -sv -ul -ua -x -c -a --raw --start/-ts` values; aureport `-au -x -k --summary --failed -l -f --tty`. Fixed: `ausearch -ua` was described as login uid (it matches any of uid, euid, auid; `-ul` is the login uid). Removed unconfirmed claims: RHEL service-control behaviour, CIS and STIG attributions, the SUID find/awk pipeline, pam_tty_audit setup, the audit_backlog_limit boot parameter, aulast/aulastlog and plugin file names.

Method: documentation only; no commands were run.
