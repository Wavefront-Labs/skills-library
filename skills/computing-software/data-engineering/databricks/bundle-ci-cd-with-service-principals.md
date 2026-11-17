---
id: computing-software.data-engineering.databricks.bundle-ci-cd-with-service-principals
name: bundle-ci-cd-with-service-principals
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-asset-bundles, databricks-cicd, service-principal, github-actions, oidc, workload-identity-federation, oauth-m2m, run-as]
level: practitioner
status: docs-checked
description: "Deploy Databricks Asset Bundles from CI with a service principal: OAuth M2M or GitHub OIDC federation, per-environment SPs, run_as, and gating prod on tests."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/bundles/ci-cd-bundles
  - https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m
  - https://docs.databricks.com/aws/en/dev-tools/auth/oauth-federation
  - https://github.com/databricks/setup-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle CI/CD with service principals

**Goal:** no human credential deploys to or runs in production; CI deploys with a service principal (SP) that owns the jobs.

## 1. Identities
- One SP per environment (`sp-etl-staging`, `sp-etl-prod`), added to the workspace, granted only the Unity Catalog privileges its jobs need.
- Jobs run as the SP through the bundle `run_as` setting in the prod target (see the bundle settings page for the exact keys).

## 2. Auth options, best first
1. **Workload identity federation (OIDC)** — no secret stored. Create a federation policy on the SP trusting `https://token.actions.githubusercontent.com` with subject `repo:<org>/<repo>:environment:prod`. In the workflow set `DATABRICKS_AUTH_TYPE=github-oidc`, `DATABRICKS_CLIENT_ID=<sp-app-id>`, `DATABRICKS_HOST`, and `permissions: id-token: write`.
2. **OAuth M2M** — SP OAuth secret stored as a CI secret: `DATABRICKS_HOST`, `DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET`. A secret's lifetime is set in days (maximum 730 days); calendar the rotation.
3. Personal access tokens — avoid; tied to a user and leak easily.

## 3. GitHub Actions pipeline
```yaml
name: deploy
on:
  pull_request:
  push: {branches: [main]}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - run: pip install -r requirements-dev.txt && pytest tests/
      - run: databricks bundle validate -t staging
        env: {DATABRICKS_HOST: "${{ vars.DBX_HOST }}", DATABRICKS_CLIENT_ID: "${{ vars.SP_STAGING }}", DATABRICKS_CLIENT_SECRET: "${{ secrets.SP_STAGING_SECRET }}"}
  deploy-prod:
    if: github.ref == 'refs/heads/main'
    needs: test
    environment: prod                 # required reviewers live here
    permissions: {id-token: write, contents: read}
    runs-on: ubuntu-latest
    env: {DATABRICKS_AUTH_TYPE: github-oidc, DATABRICKS_HOST: "${{ vars.DBX_HOST }}", DATABRICKS_CLIENT_ID: "${{ vars.SP_PROD }}"}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - run: databricks bundle deploy -t prod
      - run: databricks bundle run -t prod smoke_test
```

## 4. Gotchas
- Use a release tag of `databricks/setup-cli` instead of `@main` (the setup-cli README says `@main` always uses the latest CLI) so a CLI upgrade does not change deploy behaviour mid-release.
- Run integration tests in a staging target with its own catalog, not the prod catalog.
- Prevent manual prod deploys: deny humans `CAN_MANAGE` on prod jobs; only the SP has it.
- Concurrent pipeline runs to one target contend for the deployment lock; serialise pipeline runs per target in your CI system.

## Verify
- [ ] The prod job's "Run as" shows the SP, and its owner is the SP.
- [ ] Revoking your own workspace access does not stop prod jobs.
- [ ] A PR cannot reach the prod deploy step (branch + environment protection).
- [ ] Federation subject is scoped to repo + environment, not the whole org.

## Checked
2026-10-28. Confirmed against the OAuth M2M page (DATABRICKS_HOST, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET, secret lifetime maximum 730 days), the GitHub OIDC page (DATABRICKS_AUTH_TYPE github-oidc, issuer https://token.actions.githubusercontent.com, subject repo:<org>/<repo>:environment:prod, id-token: write, setup-cli@main and release tags) and the bundle commands page (--force-lock disables the concurrent-deployment guard). Removed: UC privilege names, CAN_USE and Service Principal User statements, Azure DevOps/GitLab/Entra remarks and the setup-cli version: input.
Method: documentation only; no commands were run.
