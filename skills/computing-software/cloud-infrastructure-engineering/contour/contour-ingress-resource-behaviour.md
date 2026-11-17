---
id: computing-software.cloud-infrastructure-engineering.contour.contour-ingress-resource-behaviour
name: contour-ingress-resource-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [ingress-v1, pathtype, defaultbackend, wildcard-hostnames, ingress-tls, applytoingress, implementationspecific]
level: practitioner
status: docs-checked
description: "How Contour implements Ingress v1: default backend, wildcard hostname rules, path types (Exact, Prefix segments, ImplementationSpecific), TLS host matching, status, headers."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/ingress.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour Ingress behaviour

Contour 1.16+ requires Kubernetes 1.19+ (Ingress v1); it is validated against Kubernetes N to N-2. The API server converts v1beta1 to v1.

- Backends: only Services (no other resource types). `defaultBackend` receives requests matching no rule, but cannot serve TLS because the host set is unbounded.
- Hostnames: wildcards only for the whole first label (`*.foo.com` valid; `*foo.com`, `foo*.com`, `foo.*.com` and `*` are not). Precise hostnames beat wildcards: `bar.foo.com` goes to its own backend even if `*.foo.com` exists.
- Path types (since 1.14.0):
  - `Exact`: matches exactly.
  - `Prefix`: segment prefix, so `/foo/bar` matches `/foo/bar`, `/foo/bar/`, `/foo/bar/baz` but not `/foo/barbaz`.
  - `ImplementationSpecific`: legacy behaviour; paths containing any of `^+*[]%` become regex matches, others string prefixes.
- TLS: a secret in `spec.tls` applies only to rules whose Host exactly matches an entry in `hosts`; non-matching secrets are ignored. Ingress v1 cannot use `namespace/name` in `secretName`; use the `projectcontour.io/tls-cert-namespace` annotation with TLS certificate delegation.
- Status: address from `--ingress-status-address`, otherwise from the Envoy Service (`--envoy-service-name`, `--envoy-service-namespace`).
- Headers: Ingress cannot manipulate headers, but setting `applyToIngress: true` in the config-file `policy` block applies the global header policy to Ingress-derived routes.

## Checked

2026-11-04. Confirmed against the Contour Ingress support page (config/ingress.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
