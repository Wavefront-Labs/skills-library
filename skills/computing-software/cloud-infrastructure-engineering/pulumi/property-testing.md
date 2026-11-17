---
id: computing-software.cloud-infrastructure-engineering.pulumi.property-testing
name: property-testing
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, property-test, property-testing, policy-testing, remote-policy-test]
level: practitioner
status: docs-checked
description: "Pulumi property tests: Pulumi Policies used as test assertions that run in the CLI during deployment, compared with unit and integration tests."
sources:
  - https://www.pulumi.com/docs/iac/concepts/testing/
  - https://www.pulumi.com/docs/iac/crossguard/core-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property testing

Property tests are based on Pulumi Policies: each policy becomes a property, an invariant, that a test evaluates and asserts. They run inside the Pulumi CLI before and after infrastructure is provisioned.

How the three styles differ:
- **Unit tests**: run quickly on mocked values and validate program logic.
- **Property tests**: policy rules see all input and output values of all cloud resources in the stack, including real values returned by the cloud provider rather than mocks. They validate key correctness invariants (for example "no public buckets").
- **Integration tests**: black-box, deploy to an ephemeral environment and test end to end.

Property tests can run against a persistent "acceptance" stack, an ephemeral environment per pull request, or both. Many teams combine all three.

To run a policy pack on a stack, pass it to the CLI (local execution works with any backend):
```bash
pulumi preview --policy-pack /path/to/policy-pack
```
A violation of a `mandatory` policy blocks the deployment. See `policy-pack-enforcement` for enforcement levels.

## Gotchas
- Keep the same pack in CI and in the policy group so tests and enforcement agree.
- Pulumi documents a TypeScript property-testing guide ("Property tests in TypeScript") that is the place to look for the test-harness code; this skill does not reproduce it.

## Checked
2026-11-03. Confirmed on the Pulumi testing overview page and the Policy as code page. The dedicated property testing page returned 404, so test-harness code was removed along with: the unit-test mock snippet, `echo $?` exit-code claim, drift (`refresh --expect-no-changes`) remark and the Verify paragraph.
Method: documentation only; no commands were run.
