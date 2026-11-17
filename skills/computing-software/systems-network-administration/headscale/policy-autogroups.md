---
id: computing-software.systems-network-administration.headscale.policy-autogroups
name: policy-autogroups
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, autogroup, member, tagged, self, nonroot]
level: practitioner
status: docs-checked
description: "The Headscale policy autogroups supported, which are source-only or destination-only, with grant and SSH examples and the autogroup:self performance caveat."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autogroups

| Autogroup | Meaning |
|---|---|
| `autogroup:internet` | internet via exit nodes; destination only |
| `autogroup:member` | all personal (untagged) devices |
| `autogroup:tagged` | devices with at least one tag |
| `autogroup:self` | devices where the same user is authenticated on source and destination; excludes tagged; destination only |
| `autogroup:nonroot` | Tailscale SSH users excluding root; only in SSH `users` |
| `autogroup:danger-all` | resolves to `0.0.0.0/0` and `::/0`; source only |

## Examples

```json
{ "grants": [ { "src": ["autogroup:member"], "dst": ["tag:prod-app-servers"], "ip": ["80,443"] } ] }
```

```json
{ "grants": [ { "src": ["autogroup:member"], "dst": ["autogroup:self"], "ip": ["*"] } ] }
```

```json
{ "ssh": [ { "action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:self"], "users": ["autogroup:nonroot"] } ] }
```

## Gotcha

`autogroup:self` can degrade performance on the Headscale coordinator in large deployments because filter rules must be compiled per node rather than globally. If you see performance issues, use more specific rules or limit `autogroup:self`; the docs' fallback is explicit per-user rules, e.g. `{"src": ["dev1@"], "dst": ["dev1@"], "ip": ["*"]}` for each user.

Only a subset of Tailscale autogroups is available (policy-limitations).

## Checked

2026-11-04. Confirmed against the Headscale policy page, Autogroups section (each autogroup, its source or destination restriction, the three examples, the autogroup:self warning and fallback).

Method: documentation only; no commands were run.
