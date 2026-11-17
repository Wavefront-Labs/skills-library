---
id: computing-software.devops-ci-cd.gitlab-ci.docker-executor-volumes-pull-policy-and-allowed-images
name: docker-executor-volumes-pull-policy-and-allowed-images
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, docker-volumes, allowed-images, docker-pull-policy, allowed-services, docker-executor-config]
level: advanced
status: docs-checked
description: "Harden and tune the GitLab Runner Docker executor in config.toml: volumes, pull_policy, allowed_images/services/pull_policies, privileged, resources and helper image."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/#the-runnersdocker-section", "https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker executor: volumes, pull policy, allowed images

```toml
concurrent = 8
[[runners]]
  name = "docker-shared"
  executor = "docker"
  [runners.docker]
    image = "alpine:3.20"                       # the image to run jobs with
    privileged = false
    pull_policy = ["always", "if-not-present"]  # several policies allowed
    allowed_pull_policies = ["always", "if-not-present"]
    allowed_images = ["registry.example.com/*/*:*", "docker.io/library/*:*"]
    allowed_services = ["postgres:*", "redis:*", "docker:*-dind"]
    volumes = ["/cache"]                        # anonymous volume for local cache
    shm_size = 268435456                        # shared memory in bytes (256 MB)
    memory = "4g"
    cpus = "2"
    disable_cache = false
    wait_for_services_timeout = 60
    helper_image_flavor = "ubuntu"              # or alpine (default)
```

## Key decisions
- **volumes:** `"/cache"` = per-container anonymous volume (local cache). Host binds like
  `"/srv/ci-cache:/cache"` persist across jobs; `"/var/run/docker.sock:/var/run/docker.sock"` gives
  jobs root on the host — only on single-tenant runners.
- **pull_policy:** `always` is the default. With `if-not-present` on a shared runner, other users may reach private images cached there; read the Docker executor docs section "Usage of private Docker images with if-not-present pull policy".
- **allowed_images/services:** wildcard lists (if absent, all images are allowed); a job asking for anything else is rejected. Essential on shared runners.
- **allowed_privileged_images:** a wildcard subset of `allowed_images` that runs privileged when `privileged` is enabled; if absent, all images are allowed.
- **privileged:** insecure; isolate such runners with tags (`tags: [dind]`) and do not run untrusted projects on them.
- `shm_size`, `memory`, `cpus` prevent one job starving others when `concurrent > 1`.
- Apply changes: the runner checks `config.toml` every 3 seconds and reloads it (log line `Configuration loaded`), or on SIGHUP.

## Gotchas
- Docker Hub rate limits: point `image` at a mirror or the GitLab dependency proxy.
- Disk fills with images/volumes: use the runner's `clear-docker-cache` to remove unused containers and volumes it created.

## Verify
- [ ] A job using a disallowed image is rejected.
- [ ] `docker inspect` of a job container shows the memory/cpu limits.

## Checked

2026-10-31. Confirmed against the GitLab Runner docker section of the advanced configuration page and the Docker executor page: allowed_images, allowed_services, allowed_privileged_images semantics, pull_policy default always, allowed_pull_policies, helper_image_flavor values (alpine default, ubuntu), wait_for_services_timeout, shm_size in bytes, memory and cpus as strings, disable_cache, config reload every 3 seconds and on SIGHUP, clear-docker-cache, and the if-not-present private-image security note.
Removed: the 64 MB shm_size default, the empty allowed_privileged_images meaning, the quoted allowed-images error text, the allowed_images dual-form claim, the dind requirement claim and the prune command.

Method: documentation only; no commands were run.
