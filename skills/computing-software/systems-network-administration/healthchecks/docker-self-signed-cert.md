---
id: computing-software.systems-network-administration.healthchecks.docker-self-signed-cert
name: docker-self-signed-cert
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, self-signed-certificate, ca-certificates, tls-handshake-failed, container-trust-store]
level: advanced
status: docs-checked
description: "Make a Healthchecks container trust a self-signed certificate used by a notification target by mounting it and running update-ca-certificates."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Symptom: notifications to a server with a self-signed certificate fail with "TLS handshake failed". Disabling certificate validation is discouraged; trust the certificate instead.

1. In `docker-compose.yml`, under the `web:` service, mount the certificate using an absolute host path:

```
volumes:
    - /path/to/cert.pem:/usr/local/share/ca-certificates/my-selfsigned-cert.crt:ro
```

2. Restart the stack and refresh the trust store:

```
docker compose up
docker compose exec -u root web update-ca-certificates
```

Notes:
- Use an absolute path on the host.
- Run the exec step as root.

## Checked

2026-11-04. Confirmed against the Healthchecks Docker documentation: the TLS handshake failed symptom, libcurl validation and the discouragement of disabling it, the volume mount in the web service with an absolute path, and the compose up plus update-ca-certificates steps run as root. Removed the .crt extension note and the unrelated private-IP setting, which this page does not cover.

Method: documentation only; no commands were run.
