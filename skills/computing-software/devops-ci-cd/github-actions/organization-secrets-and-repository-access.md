---
id: computing-software.devops-ci-cd.github-actions.organization-secrets-and-repository-access
name: organization-secrets-and-repository-access
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, organization-secrets, secret-access-policy, secret-visibility, secret-precedence, gh-secret-org]
level: practitioner
status: docs-checked
description: "Share one credential across many repos with organization secrets: visibility (all/private/selected), per-repo access lists, precedence and the documented secret limits."
sources: ["https://docs.github.com/en/actions/reference/security/secrets", "https://cli.github.com/manual/gh_secret_set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organization secrets and repository access policies

**Goal:** one rotated value (registry token, Sonar token) instead of the same secret pasted into
40 repos, while keeping it away from repos that should not see it.

## 1. Create with an explicit access policy
```bash
# only listed repos can read it (value read from stdin when --body is omitted)
gh secret set REGISTRY_TOKEN --org my-org --visibility selected --repos api,web,worker < token.txt
# visibility "private"
gh secret set SONAR_TOKEN --org my-org --visibility private --body "$SONAR"
gh secret list --org my-org --json name,visibility,updatedAt
```
`gh secret set --visibility` accepts `all`, `private` or `selected` (default `private`); `--repos` lists the repositories
that can access an organisation secret and `--no-repos-selected` grants none. Prefer `selected` for anything that can write.

## 2. Precedence and limits
- Same name at several levels: the **environment** secret takes precedence over repository and organisation
  secrets. A stale repository secret therefore shadows a rotated organisation one (`gh secret list -R org/repo`).
- You can store up to 1,000 organisation secrets, 100 repository secrets and 100 environment secrets. A workflow can use
  all 100 repository secrets, all 100 environment secrets and, if the repository can access more than 100 organisation
  secrets, only the first 100 sorted alphabetically by name.
- Secrets are limited to 48 KB each.
- Secrets are not passed to a reusable workflow unless the caller passes them (`secrets: inherit` or by name).

## 3. Governance
- Name with a scope prefix (`ORG_`, `DEPLOY_`) so shadowing is visible.
- Pair write-capable secrets with environments and required reviewers rather than organisation-wide reach.
- Prefer OIDC for cloud credentials; organisation secrets for things that cannot federate.

## Verify
- [ ] A repository outside the selected list gets an empty value.
- [ ] No repository-level secret of the same name exists in consumer repositories.
- [ ] The access list matches the intended repositories (organisation secret settings).

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and cli/cli source (gh v2.103.2).
- Secret limits (1,000 org, 100 repo, 100 environment, first 100 org secrets alphabetically, 48 KB) and environment-over-repository-over-organisation precedence: confirmed in the secrets reference.
- gh secret set flags (--org, --visibility all|private|selected default private, --repos, --no-repos-selected, --body with stdin, --env, --app) and gh secret list --json fields (name, visibility, updatedAt): confirmed in cli/cli pkg/cmd/secret source (gh v2.103.2). Reusable workflow secret passing: confirmed in reuse-workflows.
- Removed unconfirmed claims: the REST repositories calls, public-repository exposure statement, Free plan behaviour, audit-log event name and the fork-PR secret statement.

Method: documentation only; no commands were run.
