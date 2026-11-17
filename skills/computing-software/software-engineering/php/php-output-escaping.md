---
id: computing-software.software-engineering.php.php-output-escaping
name: php-output-escaping
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, output-escaping]
level: practitioner
status: docs-checked
description: "Escape output with htmlspecialchars in the right context and set secure defaults."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output escaping and XSS
- `htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')` for HTML text and attributes; JSON in script: `json_encode($v, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT)`; URLs: `rawurlencode`.
- Escape at output, per context; prefer a templating engine with auto-escaping (Twig, Blade).
- Add Content-Security-Policy as defence in depth.
Verify: inject `<script>` payloads in tests.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
