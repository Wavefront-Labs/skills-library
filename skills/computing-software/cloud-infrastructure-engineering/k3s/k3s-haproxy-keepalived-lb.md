---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-haproxy-keepalived-lb
name: k3s-haproxy-keepalived-lb
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, haproxy, keepalived, virtual-ip]
level: advanced
status: docs-checked
description: "Front K3s servers with a redundant HAProxy pair and a KeepAlived virtual IP on port 6443."
sources:
  - https://docs.k3s.io/datastore/cluster-loadbalancer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a highly available TCP load balancer for the K3s API and registration address. The docs example uses three servers, two LB nodes and a VIP; each server is configured in /etc/rancher/k3s/config.yaml with a token and `tls-san` set to the VIP.

Install: `sudo apt-get install haproxy keepalived`.

/etc/haproxy/haproxy.cfg on both LB nodes:

```
frontend k3s-frontend
    bind *:6443
    mode tcp
    option tcplog
    default_backend k3s-backend
backend k3s-backend
    mode tcp
    option tcp-check
    balance roundrobin
    default-server inter 10s downinter 5s
    server server-1 10.10.10.50:6443 check
```

(add one `server` line per K3s server).

/etc/keepalived/keepalived.conf defines a vrrp_script chk_haproxy (`killall -0 haproxy`, interval 2) and a vrrp_instance with virtual_router_id 51, the VIP under virtual_ipaddress, state MASTER with priority 200 on lb-1 and BACKUP with priority 100 on lb-2, and track_script chk_haproxy.

Restart: `systemctl restart haproxy` and `systemctl restart keepalived` on both nodes.

Agents join through the VIP:

```
curl -sfL https://get.k3s.io | K3S_TOKEN=lb-cluster-gd sh -s - agent --server https://10.10.10.100:6443
```

This is distinct from the embedded ServiceLB, which serves LoadBalancer Services.

## Checked

2026-11-03: read docs.k3s.io datastore/cluster-loadbalancer. Confirmed: the three-server/two-LB/VIP layout, haproxy.cfg frontend and backend settings, keepalived vrrp_script and vrrp_instance values, and the agent join through the VIP.

Method: documentation only; no commands were run.
