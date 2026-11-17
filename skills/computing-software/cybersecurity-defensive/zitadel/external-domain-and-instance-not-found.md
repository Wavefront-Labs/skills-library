---
id: computing-software.cybersecurity-defensive.zitadel.external-domain-and-instance-not-found
name: external-domain-and-instance-not-found
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, external-domain, custom-domain, host-header, troubleshooting]
level: practitioner
status: docs-checked
description: "Configure ExternalDomain, ExternalPort and ExternalSecure correctly, and fix Instance not found errors caused by Host header mismatches."
sources:
  - https://zitadel.com/docs/self-hosting/manage/custom-domain
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL serves only requests that match the expected protocol, host and port, because it uses the request Host header to find the virtual instance. A mismatch produces an "Instance not found" error.

Local testing:

```yaml
ExternalDomain: localhost
ExternalPort: 8080
ExternalSecure: false
```

Production, with HTTPS and your own domain:

```yaml
ExternalDomain: 'zitadel.my.domain'
ExternalPort: 443
ExternalSecure: true
```

You can change these at any time, but ZITADEL only picks up the change after you rerun the setup phase.

Behind a reverse proxy, the proxy must either put the original Host header value into the host directive of the Forwarded header or leave the original Host header unchanged.

Organization domains, by default, do not serve ZITADEL. They route users to the right organization by login method. To serve ZITADEL at an organization domain, add the domain through the System API; you will not automatically get that organization's context.

Each new virtual instance gets a random generated subdomain, so you can reach its console and APIs straight away.

Check ExternalDomain, port and scheme against the URL in the browser first.

## Checked

2026-11-08. Read the custom domain page in full.

Method: documentation only; no commands were run.
