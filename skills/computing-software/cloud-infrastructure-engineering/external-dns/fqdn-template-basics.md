---
id: computing-software.cloud-infrastructure-engineering.external-dns.fqdn-template-basics
name: fqdn-template-basics
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, fqdn-template, go-templates, template-fields, combine-fqdn-annotation]
level: practitioner
status: docs-checked
description: "Generate DNS names from Kubernetes metadata with --fqdn-template: available fields, multiple templates, Helm escaping, kubectl explain, and which sources support it."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/fqdn-templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FQDN templating basics

`--fqdn-template` takes a Go template rendered per source object.

```sh
external-dns --provider=aws --source=service \
  --fqdn-template="{{ .Name }}.example.com" \
  --fqdn-template="{{ .Name }}.{{ .Namespace }}.example.tld"
```
Repeat the flag for more templates. Duplicates and surrounding whitespace are ignored. Each template adds records per resource, so API calls rise.

**Fields:** `.Kind`, `.APIVersion`, `.Name`, `.Namespace`, `.Labels` (`{{ .Labels.key }}` or `{{ index .Labels "key" }}`), `.Annotations` (`index`), `.Spec`, `.Status`. Discover them with `kubectl explain service --api-version=v1 --recursive`.

**Supported sources (FQDN):** contour-httpproxy, gateway-grpcroute, gateway-httproute, gateway-tcproute, ingress, istio-gateway, istio-virtualservice, node, openshift-route, pod, service, skipper-routegroup. Not supported: ambassador-host, connector, crd, f5, fake, gateway-tlsroute, gateway-udproute, gloo-proxy, kong-tcpingress, traefik-proxy. The "combine" column is yes for contour, ingress, istio, node, openshift, pod, service and skipper only.

**Gotchas**
- With `--fqdn-template`, `external-dns.kubernetes.io/hostname` annotations are ignored unless `--combine-fqdn-annotation` is also set.
- Write `{{ .Name }}`, with the dot, not `{{name}}`.
- Inside Helm `tpl`, escape: `--fqdn-template={{ `{{ .Name }}.uat.example.com` }}`.
- An Ingress host that is a bare subdomain (for example `foo`) does not get the template applied (issue 1872, documented as unsupported).
- `index` on a missing label returns an empty string and gives invalid names like `my-service..example.com`; other nil values can cause errors or skipped entries.

## Checked

2026-11-04. Read the FQDN templating guide (How It Works, Supported Sources table, Multiple FQDN Templates, Tips, FAQ on Helm escaping and subdomain-only hostnames). Confirmed the field list, kubectl explain, the supported-source and combine columns, deduplication, the Helm tpl escape and the issue 1872 limitation. Reworded the missing-label gotcha to match the page, which ties the empty-string result to index.

Method: documentation only; no commands were run.
