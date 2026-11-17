---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-nginx-metrics-and-access-logs
name: ingress-nginx-metrics-and-access-logs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, ingress-access-logs, ingress-nginx, prometheus, access-logs]
level: practitioner
status: docs-checked
description: "Expose ingress-nginx Prometheus metrics, tune the access log format to JSON and query request rates, latency and errors per Ingress and host."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/monitoring/", "https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/", "https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/log-format/", "https://github.com/kubernetes/ingress-nginx/blob/main/internal/ingress/metric/collectors/socket.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ingress-nginx metrics and access logs

## Metrics
Helm values:
```yaml
controller:
  metrics:
    enabled: true            # /metrics on port 10254
    serviceMonitor:
      enabled: true
      additionalLabels: {release: kube-prometheus-stack}   # must match your kube-prometheus-stack Helm release name
```
Useful series:
```promql
sum by (ingress, status) (rate(nginx_ingress_controller_requests[5m]))
histogram_quantile(0.99, sum by (le, ingress) (rate(nginx_ingress_controller_request_duration_seconds_bucket[5m])))
sum(rate(nginx_ingress_controller_requests{status=~"5.."}[5m])) by (ingress) / sum(rate(nginx_ingress_controller_requests[5m])) by (ingress)
```
Request metrics carry labels such as `ingress`, `status` and `path`; the monitoring docs say running the controller with `--metrics-per-host=false` drops the hostname label to reduce cardinality.

## Access logs as JSON
```yaml
controller:
  config:
    log-format-escape-json: "true"
    log-format-upstream: '{"time":"$time_iso8601","host":"$host","method":"$request_method","uri":"$uri","status":$status,"bytes":$bytes_sent,"req_time":$request_time,"upstream":"$upstream_addr","upstream_time":"$upstream_response_time","req_id":"$req_id","ingress":"$ingress_name","ns":"$namespace"}'
```
Turn off noisy endpoints per Ingress: `nginx.ingress.kubernetes.io/enable-access-log: "false"`.

## Reading a 502 or 504 in the log
Compare `status` with the documented log variables `$upstream_addr` (address of the contacted
upstream), `$upstream_response_time` and `$request_time`; the default log format also includes
`$upstream_status`. Match them against the proxy timeouts set in the Ingress annotations.

## Verify
`kubectl -n ingress-nginx port-forward deploy/ingress-nginx-controller 10254` then
`curl -s localhost:10254/metrics | grep -c nginx_ingress_controller_requests` is non-zero, and
log lines parse as JSON.

## Checked
2026-10-26. Checked against the ingress-nginx docs and source (repository kubernetes/ingress-nginx, archived, last commit 2026-03-23). Confirmed: `controller.metrics.enabled`, `controller.metrics.serviceMonitor.enabled` and `additionalLabels.release` (must match the kube-prometheus-stack release name); metrics on port 10254; metric names `nginx_ingress_controller_requests` and `nginx_ingress_controller_request_duration_seconds`; request metric labels include `status` and `ingress` (the `host` label is added when per-host metrics are on); `--metrics-per-host=false` reduces cardinality; log variables `$namespace`, `$ingress_name`, `$req_id`, `$upstream_addr`, `$upstream_response_time`, `$request_time`; `log-format-upstream` and `log-format-escape-json` keys; annotation `enable-access-log`. Removed as unconfirmed: the 499 and timeout interpretation of 502 and 504 log lines and the claim about log shippers.
Method: documentation only; no commands were run.
