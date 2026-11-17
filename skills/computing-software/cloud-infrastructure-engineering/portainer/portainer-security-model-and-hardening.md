---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-security-model-and-hardening
name: portainer-security-model-and-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [security, shared-responsibility, air-gapped, vulnerability-reporting]
level: intro
status: docs-checked
description: "Read Portainer's stated shared-responsibility security model, privacy position and what counts as a vulnerability."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer runs entirely on your servers behind your firewalls. It does not host your infrastructure, so it holds no SOC or PCI/DSS compliance of its own, and it can run fully air-gapped. It collects no behavioural product analytics. Business Edition sends basic installation and licensing metadata to the licensing service to administer the license; Community Edition and air-gapped installs do not send it. Published container images are scanned for known vulnerabilities as part of release.

The security model is shared responsibility. Portainer's side: every request is checked against your access rules and governance policies before it proceeds, including requests proxied to the Docker and Kubernetes APIs on a caller's behalf. Your side: the roles and policies you define, how permissive you leave them, and whether and how you expose Portainer to the network. Within the access you grant, Portainer does not restrict what Docker or Kubernetes permits.

The page's hardening list points to: your own SSL certificate and a reverse proxy (serve HTTPS, disable plain HTTP, set trusted origins); the Edge Agent and mTLS for anything internet-facing; access control and least-privilege roles; encrypting the Portainer database; streaming auth and activity logs to a SIEM; and the CLI configuration options. It ends with the vulnerability-reporting process.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Replaced the writer's own hardening advice with the page's hardening list.

Method: documentation only; no commands were run.
