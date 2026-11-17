---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-gator-verify-test-suites
name: opa-gatekeeper-gator-verify-test-suites
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, gator, gator-verify, test-suite, assertions, inventory, admissionreview, unit-testing]
level: advanced
status: docs-checked
description: "Write gator verify suites with tests and cases, assertions on violation counts and message regexes, inventory for referential policies, and AdmissionReview inputs."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/gator.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper gator verify test suites

`gator verify` runs Suites. A Suite file defines Tests; a Test compiles one ConstraintTemplate, instantiates one Constraint (its kind must equal `spec.crd.spec.names.kind`), optionally an ExpansionTemplate, and lists Cases. Paths in a Suite are relative to the Suite file, absolute paths are not allowed, and files that are not Suites are silently ignored. Tests in a Suite are independent.

A Case validates one object and sets `assertions`. Fields:
- `violations`: `yes` (at least one, the default), `no`, or a non-negative integer for an exact count.
- `message`: case-sensitive regular expression; empty matches all messages.

Multiple assertions per Case are allowed, for instance exactly two violations in total, exactly one containing `initContainer`, and exactly one containing `container`. You can assert that no violation matches a message by combining `violations: no` with that message.

A Case may list `inventory` files, objects placed in `data.inventory` to test referential constraints. To test metadata-dependent policies (operation, `userInfo`), give an `AdmissionReview` instead of a plain object; for DELETE put the deleted object in `oldObject`. Audit and `gator test` have no AdmissionReview metadata.

Run one Suite by path, all Suites recursively with a directory, or filter by test name using the regular-expression `run` flag.

## Checked

Method: docs-checked 2026-11-09 against the Gatekeeper website docs gator.md (raw markdown, the gator verify section read in full).
