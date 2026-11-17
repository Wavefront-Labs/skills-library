---
id: computing-software.systems-network-administration.cisco-networking.console-and-aux-line-security
name: console-and-aux-line-security
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, console-line, aux-port, line-security, transport-input-none, no-exec, device-hardening, physical-security]
level: practitioner
status: draft
description: "Lock down IOS console and AUX lines: AAA login, exec-timeout, disabling AUX exec and transport, logging synchronous, and protecting against password recovery."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_cfg/configuration/xe-16/sec-usr-cfg-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Console and AUX line security

## Console
```
aaa new-model
aaa authentication login CONSOLE local            ! keep local so console works when AAA servers are down
line con 0
 login authentication CONSOLE
 exec-timeout 5 0
 logging synchronous
 transport output none
 privilege level 1
```
- Use a separate method list for console with local fallback; a dead TACACS+ server must never lock you out.
- `logging synchronous` stops log messages breaking your typing.

## AUX port
The AUX port (routers) was for modems; an attached modem or terminal server is a back door.
```
line aux 0
 no exec
 transport input none
 transport output none
 exec-timeout 0 1
 login authentication CONSOLE
```
If you use AUX for an out-of-band modem/cellular, treat it like VTY: strong AAA, ACLs, logging.

## Password recovery protection
Physical console access + reload = password recovery (config-register 0x2142). To stop it on
routers that support it:
```
no service password-recovery
```
Then recovery wipes the config (startup-config is erased before access). Make sure you have backups;
on Catalyst the equivalent is `no service password-recovery` too (switch erases config on recovery).

## Other hardening
- Set `usb-inactivity-timeout` on platforms with a USB console port, or disable the USB console
  where the platform supports it.
- Physically secure the device; console access defeats most controls.
- Log console logins (`login on-success log`).

## Verify
- [ ] `show line` shows aux with no exec; console exec-timeout set.
- [ ] With AAA servers unreachable, console local login still works (test in a window).
