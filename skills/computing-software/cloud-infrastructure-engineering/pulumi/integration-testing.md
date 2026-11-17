---
id: computing-software.cloud-infrastructure-engineering.pulumi.integration-testing
name: integration-testing
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, integration-test, integration-testing, programtest, ephemeral-stack]
level: practitioner
status: docs-checked
description: "Choose an integration testing approach for Pulumi programs: the Go integration framework, Automation API, or shell scripts against ephemeral stacks."
sources:
  - https://www.pulumi.com/docs/iac/concepts/testing/integration/
  - https://www.pulumi.com/docs/iac/concepts/testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integration testing

Integration tests run the program with the Pulumi CLI or Automation API, deploy to an ephemeral environment, test the results from the outside ("black-box"), and usually destroy the infrastructure afterwards.

They verify that: the code runs without errors; stack config and secrets are interpreted correctly; the project deploys to your cloud; resources of the desired shape are created; the infrastructure behaves as expected (a health-check endpoint returns a valid document, application-level tests pass against the public API); the project can be updated from its starting state to other states; and it can be destroyed cleanly.

## Options
| Approach | Good for | Constraints |
|---|---|---|
| Go integration testing framework | Drives lifecycle: deploy a new stack, optionally update with variations, tear down; tests update/upgrade paths; runs programs written in any supported language | Tests must be written in Go |
| Automation API | Tests in your preferred language and test framework, full programmatic control of the stack lifecycle (Node.js, Python, .NET, Go, Java) | Not available in YAML |
| DIY shell | Any language; only the Pulumi CLI needed | More manual error handling, less type-safe, harder to extract resource properties |

## Gotchas
- Unlike unit tests (mocked cloud) these deploy real infrastructure: always destroy what you create, and use a separate stack per run.
- Policy as Code checks expectations on specific resources; integration tests check behavior end to end. Many teams combine unit, property and integration tests.

## Checked
2026-11-03. Confirmed on the Pulumi integration testing page and the testing overview. Removed: all `integration.ProgramTest` Go code and Automation API TypeScript snippets, the `EditDirs` and nightly sweeper remarks, and the Verify paragraph; none are documented on pages read. See the Pulumi Automation API and the integration framework docs for code.
Method: documentation only; no commands were run.
