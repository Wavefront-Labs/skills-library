---
id: computing-software.cloud-infrastructure-engineering.knative.request-logging
name: request-logging
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [request-logging, enable-request-log, request-log-template, config-observability, probe-request-log]
level: practitioner
status: docs-checked
description: "Turn on queue-proxy request logs with config-observability and a single-line Go template."
sources:
  - https://knative.dev/docs/serving/observability/logging/request-logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: log every request that passes through a Revision's queue-proxy.

Request logging is managed in the `config-observability` ConfigMap in `knative-serving`. The queue-proxy sidecar prints the request logs.

Keys:
- `logging.enable-request-log`: if true, request logging is enabled.
- `logging.enable-probe-request-log`: if true, the queue proxy also writes request logs for probe requests to stdout, using the same template as user requests.
- `logging.request-log-template`: the shape of each log line. It must be a valid Go `text/template`, and it is important to keep it on a single line: most collection agents parse multiple lines as separate entries and would split one request log apart.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-observability
  namespace: knative-serving
data:
  logging.enable-request-log: "true"
```

Read the logs from the `queue-proxy` container of a Revision's pod, for example with `kubectl logs <pod-name> -c queue-proxy`.

Probe request logging is controlled separately by `logging.enable-probe-request-log`, so set it only if you want probe requests in the output.

## Checked

2026-11-04. Confirmed against the Configuring Request Log Settings page (knative/docs source): logging managed in the `config-observability` ConfigMap in `knative-serving`, request logs printed by the queue-proxy sidecar, and the three keys `logging.enable-request-log`, `logging.enable-probe-request-log` (same template as user requests) and `logging.request-log-template` (valid Go text/template, keep on a single line). Removed the claims that probe logging is off by default and that the lines show requests the user container never answered, which the page does not state. The `kubectl logs ... -c queue-proxy` command follows from the page saying the sidecar prints the logs but is not itself shown there.

Method: documentation only; no commands were run.
