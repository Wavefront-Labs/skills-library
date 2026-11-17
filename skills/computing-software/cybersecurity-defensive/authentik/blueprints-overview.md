---
id: computing-software.cybersecurity-defensive.authentik.blueprints-overview
name: blueprints-overview
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, blueprints, configuration-as-code, oci, instances, discovery]
level: advanced
status: docs-checked
description: "How authentik blueprints are applied, stored (local file, OCI, database), discovered and executed atomically, and how to avoid auto-instantiation."
sources:
  - https://docs.goauthentik.io/customize/blueprints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: template and automate authentik configuration as YAML. The `default-authentication-flow` itself comes from a blueprint.

## Applying
- **Blueprint instance**: refers to a YAML file (mounted in the worker container, in an OCI registry, or in the database). Create via **Blueprints > New Blueprint**: unique name, file, and **Context** (JSON or YAML) which fills `!Context` tags. Several instances can use one file.
- **Imported flow**: **Import** on Flows or Blueprints pages; **Local path** (bundled examples) or **File upload**. Applied once, not watched afterwards.
Modifying a default flow and saving yields a merge of the blueprint plus your changes; to reset, delete the modified flow first, then re-apply its blueprint. Review imports: they can contain policies, users and groups.

## Discovery
authentik watches the blueprint directory; new files trigger discovery and an auto-created instance, modified files trigger apply. It also rescans every 60 minutes by default (change under **System Tasks > Schedules**, task `authentik.blueprints.v1.tasks.blueprints_discovery`). Prevent auto-instantiation:
```yaml
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
```

## Execution
All entries run in one atomic transaction: any failure rolls back the whole blueprint. Built-in context variables: `goauthentik.io/enterprise/licensed` and `goauthentik.io/rbac/models` (`conditions: - !Context goauthentik.io/enterprise/licensed`). Discovery and evaluation order between blueprints is not guaranteed; if blueprints depend on each other, use meta models to create objects in the correct order.

## Storage
Local: `/blueprints` with `default`, `example`, `system` subdirectories; mount an empty file over one to disable it. File blueprints vanish when unavailable but created objects stay. OCI: `oci://ghcr.io/<username>/<package-name>:<ref>`, re-fetched each run, credentials embeddable; push with `oras push ghcr.io/<username>/blueprint/<blueprint name>:latest <yaml file>:application/vnd.goauthentik.blueprint.v1+yaml`. Database: lets tools like Terraform manage them; validated on submission.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/customize/blueprints/ (read in full); dropped the !Env/!File re-apply claim and the !KeyOf/!Find ordering claim, which the page does not state.
