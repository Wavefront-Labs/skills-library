---
id: computing-software.devops-ci-cd.github-actions.defaults-run-shell-and-working-directory
name: defaults-run-shell-and-working-directory
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, defaults-run, working-directory, shell-keyword, shell-options, bash-pipefail, pwsh-shell, python-shell, sh-shell, cmd-shell, custom-shell, set-e, errexit, monorepo-subdirectory, workflow-syntax]
level: practitioner
status: verified
description: "Set defaults.run shell and working-directory at workflow/job level, and know each shell's implicit flags (bash -eo pipefail vs sh -e vs pwsh) so a failing pipe actually fails the step."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#defaultsrun", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defaults.run: shell and working-directory

**Goal:** stop repeating `working-directory: services/api` and `shell: bash` on every step, and
know which shell swallows errors.

## 1. Where defaults live
```yaml
defaults:                 # workflow level: applies to every job
  run:
    shell: bash
    working-directory: services/api
jobs:
  test:
    defaults:             # job level overrides workflow level
      run:
        working-directory: services/web
    steps:
      - uses: actions/checkout@v4
      - run: npm ci       # runs in services/web
      - run: ls
        working-directory: .   # step level overrides both (relative to GITHUB_WORKSPACE)
```
Precedence: step > job > workflow. `defaults.run` applies to `run` steps only; actionlint rejects
`shell:`/`working-directory:` on a `uses:` step (pass paths through `with:` instead). The directory must
exist *before* the step runs, so a `run` in a subdirectory before `checkout` has nothing to run in.

## 2. What each shell really executes
| `shell:` | Command the runner builds | Implication |
|---|---|---|
| (unset, non-Windows) | `bash -e {0}` (falls back to `sh -e`) | **no `pipefail`**: `cmd \| tee log` passes when `cmd` fails |
| `bash` (explicit) | `bash --noprofile --norc -eo pipefail {0}` | pipelines fail correctly — always set this |
| `sh` | `sh -e {0}` | POSIX only, no arrays/`[[ ]]` |
| `pwsh` | `pwsh -command ". '{0}'"` | the default shell on Windows; the runner prepends `$ErrorActionPreference = 'stop'` and appends `if ((Test-Path -LiteralPath variable:\LASTEXITCODE)) { exit $LASTEXITCODE }`, so the step takes the exit code of the *last* native command (an earlier failing native command does not stop the script) |
| `powershell` | `powershell -command ". '{0}'"` | Windows PowerShell (Desktop); same prepend/append behaviour |
| `cmd` | `%ComSpec% /D /E:ON /V:OFF /S /C "CALL "{0}""` | no fail-fast: check each error code yourself; exits with the last program's error level |
| `python` | `python {0}` | the script is written to a temporary file |
| custom | `shell: perl {0}` / `deno run {0}` | `{0}` = temp file path; must be on `PATH` |

The classic false-green: the unset default has no `pipefail`. A workflow-level
`defaults.run.shell: bash` fixes every step at once. The explicit `bash` also passes `--noprofile --norc`,
so profile files are not read.

## 3. pwsh exit-code pattern
The runner already exits with the last native command's code. When several native commands run in one
step, check each one:
```yaml
- shell: pwsh
  run: |
    dotnet build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    dotnet test
```

## 4. Gotchas
- `defaults` accepts only `run` (actionlint: `expected "run" key for "defaults" section`); use the `env:`
  key for variables.
- `shell: bash` on Windows runs the bash that ships with Git for Windows.

## Verify
- [ ] A step with `false | true` fails under your default shell.
- [ ] No step repeats `working-directory` that the job default already provides.
- [ ] pwsh steps with several native commands check `$LASTEXITCODE` between them.
