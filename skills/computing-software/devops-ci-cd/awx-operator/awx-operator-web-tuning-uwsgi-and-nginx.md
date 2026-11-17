---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-web-tuning-uwsgi-and-nginx
name: awx-operator-web-tuning-uwsgi-and-nginx
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, uwsgi, nginx, listen-queue, somaxconn, worker-processes, web-scaling]
level: advanced
status: docs-checked
description: "Tune AWX web throughput with uwsgi_processes, listen queue sizes and nginx worker settings, extending nginx.conf via extra volumes."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/custom-volume-and-volume-mount-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator web tuning uwsgi and nginx

uWSGI: `uwsgi_processes` (default 5) and `uwsgi_listen_queue_size` (default 128). More processes let each web pod handle more active requests but use more CPU and memory, so raise resource requests together. A bigger listen queue lets uwsgi queue bursts (more than 128 requests in a short period). Going above 128 requires the sysctl `net.core.somaxconn` to be at least equal; the operator sets the securityContext sysctl, but you must allow that sysctl in the kubelet allowlist.

nginx: variables are `nginx_worker_processes` (default 1), `nginx_worker_cpu_affinity` (auto), `nginx_worker_connections` (minimum 1024), `nginx_listen_queue_size` (defaults to the uwsgi listen queue size) and `nginx_client_max_body_size` (5M).

Extending nginx.conf: AWX's nginx config includes `/etc/nginx/conf.d/*.conf` if present, so:
1. Create a ConfigMap with the extra settings.
2. Add an `extra_volumes` entry for it.
3. Add a `web_extra_volume_mounts` entry mounting it.

The same extra-volume mechanism swaps the UI logos and favicon: mount ConfigMaps built from `logo-login.svg`, `logo-header.svg` or `favicon.ico` with `subPath` at `/var/lib/awx/public/static/media/<file>` using `web_extra_volume_mounts`.

## Checked

2026-11-09. Confirmed the uwsgi and nginx variables and defaults, the somaxconn and kubelet allowlist note, the nginx.conf extension steps and the logo and favicon mounts against the AWX Operator custom volume page (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/user-guide/advanced-configuration/custom-volume-and-volume-mount-options.md
