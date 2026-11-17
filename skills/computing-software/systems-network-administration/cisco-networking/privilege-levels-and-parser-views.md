---
id: computing-software.systems-network-administration.cisco-networking.privilege-levels-and-parser-views
name: privilege-levels-and-parser-views
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, privilege-levels, parser-view, role-based-cli, privilege-exec, enable-view, least-privilege]
level: practitioner
status: draft
description: "Give helpdesk staff limited IOS command access with custom privilege levels or role-based CLI parser views, and check what each user can actually run."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_cfg/configuration/xe-16/sec-usr-cfg-xe-16-book/sec-role-base-cli.html
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/terminal-access-controller-access-control-system-tacacs-/23383-showrun.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Privilege levels and parser views

IOS has levels 0-15: 1 = user EXEC, 15 = everything. Levels 2-14 are empty until you move
commands into them. For larger teams, central TACACS+ command authorization is cleaner; this
is the on-box method.

## Custom privilege level (helpdesk: show + bounce a port)
```
privilege exec level 5 show running-config      ! sees only commands it may configure
privilege exec level 5 configure terminal
privilege configure level 5 interface
privilege interface level 5 shutdown
privilege interface level 5 no shutdown
privilege interface level 5 description
username helpdesk privilege 5 algorithm-type scrypt secret <PASSWORD>
```
Gotchas:
- `show running-config` at a low level shows only lines the user could configure; use
  `file privilege` or `show running-config` at 15 for full output.
- Moving a command like `show` moves all its keywords; be specific (`show ip`...).
- `privilege exec all level 5 ...` changes subcommands too; easy to over-grant.

## Role-based CLI views
```
aaa new-model                                  ! required
enable view                                    ! enter root view with enable secret
parser view HELPDESK
 secret <VIEW_SECRET>
 commands exec include show interfaces
 commands exec include show ip interface brief
 commands exec include configure terminal
 commands configure include interface
 commands interface include shutdown
 commands interface include no shutdown
username helpdesk view HELPDESK algorithm-type scrypt secret <PASSWORD>
```
Views are explicit allow-lists, easier to audit than shuffled privilege levels.

## Verify
Log in as the user and run `show privilege` / `show parser view`; try a forbidden command
(`% Invalid input` expected). Keep an emergency local level-15 account.
- [ ] Helpdesk account can bounce ports and view status, cannot reload or edit routing.
