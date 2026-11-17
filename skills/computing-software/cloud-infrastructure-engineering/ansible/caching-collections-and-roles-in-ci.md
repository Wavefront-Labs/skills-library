---
id: computing-software.cloud-infrastructure-engineering.ansible.caching-collections-and-roles-in-ci
name: caching-collections-and-roles-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ci-pipelines, collection-caching, ci-cache, github-actions-cache, gitlab-ci-cache, pip-cache, requirements-yml, execution-environments]
level: practitioner
status: docs-checked
description: "Cut Ansible CI time by caching pip, Galaxy collections and roles keyed on requirements file hashes in GitHub Actions and GitLab CI, or by baking them into a CI image or EE."
sources: ["GitHub actions/cache README (https://github.com/actions/cache)", "GitHub actions/setup-python README (https://github.com/actions/setup-python)", "GitLab CI caching (https://docs.gitlab.com/ci/caching/)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caching collections and roles in CI

Goal: stop downloading `ansible-core`, `community.general` (large) and friends on every job,
and stop failing when Galaxy is slow or down — without ever running stale versions.

## What to cache, keyed on what
| Path | Key |
|---|---|
| pip cache directory | hash of `requirements.txt` |
| `./collections` (installed with `-p ./collections`) | hash of `collections/requirements.yml` |
| `./roles` (`ansible-galaxy role install -p ./roles`) | hash of `roles/requirements.yml` |
Pin exact versions in the requirements files; a cache keyed on a file with `>=` ranges freezes
whatever version was first resolved.

## GitHub Actions
```yaml
- uses: actions/setup-python@v7
  with: {python-version: "3.12", cache: pip}
- run: pip install -r requirements.txt
- uses: actions/cache@v6
  id: galaxy
  with:
    path: |
      collections/ansible_collections
      roles/external
    key: galaxy-${{ runner.os }}-${{ hashFiles('collections/requirements.yml', 'roles/requirements.yml') }}
- if: steps.galaxy.outputs.cache-hit != 'true'
  run: |
    ansible-galaxy collection install -r collections/requirements.yml -p ./collections
    ansible-galaxy role install -r roles/requirements.yml -p ./roles/external
```

## GitLab CI
```yaml
cache:
  - key: {files: [collections/requirements.yml]}
    paths: [collections/ansible_collections]
before_script:
  - pip install -r requirements.txt
  - ansible-galaxy collection install -r collections/requirements.yml -p ./collections   # no-op when cached versions satisfy
```
`ansible-galaxy collection install` skips collections that are already installed ("is already installed, skipping"), so running it unconditionally after a cache restore is cheap. GitLab allows up to four caches per job and `cache:key:files` derives the key from the content of the listed files.

## Better for many repos: bake an image
Build a CI image or execution environment with the collections already installed
(`ansible-builder` with `requirements.yml`), tag it with the requirements hash, and run jobs in
it (`container:` in GitHub, `image:` in GitLab, `ansible-navigator --eei`). No cache logic, and
CI uses the same EE as production.

## Gotchas
- Caching `~/.ansible/collections` while also installing to `./collections`: two copies, unclear winner. Pick one path and set `collections_path` in `ansible.cfg`.
- Git-sourced collections/roles pinned to a branch never change the cache key; pin to tags or commit SHAs.

## Verify
- [ ] Second run shows a cache hit and the install step is skipped or reports collections as already installed.
- [ ] Bumping a version in `collections/requirements.yml` produces a cache miss and the new version in `ansible-galaxy collection list -p ./collections`.

## Checked

Checked 2026-10-26 against the actions/cache and actions/setup-python READMEs (latest releases v6.1.0 and v7.1.0), the GitLab CI caching documentation (gitlabhq mirror) and ansible-core devel (`lib/ansible/galaxy/collection/__init__.py`). Fixed stale action versions (v5 and v4 to v7 and v6). Confirmed `cache: pip` input, `cache-hit` output, GitLab `cache:key:files`, the four-cache limit and the "already installed, skipping" behaviour. Removed the unconfirmed GitLab pip cache variable and cache-on-failure claims.

Method: documentation only; no commands were run.
