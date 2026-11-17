---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.configuration-tests
name: configuration-tests
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [configuration-tests, config-file-testing, testing-for-reliability, conftest, kubeconform, config-drift]
level: practitioner
status: docs-checked
description: "Configuration tests per the SRE Book: compare how production is actually configured against the checked-in file, plus conftest policies and kubeconform schema checks."
sources: ["https://sre.google/sre-book/testing-reliability/", "https://www.conftest.dev/", "https://github.com/yannh/kubeconform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration tests

## SRE Book definition (Testing for Reliability)
- At Google, web service configurations are described in files in version control. For each configuration file, a separate configuration test examines production to see how a particular binary is actually configured and reports discrepancies against that file. Such tests are inherently not hermetic.
- Configuration tests are built and tested for a specific version of the checked-in file. Comparing which version of the test passes with the goal version for automation shows how far production lags behind engineering work.
- They are especially valuable in a distributed monitoring solution: the pattern of passes and fails across production can identify paths through the service stack with no sensible combination of local configurations, and rules match actual user-request paths from trace logs against those undesirable paths to raise alerts that a rollout is not proceeding safely.
- Simple case: production uses the actual file content and offers a real-time query to retrieve it, so the test issues that query and diffs the response against the file.
- Harder cases: configuration that implicitly incorporates defaults built into the binary (tests become separately versioned), passes through a preprocessor such as bash into command-line flags (tests are subject to expansion rules), or specifies behavioural context for a shared runtime (tests depend on that runtime's release schedule).
- Configuration is often kept separate from developer source, and test infrastructure often cannot see production configuration; a system test that passes against a configuration version for which the configuration test fails is valid hermetically but not operationally.
- Syntax choice matters: text in a custom syntax needs every category of test covered from scratch, while an existing syntax such as YAML with a heavily tested parser (the book names Python safe_load) removes some toil. Protocol buffers define the schema in advance and check it at load time.
- Example of defence in depth: an edit makes the parser stop after half of the user list; the tool that maintains home directories notices the mismatch and should report it urgently rather than remediate by deleting user data.

## Pre-push tools
- **conftest** uses Rego from Open Policy Agent. Policies default to a directory called `policy`, overridable with `--policy`. It looks for `deny`, `violation` and `warn` rules (optionally suffixed `_identifier`). Run `conftest test deployment.yaml`, and unit-test policies with `conftest verify --policy ./policy`.
- **kubeconform** validates Kubernetes manifests; its options include `-strict`, `-summary` and `-kubernetes-version`.

## Checked
- 2026-11-08: the SRE Book points above on the Testing for Reliability page; conftest policy location, rule names, `conftest test` and `conftest verify` on the conftest page; kubeconform flags on its README.
- Removed: the example Rego rules (replica and memory-limit policy), promtool, nginx and terraform commands, `amtool`, `router_check_tool`, ArgoCD and Flux drift commands, `terraform plan -detailed-exitcode`, and the checksum drift tip, none of which the cited pages cover.
Method: docs-only read of cited pages, 2026-11-08
