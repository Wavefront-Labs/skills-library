---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-acceptance-tests-with-terraform-plugin-testing
name: provider-acceptance-tests-with-terraform-plugin-testing
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, acceptance-tests, resource-test, terraform-plugin-testing, provider-development, go, statecheck, plancheck, import-state-verify, sweepers]
level: advanced
status: gated
description: "Write provider acceptance tests with terraform-plugin-testing: resource.Test steps, state and plan checks, import verification, destroy checks, sweepers and CI gating."
sources: ["https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests", "https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests/teststep", "https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests/state-checks", "https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests/sweepers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider acceptance tests

Acceptance tests run a real Terraform binary against the real API through your
provider. They are the only tests that catch perpetual diffs, broken import and
leaked resources, so every resource gets at least: create, update, import, destroy.

## 1. Skeleton
```go
func TestAccWidget_basic(t *testing.T) {
    name := acctest.RandomWithPrefix("tf-acc")
    resource.ParallelTest(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },      // fail fast on missing env creds
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,   // framework provider
        CheckDestroy:             testAccCheckWidgetDestroy,
        Steps: []resource.TestStep{
            {   // create
                Config: testAccWidgetConfig(name, 1),
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue("widget_thing.test",
                        tfjsonpath.New("size"), knownvalue.Int64Exact(1)),
                },
            },
            {   // update in place, and prove it is not a replace
                Config: testAccWidgetConfig(name, 2),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectResourceAction("widget_thing.test", plancheck.ResourceActionUpdate),
                    },
                },
            },
            {   // import round-trip
                ResourceName:            "widget_thing.test",
                ImportState:             true,
                ImportStateVerify:       true,
                ImportStateVerifyIgnore: []string{"password"}, // write-only / not returned by API
            },
        },
    })
}
```
Packages: `github.com/hashicorp/terraform-plugin-testing/{helper/resource,helper/acctest,statecheck,plancheck,knownvalue,tfjsonpath}`. (gated: unconfirmed, source is paywalled or blocked)

## 2. What the harness already does
- After every `Config` step it runs another plan and fails with "After applying this
  test step, the plan was not empty" if anything would change. That is the idempotency
  check; do not disable it with `ExpectNonEmptyPlan` unless the drift is intended.
- After the last step it destroys everything and calls `CheckDestroy`, which must
  query the API and return an error if the object still exists.

## 3. Negative and drift cases
- Validation: `ExpectError: regexp.MustCompile("size must be between")` on a step.
- Out-of-band delete: a step with `PreConfig` that deletes the object through the
  API client, then the same config with a `PreApply` check for `ResourceActionCreate`.
  This proves `Read` calls `RemoveResource` instead of erroring.
- Schema upgrade: a first step pinned to the previous release via
  `ExternalProviders: map[string]resource.ExternalProvider{"widget": {Source: "acme/widget", VersionConstraint: "1.4.0"}}`,
  then a step on the new code with `plancheck.ExpectEmptyPlan()`.

## 4. Running
```bash
TF_ACC=1 go test ./internal/provider -run 'TestAccWidget_' -v -timeout 120m -parallel 4
```
Without `TF_ACC` the tests skip. Pin the CLI with `TF_ACC_TERRAFORM_VERSION=1.9.8` (or
`TF_ACC_TERRAFORM_PATH`) so CI and laptops test the same core; add a matrix over the
oldest and newest supported Terraform versions. `resource.UnitTest` exists for tests that
need no API (provider functions, validators).

## 5. Sweepers
Failed runs leak resources. Register a sweeper that deletes everything prefixed
`tf-acc`, wire `func TestMain(m *testing.M) { resource.TestMain(m) }`, and run
`go test ./internal/provider -v -sweep=<region>` nightly before acceptance tests.

## Gotchas
- `resource.ParallelTest` plus shared fixtures (one account quota, one DNS zone) gives
  flaky conflicts; use random names everywhere and `resource.Test` for singleton APIs.
- `ImportStateVerify` failing on a field means `Read` does not set it. Fix `Read`
  before reaching for `ImportStateVerifyIgnore`.
- Real credentials live in CI secrets for a dedicated test account, never production.

## Verify
- [ ] Each resource has create, update, import and disappears tests passing with `TF_ACC=1`.
- [ ] `CheckDestroy` queries the API, not state.
- [ ] Sweeper run leaves no `tf-acc` objects in the test account.

## Checked

2026-11-02

- Confirmed: Terraform plugin testing acceptance-tests, test step and sweepers pages were fetched.
- Removed or gated: The state-checks page is a stub and the fetched pages do not show every helper (statecheck, plancheck, knownvalue) name or the TF_ACC_TERRAFORM_VERSION variable; gated, confirm in the plugin testing docs.

Method: documentation only; no commands were run.
