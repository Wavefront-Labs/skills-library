---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-profiler-agent-setup-by-language
name: cloud-profiler-agent-setup-by-language
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-profiler, profiling, java, go, python, nodejs]
level: practitioner
status: docs-checked
description: "Install the Cloud Profiler agent for Java, Go, Python and Node.js: service names and versions, IAM, profile types per language."
sources: ["https://cloud.google.com/profiler/docs/profiling-java", "https://cloud.google.com/profiler/docs/profiling-go", "https://cloud.google.com/profiler/docs/profiling-python", "https://cloud.google.com/profiler/docs/profiling-nodejs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Profiler agent setup by language

Grant the workload service account `roles/cloudprofiler.agent` (Cloud Profiler Agent); enable the Cloud Profiler API.
Use the same `service` name across replicas and set a real version so releases can be compared in the UI.

## Java
```dockerfile
ENTRYPOINT ["java","-agentpath:/opt/cprof/profiler_java_agent.so=-cprof_service=orders,-cprof_service_version=1.4.2,-cprof_enable_heap_sampling=true","-jar","app.jar"]
```
Install the agent into `/opt/cprof` as the "Installing the Profiler agent" section describes (glibc and Alpine/musl
builds differ). `-cprof_service` is required when not on App Engine; `-cprof_service_version` enables per-version
analysis. Profiles: CPU time, heap (needs Java 11 or App Engine standard, disabled by default), wall time.
Supported on Linux with glibc or musl. Alpine is supported only on GKE.

## Go
```go
import "cloud.google.com/go/profiler"
if err := profiler.Start(profiler.Config{Service: "orders", ServiceVersion: "1.4.2", MutexProfiling: true}); err != nil { log.Printf("profiler: %v", err) }
```
Profiles: CPU time, heap, allocated heap, contention (Go mutex, enabled by `MutexProfiling: true`), threads (goroutines).

## Python
```python
import googlecloudprofiler
try:
    googlecloudprofiler.start(service="orders", service_version="1.4.2", verbose=1)
except (ValueError, NotImplementedError) as e:
    print(e)
```
`service` is required; `service_version` optional. Profiles: CPU time and wall time (main thread). The docs cover
Python 3.6 through 3.11.0 and a build toolchain (`build-essential`; `build-base` on Alpine) is needed to install the
agent. `NotImplementedError` means a non-Linux environment.

## Node.js
```js
require('@google-cloud/profiler').start({serviceContext: {service: 'orders', version: '1.4.2'}});
```
Profiles: heap and wall time.

## Gotchas
- Outside Google Cloud, pass the project ID (Java: `-cprof_project_id`) and credentials explicitly.
- Wrap start in error handling so a profiler failure never crashes the app.

## Verify
- [ ] Profiler UI lists the service and version with profiles of each type.

## Checked
2026-10-28. Confirmed on the four language pages: role id, Java options and profile types, Go config and profile types,
Python `start` arguments, exceptions, profile types, version range and build packages, Node profile types, Linux
support. Removed (not on the pages): overhead figure, Java ARM/x86 claim, Cloud Run throttling note, Node "first
require" rule, GKE service-name defaults, "within minutes" wording, the agent download URL.
Method: documentation only; no commands were run.
