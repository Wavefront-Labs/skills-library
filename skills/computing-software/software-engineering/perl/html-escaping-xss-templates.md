---
id: computing-software.software-engineering.perl.html-escaping-xss-templates
name: html-escaping-xss-templates
category: computing-software
field: software-engineering
product: perl
tags: [perl, html-escape, xss-prevention, output-encoding, uri-escape, auto-escape, html-escaping-xss-templates]
level: practitioner
status: draft
description: "Escape HTML, attributes, URLs and JSON properly when generating pages from Perl, with template auto-escape or explicit helpers."
sources: ["https://metacpan.org/pod/HTML::Escape", "https://metacpan.org/pod/URI::Escape", "https://docs.mojolicious.org/Mojolicious/Guides/Rendering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Escaping output and avoiding XSS in generated HTML

**Goal:** every untrusted value is encoded for the context it lands in.

```perl
use HTML::Escape qw(escape_html);           # fast escaper (CPAN); alternative: HTML::Entities::encode_entities
my $safe = escape_html($user_text);         # & < > " ' become entities
use URI::Escape qw(uri_escape_utf8);        # URL components
my $q = '?name=' . uri_escape_utf8($name);
use JSON::PP; my $json = JSON::PP->new->utf8->canonical->encode($data);
use Mojo::Util qw(xml_escape url_escape);   # inside Mojolicious apps
```

## Contexts
| Where the value goes | Encode with |
|---|---|
| HTML text node | HTML entity escape |
| HTML attribute (quoted) | HTML escape, and always quote attributes |
| URL query value or path segment | percent-encoding of UTF-8 bytes |
| script data | JSON encode, place in a `data-` attribute or a JSON script block; never interpolate into JS code |
| CSS | avoid; use allow-lists |
| Email headers, shell, SQL | context-specific rules (placeholders, list-form exec) |

## Rules
- Prefer templates that escape by default: Mojolicious `<%= %>` escapes and `<%== %>` does not (use rarely, with trusted markup); Template Toolkit needs `| html` per value or an auto-filter option.
- Mark trusted fragments explicitly (Mojo::ByteStream `b($html)`) rather than turning escaping off.
- Validate URLs before putting them in `href`: allow `http`, `https`, `mailto` only (a `javascript:` URL is not stopped by HTML escaping).
- Send `Content-Type: text/html; charset=utf-8` and encode output once.
- Add a Content-Security-Policy header and cookie flags `HttpOnly`, `Secure`, `SameSite` at the framework layer.
- Sanitising rich HTML: use a maintained allow-list sanitiser (for example HTML::Scrubber; check its configuration docs) rather than regexes.
- Test with strings like `<script>alert(1)</script>` and values containing quotes.

## Self-check
- [ ] A comment containing `<script>` renders visibly as text, not as markup, in the page source.
