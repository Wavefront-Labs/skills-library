---
id: computing-software.cloud-infrastructure-engineering.external-dns.fqdn-template-functions-and-conditionals
name: fqdn-template-functions-and-conditionals
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, issource-function, haskey, fromjson, kind-conditional, template-functions]
level: advanced
status: docs-checked
description: "ExternalDNS FQDN template helper functions (contains, isSource, hasKey, fromJson and more) and conditional patterns by Kind, source and label."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/fqdn-templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template functions and conditionals

**Custom functions:** `contains`, `isIPv4`, `isIPv6`, `isSource` (case-insensitive source name), `replace` (`{{ replace "l" "w" "hello" }}` gives `hewwo`), `trim`, `toLower`, `trimPrefix`, `trimSuffix`, `hasKey`, `fromJson`.

**By Kind** (only Services get a record):
```sh
--fqdn-template='{{ if eq .Kind "Service" }}{{ .Name }}.svc.example.com{{ end }}'
```

**By source.** `isSource` matches the `--source` value, not the Kubernetes Kind. One source such as `traefik-proxy` emits IngressRoute, IngressRouteTCP and IngressRouteUDP.
```sh
--fqdn-template='{{ if isSource "traefik-proxy" }}{{ .Name }}.proxy.example.com{{ end }}{{ if isSource "service" }}{{ .Name }}.svc.example.com{{ end }}'
```

**Guard labels with `hasKey`.** `index` returns an empty string for both a missing key and an empty value, giving `my-service..example.com`.
```sh
--fqdn-template={{ if hasKey .Labels "app" }}{{ .Name }}.{{ index .Labels "app" }}.example.com{{ end }}
```

**Spec fields:** `{{ if eq .Spec.Type "ExternalName" }}...{{ end }}` or `{{ index .Spec.Selector "app" }}`.

**Several names from JSON in a label:**
```sh
--fqdn-template={{ if hasKey .Labels "records" }}{{ range $entry := (index .Labels "records" | fromJson) }}{{ index $entry "dns" }},{{ end }}{{ end }}
```

**Ranging:** use `$.Name` for the root object inside `range`, and `{{ printf "," }}` to separate multiple names.

**Test** templates on simple resources first; mismatched fields or nil values cause errors or skipped entries.

## Checked

2026-11-04. Read the FQDN templating guide (Custom Functions table, Kind, isSource, Spec fields, range, hasKey and fromJson sections). Confirmed all eleven functions, the replace example, the Kind and isSource patterns, the hasKey rationale, the fromJson example, $.Name inside range and the testing tip. Removed nothing.

Method: documentation only; no commands were run.
