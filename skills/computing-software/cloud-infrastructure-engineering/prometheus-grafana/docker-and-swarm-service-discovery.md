---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.docker-and-swarm-service-discovery
name: docker-and-swarm-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, docker-sd-configs, dockerswarm-sd, docker-sd, dockerswarm-sd-configs, container-labels, docker-socket, swarm-tasks, swarm-services, swarm-nodes, compose-monitoring, host-networking, pca]
level: practitioner
status: docs-checked
description: "Discover containers via docker_sd or Swarm via dockerswarm_sd (tasks/services/nodes): socket access, label keep rules, port choice, network pitfalls."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#docker_sd_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#dockerswarm_sd_config", "https://prometheus.io/docs/guides/dockerswarm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker and Swarm service discovery

**Goal:** scrape containers that opt in via a label, on one Docker host or across a Swarm, without a target file.

## 1. Single host: docker_sd_configs
```yaml
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 60s
    relabel_configs:
      - source_labels: [__meta_docker_container_label_prometheus_scrape]
        regex: "true"
        action: keep
```
- Discovers containers and creates a target for each network IP and port the container is configured to expose.
- Options: `host` (daemon address), `port`, `host_networking_host` (default `localhost`, used for containers in host networking mode), `match_first_network` (default true: sort the container's networks by name and use the first, which avoids duplicate targets), `filters` (Docker API ContainerList filters), `refresh_interval` (default 60s) and the usual `http_config` (TLS, auth).
- The page says relabeling is the preferred, more powerful way to filter; for thousands of containers the Docker API `filters` can be more efficient.
- Container labels become `__meta_docker_container_label_<labelname>` with unsupported characters turned into underscores (so `prometheus.scrape` becomes `prometheus_scrape`).
- Other meta labels: `__meta_docker_container_id`, `_name`, `_image`, `_image_id`, `_network_mode`; `__meta_docker_network_id`, `_name`, `_ingress`, `_internal`, `_scope`, `_ip` (container IP in that network), `__meta_docker_network_label_<labelname>`; `__meta_docker_port_private`, `__meta_docker_port_public`, `__meta_docker_port_public_ip` (public ones when a port mapping exists).

## 2. Swarm: dockerswarm_sd_configs
`host` and a required `role` of `services`, `tasks` or `nodes`; options `port` (default 80, used for `nodes` and for tasks/services without published ports), `filters` (Docker Swarm API list filters for the role), `refresh_interval` (default 60s), `http_config`.
| Role | Targets | Use |
|---|---|---|
| `tasks` | one per published port of each task (a target per task using `port` if none published) | individual containers; each task gets its service labels; usually the one you want |
| `services` | one per published port of each service | the guide says you usually want `tasks` instead |
| `nodes` | Swarm hosts | Docker daemons or node exporters on the hosts |

The guide says Prometheus discovers only tasks and services that expose ports. The guide assumes Prometheus runs on a manager node with access to `/var/run/docker.sock`.

Nodes (from the guide), scraping the Docker daemon metrics on port 9323 after enabling `metrics-addr` and `experimental` in `/etc/docker/daemon.json`:
```yaml
    dockerswarm_sd_configs:
      - host: unix:///var/run/docker.sock
        role: nodes
    relabel_configs:
      - source_labels: [__meta_dockerswarm_node_address]
        target_label: __address__
        replacement: $1:9323
      - source_labels: [__meta_dockerswarm_node_hostname]
        target_label: instance
```
Relabeling is recommended over the `port` parameter for `nodes`, as it lets Prometheus reuse the same API calls across identical Swarm configurations.

Tasks (from the guide):
```yaml
    dockerswarm_sd_configs:
      - host: unix:///var/run/docker.sock
        role: tasks
    relabel_configs:
      - source_labels: [__meta_dockerswarm_task_desired_state]
        regex: running
        action: keep
      - source_labels: [__meta_dockerswarm_service_label_prometheus_job]
        regex: .+
        action: keep
      - source_labels: [__meta_dockerswarm_service_label_prometheus_job]
        target_label: job
```
More patterns from the guide: keep one network with `__meta_dockerswarm_network_name` (regex `ingress` in the guide), keep global tasks with `__meta_dockerswarm_service_mode` = `global` plus `__meta_dockerswarm_task_port_publish_mode` = `host`, and add the node with `__meta_dockerswarm_node_hostname`.
- The page notes `__meta_dockerswarm_network_*` labels are not populated for ports published with mode=host.
- Task container labels: `__meta_dockerswarm_container_label_<labelname>` (labels from the task ContainerSpec; image labels are not available through the task API).
- Connect with the unix socket, or HTTP/HTTPS via `host` and `http_config`.

## Verify
- [ ] The Prometheus Service Discovery page (Status menu) shows the discovered labels and one target per container or task you expect.
- [ ] Scaling a service changes the target count within about `refresh_interval`.

## Checked
Date: 2026-11-07. Read: the `<docker_sd_config>` and `<dockerswarm_sd_config>` sections (roles, meta labels, options, defaults) of the Prometheus configuration page, and the Prometheus Docker Swarm guide in full. The configuration page is ~3600 lines; I read only those sections. Corrections: the draft claimed one target per container per network (duplicates unless relabeled); the page says `match_first_network` defaults to true to avoid duplicate targets. Trims: the `docker_sd` `filters` examples and the `__tmp_port` relabel chain, "mount the socket read-only", the claim that default-bridge containers are not reachable, Docker API TCP-without-TLS remote-root warning, the `tls_config` Swarm example, "Prometheus as a Swarm global service" deployment recipe, the VIP-scraping claim about services, "overlay networks give each task an IP per network", "published ports point at the host/ingress mesh" and the container ID label advice, none of which these pages state. Not opened: the example prometheus-docker.yml files linked from the page.
Method: documentation only; no commands were run.
