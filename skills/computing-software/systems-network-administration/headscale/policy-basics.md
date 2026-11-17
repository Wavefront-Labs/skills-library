---
id: computing-software.systems-network-administration.headscale.policy-basics
name: policy-basics
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, policy, grants, allow-all, deny-all, reload]
level: practitioner
status: docs-checked
description: "Load a Headscale policy file, understand allow-all versus deny-all defaults, write a grant, and reload with SIGHUP or systemctl reload."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy basics

Set the file in the config:

```yaml
policy:
  mode: file
  path: /etc/headscale/policy.hujson
```

`mode` is `file` or `database`; with `file`, `path` points to a HuJSON file. (The path value here is an example.)

## Defaults

- No policy loaded: all traffic between nodes is allowed.
- Allow all: omit `acls`/`grants` (`{}`).
- Deny all: an empty array:

```json
{ "grants": [] }
```

## A grant

```json
{
  "grants": [
    { "src": ["alice@"], "dst": ["autogroup:internet"], "ip": ["*"] }
  ]
}
```

## Reload

```
sudo systemctl reload headscale
sudo kill -HUP $(pidof headscale)
```

Each reload logs the policy processing result.

## Gotchas

- Policy changes apply only after reload.
- Users are written `alice@`.
- Storing the policy in the database is typically needed only with a web interface; recovery steps are in policy-recovery.
- Tailscale's docs cover further ACL, grant, SSH and tag examples.

## Checked

2026-11-04. Confirmed against the Headscale policy page and config-example.yaml: policy.mode and policy.path, no policy meaning allow all, allow-all and deny-all forms, the grants example, SIGHUP and systemctl reload, reload logging, and the database footnote. The trailing-@ user form is from the OIDC page.
Method: documentation only; no commands were run.
