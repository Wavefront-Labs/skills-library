---
id: computing-software.systems-network-administration.jellyfin.firewall-and-port-forwarding
name: firewall-and-port-forwarding
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, firewall, port-forwarding, nat, ufw, firewalld, docker]
level: practitioner
status: docs-checked
description: "Open Jellyfin ports at the right firewall layer and understand port forwarding versus opening a port."
sources: ["https://jellyfin.org/docs/general/post-install/networking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Firewalls and port forwarding

Firewalls block incoming traffic between networks. To reach Jellyfin across one, open or forward its ports; but opening a port gives full access to that port to the next higher network, so opening Jellyfin directly to the internet is insecure and not recommended.

**Layers where a firewall can sit**

| Layer | Example | Open ports here to |
| --- | --- | --- |
| Local | Docker, VM | let traffic from the host enter the application |
| Host | physical machine, OS | let traffic from the network enter the host |
| Network | router | let traffic from the internet enter the local network |

**Forward versus open.** Routers usually forward a port; firewalls open one. Opening just lets traffic on that port through. Forwarding is the NAT case: traffic arrives on your public IP and the rule names which internal device receives it; some routers also map an external port to a different internal port.

How to open a port depends on the firewall: the docs link guides for Windows Firewall, firewalld, Uncomplicated Firewall (ufw) and nftables.

Check by testing each layer from the side that should be allowed and the side that should not.

## Checked

2026-11-08. Confirmed against the Jellyfin Networking page: firewall layers table, port forwarding versus opening a port, insecurity of opening ports directly to the internet, the linked firewall guides. Removed: the typical-result paragraph, which is the author's own recommendation and not in the page. Page read in full.

Method: documentation only; no commands were run.
