---
id: computing-software.cloud-infrastructure-engineering.talos-linux.wireguard-link-config
name: wireguard-link-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [wireguard, wireguardconfig, overlay, keys, networking, peers]
level: advanced
status: docs-checked
description: "Hand-configure a WireGuard interface with WireguardConfig: key generation, overlay addresses, peers and endpoints, plus when to use KubeSpan instead."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/advanced/wireguard.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a manual WireGuard mesh, generate a key pair on each machine:

```bash
wg genkey | tee privatekey | wg pubkey > publickey
```

Choose overlay addresses that do not conflict with existing networks, for example `10.0.0.0/24`, then apply a `WireguardConfig` document to each machine:

```yaml
apiVersion: v1alpha1
kind: WireguardConfig
name: wg.int
privateKey: GA1E1VB+g41Dl0+UH2TMW9C5953y+moVg6JIIqkJbmw= # private key of this machine
listenPort: 5042 # optional
peers:
    - publicKey: 735jkJdcVDninU5PzLJ/S+bfN6Q3QOk6svWrVLMJQAk= # public key of another machine
      allowedIPs:
        - 10.0.0.2/32 # overlay address of another machine
      endpoint: 192.168.1.2:5042 # endpoint to connect to, only one of the peers needs to specify this
    - publicKey: uvdlJNva1X8/OCOZM+0gGT4Yu9x20odd3AWbbQUF7nM= # public key of yet another machine
      allowedIPs:
        - 10.0.0.3/32 # overlay address of yet another machine
up: true
addresses:
    - address: 10.0.0.1/32 # overlay address of this machine
```

This creates interface `wg.int` with overlay address `10.0.0.1/32`. Applied on every machine with its own key, address and peer list, the machines reach each other over the overlay.

Only one side of a peer pair needs an `endpoint`. Routing of specific networks over the interface is not automatic: you must add routes yourself. If you want Talos to build and maintain a WireGuard mesh across the whole cluster automatically, use KubeSpan instead.

## Checked

Key generation command, WireguardConfig YAML, endpoint note, routing and KubeSpan remarks confirmed on the Wireguard page.

Method: docs-checked 2026-11-09 against the raw Wireguard page (v1.15 folder), read in full.
