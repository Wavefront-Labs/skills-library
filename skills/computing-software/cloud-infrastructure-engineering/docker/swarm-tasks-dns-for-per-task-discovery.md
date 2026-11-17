---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-tasks-dns-for-per-task-discovery
name: swarm-tasks-dns-for-per-task-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-overlay, tasks-dns, service-discovery, endpoint-mode, dnsrr, prometheus-dns-sd]
level: advanced
status: docs-checked
description: "Discover individual Swarm task IPs with tasks.<service> DNS instead of the VIP: clustering databases, Prometheus scraping every replica, and how it differs from dnsrr."
sources: ["https://docs.docker.com/engine/swarm/networking/", "https://docs.docker.com/engine/swarm/ingress/", "https://github.com/prometheus/prometheus/blob/main/docs/configuration/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tasks.<service> DNS for per-task discovery

On an overlay network, Swarm's embedded DNS answers:
| Query | Answer |
|---|---|
| `<service>` (default `endpoint_mode: vip`) | One virtual IP; IPVS load-balances connections across tasks |
| `<service>` with `endpoint_mode: dnsrr` | A records of all task IPs |
| `tasks.<service>` | A records of the task IPs, one per running replica |

```bash
docker exec -it $(docker ps -q -f name=shop_api | head -1) sh -c \
  'nslookup shop_web; nslookup tasks.shop_web'
```

## When you need it
- **Prometheus scraping each replica** (VIP would hit a random one each scrape):
```yaml
scrape_configs:
  - job_name: node-exporter
    dns_sd_configs:
      - names: ["tasks.monitoring_node-exporter"]
        type: A
        port: 9100
```
- **Clustered software** that needs peer addresses: point its seed or peer-discovery setting at `tasks.<service>`.
- **Client-side load balancing**, where the client wants all task addresses instead of one VIP.

## Behaviour notes
- Answers change as tasks move; clients must re-resolve (DNS caching in client runtimes can hide changes).
- Queries are answered by Docker's embedded DNS for containers on a network the service is attached to.

## dnsrr vs tasks.
`endpoint_mode: dnsrr` has no single VIP: a DNS query for the service name returns the task IPs and the client connects directly. It is meant for use with your own load balancer, and the routing mesh cannot publish ports in
ingress mode for such a service. `tasks.<service>` returns the task IPs while the VIP stays for normal clients.

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the Prometheus configuration reference (`dns_sd_configs`: `names`, `type` A, `port`). Confirmed: a service name resolves to a VIP by default and `tasks.<service>` returns all task IPs, one per running replica; `dnsrr` returns a task IP list, is meant for external load balancers and cannot be combined with ingress publishing. Removed: Elasticsearch, RabbitMQ, Cassandra and gRPC specifics, JVM cache property, healthy-only claim, short-name claim, UDP truncation and Compose gotchas.
Method: documentation only; no commands were run.
