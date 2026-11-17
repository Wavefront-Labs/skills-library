---
id: computing-software.systems-network-administration.keepalived.vrrp-instance-basics
name: vrrp-instance-basics
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp-instance, state, priority, virtual-router-id, advert-int, interface]
level: practitioner
status: docs-checked
description: "Core vrrp_instance keywords: state MASTER or BACKUP, interface, virtual_router_id, priority and advert_int, with the case-study values 51-54, 150/100 and 1."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vrrp_instance basics

```
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 150
    advert_int 1
    ...
}
```
- `state`: MASTER or BACKUP, the instance state in standard use.
- `interface`: the NIC the instance runs on.
- `virtual_router_id`: the VRRP router id the instance belongs to (the case study uses 51, 52, 53, 54).
- `priority`: the instance priority in the VRRP router (150 on the MASTER and 100 on the BACKUP instances in the case study).
- `advert_int`: advertisement interval in seconds; the synopsis shows 1.
- `mcast_src_ip`: source IP for advertisement IP headers.
- `lvs_sync_daemon_interface`: interface for the LVS sync daemon.
- `smtp_alert`: send SMTP notification on MASTER transitions.

Verify: ip address on the intended master lists the VIPs, and the peer holds none of them.

## Checked

2026-11-04. Confirmed the keywords, the VRID, priority and advert_int values, mcast_src_ip, lvs_sync_daemon_interface and smtp_alert on the configuration synopsis page and the Failover case study page. Removed claims that the highest priority wins and that VRIDs must match and be unique, which the pages do not state.

Method: documentation only; no commands were run.
