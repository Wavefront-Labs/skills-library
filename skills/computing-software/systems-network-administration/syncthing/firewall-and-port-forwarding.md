---
id: computing-software.systems-network-administration.syncthing.firewall-and-port-forwarding
name: firewall-and-port-forwarding
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, firewall, port-forwarding, port-22000]
level: practitioner
status: docs-checked
description: "Open the right ports for Syncthing (22000 TCP and UDP, 21027 UDP), use ufw or firewalld presets and check for direct connections."
sources: ["https://docs.syncthing.net/users/firewall.html", "https://docs.syncthing.net/users/faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall and port forwarding

## Ports
- `22000/TCP` carries the TCP sync protocol.
- `22000/UDP` carries QUIC sync traffic.
- `21027/UDP` is for discovery broadcasts on IPv4 and multicasts on IPv6.

Open them for incoming and outgoing traffic. If you configured a custom port in the Sync Protocol Listen Address setting, adapt the firewall rules accordingly.

## Router
If the router supports UPnP, enable it on both the router and Syncthing; on success a console message reads `Created UPnP port mapping for external port XXXXX on UPnP device YYYYY.` Otherwise forward 22000/TCP and 22000/UDP (or the port set in the Sync Protocol Listen Address); the external and internal ports have to be the same. Because communication works both ways, a port forward on one device lets other devices connect to it even from behind a NAT or firewall. Without forwarding, relaying may work but performs poorly compared with a direct connection.

Local discovery needs the router to allow broadcasts and multicasts, usually allowed within one subnet but possibly blocked between subnets or between bridged Wi-Fi and LAN. If that cannot be fixed and devices have static IPs, change the Addresses setting from the default dynamic to something like `tcp://192.168.1.xxx:22000, dynamic`.

## Host firewalls
```sh
sudo ufw allow syncthing
sudo ufw allow syncthing-gui   # only if the GUI must be reachable
sudo firewall-cmd --zone=public --add-service=syncthing --permanent
sudo firewall-cmd --reload
```

## Check
In the Remote Devices list, the Connection Type should not start with `Relay`. A relay connection means a direct connection could not be established. On Windows, a network profile of Public (the default for new networks) commonly prevents Syncthing from making direct connections and forces a relay; the FAQ points to the Microsoft instructions for changing it to Private.

## Checked
2026-11-04. Read Firewall Setup and the FAQ entries on relays and Windows: ports and protocols, UPnP message, forwarding rules, local discovery caveat, static address form, ufw and firewalld commands, relay check and the Windows profile cause. Reworded the router and Windows paragraphs to what the pages say.
Method: documentation only; no commands were run.
