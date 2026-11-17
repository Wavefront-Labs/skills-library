---
id: computing-software.devops-ci-cd.github-actions.creating-and-publishing-actions
name: creating-and-publishing-actions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, creating-actions, custom-action, javascript-action, typescript-action, docker-container-action, action-toolkit, actions-core, actions-github, actions-exec, actions-tool-cache, action-yml, inputs-outputs, runs-using-node20, ncc, dist-folder, marketplace, action-versioning, major-tag, semver-tags, branding, pre-post-steps, octokit, github-script, action-testing]
level: advanced
status: draft
description: "Build a custom GitHub Action: action.yml contract, JS/TS with @actions/core and @actions/github bundled via ncc, Docker actions, pre/post steps, v1 major-tag release flow and Marketplace publishing."
sources: ["https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-javascript-action", "https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions", "https://github.com/actions/toolkit", "https://docs.github.com/en/actions/sharing-automations/creating-actions/publishing-actions-in-github-marketplace", "https://github.com/actions/typescript-action"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creating and publishing actions

**Goal:** a reusable action with a clean input/output contract that installs in zero seconds,
is versioned like a library and is safe for strangers to pin.

## 1. Pick the type
| type | when | startup |
|---|---|---|
| composite (`runs.using: composite`) | glue of shell + other actions, no code to ship | instant |
| JavaScript (`using: node20`) | logic, API calls, cross-platform; needs no Docker | ~1 s |
| Docker (`using: docker`) | needs a specific toolchain/OS; Linux runners only | 10–60 s (image build/pull every run unless `image: docker://ghcr.io/...`) |

Default to composite; go JS when you need the toolkit; go Docker only for a pinned toolchain.

## 2. action.yml — the contract
```yaml
name: 'Deploy Preview'
description: 'Deploys a preview environment and comments the URL on the PR'
author: 'platform-team'
branding: { icon: 'upload-cloud', color: 'blue' }
inputs:
  token:
    description: 'GitHub token'
    required: false
    default: ${{ github.token }}     # lets callers omit it
  environment:
    description: 'Target environment'
    required: true
outputs:
  url:
    description: 'Preview URL'
runs:
  using: node20
  main: dist/index.js
  post: dist/cleanup.js           # runs at job end; default post-if is always(), narrow with post-if: success()
```
Inputs arrive as env vars `INPUT_<UPPER_NAME>` (dashes stay, spaces→underscores); `required: true`
is enforced only by `core.getInput(name, {required: true})`, not by the runner.
Composite outputs must be mapped: `outputs.url.value: ${{ steps.deploy.outputs.url }}`.

## 3. JavaScript/TypeScript with the toolkit
```ts
import * as core from '@actions/core'
import * as github from '@actions/github'
import { exec } from '@actions/exec'
async function run() {
  try {
    const env = core.getInput('environment', { required: true })
    const octokit = github.getOctokit(core.getInput('token'))
    core.setSecret(core.getInput('token'))
    await exec('kubectl', ['apply', '-f', 'preview.yaml'])
    const url = `https://${env}.example.test`
    core.setOutput('url', url)
    core.summary.addHeading('Preview').addLink(url, url).write()
    if (github.context.payload.pull_request)
      await octokit.rest.issues.createComment({ ...github.context.repo,
        issue_number: github.context.payload.pull_request.number, body: `Preview: ${url}` })
  } catch (e) { core.setFailed((e as Error).message) }
}
run()
```
Rules:
- The runner does **not** `npm install`; ship a bundle: `ncc build src/index.ts -o dist
  --license licenses.txt` and **commit `dist/`**. Add a CI check that `dist/` is up to date
  (`git diff --exit-code dist/` after a build) — the classic broken-action bug.
- `core.getBooleanInput`, `core.getMultilineInput`; `core.exportVariable`, `core.addPath`
  affect later steps; `core.saveState`/`getState` pass data from `main` to `post`.
- `@actions/tool-cache` to download+cache CLIs (`tc.find('kubectl', ver)` then `tc.downloadTool` + `tc.cacheDir`).
- Start from `actions/typescript-action` template (jest, eslint, `ncc`, release workflow included).

## 4. Docker actions
`runs: { using: docker, image: Dockerfile }` rebuilds every run — prefer
`image: docker://ghcr.io/org/tool:1.4.2` (pre-built, pinned). Inputs become `INPUT_*` env
vars and `args:`; the workspace is mounted at `/github/workspace`; write outputs with
`echo "url=$URL" >> "$GITHUB_OUTPUT"`. Must run as root or a user that can write the
workspace; `WORKDIR` is overridden.

## 5. Versioning and release flow
Consumers reference `uses: org/action@v1`. Maintain a **moving major tag**:
```bash
git tag -fa v1 -m "v1 -> v1.4.2" && git push -f origin v1   # after tagging v1.4.2
```
Or automate with `actions/publish-action` / `JasonEtco/build-and-tag-action` which builds
`dist/` on the tag and updates the major tag. Security-conscious users pin the SHA; document
it. Never rewrite a released patch tag.

Private/internal actions: the consumer needs access; enable *Actions → Access* on the action
repo ("Accessible from repositories in the org"). Reference form `uses: org/repo/path@ref`
for actions in subdirectories of a monorepo.

## 6. Marketplace
Requirements: public repo, `action.yml` at root, unique `name`, `branding`, README, a release
with the "Publish this Action to the GitHub Marketplace" box ticked. Two-factor on the
publishing account. Each release updates the listing; the listing is the release note.

## 7. Testing
- Unit: mock `@actions/core` (`jest.spyOn(core, 'getInput')`) and `@actions/github` context.
- Integration: a `test.yml` workflow in the same repo using `uses: ./` with `with:` inputs,
  asserting on outputs in a following step. Run on `pull_request` and before tagging.
- Local: `act -j test` works for JS/composite actions; Docker actions need Docker-in-act.

## Verify
- [ ] `dist/` matches source (CI diff check passes).
- [ ] `uses: ./` integration workflow passes; outputs read correctly downstream.
- [ ] `v1` major tag moves on release; patch tags immutable.
- [ ] Secrets passed as inputs are `core.setSecret`-ed so they mask in logs.
