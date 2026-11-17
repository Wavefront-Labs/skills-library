---
id: computing-software.cloud-infrastructure-engineering.google-cloud.packet-capture-with-tcpdump-on-vms
name: packet-capture-with-tcpdump-on-vms
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-observability, vm-packet-capture, tcpdump, wireshark, mtu, tls-handshake-debugging]
level: practitioner
status: docs-checked
description: "Capture and read packets on Compute Engine VMs and GKE nodes with tcpdump: filters, rotating captures to GCS, MTU and TLS patterns, and when to mirror instead."
sources: ["https://www.tcpdump.org/manpages/tcpdump.1.html", "https://cloud.google.com/vpc/docs/mtu", "https://cloud.google.com/vpc/docs/packet-mirroring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet capture with tcpdump on VMs

## Capture
```bash
ip -br link                      # list interface names; capture on the primary NIC
sudo tcpdump -i ens4 -nn -s 0 -w /tmp/cap.pcap 'host <PEER_IP> and tcp port 5432'
# rotating, bounded capture for intermittent issues
sudo tcpdump -i ens4 -nn -s 256 -C 100 -W 10 -w /var/tmp/cap.pcap 'port 443'
gcloud storage cp /var/tmp/cap.pcap* gs://netdebug-<P>/$(hostname)/
```
`-s 256` truncates each packet to 256 bytes (the default snaplen is 262144); `-C 100 -W 10` rotates files (`-C` size, `-W` file count; see the tcpdump man page).

## GKE
- Node-level: `gcloud compute ssh <node>`, then run tcpdump on the node.
- Pod-level: ephemeral debug container sharing the pod network namespace:
  `kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container> -- tcpdump -i eth0 -nn port 8080`.

## Reading common problems
| Pattern | Likely cause |
|---|---|
| SYN, no SYN-ACK | firewall/implied deny, wrong route, NAT port exhaustion |
| SYN-ACK then RST | nothing listening / LB health issue |
| Large packets retransmitted, small fine | MTU mismatch (VPC default MTU is 1,460 bytes, configurable 1,300-8,896; Cloud VPN has its own MTU) -> check MSS clamping |
| ClientHello then RST/alert | TLS version/cipher or SNI mismatch |
| Many retransmissions after idle | middlebox or NAT idle timeout |

Filter in Wireshark: `tcp.analysis.retransmission`, `tls.handshake.type == 1`, `icmp.type == 3 && icmp.code == 4` (fragmentation needed).

## When not tcpdump
Packet Mirroring for out-of-band capture of many VMs or IDS feeds; VPC Flow Logs for flow-level
metadata at scale.

## Gotchas
- Captures may contain sensitive data: limit snap length, store in a restricted bucket with lifecycle delete.

## Verify
- [ ] Capture shows the handshake for a reproduced failure; root cause matches one of the patterns.

## Checked
2026-10-28. Confirmed: tcpdump man page (`-s snaplen` default 262144, `-C file_size`, `-W filecount`, `-w`); VPC MTU page (default 1,460 bytes, range 1,300-8,896, Cloud VPN has separate MTU and MSS clamping applies); Packet Mirroring page cited for out-of-band capture.
Removed: interface naming (ens4/gVNIC), `toolbox` on COS, Autopilot SSH claim, Cloud NAT timeout name, same-host traffic claim, "no payload exposure" wording.
Method: documentation only; no commands were run.
