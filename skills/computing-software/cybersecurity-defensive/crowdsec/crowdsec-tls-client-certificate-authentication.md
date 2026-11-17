---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-tls-client-certificate-authentication
name: crowdsec-tls-client-certificate-authentication
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [tls-auth, client-certificates, crl, ocsp, allowed-ou, auto-registration]
level: advanced
status: docs-checked
description: "Authenticate CrowdSec agents and bouncers with TLS client certificates keyed by certificate OU, including CRL and OCSP revocation checks."
sources: ["https://docs.crowdsec.net/docs/local_api/tls_auth", "https://docs.crowdsec.net/docs/configuration/crowdsec_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS client authentication replaces login/password (agents) and API keys (bouncers). It suits autoscaling fleets where credentials cannot be pre-generated. The LAPI decides what a client is allowed to do from the certificate **OU** field.

## LAPI side

Configure under `api.server.tls`:

```yaml
api:
  server:
    tls:
      cert_file: /path/to/server.pem
      key_file: /path/to/server-key.pem
      ca_cert_path: /path/to/inter.pem
      bouncers_allowed_ou:
        - bouncer-ou
      agents_allowed_ou:
        - agent-ou
```

`ca_cert_path` is the CA used to verify client certificates.

## Agent side

In `local_api_credentials.yaml`, set `ca_cert_path` (CA trusted for the server certificate), `key_path` and `cert_path` for the client key and cert. When an agent with an allowed OU connects for the first time, the log shows the OU matched and a new machine is created automatically.

## Revocation

CrowdSec checks both:

- **CRL**: give a CRL file path (`crl_path` under `api.server.tls`); it is re-read at each check, so a cron job can refresh it without reloading crowdsec. A missing, invalid or expired CRL file skips the check.
- **OCSP**: used if the client certificate has an OCSP URL. A malformed OCSP response is ignored.

Results are cached for `api.server.tls.cache_expiration`. The log warns `no crl_path, skipping CRL check` when none is set. Idle TLS-authenticated clients can be pruned with `flush.bouncers_autodelete.cert` and `flush.agents_autodelete.cert` under `db_config`.

## Checked
2026-11-08. Confirmed against the TLS Authentication page (config sections, OU-based access, CRL and OCSP behaviour and caching, example configuration, auto-created machines, log lines) and the `db_config.flush` section of the CrowdSec configuration page (read in part). Nothing removed.
Method: documentation only; no commands were run.
