---
id: computing-software.cloud-infrastructure-engineering.gateway-api.listener-certificates-wildcard-and-per-host
name: listener-certificates-wildcard-and-per-host
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [tls, certificates, wildcard, sni, listener, hostname]
level: advanced
status: docs-checked
description: "Choose between wildcard and per-hostname certificates on Gateway listeners, how SNI and hostnames select them, and limits on automating wildcards."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/hostnames.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Downstream TLS is configured on Gateway listeners, per domain or subdomain: a listener's TLS settings apply to all domains satisfying its hostname criteria. A listener with `protocol: HTTPS` (or `TLS`) uses `tls.mode: Terminate` and `tls.certificateRefs` pointing at a Secret (`kind: Secret`, `group: ""`); `Passthrough` is available for `TLS` listeners and then TLS settings do not take effect.

Layouts from the TLS guide:

- Per-hostname certificates: listeners for `foo.example.com` and `bar.example.com`, each with its own certificate. Listeners on the same port are distinct when their hostnames differ. A Route attaches to a listener whose hostname intersects its own `hostnames`, and `sectionName` can pin it.
- Wildcard plus specific: a listener for `*.example.com` with a wildcard certificate and another for `foo.example.com` with its own. The specific match takes priority, so `foo.example.com` gets the specific certificate and all other requests get the wildcard one.
- Cross-namespace certificate: a `certificateRefs` entry in another namespace is valid only if a ReferenceGrant in the target namespace allows it.

Wildcard differences to keep straight (hostnames page):

- In Gateway API hostnames, `*.example.com` matches one or more labels (`sub.domain.example.com`) but not `example.com`.
- Certificate wildcards are matched against the SNI under RFC-2818 rules and match a single label, so `*.example.com` on a certificate does not cover `foo.bar.example.com`. The certificate must cover the intersected hostname (the result of listener and Route hostname intersection), not the listener hostname, or SNI matching can fail. Gateway API does not require implementations to verify this; many proxies match SNI as a suffix, in which case the behaviour is the same.
- An SNI value is never a wildcard.

Automation: integrations MUST NOT use the hostname field to programmatically generate wildcard certificates; if the intersected hostname contains a wildcard, certificate integrations must ignore it. Every non-wildcard intersected hostname on a listener must be represented (CN or SAN) in a generated certificate on that listener. Managing wildcards through a dedicated API such as the cert-manager Certificate API is described as acceptable, with cross-namespace references and ReferenceGrants.

Upstream (backend) TLS is separate: BackendTLSPolicy, not listener settings.

## Checked

2026-11-08. Read in full (GitHub markdown): the TLS Configuration guide and the Hostnames page. Confirmed: listener TLS fields and modes, wildcard-plus-specific precedence, cross-namespace ReferenceGrant rule, hostname versus certificate wildcard semantics, SNI rules, certificate automation rules. Removed: the claim that a wildcard matches one label only in Gateway API hostnames (it matches one or more), the claim about HTTP-validated automation, and the multi-certificate listener sentence (not covered). Example YAML files in the guide are includes and were not visible.

Method: documentation only; no commands were run.
