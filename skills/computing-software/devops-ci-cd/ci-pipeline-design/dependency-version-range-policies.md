---
id: computing-software.devops-ci-cd.ci-pipeline-design.dependency-version-range-policies
name: dependency-version-range-policies
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, version-ranges, dependency-pinning, component-pipelines]
level: practitioner
status: docs-checked
description: "Set version range policies for internal and external dependencies: exact pins vs caret/tilde ranges for apps vs libraries, lockfiles, and how updates flow through pipelines."
sources: ["https://semver.org/", "https://peps.python.org/pep-0440/", "https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency version range policies

## Rule of thumb
| Artifact | Declare | Why |
|---|---|---|
| Applications/services | exact versions or ranges + **committed lockfile** | reproducible builds |
| Libraries published for others | compatible ranges (a lower bound plus a cap at the next major) | avoid diamond conflicts for consumers |
| Internal libraries in a monorepo | your package manager's workspace mechanism | always latest in-repo |
| Docker base images, CI actions | digests | immutable |

## Range syntax cheat sheet
- Python (PEP 440): the compatible release clause `~=` allows later versions within the stated precision (`~=3.1.2` is 3.1.2 or later but below 3.2.0); `~=` needs at least two segments. Libraries should avoid upper caps unless known-breaking.
- Cargo: a caret requirement is the default (`log = "^1.2.3"` is the same as `log = "1.2.3"`); tilde requirements (`~1.2.3`) allow only patch-level updates.
- Other ecosystems: read the package manager's range documentation; ranges generally defeat reproducibility, so pair them with a lockfile.

## Pipeline flow
- Lockfile enforced in CI (your package manager's frozen or locked install mode).
- Renovate/Dependabot updates the lockfile and pins; groups minor/patch; majors are separate PRs.
- Library CI tests against both lowest and highest allowed versions
  to keep declared lower bounds honest (use your resolver's lowest-version option).

## Checked
2026-11-01. Confirmed from PEP 440 (`~=` semantics) and the Cargo dependency reference (caret default, tilde). Removed npm, Maven
and Go range specifics, workspace protocol, and specific lockfile and resolver command lines (not confirmed).
Method: documentation only; no commands were run.

## Verify
- [ ] Fresh clone + CI install produces the same dependency tree as the lockfile; lowest-version job passes for libraries.
