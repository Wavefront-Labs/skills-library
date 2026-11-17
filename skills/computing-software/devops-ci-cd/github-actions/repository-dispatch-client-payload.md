---
id: computing-software.devops-ci-cd.github-actions.repository-dispatch-client-payload
name: repository-dispatch-client-payload
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, repository-dispatch, client-payload, repository-dispatch-api, event-type, cross-repo-trigger, gh-api-dispatches, peter-evans-repository-dispatch, downstream-trigger, external-trigger, webhook-to-workflow, workflow-triggers]
level: practitioner
status: verified
description: "Trigger a workflow from outside (another repo, a server, a cron) with repository_dispatch: the API call, event_type filtering, reading client_payload, token scope and the 10-property limit."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#repository_dispatch", "https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# repository_dispatch and client_payload

**Goal:** let an external system (or another repo's workflow) start a run with structured
data, without `workflow_dispatch`'s string-only inputs.

## 1. Receiving side
```yaml
on:
  repository_dispatch:
    types: [deploy-request, rebuild]     # omit = any event_type
jobs:
  deploy:
    if: github.event.action == 'deploy-request'   # payload `action` = the event_type that was sent
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "service=${{ github.event.client_payload.service }}"
          echo "sha=${{ github.event.client_payload.sha }}"
      - run: echo '${{ toJSON(github.event.client_payload) }}' > payload.json
```
Runs always execute on the **default branch**'s copy of the workflow file (`github.ref` is the
default branch) — you cannot dispatch to a feature branch. `github.sha` is the default branch
head, so pass the real commit in the payload and `checkout` it explicitly.

## 2. Sending side
```bash
gh api -X POST repos/octo-org/app/dispatches \
  -f event_type=deploy-request \
  -F 'client_payload[service]=api' -F 'client_payload[sha]=abc123'
# or raw JSON
curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/octo-org/app/dispatches \
  -d '{"event_type":"deploy-request","client_payload":{"service":"api","sha":"abc123"}}'
```
From a workflow in another repo: `peter-evans/repository-dispatch` (current major `v4`) with
`repository`, `event-type`, `client-payload: ${{ toJSON(steps.x.outputs) }}` and a token.

Token: the workflow's `GITHUB_TOKEN` is scoped to its own repository (and `repository_dispatch` events
created with it do start runs; they are an exception to the no-recursion rule). To dispatch to *another*
repository use a PAT or GitHub App installation token that can write to it: classic PATs and OAuth tokens
need the `repo` scope, and for fine-grained tokens follow the endpoint's "Fine-grained access tokens"
section. The response is `204` with no body, so there is no run id; poll
`gh run list --event repository_dispatch`.

## 3. Limits
- `client_payload` allows at most **10 top-level properties** and under 64 KB in total (the docs say 65,535
  characters); nest objects to carry more. `event_type` is 1-100 characters.
- Payload values are JSON, so booleans and numbers keep their type.
- To de-duplicate, add an idempotency key to the payload and set the job
  `concurrency: { group: "dispatch-${{ github.event.client_payload.key }}" }`.
- `paths` filters exist only for `push` and `pull_request`, so they do not apply here.

## 4. Security
Treat `client_payload` as untrusted input: never interpolate it into `run:` directly
(`${{ }}` inside a shell line = injection). Read it via `env:` and `"$VAR"`:
```yaml
      - env: { SVC: "${{ github.event.client_payload.service }}" }
        run: ./deploy.sh "$SVC"
```

## Verify
- [ ] `gh api .../dispatches` returns 204 and a run with event `repository_dispatch` appears.
- [ ] `github.event.action` equals the sent `event_type` in the job log.
- [ ] Payload fields are read through `env`, not inline in `run`.
