---
id: computing-software.cloud-infrastructure-engineering.ansible.ci-check-mode-diffs-and-version-matrix
name: ci-check-mode-diffs-and-version-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ci-pipelines, ci-check-mode, ci-matrix, ansible-check-diff-review, github-actions]
level: practitioner
status: docs-checked
description: "Post Ansible check-mode diffs to pull requests and test roles across ansible-core and Python versions with a GitHub Actions matrix, using the documented support table."
sources: ["https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs", "https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# CI: check-mode diffs on PRs and version matrix

## Check-mode diff as a PR comment (GitHub Actions)
```yaml
jobs:
  plan:
    runs-on: [self-hosted, staging-network]
    steps:
      - uses: actions/checkout@v4
      - run: pip install ansible-core==2.19.* && ansible-galaxy install -r requirements.yml
      - name: Check mode against staging
        env:
          ANSIBLE_FORCE_COLOR: "false"
          ANSIBLE_DISPLAY_SKIPPED_HOSTS: "false"
          ANSIBLE_DISPLAY_OK_HOSTS: "false"
        run: |
          ansible-playbook -i inventories/staging playbooks/site.yml --check --diff \
            --vault-password-file <(echo "$VAULT_PASS") 2>&1 | tee plan.txt
      - name: Comment
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: plan.txt
```
- The Ansible docs call check mode "just a simulation": modules that support it report the changes they would make; others report nothing and do nothing. Label the PR comment as an approximation.
- `--diff` works alone or with `--check`; the docs warn it produces a large amount of output and is best used one host at a time (`--limit`). The ok/skipped display env vars above are a CI convenience (from the project, not these pages) to leave only changes.
- Hide diffs for sensitive data with `diff: false` on the task (documented example: a template writing `/etc/secret.conf`). The page does not mention `no_log`; add it yourself for secrets in task arguments.
- Check mode does not generate output for tasks with conditionals based on registered variables. Tasks that must run during `--check` can set `check_mode: false`; `ansible_check_mode` can gate tasks (`when: not ansible_check_mode`).

## Version matrix
```yaml
jobs:
  molecule:
    strategy:
      fail-fast: false
      matrix:
        include:
          - {ansible: "2.19", python: "3.12", experimental: false}
          - {ansible: "2.20", python: "3.13", experimental: false}
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "${{ matrix.python }}"}
      - run: pip install "ansible-core~=${{ matrix.ansible }}.0" molecule molecule-plugins[podman]
      - run: molecule test
```
Matrix mechanics (GitHub docs): `strategy.matrix` runs one job per combination, values read as `${{ matrix.name }}`; `include` adds keys or standalone combinations, `exclude` removes matches, `fail-fast: false` stops one failure cancelling the rest (set it explicitly), `max-parallel` caps concurrency, and `continue-on-error: ${{ matrix.experimental }}` lets flagged combinations fail without failing the run.

ansible-core support (release and maintenance page, read 2026-11-08): the latest release plus two older ones are maintained; majors ship about every six months (May and November). Controller Python: 2.16 and 2.17 3.10-3.12; 2.18 and 2.19 3.11-3.13; 2.20 3.12-3.14 (so 2.18 dropped controller Python 3.10). EOL: 2.16 July 2025, 2.17 Nov 2025, 2.18 May 2026, 2.19 Nov 2026, 2.20 May 2027. Check the page for versions newer than 2.20 before pinning. For collections, run `ansible-test` per core version (not covered by these pages).

## Gotchas
- Matrix explosion: test oldest supported and current (optionally devel as `experimental`) rather than every pair.
- Self-hosted runners reaching staging must not run untrusted fork PRs (general CI hygiene, not from the pages).

## Verify
- [ ] PR shows a check-mode comment; matrix jobs all green or experimental-only failures.

## Checked
Method: 2026-11-08 docs-only read of the Ansible check-mode page, the GitHub Actions matrix page and the ansible-core release/maintenance page. Updated the matrix from 2.16-2.18 (now end of life per the table) to 2.19/2.20 and added the documented support table; the claim that fail-fast defaults to true was not stated on the page, so it is set explicitly. Removed the "check mode skips commands" detail except as the generic simulation statement.
