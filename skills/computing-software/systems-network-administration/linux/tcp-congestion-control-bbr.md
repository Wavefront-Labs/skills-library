---
id: computing-software.systems-network-administration.linux.tcp-congestion-control-bbr
name: tcp-congestion-control-bbr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysctl, tcp-bbr, congestion-control, tcp-congestion-control, fq-qdisc, cubic, network-tuning, throughput]
level: advanced
status: docs-checked
description: "Switch and verify TCP congestion control (cubic vs BBR): available algorithms, fq qdisc pairing, per-route congestion control, testing with iperf3 and ss -ti."
sources:
  - https://docs.kernel.org/networking/ip-sysctl.html
  - https://github.com/google/bbr/blob/master/Documentation/bbr-quick-start.md
  - https://man7.org/linux/man-pages/man8/ip-route.8.html
  - https://docs.kernel.org/networking/ip-sysctl.html
  - https://docs.kernel.org/admin-guide/sysctl/net.html
  - https://github.com/iproute2/iproute2/blob/main/man/man8/ip-route.8.in
  - https://github.com/esnet/iperf/blob/master/src/iperf3.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP congestion control and BBR

**When it helps:** candidate paths are high-bandwidth, high-latency, slightly lossy links (WAN, backups across
regions); measure to confirm, since the benefit depends on the path.

## Check and switch
```bash
sysctl net.ipv4.tcp_available_congestion_control     # algorithms available now
sysctl net.ipv4.tcp_congestion_control               # default for new connections ("reno" is always available)
modprobe tcp_bbr
cat >/etc/sysctl.d/60-bbr.conf <<'EOF'
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF
sysctl --system
echo tcp_bbr > /etc/modules-load.d/bbr.conf   # load the module at boot
```
- `net.core.default_qdisc` sets the default queuing discipline for network devices (the kernel default is pfifo_fast unless overridden); check the BBR documentation for your kernel for any qdisc requirement.
- `tcp_congestion_control` applies to **new** connections.

## Per-route
`ip route change default via 192.0.2.1 dev eth0 congctl bbr` — `congctl NAME` is a documented per-route attribute, so one path can use a different algorithm.

## Measure, don't assume
```bash
ss -tin dst 198.51.100.7      # per-connection TCP details, including the algorithm in use
iperf3 -c host -t 30 -C cubic ; iperf3 -c host -t 30 -C bbr      # -C/--congestion picks the algorithm per test (Linux and FreeBSD)
```

## Gotchas
- Test on the real path before a fleet-wide rollout.
- Also check buffers (`tcp_rmem/tcp_wmem`) — congestion control can't fix a window too small for the BDP.

## Verify
- [ ] `ss -ti` on new connections shows `bbr`; throughput/latency improvement measured on the real path.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (networking/ip-sysctl, admin-guide/sysctl/net), the iproute2 `ip-route(8)` source and the iperf3 man page source on 2026-10-26. Confirmed: `tcp_congestion_control` (new connections, reno always available), `tcp_available_congestion_control`, `net.core.default_qdisc` (default pfifo_fast unless overridden), `ip route ... congctl NAME`, iperf3 `-C/--congestion`. Removed: the kernel-4.13 fq claim, `tc qdisc replace`, BBR fairness and container claims, cubic-versus-BBR behaviour statements, and the claim that only the sender matters.

Method: documentation only; no commands were run.
