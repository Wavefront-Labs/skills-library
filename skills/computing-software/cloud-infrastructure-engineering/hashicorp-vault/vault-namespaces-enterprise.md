---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-namespaces-enterprise
name: vault-namespaces-enterprise
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-namespaces, namespace, enterprise]
level: practitioner
status: docs-checked
description: "Create and use Vault Enterprise namespaces, address them with the X-Vault-Namespace header, and know naming rules, inheritance and delegation."
sources: ["https://developer.hashicorp.com/vault/docs/enterprise/namespaces", "https://developer.hashicorp.com/vault/docs/commands/namespace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Namespaces need a Vault Enterprise license or an HCP Vault Dedicated cluster. A namespace is an isolated environment with separate login paths, a mini-Vault inside the installation, holding its own secrets engines, auth methods, ACL/EGP/RGP policies, password policies, entities, identity groups and tokens.

```sh
vault namespace create ns1/
vault namespace create -custom-metadata=foo=abc ns1/
vault namespace list
vault namespace list -detailed
vault namespace lookup ns1/
vault namespace delete ns1/
vault namespace lock ns1/
vault namespace unlock -unlock-key <unlock key> ns1/
```

- The `vault namespace` subcommands act in the namespace of the logged-in token; `list` lists child namespaces.
- API calls target a namespace with the `X-Vault-Namespace` header (absolute or relative path; relative paths are children of the calling namespace), or with the namespace in the request path. `secret/foo` with header `ns1/ns2/` equals path `ns2/secret/foo` with header `ns1/`.
- Names cannot end with `/`, cannot contain spaces, and cannot be `root`, `sys`, `audit`, `auth`, `cubbyhole` or `identity`.
- Children can inherit from parents: a child's policies can reference parent entities or groups, and parents can assert policies on identities in a child. The `group-policy-application` API endpoint sets the inheritance behaviour.
- Delegate admins can manage their own namespace and create child namespaces and subordinate delegate admins. Administrative namespaces grant access to a predefined subset of privileged `sys/` endpoints (for example `sys/audit-hash` yes, `sys/audit` and `sys/config/auditing/*` no).
- Some `sys` endpoints are restricted to the root namespace, or to a token in it.

## Checked
2026-11-03. Confirmed on the Namespaces overview page (Enterprise requirement, contents, naming, child inheritance, delegation, header, administrative namespace table) and the `namespace` command page (subcommands, `-detailed`, `-custom-metadata`, lock/unlock). Removed: `VAULT_NAMESPACE` and `-namespace` flag usage, the claim that child policies cannot reach the parent (the page says children can inherit from parents), license-limit and "deletion requires empty" statements, audit-at-root claim, the Verify step and the design advice.
Method: documentation only; no commands were run.
