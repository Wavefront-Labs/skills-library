---
id: computing-software.devops-ci-cd.nomad.tls-cert-create
name: tls-cert-create
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, tls-cert-create, tls, ca-create, nomad-tls, certificates, name-constraint, mtls, server-certificate, cli]
level: practitioner
status: docs-checked
description: "Generate a Nomad CA and server, client and CLI certificates with nomad tls ca create and nomad tls cert create, including name constraints, days, domain, region and SAN flags."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/tls/ca-create.mdx", "https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/tls/cert-create.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad tls ca create and cert create

Built-in helpers for cluster TLS. They write files only; you must copy them and edit agent config yourself.

## CA
```
nomad tls ca create
nomad tls ca create -name-constraint="true" -domain="foo.com"
```
Writes `nomad-agent-ca.pem` and `nomad-agent-ca-key.pem` (prefix becomes the domain when `-domain` is used, for example `foo.com-agent-ca.pem`).
- `-days` - validity, default 5 years.
- `-common-name` - default `Nomad Agent CA`.
- `-name-constraint` (default false) - reject certificates for DNS names outside the allowed set; when true, `localhost` and `-domain` (default `nomad`) are allowed. `-additional-domain` (repeatable) adds names and only works with `-domain` and `-name-constraint`.
- Subject fields: `-country` (US), `-organization`, `-organizational-unit` (Nomad), `-locality`, `-province`, `-postal-code`, `-street-address`.

Warning: with `-name-constraint`, add the Web UI's DNS name via `-additional-domain` now; it cannot be added later.

## Certificates
```
nomad tls cert create -server
nomad tls cert create -client
nomad tls cert create -cli
```
Outputs like `global-server-nomad.pem` and `global-server-nomad-key.pem`. Pick one of `-server`, `-client`, `-cli`.
- `-ca` and `-key` - paths, default `#DOMAIN#-agent-ca.pem` and `#DOMAIN#-agent-ca-key.pem`.
- `-days` - default 1 year.
- `-region` - default `global`.
- `-domain` - matters only for server certificates.
- `-additional-dnsname` and `-additional-ipaddress` - repeatable extra SANs; `localhost` and `127.0.0.1` are always included.

The tool warns that server certificates grant authority to become a server and read all state including root keys and ACL tokens: store them like CA keys and never ship them to non-server hosts.

## Checked

2026-11-03. Confirmed against the commands/tls/cert-create and ca-create pages (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
