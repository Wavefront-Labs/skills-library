---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ipsec-tunnels
name: ipsec-tunnels
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ipsec, psk, ovs-monitor-ipsec, remote-cert, remote-name, ipsec-skb-mark, gre, geneve, vxlan]
level: advanced
status: docs-checked
description: "Encrypt Open vSwitch GRE, Geneve and VXLAN tunnels with IPsec: PSK, self-signed and CA-signed authentication, ovs-monitor-ipsec troubleshooting, and plaintext leak control."
sources:
  - https://docs.openvswitch.org/en/latest/tutorials/ipsec/
  - https://docs.openvswitch.org/en/latest/howto/ipsec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipsec tunnels
Install: Ubuntu 22.04 `apt-get install openvswitch-ipsec`; Fedora `dnf install python3-openvswitch libreswan openvswitch openvswitch-ipsec`, then `systemctl start openvswitch-ipsec.service` and open the firewall with `firewall-cmd --add-service ipsec`.

Authentication (pick one; do not mix PSK with certificate options):
- PSK: `ovs-vsctl add-port br-ipsec tun -- set interface tun type=gre options:remote_ip=$ip_2 options:psk=swordfish`
- Self-signed: set `options:remote_cert=/etc/keys/host_2-cert.pem` instead.
- CA-signed: `options:remote_name=host_2` (certificate CN).
- Local certs: `ovs-vsctl set Open_vSwitch . other_config:certificate=/etc/keys/host_1-cert.pem other_config:private_key=/etc/keys/host_1-privkey.pem`, plus `other_config:ca_cert=/etc/keys/cacert.pem` for CA-signed.
- Optional `options:local_ip=$ip_1`; custom connection options are `options:ipsec_*` (e.g. `options:ipsec_encapsulation=yes`).

Certificates need x.509 v3 with subjectAltName DNS; `ovs-pki` before OVS 2.10.90 did not make v3.

Plaintext control (Open_vSwitch other_config): `ipsec_skb_mark=0/1` drops unencrypted tunnel packets but affects all OVS tunnels; `1/1` passes them unless OpenFlow rules block a non-zero skb_mark. Default may send plaintext before negotiation completes.

Verify and debug:
- `ovs-appctl -t ovs-monitor-ipsec tunnels/show` (state should be CONFIGURED); `... refresh`.
- `tcpdump -ni any net $ip_2` should show ESP.
- Log: `/var/log/openvswitch/ovs-monitor-ipsec.log`.

## Checked

2026-11-09. Confirmed against the OVS IPsec Tutorial and Encrypt Open vSwitch Tunnels with IPsec pages: Ubuntu and Fedora install commands, firewall-cmd, the three authentication methods and commands, local_ip, ipsec_* custom options, x.509 v3 and the 2.10.90 ovs-pki note, ipsec_skb_mark 0/1 and 1/1 behaviour, tunnels/show, refresh, tcpdump ESP check, log path. Nothing removed.
Method: documentation only; no commands were run.
