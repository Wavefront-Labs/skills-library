---
id: computing-software.systems-network-administration.headscale.register-tagged-nodes
name: register-tagged-nodes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, tagged-devices, tagowners, personal-nodes, advertise-tags]
level: practitioner
status: docs-checked
description: "Personal versus tagged Headscale nodes, who owns each, how tagOwners authorises web-auth tag requests, and tagged-key registration."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Personal and tagged nodes

- **Personal nodes**: owned by one human user; laptops, workstations, phones.
- **Tagged nodes**: service-based, non-human (web and database servers), usually managed by a team. They have extra restrictions, for example they cannot use Tailscale SSH to reach a personal node.
- Headscale assigns personal nodes to a user and tagged nodes to the special user `tagged-devices`.

Both registration methods (web authentication, pre-authenticated keys) work for both node types.

## Authorise a user to request tags

```json
{
  "tagOwners": {
    "tag:server": ["alice@"]
  }
}
```

Then, on the node:

```
tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-tags tag:server
headscale auth register --user alice --auth-id <AUTH_ID>
```

## Tagged key

```
headscale preauthkeys create --tags tag:server
```

The tags are read from the key, so `--advertise-tags` is not needed on the node.

## Check

`headscale nodes list` shows owner and tags.

## Gotcha

Headscale checks that the user is allowed to register the requested tags (`tagOwners` in the policy) before ownership moves to `tagged-devices`. See node-tags-cli to retag existing nodes.

## Checked

2026-11-04. Confirmed against the Headscale registration reference: personal versus tagged definitions, Tailscale SSH restriction, `tagged-devices`, the tagOwners example, and tag keys. Removed the claim about what happens without a tagOwners entry beyond the documented check.
Method: documentation only; no commands were run.
