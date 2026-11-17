---
id: computing-software.web-development.hugo.fingerprint-sri
name: fingerprint-sri
category: computing-software
field: web-development
product: hugo
tags: [fingerprint, cache-busting, subresource-integrity, sha256, resource-hash]
level: intro
status: docs-checked
description: "Fingerprint resources with resources.Fingerprint: algorithms, hashed permalinks and the Data.Integrity value for SRI attributes."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/resources/Fingerprint.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`resources.Fingerprint [ALGORITHM] RESOURCE` (alias `fingerprint`) returns a fingerprinted resource by cryptographically hashing its content. It is most often used with CSS and JavaScript but works with any resource type.

- Algorithms: `md5`, `sha256` (default), `sha384`, `sha512`.
- `Permalink` and `RelPermalink` include the hash sum.
- `.Data.Integrity` returns an SRI value: the algorithm name, a hyphen, then the base64-encoded hash.

```go-html-template
{{ with resources.Get "js/main.js" }}
  {{ with . | fingerprint "sha256" }}
    <script src="{{ .RelPermalink }}" integrity="{{ .Data.Integrity }}" crossorigin="anonymous"></script>
  {{ end }}
{{ end }}
```

## Checked

2026-11-04. Confirmed against the Hugo docs page resources.Fingerprint: the signature and `fingerprint` alias, the four algorithms and the sha256 default, hashed `Permalink` and `RelPermalink`, the `.Data.Integrity` SRI format and the example. Removed the cache-busting remark, which the page does not state.

Method: documentation only; no commands were run.
