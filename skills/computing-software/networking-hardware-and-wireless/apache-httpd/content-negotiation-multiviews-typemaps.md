---
id: computing-software.networking-hardware-and-wireless.apache-httpd.content-negotiation-multiviews-typemaps
name: content-negotiation-multiviews-typemaps
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, content-negotiation, multiviews, type-map, languagepriority, vary]
level: advanced
status: docs-checked
description: "Serve language or format variants with MultiViews or .var type maps, source quality qs values, LanguagePriority and the Vary behaviour for caches."
sources:
  - https://httpd.apache.org/docs/2.4/content-negotiation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content negotiation
## MultiViews
Per-directory and not part of `Options All`; name it explicitly.
```apache
<Directory "/var/www/docs">
    Options +MultiViews
</Directory>
```
If `foo` does not exist, httpd scans `foo.*` and builds an implicit type map. It also applies to `DirectoryIndex`.

## Type maps
```apache
AddHandler type-map .var
```
```
URI: foo.en.html
Content-type: text/html
Content-language: en
```
URIs are relative to the map. A `.var` file beats MultiViews scanning; files not listed are ignored.

## Quality
- `qs` in a type map is source quality, 0.000-1.000 (default 1.0; 0 is never chosen), e.g. `Content-type: image/jpeg; qs=0.8`.
- Client `Accept-*` q-values are multiplied by `qs`, then language, charset, encoding and length tests apply.
- Accept headers without q-values: `*/*` gets 0.01 and `type/*` 0.02.

## Language fallback
`LanguagePriority` sets the server's language order. `ForceLanguagePriority` lets the server substitute its own choice for the 406 "No Acceptable Variant" and Multiple Choices responses. `en-GB` can fall back to `en`.

## Caching
HTTP/1.1 responses carry `Vary`. HTTP/1.0 negotiated responses are uncacheable unless `CacheNegotiatedDocs`. `force-no-vary` encourages caches to reuse a copy.

## Checked

2026-11-08. MultiViews scope and the Options All exception, implicit type map and DirectoryIndex use, AddHandler type-map, URI relativity and precedence over MultiViews, qs range and default, Accept wildcard q-values, language fallback including en-GB to en, and Vary and cache behaviour confirmed against the content negotiation page. Removed the ForceLanguagePriority arguments, which that page does not show.

Method: documentation only; no commands were run.
