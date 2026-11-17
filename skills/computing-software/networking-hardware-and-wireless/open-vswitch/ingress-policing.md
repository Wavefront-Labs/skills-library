---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ingress-policing
name: ingress-policing
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ingress-policing, policing-rate, qos, rate-limit, burst]
level: intro
status: docs-checked
description: "Rate-limit traffic a VM sends into Open vSwitch with ingress_policing_rate and ingress_policing_burst (kbps and kb), with sizing rules for TCP and UDP."
sources:
  - https://docs.openvswitch.org/en/latest/howto/qos/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ingress policing
Set on the Interface of the VM's port:
```
ovs-vsctl set interface tap0 ingress_policing_rate=1000
ovs-vsctl set interface tap0 ingress_policing_burst=100
```
- `ingress_policing_rate` is in kbps (1000 = 1 Mbps); default 0 disables.
- `ingress_policing_burst` is in kb; when 0, 8000 kbit is used.
- Packet-rate variants: `ingress_policing_kpkts_rate` and `ingress_policing_kpkts_burst` (default burst 16 kpkts when 0).

Verify: `ovs-vsctl list interface tap0` shows current limits; run `netperf -H <ip>` from the VM and compare to the rate.
Clear: `ovs-vsctl set interface tap0 ingress_policing_rate=0`.

Sizing and caveats:
- Policing drops packets over the rate; it does not queue.
- Avoid burst below the MTU.
- For TCP, a burst above about 10% of the rate helps a flow reach the full rate (the database reference says a value at least 80% of the rate helps); a very large burst can push the average slightly above the policed rate.
- For UDP, set burst slightly above the MTU and keep packets within the MTU (e.g. `netperf -t UDP_STREAM -- -m 1000`).
- Linux implements this with traffic control: if limits have no effect, check the kernel has the ingress qdisc and that `/sbin/tc` is installed.

## Checked

2026-11-09. Confirmed against the Quality of Service (QoS) Rate Limiting how-to and the Interface table of ovs-vswitchd.conf.db(5): rate in kbps and burst in kb, default 0 disables, default burst 8000 kbit when 0, kpkts variants and the 16 kpkts default, list interface, netperf test commands, policing drops rather than queues, MTU and TCP and UDP burst advice, ingress qdisc and tc requirement. Nothing removed.
Method: documentation only; no commands were run.
