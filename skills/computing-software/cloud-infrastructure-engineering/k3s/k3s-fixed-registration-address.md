---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-fixed-registration-address
name: k3s-fixed-registration-address
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, tls-san, registration-address, load-balancer]
level: practitioner
status: docs-checked
description: "Give agents and kubectl a stable registration endpoint in front of K3s servers using --tls-san."
sources:
  - https://docs.k3s.io/datastore/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid depending on one server IP when nodes come and go (for example cloud scaling groups).

Put a stable endpoint in front of the servers. The docs list: a layer-4 (TCP) load balancer, round-robin DNS, or virtual/elastic IP addresses.

The endpoint can also serve Kubernetes API access, so you may point your kubeconfig at it instead of a node.

To avoid certificate errors, start servers with:

```
--tls-san=YOUR_IP_OR_HOSTNAME_HERE
```

This adds a hostname or IP as a Subject Alternative Name in the TLS certificate. Repeat the option to cover both an IP and a hostname.

Agents then register against the endpoint:

```
K3S_TOKEN=SECRET k3s agent --server https://server-or-fixed-registration-address:6443
```

## Checked

2026-11-08: read the whole High Availability External DB page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/datastore/ha). Confirmed the endpoint options, kubeconfig use, --tls-san behaviour and the agent join command. Removed unsupported claims: the config.yaml list form and the stale-SAN recovery steps (stop K3s, k3s certificate rotate, kubectl check) are not on this page.

Method: documentation only; no commands were run.
