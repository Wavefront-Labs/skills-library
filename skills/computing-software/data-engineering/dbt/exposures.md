---
id: computing-software.data-engineering.dbt.exposures
name: exposures
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, exposures, dbt-docs, downstream-lineage, dashboards, impact-analysis, exposure-selection, maturity, owner]
level: practitioner
status: docs-checked
description: "Declare dbt exposures for dashboards, ML models and apps: YAML fields, depends_on refs, selecting +exposure:name to rebuild what a dashboard needs, and impact analysis."
sources:
  - https://docs.getdbt.com/docs/build/exposures
  - https://docs.getdbt.com/reference/exposure-properties
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exposures

**Goal:** the DAG shows who consumes each model, so changes can be assessed for impact and critical consumers can be built and tested as a unit.

## Declare
```yaml
# models/marts/finance/_finance__exposures.yml
exposures:
  - name: weekly_revenue_dashboard
    label: Weekly Revenue (Looker)
    type: dashboard                 # dashboard | notebook | analysis | ml | application
    maturity: high                  # high | medium | low
    url: https://looker.acme.com/dashboards/412
    description: Exec revenue review every Monday 09:00.
    depends_on:
      - ref('fct_revenue')
      - ref('dim_customers')
      - metric('weekly_net_revenue')       # ref, source and metric are allowed
    owner:                          # name or email required
      name: Finance Analytics
      email: finance-analytics@acme.com
    config:
      tags: ['tier1']
```

## Use them
```bash
dbt build -s +exposure:weekly_revenue_dashboard          # everything the dashboard needs, with tests
dbt ls -s "state:modified+" --resource-type exposure --state prod-state   # exposures downstream of modified nodes
```

## Keep them current
- Exposures declared in YAML are manual; the dbt platform can also create downstream exposures automatically for supported integrations (see downstream exposures docs). Stale manual exposures mislead.
- `owner` needs a `name` or `email` (more properties are allowed), so decide a convention that lets incidents be routed.

## Verify
- [ ] The docs lineage graph shows the exposure node downstream of its models, and `url` populates the "View this exposure" link.
- [ ] `dbt ls -s +exposure:<name>` returns the expected upstream set.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt exposures and exposure-properties pages: `exposures:` key in `.yml` files, `type` values (dashboard, notebook, analysis, ml, application), `maturity` values (high, medium, low), `url`, `label`, `owner` needing name or email, `depends_on` of ref, source and metric, `config` with tags and meta (v1.10), automatic exposures from the dbt platform, and `+exposure:<name>` selection (`dbt run -s +exposure:...`, `dbt test`). Removed unconfirmed CI-comment and tier-severity advice and third-party BI sync tools.

Method: documentation only; no commands were run.
