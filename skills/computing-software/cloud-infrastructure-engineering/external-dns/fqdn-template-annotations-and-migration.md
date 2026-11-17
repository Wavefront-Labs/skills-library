---
id: computing-software.cloud-infrastructure-engineering.external-dns.fqdn-template-annotations-and-migration
name: fqdn-template-annotations-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, combine-fqdn-annotation, dns-scheme-migration, multi-variant-domains, node-address-fqdn]
level: advanced
status: docs-checked
description: "Combine --fqdn-template with annotations via --combine-fqdn-annotation, migrate DNS naming schemes, build multi-region variants, and name records after Node IPs."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/fqdn-templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates with annotations, migration and variants

**Annotations plus template.** `--combine-fqdn-annotation` is required to merge template output with annotation processing.
```yml
args:
  - --combine-fqdn-annotation
  - --fqdn-template={{ or .Annotations.dns "invalid" }}.example.com
  - --exclude-domains=invalid.example.com
```
`or` supplies a default so a missing annotation yields a name you can exclude.

An annotation as a name part:
```yml
--fqdn-template='{{ index .ObjectMeta.Annotations "dns.company.com/label" }}.{{ .Namespace }}.company.local'
```

Iterate and filter annotation keys or values with `range $key, $value := .Annotations` and `contains`; separate results with `{{ printf "," }}`.

**Scheme migration.** Add new records without editing manifests:
```yml
--fqdn-template='{{.Name}}.new-dns.example.com'
```

**Multi-variant domains:**
```sh
--fqdn-template='{{ .Name }}.{{ .Labels.env }}.{{ .Labels.region }}.example.com, {{ if eq .Labels.env "prod" }}{{ .Name }}.my-company.tld{{ end }}'
```
For Service `api` with env=prod and region=us-east-1 this gives `api.prod.us-east-1.example.com` and `api.my-company.tld`.

**Node IP names:**
```yml
--fqdn-template="{{range .Status.Addresses}}{{if and (eq .Type \"ExternalIP\") (isIPv4 .Address)}}{{.Address | replace \".\" \"-\"}}{{break}}{{end}}{{end}}.example.com"
```

**Gotchas:** the resulting FQDN must be valid and unique; multiple templates multiply DNS entries and provider API calls.

## Checked

2026-11-04. Read the FQDN templating guide (Conditional Templating combined with Annotations, Using Annotations for FQDN Templating, DNS Scheme Migration, Multi-Variant Domain Support, Node's Addresses, Tips). Confirmed --combine-fqdn-annotation, the or/exclude-domains example, the migration example, the multi-variant output and the Node address template. Removed nothing.

Method: documentation only; no commands were run.
