---
id: computing-software.systems-network-administration.patch-management.patch-orchestration-satellite-foreman-landscape
name: patch-orchestration-satellite-foreman-landscape
category: computing-software
field: systems-network-administration
product: patch-management
tags: [satellite, foreman, katello, landscape, uyuni, content-views, errata, patch-orchestration]
level: advanced
status: draft
description: "Orchestrate Linux patching at scale with Red Hat Satellite/Foreman-Katello content views and errata jobs, and Canonical Landscape, including staged promotion through environments."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_satellite/6.15/html/managing_content/index
  - https://docs.theforeman.org/
  - https://ubuntu.com/landscape/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch orchestration with Satellite, Foreman and Landscape

**Goal:** freeze a tested package set, promote it through environments, and apply it to fleets on schedule.

## Satellite / Foreman + Katello
Concepts: **repositories** sync vendor content; a **content view** is a versioned snapshot of selected repos (with filters); **lifecycle environments** (Library -> Dev -> Test -> Prod) receive promoted versions; hosts attach to a content view + environment.
```bash
hammer repository synchronize --organization ACME --product 'Red Hat Enterprise Linux for x86_64' --name 'RHEL 9 BaseOS RPMs x86_64'
hammer content-view publish --organization ACME --name cv-rhel9 --description "2026-10 patch cycle"
hammer content-view version promote --organization ACME --content-view cv-rhel9 --version 42 --to-lifecycle-environment Test
# after testing
hammer content-view version promote --organization ACME --content-view cv-rhel9 --version 42 --to-lifecycle-environment Prod
hammer job-invocation create --job-template 'Install errata by search query - Katello Script Default' \
  --inputs 'Errata search query=type = security' --search-query 'lifecycle_environment = Prod and host_collection = web-ring1'
```
Hosts in Prod can only see packages in the promoted version, so "dnf update" is reproducible across rings.

## Canonical Landscape (Ubuntu)
- Register clients (`landscape-config --computer-title ... --account-name ...`).
- Use repository profiles pointing to snapshot mirrors, tags for rings, and "Upgrade packages" activities scheduled per tag; security-only option available.
- Ubuntu Pro adds Livepatch and ESM through the same management.

## Uyuni / SUSE Manager
Similar model with channels cloned per environment (Content Lifecycle Management) and Salt-based actions.

## Gotchas
- Publishing a content view without promotion does nothing for Prod hosts; promotions are the gate.
- Filters that exclude packages also exclude their errata; test dependency resolution in Dev.

## Verify
Hosts in each environment report the expected content view version, and applicable errata counts in Prod drop to zero after the job.
