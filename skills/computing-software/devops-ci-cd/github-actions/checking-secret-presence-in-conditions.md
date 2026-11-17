---
id: computing-software.devops-ci-cd.github-actions.checking-secret-presence-in-conditions
name: checking-secret-presence-in-conditions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, secret-presence-check, secrets-in-if, github-actions-secrets]
level: practitioner
status: verified
description: "Gate steps on whether a secret exists (forks, Dependabot, optional integrations) without referencing secrets directly in if:, which Actions does not allow."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#using-secrets-in-a-workflow", "https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#secrets-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking secret presence and using secrets in `if:`

Secrets cannot be referenced directly in `if:` conditions. Map to env, then test env:
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    env:
      HAS_NPM_TOKEN: ${{ secrets.NPM_TOKEN != '' }}
    steps:
      - run: npm publish
        if: env.HAS_NPM_TOKEN == 'true'
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```
A secret that has not been set evaluates to an empty string (GitHub docs). Note that an unquoted `{ key: ${{ ... }} }` flow
mapping fails to parse (PyYAML: `while parsing a flow mapping`; actionlint: `did not find expected ',' or '}'`),
which is why the examples use block style.

## Job-level gating
`env` is not available in `jobs.<id>.if`. Use a tiny check job:
```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    outputs:
      has-token: ${{ steps.c.outputs.has }}
    steps:
      - id: c
        run: echo "has=${{ secrets.DEPLOY_KEY != '' }}" >> "$GITHUB_OUTPUT"
  deploy:
    needs: check
    if: needs.check.outputs.has-token == 'true'
```

## When secrets are empty
| Context | Secrets available |
|---|---|
| `pull_request` from fork | none (except GITHUB_TOKEN read-only) |
| Dependabot-triggered | Actions secrets are not available (see the Dependabot-on-Actions docs for Dependabot secrets) |
| Reusable workflow | secrets are not passed automatically; map them or use `secrets: inherit` |
| Environment secret | only for jobs that use the environment, after any protection rules pass |

## Gotchas
- Do not echo the secret to test it; the comparison above only emits true/false.
- `secrets.X != ''` returns the string `true`/`false` when placed in env; compare against `'true'`.
- Prefer failing loudly on main (`if: env.HAS == 'false' && github.ref == 'refs/heads/main'` then `exit 1`) so a deleted secret is not silently skipped.

## Verify
- [ ] `actionlint` accepts the file (no `context "secrets" is not allowed here`).
