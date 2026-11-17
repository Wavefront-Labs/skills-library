---
id: computing-software.systems-network-administration.icinga-2.cli-node-setup-automation
name: cli-node-setup-automation
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, node-setup, automation, pki, new-cert, save-cert, trustedcert, manual-certificates]
level: advanced
status: docs-checked
description: Automate Icinga 2 onboarding with icinga2 node setup and the pki new-cert, save-cert, new-ca and sign-csr commands - master and agent parameters and manual certificates.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI node setup automation
**Master:** `icinga2 node setup --master`. Options: `--cn` (defaults to FQDN), `--zone` (default `master`), `--listen host,port`, `--disable-confd` (adds the `api-users.conf` include; docs say available since v2.9, not set by default for compatibility with Puppet and Ansible).

**Agent/satellite:** 
1. Ensure `/var/lib/icinga2/certs` exists and belongs to the Icinga user.
2. `icinga2 pki new-cert --cn <fqdn> --key <file> --cert <file>` creates a local self-signed certificate (files by convention in `/var/lib/icinga2/certs`).
3. `icinga2 pki save-cert --trustedcert <file> --host <parent>` fetches the parent certificate; verify its fingerprint by hand to avoid MITM. The file is temporary.
4. `icinga2 node setup` with: `--cn`, `--ticket` (required), `--trustedcert` (required), `--parent_host` (optional; without it copy the parent CA to `ca.crt` yourself), `--endpoint` (required, parent endpoint name; use `cn,host,port` for the node to connect), `--zone` (required), `--parent_zone`, `--accept-config`, `--accept-commands`, `--global_zones`, `--disable-confd`, `--no-default-global-zones`. `master_host` is deprecated in favour of `--parent_host`.

Without `--parent_host` you cannot restart until the CA is copied; once started, the CSR goes to the parent, and a supplied ticket lets the master sign it, otherwise sign it manually.

For a command-endpoint agent you can disable `checker`; `node setup` already disabled `notification`. Optionally add an ApiUser for remote troubleshooting, and have the automation tool add the Endpoint and Zone (`parent = "master"`) on the master.

**Manual certificates:** `icinga2 pki new-ca` on one master, `pki new-cert --cn ... --key ... --csr ...`, `pki sign-csr --csr ... --cert ...` per instance, then copy `.crt`, `.key` and the CA `ca.crt` into `/var/lib/icinga2/certs` with correct ownership.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: node setup master and agent parameters, pki new-cert, save-cert, sign-csr, new-ca usage, --parent_host, --disable-confd (v2.9+), --no-default-global-zones and the deprecated master_host.

Method: documentation only; no commands were run.
