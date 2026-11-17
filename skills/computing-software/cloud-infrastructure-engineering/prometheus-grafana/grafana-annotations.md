---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-annotations
name: grafana-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, annotations, annotation-queries, tagged-annotations, annotations-api, deploy-markers, ci-cd]
level: practitioner
status: gated
description: "Mark deploys and incidents on Grafana graphs: annotation queries from Prometheus/Loki, tag-filtered Grafana annotations, and posting deploy events via the annotations API."
sources: ["https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/annotate-visualizations/", "https://grafana.com/docs/grafana/latest/developers/http_api/annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana annotations

## Annotation queries (dashboard settings -> Annotations)
| Source | Query | Result |
|---|---|---|
| Prometheus | `changes(kube_deployment_status_observed_generation{namespace="$namespace"}[2m]) > 0`, title `{{deployment}}` | a marker when a rollout happened (the annotation editor fields were not exercised in a browser here) (gated: unconfirmed, source is paywalled or blocked) |
| Prometheus | `ALERTS{alertstate="firing", severity="page"}` | firing periods as regions (gated: unconfirmed, source is paywalled or blocked) |
| Loki | `{app="argocd"} \|= "sync" \|= "$app"` | log line text as annotation text (no Loki ran here) (gated: unconfirmed, source is paywalled or blocked) |
| Grafana (built-in) | Filter by **Tags**: `deploy`, `$service` (template variables allowed) | events posted via API; all listed tags must match unless **Match any** is on |
Set colour per query, and "Show in" specific panels to avoid clutter.

## Post deploy events from CI
```bash
curl -s -XPOST https://grafana.example.com/api/annotations \
  -H "Authorization: Bearer $GRAFANA_SA_TOKEN" -H 'Content-Type: application/json' \
  -d "{\"tags\":[\"deploy\",\"checkout\",\"prod\"],
       \"text\":\"checkout $GIT_SHA by $CI_ACTOR <a href=\\\"$CI_URL\\\">pipeline</a>\",
       \"time\": $(date +%s000)}"
# region: add "timeEnd": <ms>; dashboard-scoped: add "dashboardUID": "abc" (and optional "panelId")
```
- Organisation-wide annotations (no dashboardUID) appear in any dashboard whose Grafana annotation query
  matches the tags; that's the scalable pattern.
- Service account role needs `annotations:create`: an Editor service account got `Annotation added`; a Viewer one got 403 `Permissions needed: annotations:create`. Deleting needs `annotations:delete` (Viewer got 403 there too).
- Query back: `GET /api/annotations?tags=deploy&tags=checkout&from=...&to=...` (repeated `tags` are ANDed; add `matchAny=true` for OR); delete: `DELETE /api/annotations/<id>` (returns `Annotation deleted`).
- A region annotation returns `timeEnd - time` equal to the span you posted; a point annotation has `timeEnd` equal to `time`.

## Gotchas
- Tag matching defaults to ALL tags (API: `matchAny=false`); turn on **Match any** (API `matchAny=true`) only when you want OR. Verified against the API: `tags=prod&tags=region` returned nothing for an annotation tagged `deploy,checkout,prod`, while `matchAny=true` returned it.
- Times are epoch **milliseconds**.
- Too many annotation queries on a dashboard slow every refresh; keep 2-4.

## Verify
- [ ] A deploy from CI appears as a marker on the service dashboard within seconds.
- [ ] Firing page alerts render as regions aligned with the error-rate spike.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 (local, scratch data dir), Prometheus 3.15.1.
- Ran the CI curl block against `/api/annotations` with an Editor service-account token (`glsa_` prefix): `Annotation added`; with a Viewer token: 403 naming `annotations:create`; region with `timeEnd`; tag queries with AND and `matchAny=true`; `DELETE` as admin worked, as Viewer returned 403 naming `annotations:delete`.
- Tag semantics and the built-in **Filter by Tags / Match any** option: Grafana docs page annotate-visualizations.
- The Prometheus and Loki annotation-query rows were not exercised in a browser (no Loki, and the editor fields were not clicked), so they carry the gated marker and the skill is `gated`.
