---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-foundation-sdk-dashboards-as-code
name: grafana-foundation-sdk-dashboards-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [foundation-sdk, grafana-foundation-sdk, dashboards-as-code, grafana-as-code, golang, typescript]
level: practitioner
status: docs-checked
description: "Generate Grafana dashboards in Go, TypeScript, Python, PHP or Java with the Grafana Foundation SDK builders, then publish the JSON via API, CLI or Git Sync."
sources: ["https://github.com/grafana/grafana-foundation-sdk", "https://grafana.com/docs/grafana/latest/as-code/observability-as-code/foundation-sdk/", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana Foundation SDK

Strongly typed types and builder libraries for dashboards and other resources (alerts among them), in Go, TypeScript,
Python, PHP and Java. The repository says it is best suited to Grafana >= 12 but works with Grafana >= 10; the docs
get-started page lists Grafana v10.0 or higher as the prerequisite.

## Install
- Go: `go get github.com/grafana/grafana-foundation-sdk/go@latest`
- TypeScript: `npm install @grafana/grafana-foundation-sdk`
- Other languages: see the repository README.

## Go example (from the repository README)
```go
import (
  "encoding/json"; "fmt"
  "github.com/grafana/grafana-foundation-sdk/go/common"
  "github.com/grafana/grafana-foundation-sdk/go/dashboard"
  "github.com/grafana/grafana-foundation-sdk/go/prometheus"
  "github.com/grafana/grafana-foundation-sdk/go/timeseries"
  "github.com/grafana/grafana-foundation-sdk/go/units"
)
func main() {
  b := dashboard.NewDashboardBuilder("Sample dashboard").
    Uid("generated-from-go").Tags([]string{"generated", "from", "go"}).
    Refresh("1m").Time("now-30m", "now").Timezone(common.TimeZoneBrowser).
    WithRow(dashboard.NewRowBuilder("Overview")).
    WithPanel(timeseries.NewPanelBuilder().Title("Network Received").Unit(units.BitsPerSecondSI).Min(0).
      WithTarget(prometheus.NewDataqueryBuilder().
        Expr(`rate(node_network_receive_bytes_total{device!="lo"}[$__rate_interval]) * 8`).
        LegendFormat("{{ device }}")))
  d, err := b.Build()   // configuration errors surface here
  if err != nil { panic(err) }
  out, _ := json.MarshalIndent(d, "", "  ")
  fmt.Println(string(out))
}
```
TypeScript uses `new dashboard.DashboardBuilder("...")`, `new timeseries.PanelBuilder()`, `.withPanel(...)` and
`builder.build()`. Besides panels and queries the SDK covers variables, thresholds, field overrides and transformations.

## Publish the JSON
After `build()`, output the JSON and then: paste it into Grafana's dashboard import, call Grafana's API, use the
Grafana CLI, or use Git Sync. Store the generator code in Git and run it from CI. The JSON model docs describe the
schema the APIs accept.

## Patterns
- Write helper functions per panel type and generate one dashboard per service from a list.
- Keep `Uid` stable so links survive regeneration (set with `.Uid(...)` as above).

## Gotchas
- Maturity: the repository calls the code "public preview": used in production by Grafana Labs but under active
  development, with no on-call support or SLAs.
- Alert rules and other resources are separate resource types; check the API reference for what the SDK covers.

## Verify
- [ ] `Build()` returns no error and the JSON imports into your Grafana version.

## Checked
Checked 2026-11-08 against the Foundation SDK GitHub README and the Grafana docs get-started page (languages,
install commands, Go example, builder pattern, publish options, public-preview maturity, Grafana version notes).
Removed: the "pin SDK branch v11.x/v12.x" advice and "newer SDK may emit fields older servers reject" gotcha (not
stated), the Grizzly and grafanactl deploy options (Grizzly is removed), the Terraform deploy route and the
`reqps` unit example (not on these pages).
Method: documentation only; no commands were run.
