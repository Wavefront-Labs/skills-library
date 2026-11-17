---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-extension-security
name: woodpecker-extension-security
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [extension-security, http-signatures, allowed-hosts]
level: sme
status: docs-checked
description: "Verify Woodpecker extension requests and restrict which hosts extensions may reach."
sources:
  - https://woodpecker-ci.org/docs/usage/extensions
  - https://woodpecker-ci.org/docs/usage/security-boundaries
  - https://woodpecker-ci.org/docs/administration/configuration/server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker extension security

Extensions receive private data (secrets, tokens) and can return harmful data such as malicious pipeline configurations, so you must trust them. Anyone with repository admin rights on the forge can configure extensions for that repository, which could be used to obtain the forge user's credentials; trust your repository admins.

Request signing: Woodpecker signs every HTTP request using HTTP signatures with an ed25519 key pair. Your extension must verify the signature with the public key, using a library such as httpsign. Fetch the key from `http://my-woodpecker.tld/api/signature/public-key` or from the repository settings extensions page.

Host restrictions: by default extensions may only call external hosts. Change this with `WOODPECKER_EXTENSIONS_ALLOWED_HOSTS`, a comma-separated list of:

- built-in networks: `loopback` (127.0.0.0/8, ::1), `private` (RFC 1918 and RFC 4193), `external` (valid non-private unicast), and `*` for all
- CIDR ranges such as `1.2.3.0/8`
- hosts with wildcards, such as `example.com`, `*.example.com`, `192.168.100.*`

Extensions are called before a pipeline is approved, and a configuration extension's output still has commit data substituted into it.

A sample service for config and secrets extensions is in the woodpecker-ci/example-extensions repository.

## Checked

2026-11-08. Read the Woodpecker Extensions page and the Security boundaries page in full, and the `EXTENSIONS_ALLOWED_HOSTS` entry of the server configuration page (default `external`). All claims were confirmed; nothing was removed.

Method: documentation only; no commands were run.
