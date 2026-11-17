---
id: computing-software.ai-ml-engineering.vllm.nginx-load-balancing
name: nginx-load-balancing
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [nginx, load-balancer, least-conn, docker-network]
level: practitioner
status: docs-checked
description: "Put Nginx in front of several vLLM containers with a least_conn upstream on a shared Docker network."
sources:
  - https://docs.vllm.ai/en/latest/deployment/nginx/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load-balance multiple vLLM serving containers behind one Nginx.

1. Nginx image: a Dockerfile `FROM nginx:latest`, remove `/etc/nginx/conf.d/default.conf`, `EXPOSE 80`, `CMD ["nginx", "-g", "daemon off;"]`; build with `docker build . -f Dockerfile.nginx --tag nginx-lb`.
2. Config `nginx_conf/nginx.conf`:

```text
upstream backend {
    least_conn;
    server vllm0:8000 max_fails=3 fail_timeout=10000s;
    server vllm1:8000 max_fails=3 fail_timeout=10000s;
}
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Add servers by appending `server vllmN:8000 max_fails=3 fail_timeout=10000s;`.
3. Build vLLM: `docker build -f docker/Dockerfile . --tag vllm` (pass `--build-arg http_proxy=...` behind a proxy).
4. Network: `docker network create vllm_nginx`.
5. Run each vLLM container with `--ipc host --network vllm_nginx --gpus device=N --shm-size=10.24gb`, a Hugging Face cache mount, distinct names (`vllm0`, `vllm1`) and host ports (8081, 8082).
6. Run Nginx: `docker run -itd -p 8000:80 --network vllm_nginx -v ./nginx_conf/:/etc/nginx/conf.d/ --name nginx-lb nginx-lb:latest`.

Start `vllm0` first and let it finish downloading so `vllm1` reuses the cache. CPU backend: drop `--gpus` and set `VLLM_CPU_KVCACHE_SPACE` and `VLLM_CPU_OMP_THREADS_BIND`. Verify with `docker logs vllm0 | grep Uvicorn`.

## Checked

2026-11-03. Confirmed against the Nginx page (docs.vllm.ai/en/latest/): Dockerfile, upstream config, network, container flags and verification.

Method: documentation only; no commands were run.
