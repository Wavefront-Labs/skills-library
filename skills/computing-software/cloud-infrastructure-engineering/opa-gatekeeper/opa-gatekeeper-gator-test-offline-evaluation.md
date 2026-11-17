---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-gator-test-offline-evaluation
name: opa-gatekeeper-gator-test-offline-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, gator, gator-test, shift-left, exit-codes, deny-only, oci, filename]
level: practitioner
status: docs-checked
description: "Evaluate Kubernetes manifests against Gatekeeper templates and constraints offline with gator test, including inputs, exit codes and output formats."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/gator.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper gator test offline evaluation

`gator` (beta since v3.11) evaluates ConstraintTemplates and Constraints locally; install a release binary, Homebrew, or `go install` (needs master or v3.16.0+). `gator test` checks Kubernetes objects against policies and signals the result through its exit status; it also expands resources when a matching `ExpansionTemplate` is supplied.

Inputs: repeatable `--filename` (file or directory; only `.json`, `.yaml`, `.yml` are read), repeatable `--image` (alpha: a content-addressable OCI artifact of policy files, copied to a temp dir that `--tempdir` overrides; HTTPS by default, `--plain-http` for registries like `localhost:5000`), and stdin, in any combination.

Exit codes: `0` when ingest succeeds and no violations; `1` for errors (message on stderr) or for violations (details on stdout). Only `deny` (or empty) enforcement produces exit `1`; `dryrun` does not, and `warn` prints violations without failing, mirroring webhook rejection. `--deny-only` (3.19+) limits output to denied constraints. `--output yaml|json` gives structured violations on stdout.

The old name of `gator verify` was `gator test`; the names changed to align with other OPA projects.

## Checked

2026-11-04. Confirmed against gator.md (gator test inputs, exit codes, enforcement actions, output). Removed or corrected: nothing.

Method: documentation only; no commands were run.
