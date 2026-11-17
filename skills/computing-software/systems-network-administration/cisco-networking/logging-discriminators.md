---
id: computing-software.systems-network-administration.cisco-networking.logging-discriminators
name: logging-discriminators
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, logging-discriminator, syslog, log-filtering, noise-reduction, logging-host]
level: practitioner
status: draft
description: "Filter IOS syslog per destination with logging discriminators: match facility, mnemonic, severity or message body, drop or include, and attach to console, buffer or hosts."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-msg-logging.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging discriminators

Severity thresholds are blunt: `logging trap informational` sends everything at level 6 and below.
A discriminator filters messages by content per destination.

## Syntax
```
logging discriminator NAME [facility drops|includes REGEX] [mnemonics drops|includes REGEX]
                           [msg-body drops|includes REGEX] [severity drops|includes LEVELS]
```
Facility is the part before the first dash (`LINEPROTO`), mnemonic after the severity
(`UPDOWN`), msg-body the free text.

## Examples
Drop noisy access-port up/down from the SIEM but keep uplinks:
```
logging discriminator NOEDGE mnemonics drops UPDOWN msg-body drops GigabitEthernet1/0/([1-9]|[1-3][0-9]|4[0-8]),
logging host 10.0.0.80 discriminator NOEDGE
```
Send only config changes and authentication to a security collector:
```
logging discriminator SECURITY facility includes PARSER|SEC_LOGIN|AAA
logging host 10.0.0.81 discriminator SECURITY
```
Keep the console quiet but the buffer complete:
```
logging discriminator CONSOLE severity includes 0,1,2
logging console discriminator CONSOLE
logging buffered 64000 debugging
```

## Verify
```
show logging | include Discriminator|Trap logging|Logging to
show logging discriminator NOEDGE        ! some releases
```
Generate a test message (`send log 6 "TEST NOEDGE"`) and check where it lands.

## Gotchas
- Up to 8 discriminators on most releases; plan them.
- A discriminator applies after the severity threshold for that destination; a message filtered by
  `logging trap warnings` never reaches the discriminator.
- Regex on msg-body is matched against the text after the mnemonic; anchor carefully.
- Dropping messages at the source loses them forever. For compliance logs, filter in the SIEM
  instead and keep the device sending everything to at least one collector.

## Verify
- [ ] Test messages appear only on intended destinations.
- [ ] SIEM event rate from the device drops as expected without losing config-change events.
