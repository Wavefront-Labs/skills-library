---
id: computing-software.devops-ci-cd.secrets-management.secrets-in-ci-best-practices
name: secrets-in-ci-best-practices
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, ci-secrets, pipeline-secrets, github-actions-secrets, environment-secrets, required-reviewers, gitlab-protected-variables, masked-variables, jenkins-credentials, groovy-interpolation, oidc, github-token-permissions, fork-pull-requests, pull-request-target, docker-build-secrets, buildkit-secret-mount, build-args, log-masking, self-hosted-runners, ephemeral-runners]
level: practitioner
status: docs-checked
description: "Keep CI secrets from leaking: who gets them (forks, environments, protected refs), untrusted code, Docker build secrets, log masking, runner hygiene."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions", "https://docs.gitlab.com/ci/variables/", "https://www.jenkins.io/doc/book/pipeline/jenkinsfile/", "https://docs.docker.com/build/building/secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets in CI: best practices

**Goal:** a secret is present only in the job that needs it, only for code you trust, and cannot end up in logs or image layers.

(Replacing stored keys with OIDC, and secret stores in general, are in `computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene`.)

## 1. Threat model
Masking and redaction are best-effort. GitHub: "automatic redaction is not guaranteed"; anyone with write access to a repository can read all its secrets. GitLab: masking "is not a guaranteed way to prevent malicious users from accessing variable values", and a merge request that changes `.gitlab-ci.yml` can send variables to a third-party server (a `curl --data` in a script), so review those changes before running the pipeline. Jenkins: a Pipeline that uses credentials can also disclose them; do not let untrusted Pipeline jobs use trusted credentials. Design around which code gets secrets.

## 2. Decide who gets secrets
- **Forks:** on GitHub, secrets other than `GITHUB_TOKEN` are not passed to the runner for workflows triggered from a forked repository; Dependabot-triggered workflows also do not get them. GitLab: pipelines from forked projects cannot access the parent's CI/CD variables by default, but a merge request pipeline run in the parent project for a fork's MR gets all variables.
- **`pull_request_target` and `workflow_run`** are privileged triggers (write access, secrets, shared main-branch cache). Do not use them with checkout of untrusted PR code; use `workflow_run` for privilege separation, and treat artifacts from other workflows with caution.
- **Environments as gates (GitHub):** required reviewers on an environment block the job from its environment secrets until approved.
- **Protected variables (GitLab):** a protected variable is available only to pipelines on protected branches or protected tags.
- **Least privilege:** set the default `GITHUB_TOKEN` permission to read-only for repository contents and raise it per job. Organisation secrets can be limited by repository policy.

