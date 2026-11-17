---
id: computing-software.systems-network-administration.headscale.policy-node-attributes
name: policy-node-attributes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, nodeattrs, magicdns-aaaa, randomize-client-port, nextdns]
level: advanced
status: docs-checked
description: "Node attributes Headscale supports in nodeAttrs: Taildrive, exit-node suggestion, NextDNS, magicdns-aaaa, disable-ipv4, random WireGuard port."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node attributes

```json
{
  "nodeAttrs": [
    {
      "target": ["*"],
      "attr": ["magicdns-aaaa"]
    }
  ]
}
```

(The docs' own example omits the comma after the target list; keep the comma.)

## Supported attributes

- `drive:access`, `drive:share`: Taildrive.
- `suggest-exit-node`, `suggest-exit-node-ui`: automatic exit node selection.
- `nextdns:<profile>`, `nextdns:no-device-info`: needs NextDNS as the global resolver in the config.
- `magicdns-aaaa`: respond to AAAA queries on the local MagicDNS resolver at 100.100.100.100.
- `disable-ipv4`: selectively disable IPv4 for specific nodes; may help work around CGNAT conflicts.
- `randomize-client-port`: random WireGuard port instead of the default 41641.
- `disable-captive-portal-detection`: disable automatic captive portal detection.
- `ssh-behavior-v1`: Tailscale SSH sessions on a Linux node without `su`, PAM or a login environment, so `ssh -tt` keeps job control but `~/.profile` is not read. Tailscale's control plane sets it on every node; Headscale leaves it off.

## Network-wide

```json
{ "randomizeClientPort": true }
```

Sets a random WireGuard port for the whole tailnet; node attributes are preferred for finer control.

## Finding more

Other key-only attributes exist. Find them in the client source: `grep -E ' Cap ' tailcfg/nodecap/nodecap.go`.

## Gotcha

Do not grant `https://tailscale.com/cap/data-plane-audit-logs` while `logtail.enabled` is false: a client with log submission disabled treats it as "the tailnet requires logging" and turns itself off, until the attribute is removed and `tailscale up` is run (logtail-privacy).

## Checked

2026-11-04. Confirmed against the Headscale policy page (node attributes list, footnote on key-only attributes, network-wide `randomizeClientPort`, the missing comma in the example) and the FAQ (data-plane-audit-logs warning). Only the attributes listed there are claimed.

Method: documentation only; no commands were run.
