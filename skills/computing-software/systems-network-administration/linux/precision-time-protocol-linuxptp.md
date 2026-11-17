---
id: computing-software.systems-network-administration.linux.precision-time-protocol-linuxptp
name: precision-time-protocol-linuxptp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ptp4l, linuxptp, phc2sys, ptp, hardware-timestamping, pmc]
level: practitioner
status: docs-checked
description: "Run Precision Time Protocol on Linux with linuxptp: check NIC timestamping, ptp4l profiles, phc2sys to the system clock, chrony PHC refclock, and monitoring offset with pmc."
sources:
  - https://github.com/richardcochran/linuxptp
  - https://github.com/mlichvar/chrony/blob/master/doc/chrony.conf.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Precision Time Protocol with linuxptp

**Goal:** sub-microsecond clock sync (trading, telecom, broadcast, industrial) where NTP's milliseconds aren't enough.

## Check hardware
```bash
ethtool -T ens1f0
#  hardware-transmit / hardware-receive / hardware-raw-clock  -> hardware timestamping
#  PTP Hardware Clock: 0                                      -> /dev/ptp0
```
No PHC means software timestamping only (`-S` in ptp4l(8)), which is less accurate. Network switches that are PTP-aware (boundary or transparent clocks) give the best results.

## ptp4l (sync the NIC's PHC to the grandmaster)
```bash
# install the distribution's linuxptp package
ptp4l -i ens1f0 -m                          # defaults: E2E delay, UDPv4, hardware timestamping; role chosen by the best master clock algorithm
ptp4l -i ens1f0 -s -m -f /etc/ptp4l.conf    # -s: clientOnly mode
```
```ini
# /etc/ptp4l.conf (excerpt)
[global]
domainNumber        0           # must match the grandmaster's domain
clientOnly          1
network_transport   L2          # default is UDPv4
delay_mechanism     E2E         # P2P for peer-delay networks
time_stamping       hardware
```
Watch the log lines for the master offset and servo state; see ptp4l(8) for their meaning.

## phc2sys (copy PHC to the system clock)
```bash
phc2sys -s ens1f0 -c CLOCK_REALTIME -w -m    # -w waits for ptp4l; handles UTC/TAI offset
phc2sys -a -r                                # automatic mode from ptp4l state
```
Alternative: let chrony read the PHC and stop phc2sys:
```
refclock PHC /dev/ptp0 poll 0 dpoll -2 tai
```
Never run chronyd/ntpd steering CLOCK_REALTIME **and** phc2sys at the same time.

## Systemd units
Distribution packages ship their own service units and option files for ptp4l and phc2sys; check your distribution's documentation.

## Monitor
```bash
pmc -u -b 0 'GET CURRENT_DATA_SET'     # offset from master and path delay
pmc -u -b 0 'GET TIME_STATUS_NP'       # grandmaster status
pmc -u -b 0 'GET PARENT_DATA_SET'
```
Export these with a pmc-based script and alert on loss of the grandmaster or a large offset.

## Pitfalls
- UTC/TAI offset errors: PTP time scale is shifted from UTC by tens of seconds; phc2sys `-w` waits for ptp4l and tracks the offset, and `-O` sets it by hand.
- Firewalls must pass the PTP transport you chose (UDP multicast for UDPv4, or L2 frames).

## Verify
- [ ] ptp4l in `s2` with stable offset; `pmc` shows the expected grandmaster identity.
- [ ] `chronyc tracking` or phc2sys logs show system clock offset in ns range.

## Checked

Checked 2026-10-27 against linuxptp man pages (ptp4l(8), phc2sys(8), pmc(8)), configs/default.cfg and README (richardcochran/linuxptp master), chrony.conf documentation (chrony master), 2026-10-27. Confirmed: ptp4l options -i/-s/-S/-m/-f, config keys domainNumber, clientOnly, network_transport, delay_mechanism, time_stamping and their defaults, phc2sys -s/-c/-w/-m/-a/-r/-O, chrony refclock PHC syntax with tai and dpoll, pmc -u -b and the CURRENT_DATA_SET, PARENT_DATA_SET and TIME_STATUS_NP commands. Removed or softened: accuracy figures, servo-state meaning, systemd unit file names, UDP port numbers, node_exporter remark, ptp_kvm remark, 37-second figure.

Method: documentation only; no commands were run.