## 3. Isolate secret-using steps from untrusted code
- A compromised third-party action has access to all secrets configured on the repository and may use `GITHUB_TOKEN` to write to it. Best protection is a workflow dependency lockfile; otherwise pin to a full-length commit SHA (verify it is from the action's repository, not a fork). A tag can be moved or deleted.
- Audit action source for secrets sent to unintended hosts or logged.
- Pass untrusted context values (such as a PR title) through an intermediate environment variable, or to an action as an input, not directly inside an inline script.
- Use `CODEOWNERS` on `.github/workflows` so workflow changes need designated review.

## 4. Docker builds
- Build arguments and environment variables are inappropriate for secrets because they persist in the final image.
- Use a secret mount: `docker build --secret id=aws,src=$HOME/.aws/credentials .` plus `RUN --mount=type=secret,id=aws ...` in the Dockerfile. The secret is available only for that instruction, by default as a file at `/run/secrets/<id>`; `target=` changes the path and `env=` mounts it as an environment variable. The source can be a file or an environment variable (`--secret id=KUBECONFIG,env=KUBECONFIG`).
- For private Git fetches use an SSH mount (`docker buildx build --ssh default .`), or the pre-defined `GIT_AUTH_TOKEN` / `GIT_AUTH_HEADER` secrets for remote Git contexts. `GIT_AUTH_TOKEN` is not compatible with GitLab `CI_JOB_TOKEN`; use `GIT_AUTH_HEADER` with a Basic header for `gitlab-ci-token`.

## 5. Keep secrets out of outputs
- **GitHub:** do not store secrets as structured data (JSON, XML, YAML blobs); create one secret per value. Register derived values (a JWT generated from a key, Base64 or URL-encoded forms) with `::add-mask::VALUE`. Redaction happens on the runner, so if an unredacted secret reaches a run log, delete the log and rotate the secret. Review logs after testing valid and invalid inputs. Secrets cannot be referenced directly in `if:` conditionals; set them as job-level environment variables first.
- **Command lines:** avoid passing secrets as command-line arguments (visible via `ps`, captured by audit events); use environment variables, STDIN or other mechanisms.
- **GitLab:** masked values must be single-line, 8+ characters, and not match an existing variable name. A modified output (for example escaped special characters) is not masked. `CI_DEBUG_SERVICES` may reveal values. File-type variables and external secrets help prevent `env`/`printenv` printing them. "Masked and hidden" values cannot be revealed in the UI again (only settable when creating the variable).
- **Jenkins Groovy:** never use Groovy string interpolation with credentials. Use single quotes so the shell expands the variable (`sh 'curl ... $API_TOKEN'`); double-quoted strings interpolate in Groovy and process listings can disclose the value. Interpolating special characters can also mangle credentials. Jenkins masks printed credentials as `****` in console output.

## 6. Runners
- GitHub-hosted runners are ephemeral clean VMs. Self-hosted runners are not guaranteed to be, and can be persistently compromised by untrusted workflow code; they should almost never be used for public repositories. Environment reviewers do not fix this, since those jobs still run on the same self-hosted machine.
- Auto-destroying runners after each job is not a guarantee, because a runner may run more than one job and secrets passed on command lines can be seen by a concurrent job.
- Use just-in-time (JIT) runners created through the REST API (they run at most one job); reused hardware must be cleaned by automation.
- Keep sensitive data and network reach on runner machines to a minimum (SSH keys, tokens, cloud metadata services). Use runner groups to restrict which repositories can use them.
- Prefer OpenID Connect for short-lived, scoped cloud tokens instead of long-lived stored credentials. Jenkins's own page warns that storing static AWS keys in Jenkins credentials is not very secure.

## 7. Audit
Review registered secrets periodically and remove unneeded ones; rotate periodically to shorten the window of a compromised secret. The org audit log records events such as `org.update_actions_secret`.

## Verify
- [ ] A test run triggered from a fork has no secrets other than `GITHUB_TOKEN` (GitHub) or no parent variables (GitLab).
- [ ] Production credentials are only in an environment with required reviewers or protected-ref scope.
- [ ] Release images are built with `--secret` mounts and no secret `ARG`/`ENV`.
- [ ] No `pull_request_target`/`workflow_run` workflow checks out untrusted code.
- [ ] Self-hosted runners are not attached to public repositories.

## Checked
Method: docs-checked 2026-11-09 against the GitHub Secure use reference (full), GitHub "Using secrets in GitHub Actions" (searched for fork, command-line, masking and environment sections), GitLab CI/CD variables page (sections on definition, security, masking, hiding and protecting read), Jenkins Pipeline Jenkinsfile page (credentials and string interpolation sections) and Docker Build secrets page (full).
Removed as unconfirmed: the OWASP Top 10 CI/CD page as a source (not read), GitHub fork `GITHUB_TOKEN` "read-only by default" wording, GitLab `environment_scope` and `CI_JOB_TOKEN` allowlists, Jenkins folder-scoped credentials and multibranch fork advice, `docker history --no-trunc` and provenance-attestation checks, `ACTIONS_STEP_DEBUG` and `CI_DEBUG_TRACE` warnings, the `set -x` advice, advice on artifacts, caches and `always()` cleanup steps, and the `RUN --mount=type=ssh` Dockerfile form.
