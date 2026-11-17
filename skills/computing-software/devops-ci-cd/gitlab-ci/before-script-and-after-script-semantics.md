---
id: computing-software.devops-ci-cd.gitlab-ci.before-script-and-after-script-semantics
name: before-script-and-after-script-semantics
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, before-script, after-script, after-script-timeout, ci-job-status, cleanup-steps]
level: practitioner
status: docs-checked
description: "Know exactly how before_script, script and after_script run: shared vs separate shells, failure and cancel behaviour, after_script timeout and CI_JOB_STATUS for cleanup."
sources: ["https://docs.gitlab.com/ci/yaml/#before_script", "https://docs.gitlab.com/ci/yaml/#after_script", "https://docs.gitlab.com/ci/variables/predefined_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# before_script and after_script semantics

## 1. Execution model
- `before_script` + `script` are concatenated and run in **one shell**: exported variables,
  `cd`, activated virtualenvs carry over. A failing `before_script` fails the job and skips `script`.
- `after_script` runs in a **new shell** after `script`. It also runs when the job is canceled while
  `before_script` or `script` is running (since GitLab 17.0) and when it fails with failure type
  `script_failure`, but not other failure types. It does **not** see variables or aliases exported in
  `script`, or changes outside the working tree; its working directory is reset to the default.
- `after_script` failing or timing out does not change the job's exit code (the job can still succeed).
- `after_script` has a separate timeout, 5 minutes by default. Override with the
  `RUNNER_AFTER_SCRIPT_TIMEOUT` variable (e.g. `10m`).

## 2. Cleanup pattern
```yaml
integration:
  before_script:
    - ./scripts/start-env.sh
  script:
    - ./scripts/run-tests.sh
  after_script:
    - |
      if [ "$CI_JOB_STATUS" != "success" ]; then
        docker compose logs > compose.log 2>&1 || true
      fi
    - docker compose down -v || true
  artifacts:
    when: always
    paths: [compose.log]
```
`CI_JOB_STATUS` is `success`, `failed` or `canceled` inside `after_script`.
`after_script` runs before cache and artifact upload, so files written there are uploaded.

## 3. Reuse without duplication
```yaml
.setup: { before_script: [apt-get update -qq, apt-get install -y -qq jq] }
job:
  before_script:
    - !reference [.setup, before_script]
    - echo extra
```

## 4. Gotchas
- Job-level `before_script` replaces `default:before_script`; it does not append.
- Anything computed in `script` must be written to a file inside the working tree to be read in `after_script`.
- For jobs that time out, `after_script` does not run by default; set `RUNNER_SCRIPT_TIMEOUT` and
  `RUNNER_AFTER_SCRIPT_TIMEOUT` so both fit inside the job timeout.

## Verify
- [ ] Force a failing test: logs are uploaded and the environment is torn down.
- [ ] Cancel a running job: `after_script` output appears in the log.

## Checked

2026-10-31. Confirmed against the GitLab CI YAML reference (after_script and before_script sections: new shell, concatenation of before_script and script into one shell, cancel behaviour since 17.0, script_failure only, working directory reset, separate 5 minute timeout and RUNNER_AFTER_SCRIPT_TIMEOUT, exit code unaffected, no after_script on job timeout by default, runs before cache and artifact upload, job keyword replaces default) and the predefined variables page (CI_JOB_STATUS values success, failed, canceled).
Removed: the claim that after_script runs on any failure, the claim that it gets its own window after a job timeout (the docs say it does not run by default), the file-variable and shell-executor gotchas.

Method: documentation only; no commands were run.
