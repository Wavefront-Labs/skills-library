---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-l2-arping
name: troubleshoot-l2-arping
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, arping, tcpdump, layer2, mac-spoofing, wifi, promiscuous, raspberry-pi, troubleshooting]
level: practitioner
status: docs-checked
description: "Verify MetalLB L2 announcements with arping and tcpdump, interpret multiple MACs or no replies, and the WiFi/Raspberry Pi promiscuous-mode workaround."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting L2 with arping and tcpdump

Prerequisite: an `L2Advertisement` exists.

From a host on the same L2 subnet:
```bash
arping -I ens3 192.168.1.240
```
The reply MAC is the one MetalLB announces. By design MetalLB answers with the MAC of the interface that received the ARP request.

On the node:
```bash
tcpdump -n -i ens3 arp src host 192.168.1.240
```
You should see `ARP, Reply 192.168.1.240 is-at <mac>`. The speaker also logs (debug) `got ARP request for service IP, sending response`.

No replies: ARP may be blocked; anti-MAC-spoofing is a common cause. Run tcpdump on the node hosting the elected speaker to see whether requests arrive and replies leave.

Multiple MACs for one IP:
- several speakers answering (split brain, check speaker logs, `computing-software.cloud-infrastructure-engineering.metallb.l2-leader-election`),
- the IP is also bound to another interface on the segment,
- the CNI answers ARP for the LB IP.

Interface selector with no matching interface on the elected node: an event appears on the Service (`kubectl describe svc`).

WiFi (for example Raspberry Pi): some devices do not answer ARP on WiFi, so the service works briefly then stops (arping times out). Workaround: `sudo ifconfig wlan0 promisc` (substitute your device).

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page, "Checking the L2 advertisement works": arping and tcpdump commands, MAC-of-receiving-interface behaviour, debug log text, multiple-MAC causes, interface-selector event, WiFi workaround.
Method: documentation only; no commands were run.
