---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-service-accounts-orgs-and-api-automation
name: grafana-service-accounts-orgs-and-api-automation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-api, service-accounts, service-account-tokens-automation, token-rotation, organizations-management, multi-org, org-api, grafana-api-pagination, api-search, folder-api]
level: practitioner
status: gated
description: "Automate Grafana safely: service accounts and token rotation, multi-org management via API, search/folder APIs with pagination, and X-Grafana-Org-Id scoping."
sources: ["https://grafana.com/docs/grafana/latest/administration/service-accounts/", "https://grafana.com/docs/grafana/latest/developers/http_api/", "https://grafana.com/docs/grafana/latest/developers/http_api/org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service accounts, orgs and API automation

## Service accounts
```bash
SA=$(curl -s -XPOST $G/api/serviceaccounts -u admin:$PW -H 'Content-Type: application/json' \
  -d '{"name":"ci-dashboards","role":"Editor","isDisabled":false}' | jq .id)
curl -s -XPOST $G/api/serviceaccounts/$SA/tokens -u admin:$PW -H 'Content-Type: application/json' \
  -d '{"name":"ci-2026-10","secondsToLive":7776000}' | jq -r .key      # glsa_... shown once
```
- Use service accounts: in Grafana 13.2.4 `GET /api/auth/keys` returns 404 (user API keys are gone; they were migrated to service accounts).
- Least privilege: Viewer + specific RBAC roles where available; one SA per automation.
- **Rotation**: create new token, deploy it, delete old (`DELETE /api/serviceaccounts/$SA/tokens/<id>`).
  `secondsToLive` forces expiry; check expiry with `GET /api/serviceaccounts/$SA/tokens` (each token has `expiration`).
- Tokens start with `glsa_`; `GET /api/serviceaccounts/search` lists accounts and each token row has `expiration`, `hasExpired`, `isRevoked`. Leaked-token scanning on GitHub is a vendor feature not checked here (gated: unconfirmed, source is paywalled or blocked).

## Organizations
```bash
curl -s -XPOST $G/api/orgs -u admin:$PW -H 'Content-Type: application/json' -d '{"name":"customer-a"}'
curl -s -XPOST $G/api/orgs/3/users -u admin:$PW -H 'Content-Type: application/json' -d '{"loginOrEmail":"alice","role":"Viewer"}'
curl -s $G/api/dashboards/uid/x -u admin:$PW -H 'X-Grafana-Org-Id: 3'     # act in another org (basic auth / server admin); a dashboard of org 1 returns `Dashboard not found` there
```
Orgs are hard isolation (separate data sources, dashboards, users' roles); service accounts belong to one org (`POST /api/serviceaccounts` with `X-Grafana-Org-Id: 2` created `sa-2-org2-sa` with `orgId: 2`, and the org-1 search did not list it).
Prefer folders + teams + RBAC inside one org unless tenants must never see each other's resources.

## Search and pagination
```bash
page=1; while :; do
  r=$(curl -s -H "Authorization: Bearer $T" "$G/api/search?type=dash-db&limit=1000&page=$page")
  [ "$(echo "$r" | jq length)" -eq 0 ] && break
  echo "$r" | jq -r '.[] | [.uid, .folderTitle, .title] | @tsv'; page=$((page+1))
done
curl -s -H "Authorization: Bearer $T" "$G/api/folders?limit=1000&page=1"      # nested folders: ?parentUid=
```
`limit` above 5000 is rejected (`limit=5001` returned HTTP 422); `limit=1&page=2` returns the second item. The documented default limit was not checked here (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] No user-owned API keys in automation; every SA has an owner and expiry.
- [ ] Backup/export script enumerates all dashboards across pages and orgs.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local.
- Ran: create SA, create token with `secondsToLive` (list showed `expiration` about 90 days out), token delete (`Service account token deleted`), org create, add user to org, `X-Grafana-Org-Id` dashboard lookup and SA create, `/api/search` with `limit` 1, 0, 5000, 5001 and `page`, `/api/folders?limit=&page=` and `parentUid=`, `/api/auth/keys` (404).
- `jq` is not installed here, so the jq filters were checked against the JSON shapes in Python (`id`, `key`, `.[]` arrays).
- Two vendor claims (leak scanning, default search limit) carry the gated marker, so the skill is `gated`.
