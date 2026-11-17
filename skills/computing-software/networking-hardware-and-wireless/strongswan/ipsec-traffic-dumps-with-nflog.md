---
id: computing-software.networking-hardware-and-wireless.strongswan.ipsec-traffic-dumps-with-nflog
name: ipsec-traffic-dumps-with-nflog
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, traffic-dumps, nflog, tcpdump, wireshark, save-keys]
level: advanced
status: docs-checked
description: "Capture correct IPsec traffic on Linux with iptables NFLOG rules and tcpdump nflog interfaces, plus decrypting IKE and ESP in Wireshark using logged keys or the save-keys plugin."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/trafficDumps.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipsec traffic dumps with nflog
**Problem.** With default libpcap capture, tcpdump and Wireshark on a normal interface show encapsulated and decapsulated IPsec traffic only for inbound packets; outbound shows just the encrypted packets. This approach works only with kernel IPsec processing and captures outbound traffic before nat POSTROUTING. To check policy matches, read the CHILD_SA counters in `swanctl --list-sas`.

**Solution.** Use iptables NFLOG with a group number (0 to 65535) and read it as `tcpdump -s 0 -n -i nflog:5`; Wireshark lists the nflog group as an interface. Examples with group 5:

```
iptables -t raw -I PREROUTING -p esp -j NFLOG --nflog-group 5
iptables -t raw -I PREROUTING -p udp -m multiport --dports 500,4500 -j NFLOG --nflog-group 5
iptables -t mangle -I PREROUTING -m policy --pol ipsec --dir in -j NFLOG --nflog-group 5
iptables -t mangle -I POSTROUTING -m policy --pol ipsec --dir out -j NFLOG --nflog-group 5
```

The filter table INPUT (`-m addrtype --dst-type LOCAL`), FORWARD (`! --dst-type LOCAL`) and OUTPUT chains take similar rules. NFLOG is non-terminating.

**libipsec.** Listen on the tun interface for decapsulated traffic, or the peer-facing interface for IKE and ESP.

**Decrypting in Wireshark.** Raise the `ike` log level to 4 and find SKEYID or Ka (IKEv1) or Sk (IKEv2); ESP keys are logged at level 4 in `chd` or come from `ip xfrm state`. From 5.6.2 the save-keys plugin writes key files in Wireshark format.

## Checked
2026-11-04. Confirmed against the Taking Traffic Dumps on Linux page: the capture anomaly, NFLOG rules and group range, tcpdump syntax, libipsec note and key extraction.

Method: documentation only; no commands were run.
