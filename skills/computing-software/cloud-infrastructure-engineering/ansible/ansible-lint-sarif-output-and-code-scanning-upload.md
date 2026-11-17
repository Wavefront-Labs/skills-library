---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-sarif-output-and-code-scanning-upload
name: ansible-lint-sarif-output-and-code-scanning-upload
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, sarif, lint-ci-output, sarif-upload, code-scanning, codeclimate, security-scanning]
level: practitioner
status: docs-checked
description: "Emit ansible-lint (and other IaC scanner) results as SARIF or Code Climate JSON and upload them to GitHub code scanning or GitLab code quality for inline PR annotations."
sources: ["ansible-lint usage, output formats (https://ansible.readthedocs.io/projects/lint/usage/)", "GitHub Docs, uploading a SARIF file (https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github)", "GitLab Docs, Code Quality (https://docs.gitlab.com/ci/testing/code_quality/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-lint SARIF output and code scanning upload

## Output formats
```bash
ansible-lint -f sarif > ansible-lint.sarif        # SARIF JSON on stdout
ansible-lint -f codeclimate > gl-code-quality.json   # Code Climate JSON
ansible-lint -f pep8       # also: full, brief, md, quiet, json
ansible-lint --sarif-file ansible-lint.sarif       # write SARIF to a file and keep the normal output on stdout
```

## GitHub code scanning
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    permissions: {contents: read, security-events: write}
    steps:
      - uses: actions/checkout@v4
      - run: pip install ansible-lint
      - run: ansible-lint --sarif-file ansible-lint.sarif
        continue-on-error: true            # let upload run; fail later if you want a gate
      - uses: github/codeql-action/upload-sarif@v4
        with:
          sarif_file: ansible-lint.sarif
          category: ansible-lint
```
Findings show in the Security tab and as PR annotations. `category` (optional) separates results when several analyses of the same commit upload SARIF.

Gate: keep a separate step `ansible-lint` without `continue-on-error`.

## GitLab code quality
```yaml
ansible-lint:
  image: python:3.12
  script:
    - pip install ansible-lint
    - ansible-lint -f codeclimate > gl-code-quality-report.json || true
  artifacts:
    reports:
      codequality: gl-code-quality-report.json
```
GitLab's report must be a single JSON array in its Code Climate-derived format (description, check_name, fingerprint, location, severity). ansible-lint's own docs recommend SARIF over Code Climate when possible because Code Climate output does not carry the rule severity.

## Gotchas
- Run ansible-lint from the project root, as its docs require, so reported paths match the repository layout.
- GitHub limits the size of a SARIF upload; check the SARIF support reference for the current limits and exclude vendored roles and collections with `exclude_paths`.
- For private and internal repositories, code scanning needs GitHub Code Security enabled for the repository.
- `continue-on-error` hides failures if you forget the gate step.

## Verify
- [ ] A PR introducing a `no-changed-when` violation shows an inline annotation on the line.

## Checked
Checked 2026-10-23: ansible-lint usage.md and cli.py (latest release v26.10.1) for the format choices (brief, full, md, json, codeclimate, quiet, pep8, sarif) and `--sarif-file`; the GitHub Docs SARIF upload page for `security-events: write`, `github/codeql-action/upload-sarif@v4`, the optional `category` input and the Code Security requirement for private repositories; the GitLab Code Quality page for the single-JSON-array report format. Removed the unconfirmed pinned version `25.*`, the 10 MB / 25k result limits (the upload page defers to the SARIF support reference), the list of other scanners' SARIF flags, the branch-protection sentence and the SAST-converter sentence. Note: `-f json` is an alias that changed meaning between releases, so it is not recommended here.
Method: documentation only; no commands were run.
