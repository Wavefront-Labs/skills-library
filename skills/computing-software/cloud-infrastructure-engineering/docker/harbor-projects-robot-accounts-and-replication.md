---
id: computing-software.cloud-infrastructure-engineering.docker.harbor-projects-robot-accounts-and-replication
name: harbor-projects-robot-accounts-and-replication
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, harbor, private-registry, harbor-projects, harbor-robot-account, harbor-replication, proxy-cache, quotas]
level: advanced
description: "Organise Harbor into projects with quotas and roles, issue scoped robot accounts for CI, and set up push/pull replication and proxy-cache projects."
sources: ["https://goharbor.io/docs/main/working-with-projects/create-projects/", "https://goharbor.io/docs/main/working-with-projects/project-configuration/create-robot-accounts/", "https://goharbor.io/docs/main/administration/configuring-replication/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Harbor projects, robot accounts and replication

## Projects
A project is the unit of access control, quota, retention, immutability and scanning.
`harbor.example.com/<project>/<repo>:<tag>`.
- **Public** projects allow anonymous pull; private need a member role.
- Roles: Project Admin, Maintainer (push, delete, scan), Developer (push, pull), Guest (pull, retag,
  see members and logs), Limited Guest (pull and list repositories and images, but not members or logs).
  The Harbor permissions-by-role table is the reference.
- Per-project settings: storage quota, "Prevent vulnerable images from running" (severity
  threshold), automatic scan on push, Cosign / Notation deployment security, CVE allowlist, webhooks,
  tag retention and tag immutability rules.

## Robot accounts for CI
UI: Project -> Robot Accounts -> New, or API:
```sh
curl -u admin:pass -H 'Content-Type: application/json' -X POST \
  https://harbor.example.com/api/v2.0/robots -d '{
  "name":"ci-api","duration":90,"level":"project",
  "permissions":[{"kind":"project","namespace":"team-a",
    "access":[{"resource":"repository","action":"push"},{"resource":"repository","action":"pull"}]}]}'
```
Login name is `<prefix><project_name>+<account_name>`; the default prefix is `robot$` and an administrator
can change it. Quote it in shells:
`docker login harbor.example.com -u 'robot$team-a+ci-api' --password-stdin`.
- Harbor does not store the secret: download or copy it at creation, and store it in the CI secret store.
  A lost secret cannot be retrieved, but it can be refreshed.
- API `duration` is in days and must be `-1` (never) or a positive integer; prefer expiry plus rotation
  with `PATCH /robots/{robot_id}` (RefreshSec).
- System robot accounts can cover multiple projects; keep them rare.

## Replication
Administration -> Registries (endpoint providers include another Harbor, Docker Hub, Docker registry,
AWS ECR, Azure Container Registry, Google registries, GitHub Container Registry, JFrog Artifactory and
others), then Replications -> rule:
- **Push-based**: local -> remote (DR site, edge registry).
- **Pull-based**: remote -> local (mirror vendor images).
- Filters: name (`team-a/**`), tag (`v*`), label, resource type; name and tag filters support `*`, `**`,
  `?` and `{alt1,alt2}`. Add `library/` to match Docker Hub official images.
- Trigger modes: Manual, Scheduled (cron) and Event Based (push, retag, and delete when "Delete remote
  resources when locally deleted" is set). Manual and scheduled runs do not replicate deletions.
- Other options: Override, destination flattening (default is flatten 1 level), per-task bandwidth, and
  copy by chunk (verified between Harbor instances only).
- Resources matching the filters and their associated Cosign signatures are replicated.

## Proxy-cache project
Create a project with "Proxy Cache" pointing at a Docker Hub endpoint, then pull
`harbor.example.com/dockerhub-proxy/library/nginx:1.27`. Harbor creates a 7 day retention policy for
each new proxy cache project. Pushing to a proxy cache project is not possible. Harbor documents
proxy cache as a way to limit requests to a public registry.

## Verify
`docker push` with the robot succeeds to its project and is refused for another project;
the replication execution log shows success and tag counts match.

## Checked

2026-10-26. Documentation release: Harbor website docs main (goharbor/website, last commit 2026-10-15) and goharbor/harbor api/v2.0/swagger.yaml. Confirmed: project role capabilities from the permissions-by-role table (Limited Guest can list repositories and images, so the old "no listing" wording was wrong), robot naming format `<prefix><project_name>+<account_name>` with default prefix robot$, secrets not stored and refreshable, API duration rule (-1 or positive days), PATCH on /robots/{robot_id} is RefreshSec, replication endpoint providers, trigger modes, deletion not replicated for manual and scheduled, filter patterns, flattening default, bandwidth and copy by chunk notes, Cosign signatures replicated, proxy cache 7 day default retention. Removed unconfirmed claims: replication copying SBOM accessories, event-based replication being push-based only, and the `unauthorized` error text.

Method: documentation only; no commands were run.
