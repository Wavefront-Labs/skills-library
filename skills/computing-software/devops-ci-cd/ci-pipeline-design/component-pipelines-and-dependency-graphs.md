---
id: computing-software.devops-ci-cd.ci-pipeline-design.component-pipelines-and-dependency-graphs
name: component-pipelines-and-dependency-graphs
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, component-pipelines, loosely-coupled-architecture, independent-deployability, branch-by-abstraction, consumer-driven-contracts, can-i-deploy, pact-broker]
level: advanced
status: docs-checked
description: "Pipeline a system of many components so each deploys independently: DORA's loose-coupling practices, Pact can-i-deploy contract gates, and branch by abstraction for large changes."
sources: ["https://dora.dev/capabilities/loosely-coupled-teams/", "https://martinfowler.com/bliki/BranchByAbstraction.html", "https://docs.pact.io/pact_broker/can_i_deploy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component pipelines and dependency graphs

**Goal:** many components, each with its own fast pipeline, that stay independently
deployable instead of being deployed together as a pre-tested set.

## 1. What independence means (DORA: loosely coupled teams)
Practices DORA lists: teams make large design changes without outside permission, finish work
without fine-grained coordination, **deploy and release on demand independently of the
services they depend on or that depend on them**, do most testing on demand without an
integrated test environment, and deploy in normal business hours with negligible downtime.
DORA notes tightly coupled architectures stop services being tested and deployed
independently, and that loosely coupled setups need more sophisticated tooling and dependency
management.

To get there DORA suggests:
- well-defined contracts between services;
- mocking and stubbing of external services, so teams can create test environments quickly;
- contract testing, to check that dependencies on a service are still met;
- independent acceptance testing and deployment of each service, which it says real
  continuous delivery needs;
- blue/green or rolling deployment with heavy automation, to deploy at any time.

## 2. Contract gates with Pact can-i-deploy
The Pact docs contrast the old way (deploying sets of pre-tested applications together, a
bottleneck) with the Pact Matrix: a table of consumer and provider versions tested against
each other. The Broker knows each application's dependencies from its contracts; recording
deployments tells it which version is in each environment. Before deploying, ask:
```bash
pact-broker can-i-deploy --pacticipant Foo --version 23 --to-environment production
# exit code 0 = yes, 1 = no
```
and after a successful deployment record it (the docs recommend doing this for pre-prod
environments too):
```bash
pact-broker record-deployment --pacticipant Bar --version 56 --environment production
```
Other can-i-deploy features per the page: polling for verification results (for example when
a webhook triggers the provider build), ignoring specific integrations (a new provider without
verification yet), and a dry-run mode where the exit code is always successful, to test the
pipeline step before enforcing it. Tag-based usage is superseded by environments, deployments
and releases. Specifying an exact `--version` avoids race conditions.

## 3. Branch by abstraction (Fowler)
A technique for making a large change gradually while still releasing regularly:
1. Create an abstraction layer capturing how client code interacts with the current supplier;
   move client code to call the supplier through it, improving test coverage along the way.
2. Build the new supplier behind the same abstraction; feature flags can run it in test
   environments to compare its behaviour with the old one.
3. Switch clients over gradually; once the old supplier is unused, delete it, and optionally
   the abstraction.
Variations exist: sometimes everything must switch at once, or the supplier can be split into
sub-components migrated one at a time. The common theme is that the system builds and runs
correctly at all times, so continuous delivery continues during the replacement.

## 4. Pipeline design points (judgement, not from the sources)
- Give each component a versioned artifact and its own pipeline; make the version, not
  "latest", what downstream pipelines consume.
- Run the consumer's pipeline on dependency upgrades so the upgrade is tested before merging.
- Keep both old and new paths tested until the old one is removed.

## Verify
- [ ] Each component can be deployed without deploying others.
- [ ] A contract gate such as `can-i-deploy` runs before each deploy and deployments are recorded.
- [ ] Large replacements go through an abstraction on trunk, not a long-lived branch.

## Checked
Confirmed 2026-11-09 against the DORA loosely coupled teams page (practices list and contract, mocking and contract-testing guidance), Fowler's Branch By Abstraction page (read in full) and the Pact can-i-deploy page (matrix, commands, exit codes, features, tags note), from local text copies.
Removed as unconfirmed: the Humble and Farley chapter 13 material (book not readable), version-numbering and semantic-release advice, Renovate grouping config, upstream/downstream trigger tooling per CI product, the diamond and cycle handling and `madge`/`oasdiff` commands, the integration-pipeline `versions.yaml` manifest design, Argo CD app-of-apps, strangler fig, monorepo versus polyrepo comparison, and the Renovate source (never read).
Method: docs-checked 2026-11-09 against dora.dev loosely-coupled-teams, martinfowler.com BranchByAbstraction, docs.pact.io can_i_deploy
