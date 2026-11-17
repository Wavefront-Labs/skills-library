---
id: computing-software.cybersecurity-defensive.pomerium.fleetdm-device-posture
name: fleetdm-device-posture
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [fleetdm, device-posture, failing-policies, vulnerabilities, external-data-source]
level: advanced
status: docs-checked
description: "Deny Pomerium Enterprise access from non-compliant or vulnerable hosts using the FleetDM external data plugin and client certificate matching."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/integrations/device-context/fleetdm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium Enterprise syncs host data from FleetDM as an external data source and matches a request's client certificate SHA-1 fingerprint to a Fleet host.

Records: `fleetdm.com/CertificateSHA1Fingerprint`, `fleetdm.com/Host`, `fleetdm.com/Policy`.

PPL criteria (deny only): `last_seen_over` (string), `vulnerabilities` (CVE strings), `failing_policies` (policy IDs), `failing_critical_policy` (bool), `failing_any_policy` (bool).

Steps (the guide is a test setup; mkcert certificates are not production):
1. Enroll a host with a `fleetd` package built via `fleetctl`, and import the client certificate into its keychain.
2. Add a Fleet query `SELECT * FROM certificates where ca != 1;`.
3. Create Fleet policies, optionally marking some Critical.
4. Run the plugin container `docker.cloudsmith.io/pomerium/datasource/datasource:main` with command `fleetdm` and flags `--api-url`, `--api-token`, `--cert-query-id`, `--address=:8080`.
5. Console: External Data, ADD EXTERNAL DATA SOURCE with the plugin URL.
6. Certificates, ADD CERTIFICATE with the root CA.
7. On the route set TLS Downstream Client Certificate Authority.
8. Policy: Add Deny Block, criterion FleetDM, operator Failing Policies or Vulnerabilities (e.g. a CVE ID).
9. Attach the policy to the route.

Production needs a private CA integrated with FleetDM, which the guide does not cover.

## Checked

2026-11-04. Confirmed against the FleetDM Integration page: record names, SHA-1 matching, the five deny-only criteria and types, setup steps, query, plugin image and flags, console steps, production limitation. Nothing removed.

Method: documentation only; no commands were run.
