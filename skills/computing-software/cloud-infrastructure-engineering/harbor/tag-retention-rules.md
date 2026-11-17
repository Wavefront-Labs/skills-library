---
id: computing-software.cloud-infrastructure-engineering.harbor.tag-retention-rules
name: tag-retention-rules
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [tag-retention, retention-policy, dry-run, retention-rules, harbor]
level: practitioner
status: docs-checked
description: "Configure Harbor tag retention: filter order, count or age options, OR logic across rules, multi-tag artifacts, 15 rule limit, dry run before run."
sources:
  - https://goharbor.io/docs/main/working-with-projects/working-with-images/create-tag-retention-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retention rules say which tags to keep; everything else matching the repository filter is deleted. A rule applies three filters in order: repositories, then quantity to retain, then tags to retain. Wildcards `*` and `**` are allowed (doublestar patterns), plus an untagged-artifacts checkbox.

Configure as project admin: Projects, project, **Policy**, **Tag Retention**, **Add Rule**:
1. Repositories: **matching** or **excluding**, then a name, comma list, wildcard such as `my_*`, or `**` for all.
2. Quantity: retain the most recently pushed # artifacts, most recently pulled # artifacts, artifacts pushed within # days, artifacts pulled within # days, or retain always.
3. Tags: matching or excluding, same pattern forms.
4. **Add**. Up to 15 rules per project.
5. Optionally **Schedule**, **Edit** (hourly, daily and so on, or Custom cron). One schedule applies to all rules.
6. **Dry Run**, then **Run Now**.

Behaviours:
- The count applies per repository, not across the project. Retaining 10 keeps up to 10 in each repository.
- Multiple rules use OR logic: a tag kept by any rule is kept.
- Retention matches tags but acts on artifacts. If an artifact has several tags and only some match, the artifact and all its tags are retained.
- Untagged artifacts are deleted unless the untagged box is checked.
- Rules cannot bypass quotas.

Warning: a run cannot be reverted. Always dry run first. Use **Action** to deactivate, edit or delete a rule.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Create Tag Retention Rules.
Method: documentation only; no commands were run.
