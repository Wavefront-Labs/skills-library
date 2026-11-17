---
id: computing-software.cloud-infrastructure-engineering.aws.iam-policies-and-roles
name: iam-policies-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, iam-policies, iam-roles, sts, assume-role, identity-center, sso, scp, rcp, service-control-policies, permission-boundaries, access-analyzer, policy-evaluation, condition-keys, aws-principalorgid, least-privilege, oidc, github-actions, irsa, eks-pod-identity, trust-policy, simulate-principal-policy, aws-organizations]
level: practitioner
status: docs-checked
description: "Write least-privilege AWS IAM: how policy evaluation really decides, roles over users, Identity Center, SCPs/RCPs, condition keys and Access Analyzer to prove it."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-assume-role-credentials.html", "https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws", "https://github.com/boto/botocore/blob/develop/botocore/data/accessanalyzer/2019-11-01/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IAM policies and roles: grant exactly what is needed, and prove it

**Goal:** humans and workloads get short-lived role credentials scoped to their job,
organisation guardrails cap what any account can do, and you can explain any
Allow/Deny by walking the evaluation logic rather than guessing.

## 1. Know how a request is decided
Within one account the IAM policy evaluation logic page describes:
1. **An explicit Deny in any applicable policy overrides any Allow** (identity-based, resource-based, SCP, RCP,
   permissions boundary, session policy).
2. **Identity-based and resource-based policies** for a principal in the same account give the **union** of their
   permissions: an allow in either is enough, unless something denies.
3. **Permissions boundaries** and **session policies** limit what identity-based policies grant: the result is the
   **intersection**.
4. **SCPs and RCPs** apply to accounts in an organization and also intersect: the action must be allowed by the
   identity-based policy, the SCP and the RCP. They cap permissions; they never grant.
