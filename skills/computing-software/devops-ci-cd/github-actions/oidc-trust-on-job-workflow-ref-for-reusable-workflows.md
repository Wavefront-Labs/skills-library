---
id: computing-software.devops-ci-cd.github-actions.oidc-trust-on-job-workflow-ref-for-reusable-workflows
name: oidc-trust-on-job-workflow-ref-for-reusable-workflows
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, job-workflow-ref, oidc-reusable-workflows, sub-claim-customization, oidc-customization-sub, include-claim-keys, trusted-deploy-workflow, platform-deploy-workflow, aws-trust-policy-job-workflow-ref, azure-federated-subject, gcp-attribute-condition, oidc, workload-identity-federation, reusable-workflows]
level: advanced
status: docs-checked
description: "Lock cloud roles to a central reusable deploy workflow by trusting the job_workflow_ref claim, so only platform-owned workflow code can assume prod roles."
sources: ["https://docs.github.com/en/actions/reference/security/oidc", "https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows", "https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC trust on job_workflow_ref for reusable workflows

**Goal:** any repo may *call* `platform/deploy.yml`, but only that workflow file — at a
tagged ref — can assume the production role. A team editing their own workflow cannot.

## 1. The claim
For a job in a reusable workflow, `job_workflow_ref` is the ref path of the **called** reusable workflow, in the form
`{owner}/{repo}/{path}/{filename}@{ref}`, while `workflow`, `ref` and the other attributes describe the caller.
Trusting it means trusting the code in that file at that ref, independent of the caller. Your cloud provider must be
able to match custom claims, or you must put the claim into `sub`.

## 2. Make it part of `sub` (for providers that only match `sub` and `aud`)
Clouds that support only the standard claims can be given a customised `sub` through the REST API. A repository
template is set with `PUT /repos/{owner}/{repo}/actions/oidc/customization/sub` and a JSON body such as:
```json
{ "use_default": false, "include_claim_keys": ["repo", "context", "job_workflow_ref"] }
```
(an organisation template and a repository opt-in to it also exist; see the OIDC reference). With `repo`, `context` and
`job_workflow_ref` the `sub` format is
`repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME:job_workflow_ref:REUSABLE-WORKFLOW-PATH`, for example
`repo:octo-org/octo-repo:environment:prod:job_workflow_ref:octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main`.
For repositories created after July 15, 2026, or that opted in to immutable subject claims, the `repo` segment
carries owner and repository IDs (`repo:OWNER@OWNER-ID/REPO@REPO-ID`), also when you customise claims, so write
conditions that match the format your repository actually uses (not on GHES).

**AWS trust policy**: use `StringEquals` on `aud` (`sts.amazonaws.com` with the official action) and `StringLike`
with wildcards on `sub` to match the reusable workflow path.
```json
"Condition": { "StringLike": { "token.actions.githubusercontent.com:sub":
  "repo:octo-org/*:environment:prod:job_workflow_ref:octo-org/octo-automation/.github/workflows/deploy.yml@refs/heads/main" },
  "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" } }
```
**Azure**: the federated credential audience is recommended as `api://AzureADTokenExchange`; check the Azure and GitHub
docs for how subject matching works for your credential type.

## 3. Providers with custom-claim conditions
HashiCorp Vault JWT roles use `bound_claims` on any claim; the GitHub docs example is
`job_workflow_ref:ORG_NAME/REPO_NAME/.github/workflows/WORKFLOW_FILE@ref`-style values. Configure conditions for
other clouds from their own documentation.

## 4. Pin the ref, protect the repo
Trusting `@refs/heads/main` means anyone who can push to the platform repository's `main` can deploy prod. The docs
also show pinning to a commit SHA in the condition. Whatever ref you trust, protect it and require review on the
workflow file. A caller using a different ref produces a different `job_workflow_ref` value, which a condition on
the trusted ref rejects.

## 5. Gotchas
- A `sub` template applies to every workflow in the repository or organisation (an organisation template does not
  affect workflows already using OIDC until the repository opts in), so existing trust policies that match the
  default `sub` stop matching once you change it. Add the new conditions first, then switch the template.
- For reusable workflows outside your organisation or enterprise, set `id-token: write` explicitly at the caller
  job or workflow level.

## Verify
- [ ] A dumped token (see the inspection skill) shows the expected `job_workflow_ref` and `sub`.
- [ ] Calling the deploy workflow at `@v3` assumes the role; a copy of the YAML in the caller
  repo gets `AccessDenied`.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23.
- job_workflow_ref semantics for reusable workflows, and the customised sub format with repo, context and job_workflow_ref: confirmed in the OIDC reference and oidc-with-reusable-workflows.
- Sub customisation endpoint PUT /repos/{owner}/{repo}/actions/oidc/customization/sub with use_default and include_claim_keys, organisation templates and opt-in: confirmed in the OIDC reference.
- Immutable subject claims for repositories created after July 15, 2026 (owner and repo IDs in the repo segment; not on GHES): confirmed in the OIDC reference and the AWS page. This was missing from the skill.
- AWS aud sts.amazonaws.com and StringLike wildcard usage, Azure audience api://AzureADTokenExchange, Vault bound_claims: confirmed in the per-provider OIDC pages.
- Removed unconfirmed claims: the gh api flag form, Azure exact-match and flexible credential statements, GCP attribute mapping, Vault glob type, local reusable workflow and composite action claims, tag-ruleset advice stated as fact.

Method: documentation only; no commands were run.
