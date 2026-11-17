---
id: computing-software.devops-ci-cd.gitlab-runner.runner-register-authentication-token
name: runner-register-authentication-token
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [register, authentication-token, glrt, non-interactive]
level: intro
status: docs-checked
description: "Register a runner with a glrt- authentication token, interactively or non-interactively."
sources: ["https://docs.gitlab.com/runner/register/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Register with an authentication token

Registration links the runner to a GitLab instance and saves the result to `config.toml`. Since GitLab Runner 15.0 the registration request format changed, so the runner version must be appropriate for the GitLab version.

Obtain a token by creating an instance, group or project runner in the GitLab UI. Runner authentication tokens have the prefix `glrt-`.

Interactive: `sudo gitlab-runner register`, then answer prompts for the GitLab URL (`https://gitlab.com` on GitLab.com), the token, a description, job tags (comma separated), an optional maintenance note and the executor.

Non-interactive:
```
sudo gitlab-runner register --non-interactive \
  --url "https://gitlab.com/" --token "$RUNNER_TOKEN" \
  --executor "docker" --docker-image alpine:latest \
  --docker-pull-policy "if-not-present" --description "docker-runner"
```
Behind a proxy, export `HTTP_PROXY` and `HTTPS_PROXY` and run with `sudo -E`. Repeat the command to register several runners on one host. Using the same token on several hosts reuses one runner configuration.

## Checked

2026-11-03. Confirmed against registration steps, the 15.0 request-format change, `glrt-` prefix, `sudo -E` behind a proxy and token reuse on the Register page.

Method: documentation only; no commands were run.
