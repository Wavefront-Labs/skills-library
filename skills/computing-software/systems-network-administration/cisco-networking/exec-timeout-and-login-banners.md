---
id: computing-software.systems-network-administration.cisco-networking.exec-timeout-and-login-banners
name: exec-timeout-and-login-banners
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, exec-timeout, banner-motd, banner-login, banner-exec, session-timeout, device-hardening, legal-notice]
level: practitioner
status: draft
description: "Set exec-timeout on console and VTY lines and configure motd/login/exec banners with proper delimiters and legal text, avoiding automation pitfalls."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/fundamentals-cr-book/fundamentals-a1.html
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-110/45038-banner.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# exec-timeout and login banners

## exec-timeout
```
line con 0
 exec-timeout 10 0          ! minutes seconds
line vty 0 15
 exec-timeout 10 0
line aux 0
 exec-timeout 5 0
```
- Default is 10 minutes; `exec-timeout 0 0` disables it (common audit finding: never leave it).
- Idle sessions hold VTY lines; with 5 VTYs an unattended session can lock admins out.
- `absolute-timeout` (line config) ends a session after N minutes regardless of activity.
- `session-timeout` applies to outgoing telnet/ssh sessions from the device.

## Banners
| Banner | Shown | Use |
|---|---|---|
| `banner motd` | before login, every connection | short notices (maintenance) |
| `banner login` | after motd, before username prompt | legal warning |
| `banner exec` | after successful login | operational info |
| `banner incoming` | reverse telnet | rarely |

```
banner login ^C
Authorised access only. Activity is logged and monitored.
Disconnect now if you are not authorised.
^C
```
The first character after `banner login` is the delimiter (`^C` typed as caret-C or Ctrl-V Ctrl-C,
or any character not in the text such as `#`).

## Legal text guidance
Do not say "Welcome". State that access is restricted to authorised users, that use is monitored,
and that unauthorised use may be prosecuted; follow your legal team's wording.
Do not include hostname, model, location or contact details useful to attackers.

## Gotchas
- Banners with `$(hostname)` token expansion exist (`$(hostname)`, `$(domain)`) but leak info.
- Automation tools that wait for a prompt can match text in a banner (e.g. a `#` in the banner);
  keep banners free of prompt-like characters.
- SSH clients show `banner login` before authentication only for keyboard-interactive/password.

## Verify
- [ ] `show line` / `show run | section line` has non-zero exec-timeout on every line.
- [ ] Banner displays before the username prompt over SSH and console.
