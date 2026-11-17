---
id: computing-software.devops-ci-cd.nomad.acl-bootstrap
name: acl-bootstrap
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, acl-bootstrap, bootstrap, management-token, acl, secret-id, bootstrap-token, cli]
level: practitioner
status: docs-checked
description: "Create the first Nomad ACL management token with nomad acl bootstrap, either system generated or supplied from a file or stdin, and handle the secret safely."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/acl/bootstrap.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad acl bootstrap

Bootstraps the initial ACL token, which the example output shows as a global `management` token.

```
nomad acl bootstrap
nomad acl bootstrap root.token
echo "<operator-chosen-uuid>" | nomad acl bootstrap -
```
- No argument: Nomad generates the token.
- A path: the file's contents become the Secret ID. `-` reads it from stdin.
- Output fields: Accessor ID, Secret ID, Name (`Bootstrap Token`), Type (`management`), Global (`true`), Policies (`n/a`), create and modify index.

## Options
- `-json` - output the response as JSON.
- `-t` - format with a Go template.

## Handling the token
The docs warn that a supplied token could be written to your terminal history, so secure it appropriately.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 acl bootstrap command page: no-argument, file and stdin forms, -json and -t options, the output fields. Removed: the run-once instruction and the secret-manager and narrower-policy advice.

Method: documentation only; no commands were run.
