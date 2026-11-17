---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-testing-with-terratest
name: terraform-testing-with-terratest
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terratest, go, golang, go-test, infrastructure-testing, integration-testing, module-testing, terraform-test, tftest, test-structure, http-helper, retry, unique-id, t-parallel, test-stages, cloud-nuke, sandbox-account, ci-testing]
level: advanced
status: docs-checked
description: "Integration-test Terraform modules with Terratest (Go): apply real infra from examples/, assert via outputs and HTTP checks with retries, always destroy, unique names."
sources: ["https://terratest.gruntwork.io/docs/getting-started/quick-start/", "https://terratest.gruntwork.io/docs/testing-best-practices/timeouts-and-logging/", "https://terratest.gruntwork.io/docs/testing-best-practices/iterating-locally-using-test-stages/", "https://terratest.gruntwork.io/docs/testing-best-practices/cleanup/", "https://terratest.gruntwork.io/docs/testing-best-practices/namespacing/", "https://terratest.gruntwork.io/docs/testing-best-practices/idempotent/", "https://terratest.gruntwork.io/docs/testing-best-practices/testing-environment/", "https://raw.githubusercontent.com/gruntwork-io/terratest/main/test/terraform_aws_hello_world_example_test.go", "https://developer.hashicorp.com/terraform/language/tests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform testing with Terratest: deploy it, poke it, tear it down

**Goal:** each module release is proven by actually creating its example in a sandbox
account, checking it *works* (not just that it applied), and destroying it, with tests
that never leak resources.

## 1. Pick the right test layer
- Native `terraform test`: available in Terraform v1.6.0 and later; test files end in
  `.tftest.hcl` (or `.tftest.json`); a `run` block can set `command = plan`; mocking provider
  data was added in v1.7.0. No Go needed, so use it first for plan-level assertions.
- **Terratest** (Go): use when the test must deploy real infrastructure and then validate it
  with HTTP requests, API calls or SSH connections. It is slower and costs money, so decide
  how often to run it (PRs touching the module, nightly) rather than on every commit.
- Run tests in an environment totally separate from production, for AWS a completely
  separate account. That means the module takes environment details (account IDs, domain
  names, IP addresses) as inputs.

## 2. Layout
Infrastructure code lives in `examples/`, Go tests in `test/`, which is its own Go module:
```
modules/service/
  examples/basic/        # the fixture: a real root module calling ../../
  test/
    go.mod               # go mod init "<MODULE_NAME>", then go mod tidy
    service_test.go
```
Terratest's terraform helpers run whichever binary you point at: by default `terraform` when
it is on PATH, otherwise `tofu`. To pin OpenTofu set `TerraformBinary: "tofu"` in
`terraform.Options`.

## 3. A test
Shape of the upstream hello-world example (current main uses the `/v2` module paths and
`...Context` helper variants; if your `go.mod` pins an older release, check that release's
helper names, which differ):
```go
func TestServiceBasic(t *testing.T) {
	t.Parallel()

	opts := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../examples/basic",
		Vars:         map[string]interface{}{"name": "tt-" + random.UniqueID()},
	})

	defer terraform.DestroyContext(t, t.Context(), opts) // registered BEFORE apply
	terraform.InitAndApplyContext(t, t.Context(), opts)

	url := "http://" + terraform.OutputContext(t, t.Context(), opts, "public_ip") + ":8080"
	httphelper.HTTPGetWithRetryContext(t, t.Context(), url, nil, 200, "Hello, World!", 30, 5*time.Second)
}
```
Imports are `github.com/gruntwork-io/terratest/modules/terraform/v2`,
`.../modules/httphelper/v2` and `.../modules/core/v2/random`.

Run it with an explicit timeout: `cd test && go test -v -timeout 30m`. Go's default test
timeout is 10 minutes, after which it kills the tests and even cleanup code does not run, so
always raise it with `-timeout`.

## 4. Assertions that matter
- Behaviour, not just apply success: an HTTP request returns the expected status and body,
  with retries because a new server can take 1 to 2 minutes to boot.
- Idempotence: a second apply must produce 0 changes. `terraform.ApplyAndIdempotentContext`
  applies and fails the test if the second apply changes anything.

## 5. Namespacing and parallel runs
Name every resource a test creates with a unique suffix so it cannot overwrite anything in the
account or clash with tests running in parallel. `random.UniqueID()` gives a 6-character
identifier. Expose the names (auto scaling group, security group, IAM role and so on) as
module variables so the test can set them.

## 6. Faster iteration with stages
Split a test into stages with the `teststructure` package (`RunTestStage`, plus
`SaveString`/`LoadString`, `SaveTerraformOptions`/`LoadTerraformOptions` to pass data between
stages). Set `SKIP_<stage_name>` to any non-empty value to skip a stage, for example
`SKIP_build_ami=true go test -v -run TestTerraformPackerExample`. Each stage saves its outputs
to the working directory for later stages to load, and when any `SKIP_*` variable is set
Terratest also skips copying to a temp folder, preserving cached state. Do not set `SKIP_`
variables in CI.

## 7. Cleanup and logging in CI
- Use `defer` for destroy so cleanup runs even when the test errors.
- Cleanup can still fail (CI server down, bug, network outage); Gruntwork runs `cloud-nuke`
  in its test AWS account nightly to remove leftovers. A scheduled reaper is the safety net.
- Go's `t.Log`/`t.Logf` buffer output until the test ends, so a long test can look hung to a
  CI system that kills jobs after about 10 silent minutes (CircleCI is the page's example).
  Use Terratest's `logger.Log`/`logger.Logf`, which write to stdout immediately.
- Go also buffers output per package until all its tests finish; `go test -timeout 30m -p 1 ./...`
  tests packages sequentially.

## Gotchas
- A test killed by timeout or a cancelled CI job skips its `defer`, so the reaper is not optional.
- Newly created infrastructure needs time to become reachable: use the retrying HTTP helper
  (the example uses 30 retries at 5-second intervals) rather than a fixed sleep.
- Helper names and import paths changed between Terratest major versions; pin the version in
  `go.mod` and read that version's docs when upgrading.

## Verify
- [ ] `go test -v -timeout 30m` passes in the sandbox and leaves no resources afterwards.
- [ ] Each test asserts behaviour (and idempotence), not only that `apply` succeeded.
- [ ] Resource names carry a unique suffix.
- [ ] A scheduled cleanup job covers tests killed mid-run.

## Checked
Checked 2026-11-08 against the Terratest docs (quick start, timeouts and logging, test stages, cleanup, namespacing, idempotent, testing environment), the upstream hello-world and packer example tests on main, and the Terraform tests page.
Removed: tflint and terraform-docs, `aws-nuke`, SDK helper names such as `aws.GetS3BucketVersioning`, `CopyTerraformFolderToTemp`, `RetryableTerraformErrors`, `InitAndPlanWithExitCode`, and the CIDR and quota guidance, none of which the cited pages state. Old helper names were replaced with the forms current on main.
Method: docs-only read of cited pages, 2026-11-08
