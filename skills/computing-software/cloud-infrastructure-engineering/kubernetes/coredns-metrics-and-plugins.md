---
id: computing-software.cloud-infrastructure-engineering.kubernetes.coredns-metrics-and-plugins
name: coredns-metrics-and-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, coredns, coredns-metrics, prometheus, cluster-dns]
level: practitioner
status: docs-checked
description: "Monitor CoreDNS with its prometheus, log, errors, health and ready plugins: key metrics for latency, SERVFAIL rate, cache hits and forward health."
sources: ["https://coredns.io/plugins/metrics/", "https://coredns.io/plugins/health/", "https://coredns.io/plugins/log/", "https://coredns.io/plugins/forward/", "https://coredns.io/plugins/cache/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoreDNS metrics and observability plugins

## Corefile plugins (kubeadm default has most)
```
.:53 {
    errors                      # log errors
    health { lameduck 5s }      # :8080/health by default, lameduck delays shutdown
    ready                       # :8181/ready once plugins are ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```
Add `log` only temporarily or with a class filter (`log . { class denial error }`); full query
logging is very noisy at cluster scale.

## Key metrics
| Metric | Watch for |
|---|---|
| `coredns_dns_requests_total` | QPS by zone/type; sudden spikes (ndots storms) |
| `coredns_dns_responses_total{rcode}` | SERVFAIL rate; NXDOMAIN ratio (search path misses) |
| `coredns_dns_request_duration_seconds` | p99 latency |
| `coredns_cache_hits_total` | hits by cache type (`coredns_cache_misses_total` is deprecated; derive misses from hits and requests) |
| `coredns_proxy_request_duration_seconds{proxy_name="forward"}`, `coredns_proxy_healthcheck_failures_total`, `coredns_forward_healthcheck_broken_total` | upstream health (the older `coredns_forward_requests_total` and `coredns_forward_healthcheck_failures_total` are deprecated) |
| `coredns_forward_max_concurrent_rejects_total` | queries rejected by `max_concurrent` |
| `coredns_panics_total` | should be 0 |

```promql
sum(rate(coredns_dns_responses_total{rcode="SERVFAIL"}[5m])) / sum(rate(coredns_dns_responses_total[5m]))
histogram_quantile(0.99, sum(rate(coredns_dns_request_duration_seconds_bucket[5m])) by (le))
```

## Scrape
The `prometheus :9153` directive serves `/metrics` on port 9153 (the plugin's default is `localhost:9153`). Point your Prometheus scrape config or ServiceMonitor at that port of the CoreDNS pods or Service.

## Readiness
`ready` serves HTTP 200 on port 8181 when plugins are ready; `health` serves `/health` on `:8080` by
default, and `lameduck DURATION` delays shutdown while `/health` still answers 200.

## Verify
```bash
kubectl -n kube-system port-forward deploy/coredns 9153
# then request http://localhost:9153/metrics and look for coredns_dns_responses_total
```

## Checked

2026-10-26, against CoreDNS plugin READMEs (coredns/coredns main, latest commit 2026-10-25) and Kubernetes website docs (dns-custom-nameservers, nodelocaldns, dns-horizontal-autoscaling). Confirmed: `coredns_dns_requests_total`, `coredns_dns_responses_total`, `coredns_dns_request_duration_seconds`, `coredns_cache_hits_total`, `coredns_panics_total`, forward and proxy metric names and deprecations, health/ready ports, lameduck, `log` class values. Wrong or stale: forward metrics `coredns_forward_requests_total` and `coredns_forward_healthcheck_failures_total` are deprecated, `coredns_cache_misses_total` is deprecated, semicolon syntax inside the kubernetes block was not valid Corefile. Removed the unconfirmed kube-prometheus-stack scrape claim.

Method: documentation only; no commands were run.
