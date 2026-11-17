---
id: computing-software.devops-ci-cd.deployment-strategies.deployment-automation-and-idempotent-scripts
name: deployment-automation-and-idempotent-scripts
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, deployment-automation, deployment-scripting, deploy-script, idempotent-deploy, idempotency, deploy-sh, same-script-every-environment, dry-run, convergence, declarative-vs-imperative, rerunnable, deploy-locks, concurrency-lock, preflight-checks, health-gate, smoke-after-deploy, rollback-command, deploy-logging, exit-codes, set-euo-pipefail, timeouts, retries-with-backoff, no-snowflakes, ansible, helm-upgrade-install, kubectl-apply, aws-cli-deploy]
level: practitioner
status: draft
description: "Write deployment automation that is boring: one script for every environment, idempotent and re-runnable, preflight checks, locks, health gates, structured logging, dry-run mode, a rollback command."
sources: ["Humble & Farley, Continuous Delivery (2010), ch. 6 Build and Deployment Scripting", "https://dora.dev/capabilities/deployment-automation/", "https://helm.sh/docs/helm/helm_upgrade/", "https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Idempotency", "https://sre.google/sre-book/release-engineering/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deployment automation and idempotent scripts

**Goal:** `deploy <version> <environment>` is the only way anything reaches any
environment, it can be run twice without harm, and a new team member can run it safely
on day one.

## 1. Principles (CD ch. 6, DORA deployment automation)
- **Same script, every environment**: differences are parameters/config, never a second
  script. Staging runs the production path, so the production path is tested daily.
- **Idempotent / convergent**: running it with the same inputs on an already-deployed
  system changes nothing and exits 0. Prefer declarative tools that converge
  (`kubectl apply`, `helm upgrade --install`, Terraform, Ansible modules) over imperative
  sequences (`create`, `restart`) that fail the second time.
- **Fail fast and loudly**: preflight checks before any change; non-zero exit on any
  failure; no "warning: … continuing".
- **Scriptable by machines and humans**: runs from CI with the pipeline identity and from
  a laptop with break-glass creds — same flags.
- **Observable**: every run logs version, environment, actor, start/end, and the result,
  to stdout and to a deployment record (deployments API, event table).
- **Reversible**: `deploy <previous-version>` *is* the rollback for stateless services;
  write the rollback steps for anything else before writing the forward steps.

## 2. Skeleton (bash; the shape matters more than the language)
```bash
#!/usr/bin/env bash
set -euo pipefail
usage() { echo "usage: deploy.sh -v VERSION -e ENV [--dry-run] [--skip-smoke]"; exit 2; }
DRY=0; SMOKE=1
while [[ $# -gt 0 ]]; do case $1 in
  -v) VERSION=$2; shift 2;; -e) ENV=$2; shift 2;; --dry-run) DRY=1; shift;; --skip-smoke) SMOKE=0; shift;; *) usage;; esac; done
: "${VERSION:?} ${ENV:?}"
log() { printf '%s deploy env=%s version=%s %s\n' "$(date -u +%FT%TZ)" "$ENV" "$VERSION" "$*"; }
run() { if (( DRY )); then log "DRY: $*"; else log "RUN: $*"; "$@"; fi; }

# --- preflight: cheap, read-only, catches 90 % of failed deploys
[[ $ENV =~ ^(dev|staging|prod)$ ]] || { log "unknown env"; exit 2; }
[[ -f "deploy/envs/$ENV/values.yaml" ]] || { log "missing env config"; exit 2; }
docker manifest inspect "ghcr.io/example/app:$VERSION" >/dev/null || { log "image $VERSION not in registry"; exit 2; }
kubectl --context "$ENV" auth can-i update deployments -n app >/dev/null || { log "no permission"; exit 2; }
[[ $ENV == prod && -n ${CI:-} && -z ${DEPLOY_APPROVED:-} ]] && { log "prod needs approval gate"; exit 2; }

# --- lock: one deploy per env at a time
LOCK="deploy-lock-$ENV"
run kubectl --context "$ENV" -n app create configmap "$LOCK" --from-literal=by="${GITHUB_ACTOR:-$USER}" --from-literal=version="$VERSION" \
  || { log "another deploy holds $LOCK"; kubectl --context "$ENV" -n app get cm "$LOCK" -o jsonpath='{.data}'; exit 3; }
trap 'kubectl --context "$ENV" -n app delete cm "$LOCK" --ignore-not-found >/dev/null' EXIT

# --- apply (declarative, convergent)
run helm upgrade --install app ./deploy/chart -n app --kube-context "$ENV" \
  -f "deploy/envs/$ENV/values.yaml" --set image.tag="$VERSION" \
  --atomic --wait --timeout 10m --history-max 10

# --- verify
(( SMOKE )) && run ./deploy/smoke.sh "$ENV"
run ./deploy/record.sh "$ENV" "$VERSION" success     # deployments API / event table
log "done"
```
Points: `--atomic` rolls back the Helm release on failure; `--wait` makes the exit code
mean "healthy"; the lock prevents two pipelines colliding (`resource_group`/
`concurrency` in CI do the same at the CI layer — keep both for laptop runs); `--dry-run`
prints every mutating command. In Python/Go the same structure: parse args → preflight →
lock → converge → verify → record, with structured logs.

## 3. Idempotency checklist
- Creating things: use create-or-update primitives (`apply`, `upgrade --install`,
  `put-parameter --overwrite`, `aws s3 sync`) or check-then-act with a tolerant exit.
- Migrations: run through a migration tool with a version table (Flyway/Liquibase/
  Alembic/golang-migrate); re-running applies nothing.
- Restarts: only when the spec changed (checksum annotation on the pod template), never
  `rollout restart` unconditionally.
- Data seeds: `INSERT … ON CONFLICT DO NOTHING` / upserts keyed by natural ids.
- External registrations (DNS, webhooks, API keys): read current state, diff, apply
  minimal change; record external ids in state (Terraform) rather than recreating.
- Temp files/dirs: unique per run, cleaned in `trap`.
- Test it: deploy twice in a row in CI; the second run must make zero changes
  (`helm diff`/`terraform plan` shows nothing; the script logs "no changes").

## 4. Preflight and health gates worth having
Preflight: artifact exists and is signed (see provenance skills); config renders and
validates; target cluster/host reachable with the needed permissions; no active incident
freeze flag; disk/capacity headroom for the new version; migration dry-run (`--check`).
Post-deploy: readiness/liveness gate (`--wait`), smoke suite against the real endpoint,
error-rate/latency check over 5–10 minutes (query Prometheus; abort + rollback above the
threshold — the canary skills cover automated analysis), synthetic transaction.

## 5. Timeouts, retries, exit codes
Every external call has a timeout (`--timeout`, `curl --max-time`); retries only for
idempotent calls with backoff (`until`/`retry` loop capped at N); distinct exit codes
(2 usage/preflight, 3 locked, 4 apply failed, 5 verification failed) so the pipeline and
humans can tell what happened; never `|| true` on a step that matters.

## 6. VM/host deployments without Kubernetes
Same principles with Ansible (`ansible-playbook -i inventory/$ENV deploy.yml -e version=$VERSION --check --diff` for dry-run;
`serial: 25%` + `max_fail_percentage` for rolling; handlers restart only on change), or
cloud-native deployers (CodeDeploy/`aws deploy`, Azure Deployment Slots, Cloud Run
revisions with `--no-traffic` then `update-traffic`). Immutable images (Packer AMIs,
container images) + instance refresh beat in-place package upgrades for repeatability.

## 7. Anti-patterns
Manual steps "just this once"; SSH-and-pull-from-Git on the server; environment-specific
branches of the script; secrets passed as CLI args (visible in `ps`); scripts that need
to be run "from the right directory"; deploy logic only in the CI YAML (not runnable
locally); no record of what version is where.

## Verify
- [ ] `deploy.sh -v X -e staging` twice in a row: second run reports no changes, exit 0.
- [ ] `--dry-run` lists every mutating command and touches nothing.
- [ ] A deliberately missing image makes preflight fail in < 10 s with a clear message, before any change.
- [ ] Two concurrent runs: one proceeds, one exits 3 with the holder's identity.
- [ ] Rollback is the same command with the previous version and is exercised in staging weekly.
