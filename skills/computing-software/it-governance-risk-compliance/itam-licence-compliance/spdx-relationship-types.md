---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-relationship-types
name: spdx-relationship-types
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-relationship-types, spdx-relationships-and-licences, spdx relationship, describes, contains, depends_on, dependency_of, generated_from, build_tool_of, relationshiptype, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Express dependencies and containment with SPDX relationships such as DESCRIBES, CONTAINS, DEPENDS_ON and GENERATED_FROM."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/relationships-between-SPDX-elements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX relationship types

Goal: represent the dependency graph correctly.

Format: SPDXElement RELATIONSHIP_TYPE related element. Examples:
- SPDXRef-DOCUMENT DESCRIBES SPDXRef-Package-app (root).
- SPDXRef-Package-app DEPENDS_ON SPDXRef-Package-lib.
- CONTAINS / CONTAINED_BY for package to file.
- GENERATED_FROM, BUILD_TOOL_OF, DEV_DEPENDENCY_OF, OPTIONAL_DEPENDENCY_OF, RUNTIME_DEPENDENCY_OF, STATIC_LINK, DYNAMIC_LINK (useful for licensing analysis), VARIANT_OF, PATCH_FOR.
- Use NONE or NOASSERTION to state no/unknown relationships.

Method: ensure every package is reachable from the DESCRIBES root (DESCRIBES is mandatory when more than one package or set of files outside a package is present).

Gotchas:
- DEPENDS_ON direction is from dependent to dependency.
- Dev dependencies should not be conflated with runtime.

Verify: graph traversal from root reaches all packages.

## Checked

2026-11-02. Checked against SPDX 2.3 clause 11 relationship table: DESCRIBES, CONTAINS, CONTAINED_BY, DEPENDS_ON, GENERATED_FROM, BUILD_TOOL_OF, DEV_DEPENDENCY_OF, OPTIONAL_DEPENDENCY_OF, RUNTIME_DEPENDENCY_OF, STATIC_LINK, DYNAMIC_LINK, VARIANT_OF, PATCH_FOR, and the NONE / NOASSERTION keywords. Nothing removed.

Method: documentation only; no commands were run.
