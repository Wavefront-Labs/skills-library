---
id: computing-software.networking-hardware-and-wireless.squid.tproxy-v4
name: tproxy-v4
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, tproxy, linux-netfilter, policy-routing, iptables]
level: sme
status: docs-checked
description: "Run fully transparent TPROXY v4 interception on Linux: kernel and iptables needs, routing, and a dedicated tproxy port."
sources:
  - https://wiki.squid-cache.org/Features/Tproxy4
  - https://www.squid-cache.org/Doc/config/http_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TPROXY v4
Requirements: Linux 2.6.37+ with NF_CONNTRACK, NETFILTER_TPROXY, NETFILTER_XT_MATCH_SOCKET and NETFILTER_XT_TARGET_TPROXY; iptables 1.4.10+; Squid 3.1+; libcap 2.09+. Build with `--enable-linux-netfilter`.
```
http_port 3128
http_port 3129 tproxy
```
```
ip -f inet rule add fwmark 1 lookup 100
ip -f inet route add local default dev eth0 table 100
iptables -t mangle -N DIVERT
iptables -t mangle -A DIVERT -j MARK --set-mark 1
iptables -t mangle -A DIVERT -j ACCEPT
iptables -t mangle -A PREROUTING -p tcp -m socket -j DIVERT
iptables -t mangle -A PREROUTING -p tcp --dport 80 -j TPROXY --tproxy-mark 0x1/0x1 --on-port 3129
```
Also enable ip_forward and set rp_filter to 0.

Caveats: the tproxy port must be dedicated (no intercept or accel); DIVERT before TPROXY; routing-only setups need exemptions for Squid's own traffic; with WCCPv2 use src_ip_hash on service 80 and dst_ip_hash on service 90; on SELinux enable squid_connect_any and squid_use_tproxy.

## Checked

2026-11-04. Read the Squid wiki Features/Tproxy4 page and confirmed the minimum versions, kernel options, dedicated tproxy port, routing and iptables DIVERT/TPROXY rules, rp_filter and ip_forward settings, SELinux booleans and WCCPv2 hash advice. Nothing was removed.

Method: documentation only; no commands were run.
