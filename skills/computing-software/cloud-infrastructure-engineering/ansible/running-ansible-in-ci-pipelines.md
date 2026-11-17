---
id: computing-software.cloud-infrastructure-engineering.ansible.running-ansible-in-ci-pipelines
name: running-ansible-in-ci-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ci-cd, ci-pipeline, pipeline, github-actions, gitlab-ci, jenkins, pre-commit, ansible-lint-action, molecule-ci, check-mode-ci, vault-in-ci, ssh-agent-ci, execution-environment-ci, ansible-navigator-ci, json-callback, junit-callback, deployment-pipeline, approval-gates, oidc]
level: advanced
status: gated
description: "Run Ansible from CI: lint and Molecule on PRs, --check --diff plan jobs, approved apply jobs with SSH keys and vault secrets injected safely, pinned EE images, JSON/JUnit output."
sources: ["https://docs.ansible.com/projects/lint/", "https://github.com/ansible/ansible/blob/devel/lib/ansible/errors/__init__.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/callback/json.py", "https://docs.github.com/en/actions", "https://docs.gitlab.com/ci/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Running Ansible in CI pipelines

**Goal:** every change is linted and tested on the PR, previewed as a diff, and
applied to prod only by the pipeline — from a pinned image, with secrets that never
touch the repo or the logs.

## 1. Stages
| Stage | Runs on | Command |
|---|---|---|
| lint | every push | `yamllint . && ansible-lint --profile production` |
| test | every PR | `molecule test` per role (matrix of distros) |
| plan | PR → main | `ansible-playbook site.yml --check --diff -l stage` → artefact/comment |
| apply stage | merge to main | `ansible-playbook site.yml --diff -l stage` |
| apply prod | manual approval / tag | `ansible-playbook site.yml --diff -l prod` with `serial` |
Pre-commit locally mirrors stage 1 (`.pre-commit-config.yaml` with `ansible-lint` hook).

## 2. A reproducible runner
Use the same execution environment image everywhere: `image: hub.example/acme/ee-platform:2.1`
in GitLab (`job.image`) or a container job in GitHub Actions, or `ansible-navigator run --mode stdout --eei <image> --pull-policy missing`.
Inside, `ansible-galaxy collection install -r requirements.yml` should be a no-op (already baked);
if it is not, the EE is stale. Pin `ansible-lint`/`molecule` versions in `requirements-dev.txt`.

## 3. Secrets
```yaml
# GitHub Actions excerpt
- uses: webfactory/ssh-agent@v0.9.0
  with: {ssh-private-key: "${{ secrets.ANSIBLE_SSH_KEY }}"}
- run: |
    install -m 0600 /dev/null .vault-pass && printf '%s' "$VAULT_PASS" > .vault-pass
    ansible-playbook site.yml --diff -l stage --vault-password-file .vault-pass
  env:
    VAULT_PASS: ${{ secrets.ANSIBLE_VAULT_PASS }}
    ANSIBLE_HOST_KEY_CHECKING: "true"
    ANSIBLE_FORCE_COLOR: "true"
```
- SSH key via agent (never written to the workspace); known_hosts seeded from a repo file (`ssh-keyscan` output committed and reviewed) or an SSH CA.
- Vault password from the CI secret store into a 0600 file (or a vault-client script using the job's cloud identity / OIDC — no long-lived secret at all).
- Cloud creds: OIDC federation (`aws-actions/configure-aws-credentials` with `role-to-assume`, GitLab `id_tokens`) instead of static keys.
- `no_log: true` on secret tasks; CI masking only hides exact secret strings, not derived values.
- Job logs are retained: avoid `-vvv` in apply jobs.

## 4. Machine-readable results
`ANSIBLE_STDOUT_CALLBACK=ansible.posix.json` (callback lives in the `ansible.posix` collection, not `ansible.builtin`) → one JSON doc (parse `stats`); or keep the
default output and enable `ANSIBLE_CALLBACKS_ENABLED=junit` with `JUNIT_OUTPUT_DIR=reports/`
so the CI shows per-task results. Exit codes (`ansible.errors.ExitCode`): 0 ok, 1 error, 2 failed hosts, 4 unreachable hosts (also used for a parser error), 5 invalid CLI option, 99 keyboard interrupt, 250 unknown error. Gate "plan" jobs on `changed=0` if the host should already be converged:
`grep -E 'changed=[1-9]' recap.txt && exit 1`.

## 5. Guard rails
- Protected branches + required checks (lint, molecule, plan) before merge.
- Environments with required reviewers for `prod` apply; concurrency group per environment so two applies never overlap (`concurrency: {group: prod-apply, cancel-in-progress: false}`).
- Inventory selection by variable, never by editing the job: `-l "${TARGET:?}"`; forbid `all` in prod apply via a pre-task `assert: ansible_limit is defined and ansible_limit != 'all'`.
- Timeouts on jobs (`timeout-minutes`) and in Ansible (`task_timeout`), so a hung host does not block the pipeline for hours.
- Keep `--check` jobs honest with `check_mode: false` on read-only commands (see the dry-run skill).

## GitLab CI skeleton
```yaml
stages: [lint, test, plan, apply]
default: {image: hub.example/acme/ee-platform:2.1}
lint: {stage: lint, script: [ansible-lint --profile production]}
plan: {stage: plan, script: [ansible-playbook site.yml --check --diff -l stage | tee plan.txt], artifacts: {paths: [plan.txt]}}
apply-prod:
  stage: apply
  script: [ansible-playbook site.yml --diff -l prod]
  environment: {name: prod}
  when: manual
  resource_group: prod
  only: [main]
```

## Gotchas
- Runners need network reach to the targets (or a bastion via `ProxyJump` configured in a committed `ssh_config` + `ansible_ssh_common_args`); the first failure is always connectivity, not Ansible.
- `ansible-lint` in CI picks up `.ansible-lint` config and `requirements.yml` collections — if it reports `couldn't resolve module`, the collections were not installed before lint.
- `--check` against brand-new hosts fails on tasks that depend on earlier changes; run plan jobs against converged stage hosts, not against empty VMs.
- Molecule in CI needs a container runtime with systemd support (`podman` on a VM runner, or `--privileged` Docker); GitHub-hosted runners can run Docker-based Molecule for most roles.
- A pipeline that applies to stage and prod from the same job with a loop defeats the approval gate; separate jobs, separate environments.

## Verify
- [ ] A PR shows lint, Molecule and a plan diff as checks; merge is blocked when lint fails.
- [ ] Prod apply requires a manual approval and cannot run concurrently with another prod apply.
- [ ] Secrets never appear in job logs (`grep -i vault` the log of a run that used them) and the SSH key is not on disk after the job.
- [ ] The apply job's `ansible --version` matches the pinned EE image and the recap is parsed into pass/fail.

## Checked

- Date: 2026-11-02.
- Confirmed against: only the existence of the ansible.posix json callback; general CI platform pages were overview-level.
- Not confirmed: the CI pipeline examples, secret names and the command line flags in them, which no fetched page states (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
