---
id: computing-software.systems-network-administration.backup-and-recovery.backup-network-and-bandwidth-design
name: backup-network-and-bandwidth-design
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-network, bandwidth-planning, throughput, dedicated-vlan, wan-sizing, data-mover]
level: advanced
status: draft
description: "Design the backup network: dedicated VLANs or fabrics, throughput maths for windows and restores, WAN sizing for off-site copies, and keeping backup traffic off production."
sources:
  - https://bp.veeam.com/vbr/
  - https://www.cisa.gov/stopransomware/ransomware-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup network and bandwidth design

## Throughput maths
Required MB/s = data per window / window seconds. Example: 20 TB changed and full-synthetic work nightly is not typical; take 2 TB incremental in 6 hours = 2,000,000 MB / 21,600 s ≈ 93 MB/s average, plan 2-3x for peaks. Restores are the harder target: RTO for a 5 TB system at 4 hours needs about 350 MB/s end to end.
1 GbE ≈ 110 MB/s real; 10 GbE ≈ 1 GB/s; 25 GbE ≈ 2.5-2.8 GB/s.

## LAN design
- Dedicated backup VLAN or physical network between proxies, repositories and gateways; jumbo frames only if end-to-end.
- Storage-side paths: Direct SAN/NFS proxies read from storage fabric, avoiding host management networks.
- NBD transport uses ESXi management vmkernel; if NBD is unavoidable, put management on 10 GbE.
- Isolate the backup network: only backup components and needed sources; firewall rules from production limited to data mover ports.

## WAN design (off-site copies)
- Daily change × reduction ÷ copy window = required Mbps. Example: 500 GB/day after compression in 10 hours ≈ 111 Mbps.
- Initial seed by shipping disks or seeding at the target site.
- WAN acceleration helps below ~100 Mbps with repetitive data; above that, direct mode.
- Throttle during business hours, encrypt in transit.

## Security
Backup networks are a lateral-movement path: no management interfaces of backup servers on user VLANs; jump hosts with MFA for admins.

## Verify
Measure: job bottleneck stats show Network under 50% busy, a 1 TB test restore meets the calculated rate, and off-site copy RPO is met for a week.
