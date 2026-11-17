---
id: computing-software.systems-network-administration.cisco-networking.eem-applets
name: eem-applets
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, network-automation, eem, embedded-event-manager, event-manager-applet, syslog-pattern, track-event, timer-cron, action-cli, on-box-automation, guestshell]
level: practitioner
status: draft
description: "Automate on-box reactions with EEM applets: syslog, track and cron triggers, CLI actions, capturing show output on events, variables, and safe testing with event none."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/eem/configuration/xe-16/eem-xe-16-book/eem-policy-cli.html
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-16/216091-best-practices-and-useful-scripts-for-ee.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EEM applets

Embedded Event Manager runs actions on the device when an event fires: no external server
needed, works when the network is down.

## Capture diagnostics when something happens
```
event manager applet CAPTURE-ON-BGP-DOWN
 event syslog pattern "%BGP-5-ADJCHANGE.*Down" maxrun 120
 action 1.0 cli command "enable"
 action 1.1 cli command "show ip bgp summary | append bootflash:bgp-down.txt"
 action 1.2 cli command "show logging | append bootflash:bgp-down.txt"
 action 1.3 cli command "show processes cpu sorted | append bootflash:bgp-down.txt"
 action 2.0 syslog priority warnings msg "EEM captured BGP-down diagnostics"
```

## React to a tracked object
```
event manager applet ISP1-DOWN
 event track 10 state down
 action 1.0 cli command "enable"
 action 1.1 cli command "configure terminal"
 action 1.2 cli command "interface Tunnel1"
 action 1.3 cli command "shutdown"
 action 2.0 syslog msg "ISP1 down: Tunnel1 shut by EEM"
```

## Scheduled jobs
```
event manager applet NIGHTLY-BACKUP
 event timer cron cron-entry "0 2 * * *"
 action 1.0 cli command "enable"
 action 1.1 cli command "copy running-config scp://backup@10.0.0.30/cfg/$_info_routername.cfg" pattern "Address|confirm|\]"
 action 1.2 cli command ""
```
`pattern` handles interactive prompts; follow with an empty command to press Enter.

## Testing
```
event manager applet TEST
 event none                        ! run manually
 action 1.0 cli command "enable"
 action 1.1 cli command "show clock"
 action 1.2 puts "$_cli_result"
event manager run TEST
show event manager history events
show event manager policy registered
debug event manager action cli     ! see each CLI step (lab)
```

## Gotchas
- With AAA command authorization, EEM CLI actions need authorization too:
  `event manager session cli username eem-user` with a local or TACACS user permitted to run them.
- Default `maxrun` is 20 s; long actions get killed silently. Set `maxrun`.
- Syslog-pattern applets that generate the same syslog they match create loops; use
  `ratelimit` on the event or a distinct message.
- Action labels sort as strings: 1.10 runs before 1.2. Use consistent numbering (1.01, 1.02 or 010, 020).

## Verify
- [ ] `event manager run` on a test applet produces the expected output.
- [ ] `show event manager history events` shows the trigger firing at the right time.
