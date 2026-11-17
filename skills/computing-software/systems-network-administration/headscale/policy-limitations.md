---
id: computing-software.systems-network-administration.headscale.policy-limitations
name: policy-limitations
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, postures, ip-sets, limitations, autogroup-self, policy-gaps]
level: advanced
status: docs-checked
description: "What Headscale policy does not support compared with Tailscale: postures, IP sets, some autogroups, OIDC groups, plus device visibility behaviour."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/features.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy limitations

## Not supported

- Device postures and related sections (`postures`, `srcPosture`).
- IP sets.
- Only a subset of autogroups is available (policy-autogroups).
- OIDC groups cannot be used in policy rules (the `groups` claim is only used to filter for allowed groups).

## Supported

ACLs, grants, auto approvers, Tailscale SSH, node attributes, and `tests`/`sshTests` are listed as supported in the feature matrix.

## Behaviour to expect

- Two nodes can appear in each other's `tailscale status` even if the policy allows traffic in one direction only. That is how Tailscale works: policy still filters traffic, and `tailscale ping` is always allowed both ways.
- `autogroup:self` may degrade coordinator performance in large deployments; the policy page suggests more specific rules, such as explicit per-user rules.
- With no policy, all traffic between nodes is allowed.

## Checked

2026-11-04. Confirmed against the Headscale policy page (limitations, defaults), features page (supported matrix, OIDC groups), FAQ (device visibility, tailscale ping) and OIDC page (groups claim use). Removed two Gotchas the pages do not state: that SaaS policies with postures or IP sets fail to load, and the advice to define group membership in the policy.

Method: documentation only; no commands were run.
