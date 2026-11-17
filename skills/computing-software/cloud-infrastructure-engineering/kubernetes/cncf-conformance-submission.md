---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cncf-conformance-submission
name: cncf-conformance-submission
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, conformance, k8s-conformance-submission, certified-kubernetes-submission, sonobuoy, hydrophone, cncf]
level: advanced
status: docs-checked
description: "Get a Kubernetes distribution or managed service Certified Kubernetes: run the full conformance suite, assemble the PR to cncf/k8s-conformance, and pass the automated checks."
sources: ["https://github.com/cncf/k8s-conformance/blob/master/instructions.md", "https://github.com/cncf/k8s-conformance/blob/master/terms-conditions/Certified_Kubernetes_Terms.md", "https://github.com/kubernetes-sigs/hydrophone/blob/main/docs/quickstart.md", "https://sonobuoy.io/docs/main/cli/sonobuoy_run/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submitting conformance results to cncf/k8s-conformance

## Prerequisites
- Certification is per Kubernetes minor version. A new offering can be self-certified for the
  current minor and the two preceding minors. Use of the marks for a minor lasts until the later
  of 12 months after that minor's release or 9 months after the next minor's release, unless you
  keep certifying each later minor.
- The vendor (legal entity) must have a signed Participation Form on file with CNCF.

## Run the full suite
Either Sonobuoy or Hydrophone (the two standard tools named in the instructions):
```bash
hydrophone --conformance --output-dir ./results       # add --conformance-image to pin the image
# or
sonobuoy run --mode=certified-conformance --wait
outfile=$(sonobuoy retrieve) && mkdir ./results && tar xzf $outfile -C ./results
```
`--mode=certified-conformance` is required for certification runs; a valid run may not skip
any conformance tests (manual settings must be `E2E_FOCUS=\[Conformance\]` with no `E2E_SKIP`).
The run can take an hour or more. Submission files: `e2e.log` and `junit_01.xml`
(Sonobuoy: `plugins/e2e/results/global/` in the tarball).

## The PR
Fork `cncf/k8s-conformance` and add a directory `vX.Y/<product-name>/` containing:
| File | Content |
|---|---|
| `PRODUCT.yaml` | vendor, name, version (of the product, not Kubernetes), website_url, documentation_url, type, description, contact_email_address; optional repo_url and product_logo_url |
| `README.md` | a script or human-readable description of how to reproduce the results |
| `e2e.log` | from the run |
| `junit_01.xml` | from the run |

PR title: `Conformance results for vX.Y/<product-name>`. One product and one Kubernetes
version per PR, in a single commit, with only the required files. The automated checks cover
the title, required files and directory structure, version match between title and folder,
PRODUCT.yaml fields and URL formats, `type` being `distribution`, `hosted platform` or
`installer`, the release still qualifying, all required tests present and none failed.

## Gotchas
- The Kubernetes minor in the title, folder and test results must match.
- Results from a run that skipped conformance tests are not a valid certification run.
- Anything "special" needed to pass must be in the README reproduction steps, so the results
  reflect the product as users get it.

## Verify
- [ ] Labels on the PR include `tests-verified-<version>`, `no-failed-tests-<version>`,
      `release-<version>` and `release-documents-checked`.

## Checked
Checked 2026-10-27 against cncf/k8s-conformance (instructions.md: required files, PRODUCT.yaml
fields, PR title format, one commit and one product per PR, requirement checks and pass
labels; Certified Kubernetes terms: eligible versions and the 12-month/9-month usage period),
the Hydrophone quickstart (`--conformance`, `--output-dir`) and the Sonobuoy `run` CLI reference
(`--mode=certified-conformance`, `--wait`). Corrected the bot label names, the renewal rule and
the PRODUCT.yaml required fields; removed unconfirmed runtime figures and a two-node minimum.

Method: documentation only; no commands were run.
