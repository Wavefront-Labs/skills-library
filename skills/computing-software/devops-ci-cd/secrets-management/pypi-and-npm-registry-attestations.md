---
id: computing-software.devops-ci-cd.secrets-management.pypi-and-npm-registry-attestations
name: pypi-and-npm-registry-attestations
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, pep-740, pypi-attestations, npm-provenance, provenance-attestations]
level: advanced
status: verified
description: "Publish packages with registry-verified attestations (PyPI PEP 740 via trusted publishing, npm provenance) and verify them as a consumer."
sources: ["https://docs.pypi.org/attestations/", "https://peps.python.org/pep-0740/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PyPI PEP 740 and npm registry attestations

## PyPI (PEP 740)
With **Trusted Publishing** from GitHub Actions (or GitLab CI), `pypa/gh-action-pypi-publish`
(latest v1.14.2) generates and uploads attestations for each distribution automatically (README: on by default for Trusted Publishing; set `attestations: false` to disable; not supported for token auth):
```yaml
permissions: { id-token: write }
steps:
  - uses: actions/download-artifact@<sha>
    with: { name: dist, path: dist/ }
  - uses: pypa/gh-action-pypi-publish@release/v1     # attestations: true is the default
```
PyPI shows "Verified details" with the publishing repository and workflow. Attestations are
available from the Integrity API: `GET https://pypi.org/integrity/<project>/<version>/<filename>/provenance` (run: HTTP 200 for `cyclonedx_bom-7.5.0-py3-none-any.whl`, `pip_audit` and `sigstore` wheels; JSON with `attestation_bundles`).

Consumer verification:
```bash
pip install pypi-attestations
pypi-attestations verify pypi --repository https://github.com/org/project pypi:project-1.2.3-py3-none-any.whl
```
Run (pypi-attestations 0.0.30): `--repository https://github.com/CycloneDX/cyclonedx-python pypi:cyclonedx_bom-7.5.0-py3-none-any.whl` printed `OK: ...`; with `org/wrong` it exited 1: `provenance was signed by repository "CycloneDX/cyclonedx-python", expected "org/wrong"`.

## npm
```bash
npm publish --provenance --access public     # in GitHub Actions/GitLab CI with id-token
```
Trusted publishing for npm (OIDC, no tokens) publishes provenance automatically.
Verify installed packages:
```bash
npm audit signatures     # checks registry signatures and provenance attestations
```
Run on npm 10.8.2 after `npm i sigstore`: `51 packages have verified registry signatures` and `21 packages have verified attestations`. The command needs an installed `node_modules` and a lockfile.

## Gotchas
- Attestations bind to the CI identity; building in one job and publishing in another is fine as
  long as the publishing workflow is the trusted publisher configured on the registry.
- npm docs: provenance requires a supported cloud CI/CD provider (GitHub Actions or GitLab CI/CD) using a cloud-hosted runner.
- Attestations prove where it was built, not that the code is safe.

## Verify
- [ ] Package page shows provenance/verified publisher; `npm audit signatures` or `pypi-attestations verify` succeeds.
