---
id: creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging
name: versioning-deprecating-and-changelogging
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [semantic-versioning, changelog, component-deprecation, semver, release-management, deprecation-policy, design-system-releases]
level: practitioner
status: draft
description: "Version a design system with semver, write human changelogs, run a deprecation policy with codemods and timelines, and communicate breaking changes."
sources:
  - "Semantic Versioning 2.0.0 (semver.org)"
  - "Keep a Changelog (keepachangelog.com)"
  - "Changesets - versioning and changelogs for monorepos (github.com/changesets/changesets)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioning, deprecation and changelogs

## Semantic versioning
- **MAJOR** breaking (removed prop, renamed component, changed behaviour or token meaning), **MINOR** backward-compatible features, **PATCH** fixes. Pre-1.0 and `-beta` for unstable parts. Tokens and Figma libraries follow the same logic and are versioned together with code where possible.
- Automate with **Changesets** (a changeset file per PR; release PR bumps versions and builds the changelog) or semantic-release with conventional commits.

## Changelog
Format per release (Keep a Changelog): Added, Changed, Deprecated, Removed, Fixed, Security; link PRs; write for **users** ("Button: `variant="ghost"` added"), include a migration snippet, and a visual diff for visual changes.

## Deprecation policy
1. **Announce:** mark deprecated in docs (banner), code (`@deprecated` JSDoc, console warning in dev only), Figma (library component description, rename with a "Deprecated" prefix), and the changelog.
2. **Timeline:** typically one or two minor releases or 3-6 months before removal; removal only in a major.
3. **Provide a replacement and a migration path:** guide plus a **codemod** (jscodeshift) for mechanical changes.
4. **Track usage** (adoption analytics, code search) and chase remaining consumers before removal.
5. **Remove** in the announced major; keep a final changelog entry.

## Communication
Release notes email and chat post, office hours for big migrations, upgrade guide per major with a checklist; a support window for the previous major.

## Verify
- [ ] Every change classified major/minor/patch; changelog entry present.
- [ ] Each deprecation has replacement, timeline, codemod or guide, and usage tracking.
- [ ] Breaking changes only in majors.
