---
id: computing-software.ai-ml-engineering.ray.serve-config-and-deploy
name: serve-config-and-deploy
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, serve-build, serve-deploy, serve-config-yaml, import-path]
level: practitioner
status: docs-checked
description: "Deploy Ray Serve from a YAML config with serve build, serve deploy and serve run, per-deployment overrides and in-place updates."
sources:
  - https://docs.ray.io/en/latest/serve/production-guide/config.html
  - https://docs.ray.io/en/latest/serve/production-guide/index.html
  - https://docs.ray.io/en/latest/serve/advanced-guides/deploy-vm.html
  - https://docs.ray.io/en/latest/serve/advanced-guides/inplace-updates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve config files

```bash
serve run module:app                                 # dev: import path is module:application
serve build module:app -o serve_config.yaml          # generate a config from code
serve deploy serve_config.yaml                       # deploy to a cluster
serve deploy serve_config.yaml -a http://127.0.0.1:8265   # explicit dashboard address (--address/-a)
serve status                                         # deployment and replica status
serve config                                         # the running app's config
```
```yaml
http_options: {host: 0.0.0.0, port: 8000}
applications:
  - name: m
    route_prefix: /predict
    import_path: app:model_app
    runtime_env: {working_dir: "s3://<BUCKET>/code.zip", pip: ["torch"]}
    args: {path: "s3://<BUCKET>/model"}              # passed to an application builder function
    deployments:
      - name: Model
        num_replicas: 4
        ray_actor_options: {num_gpus: 1}
        user_config: {threshold: 0.5}
```

## Facts from the docs
- The file holds `proxy_location`, `http_options`, `grpc_options`, `logging_config` and `applications`. `http_options` are global to the cluster and cannot be updated at runtime.
- Application `name` and `route_prefix` (default `/`) must each be unique. The smallest config is just an `import_path`.
- Config `runtime_env` can only use remote URIs for `working_dir` and `py_modules`, not local zips or directories. `serve build` always leaves `runtime_env` empty; set it by hand.
- A `deployments` entry must carry a `name` matching the code and overrides the decorator. Precedence is config file, then code, then defaults. `ray_actor_options`, `user_config` and `autoscaling_config` override as whole dictionaries.
- `user_config` changes call the class's `reconfigure()` without restarting replicas (you implement `reconfigure`).
- The dashboard default port is 8265 (`ray start --dashboard-port` changes it); `RAY_DASHBOARD_ADDRESS` also sets the target, so check your environment.
- Code updates restart replicas as a rolling restart (default `rolling_update_percentage` 0.2); a single-replica deployment has a brief interruption. For heavyweight changes such as `runtime_env`, the docs suggest a new cluster and switching traffic.

## Verify
`serve status` shows the application and deployments `RUNNING`.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/production-guide/config.md`, `production-guide/index.md`, `advanced-guides/deploy-vm.md`, `advanced-guides/inplace-updates.md`, `advanced-guides/app-builder-guide.md` (args). Removed: REST claim, "omitted applications are removed", repeated-apply claim, pinned torch version, concrete bucket names.
Method: documentation only; no commands were run.
