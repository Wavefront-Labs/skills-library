---
id: computing-software.devops-ci-cd.ci-pipeline-design.keystone-interfaces-and-dark-launching
name: keystone-interfaces-and-dark-launching
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, keystone-interface, trunk-based-development, feature-flags]
level: advanced
status: docs-checked
description: "Merge unfinished features to trunk safely using a keystone interface (wire the entry point last) and dark launching, without feature-flag sprawl."
sources: ["https://martinfowler.com/articles/continuousIntegration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keystone interfaces and dark launching

Continuous integration means integrating as soon as there is a little forward progress and
the build is healthy, often before a user-visible feature is complete. That leaves **latent
code**: code for an unfinished feature that is present in a live release. Fowler's guidance:
all code sent to the mainline must be production quality, with tests that verify it. Latent
code may never run in production, but tests still exercise it.

## Keystone interface
Make the interface that provides a path to the new feature the **last** thing added to the
code base. Tests can still check the code at every level except that final interface. In a
well-designed system such interface elements are minimal, so adding one is a short
programming episode. Fowler says keystones cover most cases of latent code.

A sequence that follows the idea: land the data model, then the service layer with tests,
then the handler that is not yet reachable, and finally the keystone that registers the entry
point. Each step is mergeable on its own. This works best when the feature has a single
entry point; if there are many, use a feature flag. (Illustrative sequence, not from the source.)

## Dark launching
Fowler: dark launching lets you test some changes in production before making them visible
to the user, and is useful for assessing the impact on performance.

## When a keystone is not possible: feature flags
Flags are checked whenever the latent code is about to execute, and are set as part of the
environment (for example an environment-specific configuration file), so the code is active
for testing and disabled in production. Flags also make runtime switching for A/B testing
and canary releases easier. Remove the flag logic promptly once the feature is fully
released so flags do not clutter the code base.

## Related techniques named in the same article
- **Branch by abstraction** for large infrastructural changes: an internal interface routes
  between old and new logic and replaces execution paths gradually.
- **Parallel change (expand-contract):** break a change into reversible steps so any step can
  be undone, for example when renaming a database field.

## Verify
- [ ] Every change merged was production quality, tested and deployable.
- [ ] The step that makes a feature reachable is last, or it is behind a flag.
- [ ] Flags for released features are removed.

## Checked
Confirmed 2026-11-09 against Martin Fowler's Continuous Integration article (section "Hide Work-in-Progress", lines 647-695, read in full). The original sources (the feature toggles article and trunkbaseddevelopment.com home page) were fetched but no keystone or dark-launching content was found in them, so they were dropped from `sources`.
Removed as unconfirmed: the checkout example PR chain as fact (kept as an illustrative sentence), the github/scientist and Scientist4J references, shadow-traffic and dual-write recipes, the Python mismatch-metric snippet, the 1-10% sampling advice and the side-effect and latency gotchas.
Method: docs-checked 2026-11-09 against martinfowler.com continuousIntegration (Hide Work-in-Progress)
