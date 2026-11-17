---
id: computing-software.systems-network-administration.cisco-networking.autoqos-on-catalyst
name: autoqos-on-catalyst
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, qos, auto-qos, autoqos, auto-qos-voip, trust-boundary, catalyst-qos, voice-qos]
level: practitioner
status: docs-checked
description: "Apply AutoQoS on Catalyst 9300 ports (voip, video, classify, trust), know what it generates and its restrictions, use compact mode, and remove it cleanly, per the 17.9 guide."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/qos/b_179_qos_9300_cg/configuring_auto_qos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AutoQoS on Catalyst switches

Syntax and behaviour are from the Catalyst 9300 IOS XE 17.9 QoS guide (page dated Aug 2022); other platforms differ.

## Commands (interface level)
| Command | Use |
|---|---|
| `auto qos trust dscp` / `auto qos trust cos` | trusted interfaces (uplink to a trusted switch or router) |
| `auto qos voip trust` | uplink to a trusted switch or router; VoIP classification in ingress packets is trusted |
| `auto qos voip cisco-phone` | conditional trust through CDP: trusted only when a Cisco IP phone is detected |
| `auto qos voip cisco-softphone` | PCs running Cisco IP SoftPhone: marks and polices traffic; port is untrusted |
| `auto qos video cts` / `ip-camera` / `media-player` | Cisco TelePresence, Cisco surveillance camera, CDP-capable digital media player; conditional trust through CDP |
| `auto qos classify [police]` | untrusted desktops and devices: classify and mark; the guide says the generated policies police |

```
interface HundredGigE 1/0/1
 auto qos trust dscp
end
show auto qos interface HundredGigE 1/0/1
show policy-map interface HundredGigE 1/0/1
```
For best results the guide says to configure auto-QoS on all devices in the network.

## What it generates
- Applying it on any interface creates global class maps and policy maps (it uses MQC). Names start `AutoQos-4.0-`, for example `AutoQos-4.0-Output-Policy` and an input policy such as `AutoQos-4.0-Trust-Dscp-Input-Policy` or `AutoQos-4.0-CiscoPhone-Input-Policy`.
- Eight egress-queue class maps and one output policy are generated the first time any auto-QoS command is used; later commands reuse them. In the guide's example output the priority queue matches DSCP cs4, cs5 and ef (CoS 5) with 30% priority; other queues get bandwidth-remaining shares.
- It attaches the policies and sets the interface trust level. Existing user configuration can make generated commands fail or be overridden without warning; if the generated commands cannot all be applied, the previous running configuration is restored.

## Restrictions and traps
- Not supported on SVI interfaces.
- Do not use `auto qos voip cisco-phone` for IP phones that support video: video DSCP markings are overwritten and the packets land in class-default.
- Auto-QoS does not generate configuration when `auto qos voip cisco-phone` arrives from startup-config. Workarounds: enter it manually, or include in the startup template the interface commands (`trust device cisco-phone`, `auto qos voip cisco-phone`, and the input and output service-policy lines) plus the global class maps, policy maps and ACEs.
- There is one table-map for exceed and one for violate markdown per switch or stack; if a table-map already exists under the exceed action, the auto-QoS policy cannot be applied.

## Compact mode
`auto qos global compact` hides the generated global and interface configuration from `show running-config`; only the auto-QoS commands you entered are saved, and the rest is regenerated at reload. Do not edit generated commands (changes are overridden at reload). View hidden config with `show derived-config`, and the `AutoQos-` objects with `show policy-map`, `show class-map`, `show access-list`, `show table-map`. To disable compact mode, first remove auto-QoS from all interfaces, then `no auto qos global compact`.

## Removing it
`no auto qos ...` on a port (for example `no auto qos voip`) removes only that port's generated interface commands. When it is removed from the last port, auto-QoS counts as disabled but the global commands remain. For upgrades the guide's procedure is: record `show auto qos`, run `no auto qos` per interface, remove leftover policy maps, class maps, `AutoQos` ACLs and table maps (`policed-dscp` included), confirm with `show running-config | i autoQos` and `show auto qos`, `write memory`, reload on the new image and reapply.

## Verify
- `show auto qos [interface <id>]` lists the auto-QoS commands per interface.
- `show policy-map interface <id>` shows the attached input and output policies and priority-queue counters.
- `debug auto qos` is the troubleshooting command.

## Checked
Date: 2026-11-08
Read in full: the Catalyst 9300 17.9 "Configuring Auto-QoS" chapter (restrictions, overview, compact, configuration table, upgrade procedure, monitoring, troubleshooting, all example policy outputs).
Confirmed: every command and its stated purpose, policy and class-map names, eight egress queues, 30% priority queue in the examples, restrictions above, compact behaviour, removal behaviour.
Removed: the claim that non-Cisco phones should use LLDP-MED with DSCP trust (not in the guide), "may remain on some releases" wording, the pass/fail expectations for a phone versus a PC (not stated), and the second source (Cisco QoS SRND book, 404 now).
Method: documentation only; no commands were run.
