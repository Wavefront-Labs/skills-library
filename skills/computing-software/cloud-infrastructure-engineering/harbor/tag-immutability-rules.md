---
id: computing-software.cloud-infrastructure-engineering.harbor.tag-immutability-rules
name: tag-immutability-rules
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [tag-immutability, immutable-tags, overwrite-protection, tag-rules, harbor]
level: practitioner
status: docs-checked
description: "Lock Harbor tags so they cannot be overwritten or their artifact deleted, with matching and excluding patterns and the 15 rule limit."
sources:
  - https://goharbor.io/docs/main/working-with-projects/working-with-images/create-tag-immutability-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a tag can be pushed repeatedly; the tag migrates to the new artifact and the old artifact becomes tagless. Immutability rules are set per project and block pushes whose tag matches an existing immutable tag.

Create a rule as project admin: Projects, project, **Policy**, **Tag Immutability**, **Add Rule**:
- **Repositories**: matching or excluding, with a comma-separated list.
- **Tags**: matching or excluding, with a comma-separated list.
- **Add**. Maximum 15 rules per project. Matching tags show **Immutable** in the Repositories tab.

Rules combine with OR: a tag matched by any rule is immutable. Use **Action** to deactivate, edit or delete a rule.

Examples:
- Everything immutable: repositories matching `**`, tags matching `**`.
- Allow `rc`, `test` and `nightly` to be overwritten: repositories matching `**`, tags **excluding** `rc,test,nightly`.

Deletion behaviour: since v2.0 you can delete a single tag without deleting the artifact. An immutable tag cannot be deleted and the artifact holding it cannot be deleted. Push `hello-world:v1`, make it immutable, retag it locally as `v2` and push: you cannot delete `v1`, but you can delete `v2` even though it shares the digest with `v1`.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Create Tag Immutability Rules.
Method: documentation only; no commands were run.
