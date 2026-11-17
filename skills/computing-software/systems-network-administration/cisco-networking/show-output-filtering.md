---
id: computing-software.systems-network-administration.cisco-networking.show-output-filtering
name: show-output-filtering
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ios-cli, show-section, output-modifiers, include, exclude, begin, section, count, redirect, append, tee, terminal-length, show-run-all, regex]
level: practitioner
status: draft
description: "Find things fast in IOS output: include/exclude/begin/section/count modifiers, IOS regex, redirecting to flash, terminal length and the show-run variants that save time."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/configuration/xe-16/fundamentals-xe-16-book/cf-cli-basics.html
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-110/13801-ios-regex.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filtering show output on IOS / IOS XE

## The pipe modifiers
```
show ip int brief | include up             ! lines matching regex (abbrev: | i)
show int status | exclude notconnect       ! drop matching lines (| ex)
show run | begin ^router ospf              ! start at first match (| b)
show run | section ^interface Gig          ! whole block whose parent line matches (| s)
show int status | count connected          ! number of matching lines
show tech | redirect bootflash:tech.txt    ! to a file, nothing on screen
show log | append bootflash:log.txt        ! append; | tee writes and displays
```

Only **one** pipe per command on classic IOS (IOS XE 16.x+ allows chaining a few, e.g.
`| s ospf | i area`). The argument is a regex, case-sensitive, and spaces matter.

## IOS regex essentials
- `|` inside the pattern is alternation: `show ip int br | i Vlan10|Vlan20`.
- `^` and `$` anchor the line: `show run | i ^username` (top-level only).
- `.` matches any char, `_` matches a delimiter (space, comma, start/end): useful in BGP
  AS-path filters and `show ip bgp regexp _65001$`.
- Brackets: `show int | i ^[GT].*line protocol is down`.

## Config views that save scrolling
```
show running-config interface Gi1/0/1     ! one interface
show running-config | section router bgp  ! one process
show running-config all | i ip cef        ! includes default commands
show running-config partition router      ! IOS with parser cache partitions
show startup-config | i hostname
show archive config differences nvram:startup-config system:running-config  ! unsaved changes
```

## Long output handling
- `terminal length 0` stops `--More--` paging for scripts and captures (session only).
- `terminal width 0` stops line wrapping.
- From config mode prefix `do`: `do show ip int brief`.
- `show tech-support | redirect bootflash:tech.txt` then copy off via SCP rather than
  scrolling thousands of lines over a console at 9600 baud.

## Gotchas
- `section` matches the **parent** line; children alone will not trigger it.
- `include` with a space-led pattern like `| i  ip` (two spaces) includes the space.
- Filters run after the device has generated output; `show tech` is still expensive on CPU.
- NX-OS uses `| grep`, `| json`, `| last N`; do not assume IOS modifiers there.

## Verify
- [ ] `show run | s ^interface` prints full interface blocks.
- [ ] `show int status | count connected` returns a count line.
- [ ] Redirected file appears in `dir bootflash:` with non-zero size.
