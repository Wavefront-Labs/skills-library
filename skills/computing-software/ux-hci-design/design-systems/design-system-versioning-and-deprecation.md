---
id: computing-software.ux-hci-design.design-systems.design-system-versioning-and-deprecation
name: design-system-versioning-and-deprecation
category: computing-software
field: ux-hci-design
product: design-systems
tags: [semver-design-system, deprecation-policy, ds-governance]
level: practitioner
status: draft
description: "Release the library with semver, changelogs, codemods and deprecation periods."
sources:
  - https://semver.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioning
- Semver: patch (fixes), minor (new features, backwards compatible), major (breaking).
- Deprecate before removal: warn in console and docs, give a replacement and timeline.
- Provide codemods for breaking changes; migration guides.
- Token renames are breaking changes; alias old names.

## Verify
- [ ] Consuming app upgrades via documented steps with no surprise breaks.
