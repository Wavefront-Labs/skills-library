---
id: computing-software.cloud-infrastructure-engineering.docker.macvlan-parent-interface-and-host-access
name: macvlan-parent-interface-and-host-access
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, macvlan, macvlan-parent, macvlan-host-access, vlan-8021q, lan-ip, promiscuous-mode, ip-range, aux-address, docker-network-create]
level: advanced
status: docs-checked
description: "Give containers real LAN addresses with macvlan: parent and 802.1q sub-interfaces, carving IP ranges away from DHCP, the host-to-container shim interface, and VM/Wi-Fi limits."
sources: ["https://docs.docker.com/engine/network/drivers/macvlan/", "https://docs.docker.com/reference/cli/docker/network/create/", "https://man7.org/linux/man-pages/man8/ip-link.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macvlan: parent interface and host access

**Goal:** a container appears on the physical LAN with its own MAC and IP (for legacy apps,
DHCP-less appliances, Pi-hole, home automation) and the host can still talk to it.

## Create the network
```bash
# LAN 192.168.1.0/24, router .1, DHCP pool .100-.199; give Docker .192/27 (.192-.223)
docker network create -d macvlan \
  --subnet 192.168.1.0/24 --gateway 192.168.1.1 \
  --ip-range 192.168.1.192/27 \
  --aux-address 'host-shim=192.168.1.223' \
  -o parent=eth0 lan

docker run -d --network lan --ip 192.168.1.200 --name pihole pihole/pihole
```
- Docker's IPAM assigns addresses itself; it does **not** use DHCP. Keep `--ip-range` outside
  the router's DHCP pool or you will get duplicate IPs.
- `--aux-address` reserves an IP so Docker never hands it out (used for the shim below).
- `-o parent=` must be the real uplink (`ip route get 1.1.1.1` shows it).

## VLAN trunk (802.1q)
```bash
docker network create -d macvlan --subnet 10.50.0.0/24 --gateway 10.50.0.1 \
  -o parent=eth0.50 vlan50
```
A parent name with a dot (`eth0.50`) is treated as an 802.1Q sub-interface that Docker creates automatically. The switch
port must be a trunk carrying VLAN 50.

## The host cannot reach its own macvlan containers
By design, the kernel does not switch traffic between a parent interface and its macvlan
children. Fix with a macvlan "shim" on the host:
```bash
sudo ip link add mac-shim link eth0 type macvlan mode bridge
sudo ip addr add 192.168.1.223/32 dev mac-shim
sudo ip link set mac-shim up
sudo ip route add 192.168.1.192/27 dev mac-shim
```
Persist it with systemd-networkd/NetworkManager or a oneshot unit; it disappears on reboot.
Other LAN machines reach the containers without any of this.

## Where macvlan does not work
- **Equipment that cannot handle multiple MACs**: the network equipment must tolerate promiscuous mode (one interface with many MAC addresses); a switch port limited to one MAC blocks extra containers, and a large number of MACs can cause "VLAN spread". ipvlan L2 shares the parent's MAC.
- **Most cloud providers** block macvlan networking.
- **Docker Desktop (Mac/Windows) and Docker Engine on Windows**: not supported. Rootless mode is not supported either.
- Requires Linux kernel 3.9 or later (4.0+ recommended).

## Compose
```yaml
networks:
  lan:
    external: true      # create once with the command above
services:
  pihole:
    networks:
      lan: { ipv4_address: 192.168.1.200 }
```

## Verify
```bash
docker exec pihole ip addr show eth0          # 192.168.1.200 with its own MAC
ping -c1 192.168.1.200                        # from the host: works only with the shim
arp -n | grep 192.168.1.200                   # from another LAN host: container's MAC
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the macvlan driver page (platform support and requirements, considerations, `macvlan_mode` and `parent` options, `--ip-range`/`--aux-address`, automatic 802.1Q sub-interface creation, host-to-container restriction and the host macvlan-interface workaround, ipvlan L2 as the single-MAC alternative). Removed hypervisor-specific settings, the Wi-Fi access-point claim and the sub-interface deletion claim, which the page does not cover.

Method: documentation only; no commands were run.
