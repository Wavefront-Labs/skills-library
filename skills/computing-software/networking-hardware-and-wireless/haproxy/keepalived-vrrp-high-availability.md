---
id: computing-software.networking-hardware-and-wireless.haproxy.keepalived-vrrp-high-availability
name: keepalived-vrrp-high-availability
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, keepalived, vrrp, floating-ip, ip-nonlocal-bind, haproxy-ha]
level: practitioner
status: docs-checked
description: "Build an active-passive HAProxy pair with keepalived VRRP, a floating IP, a non-local bind and notify hooks."
sources:
  - https://docs.haproxy.org/3.0/intro.html
  - https://docs.haproxy.org/3.0/configuration.html
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keepalived vrrp high availability
HAProxy itself does not manage a floating IP. Its introduction recommends a standard VRRP daemon such as keepalived: HAProxy copes well with floating virtual IPs, and IP redundancy protocols (VRRP/CARP) are preferred over cluster-based solutions (Heartbeat and similar) for the fastest, most seamless and most reliable switchover.

Skeleton for the primary node, using keywords from the keepalived configuration synopsis:
```
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass <SECRET>
    }
    virtual_ipaddress {
        192.0.2.100/24
    }
}
```
- `state` is `MASTER` or `BACKUP`; the peer uses `state BACKUP` and a lower `priority`.
- `virtual_router_id` identifies the VRRP router the instance belongs to; both nodes must match and it must not clash with other VRRP groups on the segment.
- `advert_int` is the advertisement interval in seconds (the synopsis says "set to 1").
- `auth_type` is `PASS` or `AH`; `auth_pass` is a string.
- The `virtual_ipaddress` block is limited to 20 addresses; `virtual_ipaddress_excluded` is unlimited and holds addresses that are not protocol VIPs.
- `notify_master`, `notify_backup` and `notify_fault` run a script on transition to that state.

The backup node does not own the VIP, so HAProxy there must still be able to bind to it. The `bind` option `transparent` (supported only on certain Linux kernels) binds addresses even if they do not belong to the local machine.

Not covered by the pages read: tying failover to the health of the haproxy process (track scripts), unicast peers, and kernel sysctls. Look these up in the current keepalived documentation before relying on them. Note the synopsis page read here is labelled for an old keepalived release.

Verify: the VIP appears on the master (`ip addr show`), and after stopping the master (or its HAProxy) the VIP moves to the backup and requests still succeed.

## Checked
2026-11-09. Confirmed against the HAProxy 3.0 introduction (keepalived and VRRP/CARP recommendation), the 3.0 configuration manual (`bind` option `transparent`) and the keepalived configuration synopsis (state, interface, virtual_router_id, priority, advert_int, authentication, auth_type PASS|AH, virtual_ipaddress limit of 20, notify_* scripts). Removed: vrrp_script and track_script, the pidof and curl health checks, ip_nonlocal_bind sysctl, freebind, unicast_peer, cloud-network claims, the 8-character auth_pass truncation, the 3 second failover figure, the split-brain claim.
Method: documentation only; no commands were run.
