---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.copyright-notice-and-header-hygiene
name: copyright-notice-and-header-hygiene
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [copyright-notice-and-header-hygiene, permissive-compliance-practice, spdx-license-identifier, reuse-specification, reuse-toml, file-header, copyright-notice, vendored-code, licence-headers, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Keep copyright notices and SPDX licence headers correct per REUSE spec 3.3: header format, LICENSES/ directory, .license sidecars, REUSE.toml, vendored code."
sources:
  - https://reuse.software/spec-3.3/
  - https://www.apache.org/licenses/LICENSE-2.0.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copyright notices and file headers

Goal: clear, machine-readable licensing in source, following REUSE Specification 3.3 (dated 2024-11-14). Check whether a newer version exists before adopting.

Method:
- Header: a Commentable File's comment header MUST contain one or more Copyright Notices and one or more SPDX-License-Identifier tag-value pairs, as close to the top of the file as possible. The value MUST be a valid SPDX License Expression (example in the spec: `GPL-3.0-or-later OR Apache-2.0`).
- Copyright Notice format: starts with `SPDX-FileCopyrightText` (recommended), `Copyright` or the copyright sign; MUST contain the holder's name; SHOULD contain year then name then contact address, with the address in angle brackets. The year may be a single year, several years or a span (your year policy: pick one and apply it consistently).
- Licence files: a project MUST include a licence file for every licence used by covered files, in a `LICENSES/` directory at the root, named by SPDX identifier plus extension (example `LICENSES/GPL-3.0-or-later.txt`). It MUST NOT include licences nothing uses, nor other files. A licence not on the SPDX list uses `LicenseRef-<idstring>`.
- Files that cannot carry comments: use an adjacent file with the extra extension `.license` (example `cat.jpg.license`). Every covered file needs licensing information, by comment header, `.license` file or REUSE.toml; the spec lists the exempt files (licence files, VCS-ignored files, symlinks and others).
- Bulk assignment: `REUSE.toml` (version 1) with `[[annotations]]` tables (`path`, optional `precedence` of `closest`, `aggregate` or `override`, plus `SPDX-FileCopyrightText` and `SPDX-License-Identifier`) suits large directories. REUSE.toml and DEP5 (deprecated) must not be used together.
- Vendored third-party code: keep the upstream notices and licence. The Apache-2.0 text, for example, says that in Source form of Derivative Works you distribute, you must retain all copyright, patent, trademark and attribution notices from the Source form of the Work (section 4(c)). Check the licence of each component for its own rules.
- Snippets under another licence use `SPDX-SnippetBegin`, `SPDX-SnippetCopyrightText`, `SPDX-License-Identifier` and `SPDX-SnippetEnd`.
- Automation: the spec names a REUSE Tool for compliance checking; run it in CI or a pre-commit hook (the exact CLI is not specified by the spec page, so use the tool's own documentation).

Gotchas:
- Do not strip upstream headers from copied code.
- Text that merely quotes an SPDX tag (docs, command output) goes between `REUSE-IgnoreStart` and `REUSE-IgnoreEnd` comments so the tool does not read it as real licensing information.

Verify: the REUSE compliance check passes for all covered files.

## Checked

2026-11-08. Confirmed against REUSE Specification 3.3 (header contents, copyright notice format, LICENSES/ rules, .license files, REUSE.toml keys and precedence, DEP5 exclusivity, snippet tags, ignore blocks) and the Apache-2.0 text (section 4(c) notice retention). Removed: the unsupported "may breach the licence" generalisation (replaced by the cited Apache-2.0 example), the `reuse lint` command (the spec names the tool but not its subcommands) and the claim that generated files specifically need a declaration (the spec covers all non-ignored files). ISO, CycloneDX, NTIA, OpenChain, OSI and GNU FAQ sources supported no remaining claim and were dropped.
Method: documentation only; no commands were run.
