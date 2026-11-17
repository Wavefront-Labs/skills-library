---
id: computing-software.cloud-infrastructure-engineering.linkerd.init-container-iptables-nft-mode
name: init-container-iptables-nft-mode
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, iptables, nftables, init-container, proxy-init]
level: advanced
status: docs-checked
description: "Choose legacy or nft iptables mode for linkerd-init to match what your node operating system supports."
sources:
  - https://linkerd.io/2.19/features/nft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The init container configures firewall rules in each injected pod, and runs in one of two modes, set at install or upgrade time and shared by all injected workloads including the control plane:

- `legacy` (default): calls `iptables-legacy`, supported by most operating systems and distributions.
- `nft`: calls `iptables-nft`, which uses the newer `nf_tables` kernel API. Rule additions and deletions are atomic.

Both use the same packet matching syntax, so choose the mode your hosts support best. Some operating systems, such as Google Container Optimized OS, lack out-of-the-box nftables modules. Others, such as the RHEL family, do not support legacy iptables. Use `nft` only if the nodes include the nftables modules.

Set it at install:

```bash
linkerd install --set "proxyInit.iptablesMode=nft" | kubectl apply -f -
```

The same Helm value applies at upgrade time. Because operations in nft mode are atomic and rulesets are only appended rather than reloaded, the init container's `-w` wait option behaves differently from legacy mode, so read the feature page's wait-option note before tuning it.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/nft/.

Removed or reworded: Troubleshooting sentence not on the page.

Method: documentation only; no commands were run.
