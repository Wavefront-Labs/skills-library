---
id: computing-software.devops-ci-cd.argocd-image-updater.calver-modifiers-variants-and-validation
name: calver-modifiers-variants-and-validation
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, calver, modifier, image-variants, layout-validation, calver-layout, test-command]
level: sme
status: docs-checked
description: "Handle calver pre-release MODIFIER tags versus image variants such as alpine, know which layouts are rejected at startup, and test a layout with the test command."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/test.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# calver modifiers, variants and validation

Pre-releases. A tag with a `MODIFIER` is a pre-release of the tag without it and never outranks it. Modifiers compare in natural order: `v2026-02-01-alpha < v2026-02-01-rc2 < v2026-02-01-rc10 < v2026-02-01`. A modifier is only matched when the layout spells `MODIFIER` (like semver excluding pre-releases unless asked). `MODIFIER` matches the rest of the tag and must be last.

Variants warning: registries use the same trailing slot for variants like `-alpine`, `-slim`, `-debian`. `MODIFIER` cannot tell them from `-rc1`, and since a plain release outranks modified ones, `vYYYY-0M-0D-MODIFIER` would move an app on `v2026-01-30-alpine` to the non-alpine `v2026-02-01`. Track a variant by writing it as a literal and omitting `MODIFIER`:

```yaml
imageName: "some/image:vYYYY-0M-0D-alpine"
```

Tags without `-alpine` do not match, so no `allowTags` is needed.

Rejected layouts (reported as errors at read time):

- no year field, or a field defined twice
- a day without a month, or a week combined with a month or day
- date split around another segment (`YY.MINOR.0M`)
- `MAJOR`/`MINOR`/`MICRO` out of order
- `MODIFIER` not last
- a variable-width token directly before another token
- an uppercase `Y`, `M`, `W`, `D` or a digit outside a token (so `vYYYY-0M-D` is caught)

Test a layout:

```
argocd-image-updater test some/image:vYYYY-0M-0D-MICRO --update-strategy calver
argocd-image-updater test some/image --update-strategy calver --calver-layout vYYYY-0M-0D-MICRO
```

`--calver-layout` overrides the layout read from the image argument.

## Checked

2026-11-04. Confirmed against update-strategies.md (Pre-releases, MODIFIER-versus-variant warning, Rejected layouts list, Testing a layout) and the test command page (`--calver-layout`, `--update-strategy`).

Method: documentation only; no commands were run.
