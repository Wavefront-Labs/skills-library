---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.dependency-update-policy-dependabot-cadence-and-ee-base-images
name: dependency-update-policy-dependabot-cadence-and-ee-base-images
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, dependency-updates, dependabot-config, update-cadence, ee-image-updates]
level: practitioner
status: docs-checked
description: "Configure Dependabot for GitHub Actions, pip, Terraform and Docker with a schedule and ignore rules, and keep execution environment base images current."
sources: ["https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference", "https://ansible.readthedocs.io/projects/builder/en/latest/definition/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency update policy

## Dependabot config
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule: {interval: weekly}
  - package-ecosystem: pip
    directory: /
    schedule: {interval: weekly}
    ignore:
      - dependency-name: ansible-core
        update-types: ["version-update:semver-minor"]
  - package-ecosystem: terraform
    directory: /stacks/app
    schedule: {interval: weekly}
  - package-ecosystem: docker
    directory: /ee
    schedule: {interval: weekly}
```
Facts from the options reference:
- `package-ecosystem` values include `github-actions`, `pip`, `terraform` and `docker`.
- `schedule.interval` takes `daily`, `weekly`, `monthly`, `quarterly`, `semiannually`, `yearly` or `cron`.
- `ignore` with `update-types` accepts `version-update:semver-patch`, `-minor` and `-major`; for `update-types` under `allow`, the option only affects version updates, not security updates. Omitting `update-types` from an `allow` rule allows all update types.
- Dependabot assumes versions of the form `x.y.z` are major.minor.patch.
- The supported ecosystems list does not include Ansible Galaxy collections (requirements.yml) or the ansible-builder execution-environment definition, so those need a different tool or a manual process.

## EE base image updates
- ansible-builder definitions name a `base_image` (for example a ubi9 image from docker.io/redhat/ubi9, with an `ee-minimal` image from the Red Hat registry shown as an alternative in a comment). ansible-builder automatically installs dependencies of any collections you install into the final image.
- A base image with a floating tag like `latest` changes under you; rebuild on a schedule and record the digest you promoted. (Practitioner guidance; Docker's own best-practice page recommends pinning bases by digest and rebuilding often.)

## Cadence and patch policy (practitioner guidance)
- Security patches for OS and base images: fast-track with automated tests.
- Patch and minor updates of tools and actions: scheduled, CI green before merge.
- Core tool minors (ansible-core, Terraform provider majors): planned upgrades with the porting guide read and a full test run, which is why the example ignores ansible-core minor bumps.
Write the policy down (a target per severity) and measure update lag.

## Verify
- [ ] Dependabot opens PRs for each configured ecosystem, and pinned base images are rebuilt on your schedule.

## Checked
Method: docs-checked 2026-11-09 against the GitHub Dependabot options reference and the ansible-builder definition page.
Removed as unconfirmed: the groups block, the claim that Renovate has an ansible-galaxy manager (Renovate not read here; see the renovate skill), trivy/smoke playbook steps, the cadence table with day-count SLAs, automerge advice, and the "rebuilt in the last 7 days" check.
