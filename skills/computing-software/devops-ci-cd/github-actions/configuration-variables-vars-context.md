---
id: computing-software.devops-ci-cd.github-actions.configuration-variables-vars-context
name: configuration-variables-vars-context
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, repository-variables, org-variables, vars-context, configuration-variables, gh-variable-set]
level: intro
status: verified
description: "Store non-secret config as repository, organization and environment variables and read them with the vars context; precedence, naming rules, limits and when not to use them."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables", "https://cli.github.com/manual/gh_variable_set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration variables and the `vars` context

**Goal:** move region names, image repos, feature switches and URLs out of YAML so they can change
per repo, org or environment without a commit — and without abusing secrets (which are masked
and unreadable).

## 1. Set them
```bash
gh variable set AWS_REGION --body eu-west-1                 # repository
gh variable set IMAGE_REPO --org my-org --visibility all --body ghcr.io/my-org
gh variable set REPLICAS --env production --body 6          # environment
gh variable list; gh variable get AWS_REGION
gh variable set -f config.env                               # bulk from dotenv file
```

## 2. Read them
```yaml
env:
  AWS_REGION: ${{ vars.AWS_REGION }}
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - run: echo "scaling to ${{ vars.REPLICAS || 2 }}"
```
`vars` is usable in `run-name`, `env`, `if:`, `with:` and `runs-on`. An undefined variable is an
empty string — use `|| default` or fail explicitly.

## 3. Rules that bite
- Precedence: the variable at the lowest level wins, so **environment > repository > organization**.
- Names: alphanumeric characters and underscores only, must not start with `GITHUB_` or a number, and
  are case-insensitive when referenced.
- Limits (github.com): 48 KB per variable; up to 1,000 organization, 500 repository and 100 environment
  variables; the combined size of organization and repository variables available to one run is capped at
  256 KB, so do not store large JSON blobs here.
- Variables are for non-sensitive data: by default they render **unmasked** in build output. Use secrets for
  tokens.
- `vars` is a context; map a variable with `env:` to read it as `$NAME` in a shell.

## Verify
- [ ] `gh variable list --env production` shows expected overrides.
- [ ] Deleting the repo variable falls back to the org value (precedence understood).
