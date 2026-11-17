---
id: computing-software.devops-ci-cd.gitlab-ci.environments-api-and-stale-cleanup
name: environments-api-and-stale-cleanup
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, environments-api, stale-environments, stop-stale-environments, review-apps-cleanup, auto-stop-in]
level: practitioner
status: docs-checked
description: "Keep environments under control: auto_stop_in, stop jobs, and the Environments API to list, stop stale and bulk-delete stopped review apps on a schedule."
sources: ["https://docs.gitlab.com/api/environments/", "https://docs.gitlab.com/ci/environments/#stop-an-environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environments API and stale cleanup

Hundreds of forgotten `review/*` environments cost money (live deployments) and clutter the UI.

## 1. Prevent: auto-stop
```yaml
deploy-review:
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.review.example.com
    on_stop: stop-review
    auto_stop_in: 3 days
stop-review:
  environment: { name: review/$CI_COMMIT_REF_SLUG, action: stop }
  when: manual
  script: ./teardown.sh "$CI_ENVIRONMENT_SLUG"
  rules: [{ if: $CI_MERGE_REQUEST_IID, when: manual }]
```
GitLab stops the environment when the branch is deleted or merged, and `auto_stop_in` accepts natural-language periods such as `1 day` or `3 days`. If the stop script lives in the repository, use merge request pipelines for the stop job so the runner can still fetch code after the branch is deleted.

## 2. Clean up: API
```bash
API="$CI_API_V4_URL/projects/$PID"
# list available review environments
curl -s -H "PRIVATE-TOKEN: $T" "$API/environments?states=available&search=review/&per_page=100" | jq -r '.[]|[.id,.name,.updated_at]|@tsv'
# stop environments not modified or deployed to since a date (excludes protected environments; `before` must be between 10 years and 1 week ago)
curl -X POST -H "PRIVATE-TOKEN: $T" "$API/environments/stop_stale?before=$(date -u -d '30 days ago' +%FT%TZ)"
# schedule deletion of stopped review apps (dry_run defaults to true; deletion runs 1 week later; default is 30 days or older)
curl -X DELETE -H "PRIVATE-TOKEN: $T" "$API/environments/review_apps?before=$(date -u -d '30 days ago' +%FT%TZ)&limit=100&dry_run=true"
# stop / delete one
curl -X POST   -H "PRIVATE-TOKEN: $T" "$API/environments/<id>/stop"
curl -X DELETE -H "PRIVATE-TOKEN: $T" "$API/environments/<id>"     # must be stopped first
```
Run these from a scheduled pipeline with a token allowed to call the Environments API (see its page for the required role).

## 3. Gotchas
- If the `on_stop` script exists only in the repository, it cannot use `GIT_STRATEGY: none` or `empty`; stop jobs for deleted branches need merge request pipelines.
- `force=true` on the stop call stops without running `on_stop` — infrastructure stays running; clean it separately.
- `review_apps` deletion only targets environments that are already stopped and in the review app folder.
- Protected environments cannot be stopped by users without deploy access.

## Verify
- [ ] Environments page shows no available review apps older than the policy.
- [ ] Cloud/K8s namespaces count matches available environments.

## Checked

2026-11-02. Confirmed: `states` filter values and `search` (3+ chars) on the list call; `stop_stale` and `review_apps` endpoints with their `before` and `dry_run` semantics; `force` parameter; delete requires a stopped environment (GitLab Environments API); auto_stop_in natural-language periods, stop on branch delete/merge, GIT_STRATEGY and on_stop caveat (GitLab environments docs). Removed: timer-reset claim, Maintainer-token claim, the incorrect `GIT_STRATEGY: none` advice for repository scripts.

Method: documentation only; no commands were run.
