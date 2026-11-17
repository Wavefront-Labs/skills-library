---
id: computing-software.devops-ci-cd.ci-pipeline-design.deployment-pipeline-anatomy-and-commit-stage
name: deployment-pipeline-anatomy-and-commit-stage
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, deployment-pipeline, pipeline-stages, commit-stage, immutable-artifact, pipeline-gates, fast-feedback, continuous-delivery, value-stream]
level: practitioner
status: docs-checked
description: "Lay out a deployment pipeline: a fast commit stage, slower later stages, one immutable artifact promoted through gates, and the minimum practices for continuous delivery."
sources: ["https://martinfowler.com/bliki/DeploymentPipeline.html", "https://martinfowler.com/articles/continuousIntegration.html", "https://dora.dev/capabilities/continuous-delivery/", "https://minimumcd.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment pipeline anatomy and the commit stage

**Goal:** every change flows through the same sequence of increasingly thorough stages, and
the pipeline decides whether it can be released.

## 1. What a deployment pipeline is
Fowler: a build should be fast for quick feedback, but comprehensive tests take a long
time. A deployment pipeline breaks the build into stages; each stage gives increasing
confidence, usually at the cost of extra time. Early stages find most problems and give
faster feedback; later stages probe more slowly and thoroughly.
- The first stage usually does compilation and provides binaries for later stages.
- Later stages may include manual checks for tests that cannot be automated.
- Stages can be automatic or require human authorisation, and can be parallelised over many
  machines. Deploying into production is usually the final stage.
- The pipeline's job is to detect changes that will cause problems in production, including
  performance, security or usability issues. It should enable collaboration between the
  groups delivering software and give everyone visibility of the flow of changes, together
  with a thorough audit trail.
- A good way to introduce continuous delivery is to model your current delivery process as
  a pipeline, then look for bottlenecks, automation opportunities and collaboration points.

## 2. The commit stage (the "commit build")
In Fowler's CI article, the commit to mainline triggers the first build, the **commit
build**, which has to be done quickly and therefore takes shortcuts that reduce its ability
to detect bugs. The aim is to balance bug finding and speed so a good commit build is
stable enough for others to work on. The XP guideline of a ten-minute build is, for most
projects, within reason; DORA likewise reports that high performers get feedback from tests in
less than ten minutes, and gives about 10 minutes as the upper limit for tests in CI.

A simple two-stage pipeline: stage one compiles and runs localised unit tests, using test
doubles (a fake in-memory database, stubs of external services), within the ten minutes.
Stage two runs suites that hit a real database and exercise more end-to-end behaviour (Fowler
says that might take a couple of hours) and may run as often as it can on the last good
commit build. Each later-stage failure should lead to a new commit-stage test where possible.

## 3. Minimum practices for continuous delivery (minimumcd.org)
- Use continuous integration.
- The application pipeline is the only way to deploy to any environment.
- The pipeline decides releasability of changes, and its verdict is definitive.
- Artifacts created by the pipeline always meet the organisation's definition of deployable.
- Immutable artifact: no human changes after commit.
- All feature work stops when the main pipeline is red.
- Production-like test environment; rollback on demand.
- Application configuration deploys with the artifact.

## 4. Measuring and improving (DORA)
DORA recommends a value stream mapping exercise: follow a single change from version control
to release, measure total time, and for each process the elapsed time, the value-add time,
and the percentage complete and accurate (%C/A, how often work is sent back). Remove
obstacles with long elapsed time versus value-add time or poor %C/A. Because a pipeline
connects multiple teams, representatives from all teams should take part and agree a common
toolchain and processes. Outcome measures include lead time, change fail rate, time to
restore service and release frequency; the goal is low-risk releases in normal business hours.

## Verify
- [ ] The commit stage is fast, and its time is measured.
- [ ] Later-stage failures add tests to the commit stage where possible.
- [ ] The artifact that is deployed is the one the pipeline produced, unchanged.
- [ ] Pipeline status and audit trail are visible to everyone involved.

## Checked
Confirmed 2026-11-09: Fowler's Deployment Pipeline page (read in full), Fowler's Continuous Integration article (commit build and two-stage example, lines 549-630), DORA's continuous delivery capability page (continuous testing, value stream mapping, measures; lines 100-230 read), and the minimumcd.org home page (minimum CD and CI activities).
Removed as unconfirmed (the Humble and Farley chapters could not be read, and the book is no longer cited): the ASCII stage diagram with timings (30-60 min acceptance, nightly capacity), the "build once by digest" and stage ordering laws as stated, commit-stage contents list (version-stamp format, 5 min unit-test budget, vulnerability and licence scans), acceptance-stage detail, the GitHub Actions, GitLab, Jenkins and Argo CD mapping, and the anti-pattern list.
Method: docs-checked 2026-11-09 against martinfowler.com DeploymentPipeline and continuousIntegration, dora.dev continuous-delivery, minimumcd.org
