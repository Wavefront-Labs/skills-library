---
id: computing-software.cloud-infrastructure-engineering.external-dns.configuration-precedence
name: configuration-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, configuration-precedence, annotation-override, filter-flags, environment-variables]
level: intro
status: docs-checked
description: "ExternalDNS precedence: resource annotations over CLI flags over environment variables over defaults, and why filter flags set scope that annotations cannot escape."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/configuration-precedence.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/ptr-records.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration precedence

Effective values come from four places, in this order:

1. **Resource annotations.** Most options can be set this way and override the matching flags and defaults. Exceptions should be documented, annotations are ignored on `kind: DNSEndpoint`, and filter flags define scope.
2. **CLI flags.** Non-filter flags apply when no annotation overrides them. Filter flags (`--source`, `--service-type-filter`, `--*-filter`) limit which resources are processed; annotations on resources outside that scope are ignored, and a filtered-out resource receives neither its annotations nor defaults.
3. **Environment variables.** May override defaults and, in some cases, flags and annotations. Behaviour depends on how the variable is mapped in code, whether it replicates a CLI flag or is provider specific (the docs name `kubectl` or `cloudflare` as examples).
4. **Defaults.**

**Worked example:** with `--create-ptr=true`, a resource annotation `record-type: ""` opts that resource out; with `--create-ptr=false`, the annotation `"ptr"` opts it in.

## Checked

2026-11-04. Confirmed against the ExternalDNS configuration precedence page (order, exceptions, filter flags, environment variables) and the PTR page (record-type worked example). Removed an unsourced debugging tip.
Method: documentation only; no commands were run.
