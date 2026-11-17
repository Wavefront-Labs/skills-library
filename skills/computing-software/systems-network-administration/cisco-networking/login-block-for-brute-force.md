---
id: computing-software.systems-network-administration.cisco-networking.login-block-for-brute-force
name: login-block-for-brute-force
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, login-block-for, login-quiet-mode, brute-force, login-delay, login-on-failure, vty]
level: practitioner
status: docs-checked
description: "Rate-limit login attempts on IOS with login block-for, quiet-mode access-class exceptions for management hosts, login delay and show login verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_cfg/configuration/xe-16/sec-usr-cfg-xe-16-book/sec-login-enhance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Login block-for (brute-force protection)

```
ip access-list standard MGMT-HOSTS
 permit 10.99.0.0 0.0.0.255
login block-for 120 attempts 5 within 60
login quiet-mode access-class MGMT-HOSTS
login delay 2
```
- `login block-for <seconds> attempts <tries> within <seconds>`: after the configured number of failed attempts within
  the window, the device refuses further Telnet and SSH logins for the quiet period. The command must be issued before
  any other `login` command can be used; all login parameters are disabled by default.
- During quiet mode all login requests are denied and the only available connection is the console.
- `login quiet-mode access-class {acl-name | acl-number}` names the hosts still allowed during quiet mode. It is
  optional but recommended. Without it, no ACL is exempt and the device creates a hidden default ACL `sl_def_acl` that
  denies telnet, www and port 22 and permits everything else (view with `show access-lists sl_def_acl`). So an
  attacker's failed attempts can lock out administrators for the quiet period unless their hosts are in the ACL.
- `login delay <seconds>` sets the delay between successive login attempts. Once `login block-for` is entered the
  default delay is 1 second.
- The feature is not enabled if AutoSecure is enabled (the Cisco page says so); AutoSecure itself enforces the
  default 1 second delay.

## Verify
```
show login                ! delay, quiet-mode ACL, thresholds, watch-mode or quiet-mode status and remaining time
show login failures       ! username, source address, local port, count, timestamp of failed attempts
```
Test from a non-management host with wrong passwords; confirm quiet mode triggers and the management host can still
log in.
- [ ] `show login` shows thresholds and quiet-mode ACL; test lockout behaved as expected.

## Checked
Checked 2026-11-08 against Cisco's Cisco IOS Login Enhancements-Login Block chapter (IOS XE 16 User Security
Configuration Guide): command syntax, defaults, the sl_def_acl default, console exception, `show login` and
`show login failures`. Removed as unconfirmed by that page: `login on-failure log` / `login on-success log`, the
SEC_LOGIN syslog message formats, and the vty access-class, management VRF and CoPP advice.
Method: documentation only; no commands were run.
