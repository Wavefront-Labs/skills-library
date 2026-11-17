---
id: computing-software.cloud-infrastructure-engineering.docker.container-cannot-reach-the-internet
name: container-cannot-reach-the-internet
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, network-troubleshooting, no-internet-in-container, ip-forward, masquerade, dns-resolution-failure, mtu-mismatch]
level: practitioner
status: docs-checked
description: "Step-by-step checklist when containers have no outbound connectivity: DNS vs IP, ip_forward, NAT masquerade, firewall/ufw, internal networks, proxies, MTU and VPN routes."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/engine/daemon/troubleshoot/#networking", "https://docs.docker.com/engine/network/drivers/bridge/", "https://docs.docker.com/engine/cli/proxy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container cannot reach the internet

## 1. Split DNS from routing
```bash
docker run --rm busybox ping -c1 -W2 1.1.1.1          # IP works?
docker run --rm busybox nslookup example.com           # DNS works?
docker run --rm curlimages/curl -sI https://example.com | head -1
```
- IP fails: routing/NAT/firewall (steps 2-5).
- IP works, DNS fails: resolver config (see container DNS skills; host on 127.0.0.53, blocked
  public DNS, VPN split DNS).
- Both work, HTTPS hangs: MTU or proxy (steps 6-7).

## 2. Network type
```bash
docker network inspect <net> -f 'internal={{.Internal}}'
```
`--internal` networks have no egress by design.

## 3. Host forwarding
```bash
sysctl net.ipv4.ip_forward                 # must be 1
```
Something (sysctl.d files, cloud-init, hardening scripts) may reset it; Docker enables it on
start unless `"ip-forward": false`.

## 4. NAT
```bash
sudo iptables -t nat -S POSTROUTING | grep MASQUERADE
sudo nft list ruleset | grep -i masquerade
```
Missing: daemon started with `"iptables": false` or `"ip-masq": false` (default bridge), or the network has
`enable_ip_masquerade=false`.

## 5. Firewall
- `FORWARD` policy DROP (Docker sets it when it enables IP forwarding) with Docker's own accept rules missing, for example because of `"iptables": false` or mixed iptables backends.
- Cloud security groups/NACLs restricting egress from the host.
```bash
sudo iptables -S FORWARD; sudo iptables -S DOCKER-USER
```

## 6. Proxy
Corporate networks without direct egress: containers need `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`
(env or `~/.docker/config.json` `proxies`), plus the MITM CA if TLS is intercepted.

## 7. MTU
Small packets work, TLS handshakes hang: host uplink MTU below 1500 (VPN, some clouds).
```bash
docker run --rm busybox ping -c1 -M do -s 1472 1.1.1.1   # fails if path MTU < 1500
```
Set `"mtu": 1400` in daemon.json (default bridge) and `com.docker.network.driver.mtu` on user
networks.

## 8. VPN on the host
VPN clients can route the Docker subnet into the tunnel or block LAN/forwarded traffic. Check
`ip route get 1.1.1.1 from 172.17.0.2 iif docker0` and choose Docker subnets that do not
overlap VPN routes.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the packet-filtering page (IP forwarding enabled by Docker, FORWARD policy DROP, `iptables: false` effects), the bridge options table (`enable_ip_masquerade`, MTU), the `dockerd` reference (`ip-forward`, `ip-masq`, `mtu` for the default bridge), the CLI proxy page (`proxies` in `~/.docker/config.json`) and the daemon troubleshooting page. Removed unconfirmed claims: the exact warning text, firewall-reload behaviour, ufw `DEFAULT_FORWARD_POLICY` and the MASQUERADE rule listing.

Method: documentation only; no commands were run.
