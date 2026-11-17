---
id: computing-software.devops-ci-cd.gitlab-ci.script-yaml-quoting-and-multiline-blocks
name: script-yaml-quoting-and-multiline-blocks
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, script-yaml-quoting, multiline-script, yaml-special-characters, folded-vs-literal-blocks]
level: intro
status: docs-checked
description: "Write GitLab script lines that survive YAML parsing: quoting colons and special characters, literal vs folded blocks, error handling in multi-line scripts and PowerShell."
sources: ["https://docs.gitlab.com/ci/yaml/script/", "https://docs.gitlab.com/ci/yaml/#script"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Script quoting and multi-line blocks

## 1. Characters that need quoting
A script line containing `: ` (colon-space) parses as a YAML map. GitLab requires single or double quotes around script lines that contain special characters.
```yaml
script:
  - 'curl --fail --header "PRIVATE-TOKEN: $TOKEN" "$CI_API_V4_URL/projects"'
  - "echo 'value: done'"
  - echo "use double quotes" # comments after a space-hash are YAML comments!
```
Wrap the **whole** line in single quotes; inside, use double quotes. A `#` preceded by a space ends the line in YAML unless quoted.

## 2. Literal `|` vs folded `>`
```yaml
script:
  - |
    if [ "$CI_COMMIT_BRANCH" = "main" ]; then
      ./deploy.sh
    fi
  - >
    docker build
    --tag "$IMAGE"
    --build-arg VERSION="$CI_COMMIT_SHORT_SHA" .
```
`|` keeps newlines (real multi-line shell); `>` joins lines with spaces (one long command, no `\` needed). GitLab supports YAML block scalar syntax for multi-line scripts.

## 3. Error handling
GitLab documents how to ignore non-zero exit codes in a script (see the `script` keyword page); failure semantics differ by shell, so test them on your runner's shell.

## 4. Keep scripts out of YAML
Anything over ~10 lines belongs in a script file (runnable locally).

## Verify
- [ ] CI Lint passes; the job runs the intended command.

## Checked

2026-11-02. Confirmed: `script` takes a string or array of strings, special characters require single or double quotes, multi-line scripts use YAML block scalar syntax, CI Lint tool (GitLab CI/CD YAML reference). Removed: quoted-error text, character list, first-line log claim, pipefail/PowerShell error-handling claims, `!reference` snippet, shellcheck claim (none found in fetched pages).

Method: documentation only; no commands were run.
