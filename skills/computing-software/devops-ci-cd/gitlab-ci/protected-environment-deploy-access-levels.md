---
id: computing-software.devops-ci-cd.gitlab-ci.protected-environment-deploy-access-levels
name: protected-environment-deploy-access-levels
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, deploy-access-levels, protected-environments, deployment-safety]
level: practitioner
status: docs-checked
description: "Restrict who can deploy to GitLab protected environments with deploy_access_levels (roles, users, groups) via UI or API, and how it interacts with branch protection."
sources: ["https://docs.gitlab.com/ci/environments/protected_environments/", "https://docs.gitlab.com/api/protected_environments/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protected environment deploy access levels

Protecting an environment limits who can deploy to it to the principals listed in its deploy access levels. The protected environments API is a Premium and Ultimate feature and needs CI/CD turned on for the project.

## API
```bash
curl --request POST --header "PRIVATE-TOKEN: $TOKEN" --header "Content-Type: application/json" \
  "https://gitlab.example.com/api/v4/projects/$PID/protected_environments" --data '{
    "name": "production",
    "deploy_access_levels": [
      {"group_id": 42, "group_inheritance_type": 1},
      {"user_id": 7}
    ]
  }'
```
Each entry takes one of `access_level` (30 Developer, 40 Maintainer, 60 Admin), `user_id` or `group_id`. `group_inheritance_type` is 0 (direct group membership only, the default) or 1 (all inherited groups). Prefer a group over a role: a role grants everyone who holds it.

## Interplay
- Protected environments do not protect the branch. Pair with protected branches so only reviewed
  code reaches the deploy job, and with protected variables so secrets exist only there.
- Group-level protected environments also exist (see the group-level protected environments API).

## Verify
- [ ] A developer outside the group cannot run the deploy job.
- [ ] `GET /projects/:id/protected_environments/production` lists the expected access levels.

## Checked

2026-10-28. Confirmed on the Protected environments API page: POST /projects/:id/protected_environments, deploy_access_levels entries of user_id, group_id or access_level, access levels 30/40/60, group_inheritance_type 0 or 1, GET /projects/:id/protected_environments/:name, Premium/Ultimate tier. Removed: required_approval_count in the create call, the permission message, the Terraform resource names, schedule-owner, tier-override and downstream-deploy claims (not on the fetched pages).
Method: documentation only; no commands were run.