Cross-account access needs the caller's side and the resource's side to both allow (for example the caller's
identity policy and the target role's trust policy or resource policy). For the exact algorithm see the
policy evaluation logic documentation.

## 2. Roles, not users
- No IAM users with long-lived access keys for humans. Prefer federation (for example IAM Identity Center with your
  identity provider) so people use short-lived role credentials.
- Workloads: use the role attached to the compute (EC2 instance profile, Lambda execution role, ECS task role,
  EKS pod roles) and **OIDC federation** for CI (GitHub Actions, GitLab); never stored keys.
- GitHub's AWS OIDC guide: use audience `sts.amazonaws.com` with the official action, and AWS recommends evaluating
  the `token.actions.githubusercontent.com:sub` condition key in the trust policy of any role that trusts GitHub's
  OIDC provider. Pin both, for example
  ```json
  "Condition": {
    "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
    "StringLike":   {"token.actions.githubusercontent.com:sub": "repo:example-org/app:ref:refs/heads/main"}
  }
  ```
  A wildcard such as `repo:example-org/*` matches every repository in the organisation, and the GitHub guide's own
  wildcard example (`repo:octo-org/octo-repo:*`) allows any branch, pull request merge branch or environment of that
  repository. For a workflow that uses an environment the `sub` has the form `repo:ORG/REPO:environment:NAME`.

## 3. Write the policy
- Scope `Resource` to ARNs, not `*`, wherever the action supports resource-level permissions; actions that do not
  support it must use `*` (check the Service Authorization Reference).
- Useful global condition keys (all present in the global condition keys reference): `aws:PrincipalOrgID` (restrict
  access to your organization), `aws:SourceVpce` / `aws:SourceVpc` (available only when the request uses a VPC
  endpoint), `aws:SecureTransport`, `aws:RequestedRegion`, `aws:PrincipalTag/<key>` with `aws:ResourceTag/<key>` for
  ABAC, and `aws:SourceArn` / `aws:SourceAccount` for service principals (the Roles Anywhere trust guide recommends
  them to prevent confused-deputy use). Third parties assuming a role pass an ExternalId; the
  assume-role settings page documents the `external_id` profile setting.
- Set operators (`ForAllValues`, `ForAnyValue`) are only for multivalued keys; do not use them with single-valued keys.
- `...IfExists` operators avoid failures when a key is absent; `aws:MultiFactorAuthPresent` is absent for long-term
  credentials, so use `BoolIfExists` in a Deny.
- Use `NotAction` mainly in Deny statements (for example region-lock SCPs exempting global services); in an Allow it
  matches every action not listed, including those of services added later.

## 4. Guardrails with Organizations
- SCPs on OUs: deny leaving the org, disabling CloudTrail/GuardDuty/Config, using non-approved regions, and creating
  IAM users/access keys. Keep a break-glass role exempt via an `aws:PrincipalArn` condition (`NotPrincipal` is not
  supported in SCPs).
- **RCPs** (resource control policies) apply guardrails to resources and take part in the evaluation as described
  above; check the current Organizations documentation for the supported-service list before relying on one.
- **Permissions boundaries** let developers create roles without escalating: require `iam:PermissionsBoundary` equal
  to your boundary ARN on `iam:CreateRole` / `iam:PutRolePolicy`.

## 5. Prove it
- `aws iam simulate-principal-policy --policy-source-arn <ROLE_ARN> --action-names s3:GetObject --resource-arns arn:aws:s3:::example-bucket/*`
  evaluates a principal's policies against an action; supply `--context-entries` for context keys.
- **IAM Access Analyzer**: external-access and unused-access findings, policy validation (`aws accessanalyzer
  validate-policy`), custom policy checks (`check-no-new-access`, `check-access-not-granted`) in CI, and policy
  generation from CloudTrail activity.
- Read CloudTrail `errorCode: AccessDenied` events to see what was denied.

## Gotchas
- An explicit Deny in an SCP cannot be overridden by an allow in the account: "AdministratorAccess but still
  denied" is often an SCP/RCP or boundary.
- A role trust policy naming an account as `Principal` (as in the IAM MFA cross-account example) lets users of that
  account assume the role only if they are also allowed by their own identity policy to call `sts:AssumeRole`.
- `iam:PassRole` is the classic escalation path: scope it to specific role ARNs and add `iam:PassedToService`; do
  not try to control PassRole with role tags, which gives unreliable results.
- Session duration: a role session can be 1-12 hours (default 1 hour, up to the role's maximum), but role chaining
  limits a session to 1 hour.

## Verify
- [ ] No human IAM users with active access keys (`aws iam generate-credential-report`).
- [ ] Every CI OIDC trust policy pins `aud` and a specific `sub`.
- [ ] SCPs deny region drift, CloudTrail tampering and IAM user creation, with a tested break-glass exemption.
- [ ] Access Analyzer shows no unexpected external-access findings.
- [ ] Policies pass `validate-policy` with no security warnings, and no Allow uses `NotAction`.
- [ ] You can explain one recent AccessDenied by naming the exact policy layer responsible.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone

## Checked
Checked 2026-10-24 against the IAM User Guide pages for policy evaluation logic, global condition keys, policy
variables, quotas, NotAction and PassRole, the AWS SDKs and Tools assume-role page, GitHub's "OIDC in AWS" guide
and the botocore Access Analyzer model. Replaced the five-step evaluation list with the union/intersection rules
the evaluation page actually states. Confirmed: explicit deny precedence; boundary and session policy
intersection; SCP/RCP intersection; the listed global condition keys and their availability notes; set operators
only for multivalued keys; `BoolIfExists` for `aws:MultiFactorAuthPresent`; role session 1-12 hours with 1-hour
role chaining; GitHub `aud`/`sub` guidance; Access Analyzer `validate-policy`, `check-no-new-access`,
`check-access-not-granted` and policy generation operations. Removed unchecked statements: the management account
exemption from SCPs, the KMS key-policy remark, the RCP supported-service list and launch date, the `ForAllValues`
absent-key rule, AND/OR condition semantics, the Identity Center CLI commands, the paid-feature remark for unused
access, the simulator coverage caveat, error-message detail, the eventual-consistency note and `sts:ExternalId`
as a named key.
Method: documentation only; no commands were run.
