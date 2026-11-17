---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pyroscope-labels-and-dynamic-tagging
name: pyroscope-labels-and-dynamic-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [pyroscope, pyroscope-labels, profile-tagging, span-profiles, cardinality]
level: advanced
status: docs-checked
description: "Add static and dynamic labels to Pyroscope profiles in Go, Java and Python (tag wrappers around code regions) and know the valid tag name format."
sources: ["https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/go_push/", "https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/java/", "https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/python/", "https://grafana.com/docs/pyroscope/latest/configure-client/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pyroscope labels and dynamic tagging

**Goal:** slice profiles by endpoint, controller or region, using labels (also called tags) that filter data in the UI.

## Valid tag names
Tags may contain ASCII letters, digits and underscores, matching `[a-zA-Z_][a-zA-Z0-9_]`. A period is not valid in a tag or label name. You can add tags with the SDK and with Alloy.

## Static labels (per process)
Go (`Tags` in the config):
```go
pyroscope.Start(pyroscope.Config{
  ApplicationName: "simple.golang.app",
  ServerAddress:   "http://pyroscope-server:4040",
  Tags:            map[string]string{"hostname": os.Getenv("HOSTNAME")},
})
```
Java: `Pyroscope.setStaticLabels(Map.of("region", System.getenv("REGION")))`, or `.setLabels(...)` on `Config.Builder`, or the `PYROSCOPE_LABELS` variable (comma separated key=value pairs).

Python: the `tags` argument of `pyroscope.configure(...)`, for example `tags = {"region": os.getenv("REGION")}`.

## Dynamic labels (per code region)
Go (the two forms are equivalent):
```go
pyroscope.TagWrapper(context.Background(), pyroscope.Labels("controller", "slow_controller"), func(c context.Context) {
  slowCode()
})
pprof.Do(context.Background(), pprof.Labels("controller", "slow_controller"), func(c context.Context) {
  slowCode()
})
```
Java:
```java
Pyroscope.LabelsWrapper.run(new LabelsSet("controller", "slow_controller"), () -> {
  slowCode();
});
```
Python:
```python
with pyroscope.tag_wrapper({ "controller": "slow_controller_i_want_to_profile" }):
    slow_code()
```
Then filter by the label in the Pyroscope UI.

## Python gotcha: forking
`pyroscope.configure()` starts background threads and is not fork-safe afterwards. Call it only after the last fork in each process; for pre-fork servers such as Gunicorn, call it from a `post_fork` hook and keep it out of modules imported in the parent when `preload_app` is on.

## Java OTLP gotcha
With `PYROSCOPE_FORMAT=otlp` (experimental), the application name and static or dynamic labels are not included in OTLP profiles, so profiles may appear under `service_name="unknown_service"`.

## Checked
2026-11-08. Confirmed in the Pyroscope Go (push), Java, Python and Configure the client pages. Removed: Ruby and .NET wrappers, span profile `span_id`/`otelpyroscope` claims, the `max_label_names_per_series` limit, Alloy discovery label names, cardinality rules (not stated on these pages) and the Verify checklist.
Method: documentation only; no commands were run.
