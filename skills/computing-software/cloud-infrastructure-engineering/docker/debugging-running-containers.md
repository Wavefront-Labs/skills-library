---
id: computing-software.cloud-infrastructure-engineering.docker.debugging-running-containers
name: debugging-running-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-exec, docker-logs, docker-inspect, docker-stats, docker-top, docker-diff, distroless-debugging, nsenter, nicolaka-netshoot, debug-container, ephemeral-debug-container, docker-events, crashloop, exit-code-137, exit-code-exec-format]
level: practitioner
status: docs-checked
description: "Debug a running or just-dead container in order: exit code, logs, inspect, exec, shell-less debugging with docker debug or a netshoot sidecar, then resource checks."
sources: ["https://docs.docker.com/reference/cli/docker/container/inspect/", "https://docs.docker.com/reference/cli/docker/container/stats/", "https://docs.docker.com/reference/cli/docker/debug/", "https://github.com/nicolaka/netshoot", "https://docs.docker.com/reference/cli/docker/container/run/#exit-status", "https://docs.docker.com/engine/logging/dual-logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging a running (or just-dead) container, systematically

**Goal:** a repeatable order of checks instead of randomly trying `exec` first and getting
stuck when the image has no shell. Each step narrows the search space for the next.

## Step 1 — exit code, before anything else
```
docker inspect <id> --format '{{.State.ExitCode}} {{.State.OOMKilled}} {{.State.Error}}'
```
The `docker run` reference defines three codes from Docker itself; any other code is the
contained command's own exit code:
- `125` — the Docker daemon itself failed (the run command did not complete).
- `126` — the contained command cannot be invoked (path wrong, missing exec bit).
- `127` — the contained command cannot be found (for example a shebang expecting a shell
  the image lacks).
- Anything else — whatever the process returned. Read it together with `OOMKilled` (see
  `cgroup-resource-limits-and-tuning`) and your application's logs; the usual shell
  conventions apply (128+N means killed by signal N, so 137 is SIGKILL).

## Step 2 — logs, with the right flags
```
docker logs --tail 200 --timestamps <id>
docker logs -f <id>                     # follow live
docker compose logs -f --tail=100 <svc> # multi-container, interleaved by service name
```
If logs are empty but you know the app writes to stdout, check the logging driver
(`docker info`). Docker Engine enables dual logging automatically when the driver cannot
be read back, so `docker logs` normally still works through the local cache; if dual
logging has been disabled, `docker logs` returns an error for remote drivers such as
`splunk`.

## Step 3 — inspect, for config-vs-reality mismatches
```
docker inspect <id>          # full JSON: env, mounts, network, restart policy, limits
docker inspect --format '{{json .Mounts}}' <id>
docker inspect --format '{{json .NetworkSettings.Networks}}' <id>
```
Confirms what's *actually* configured, not what you think the Compose file says — catches
stale containers running an old config after a `docker compose up` that didn't recreate
them (`docker compose up --force-recreate` if in doubt).

## Step 4 — exec in
```
docker exec -it <id> sh      # or bash if present
docker exec <id> ps aux      # see what's actually running inside, without a shell
```
`docker top <id>` lists the container's processes without needing a shell in the image.

## Step 5 — no shell at all (distroless, scratch)
Can't `exec` into an image with no shell binary. Three options, in order of preference:
1. `docker debug <id>` gives a shell with its own toolbox without modifying the image; for
   a running container, filesystem changes you make are visible to it.
2. A sidecar debug container sharing the target's namespaces:
   `docker run -it --rm --pid=container:<id> --net=container:<id> nicolaka/netshoot sh`
   (add `--cap-add SYS_PTRACE` for strace-style tools).
3. `nsenter -t <pid> -n -p` on the host, with the container's host PID from
   `docker inspect --format '{{.State.Pid}}' <id>`.

## Step 6 — resource and network checks
```
docker stats <id>                       # live CPU/mem/net/io, one-shot with --no-stream
docker diff <id>                        # filesystem changes since the container started
docker events --since 10m               # host-wide events (oom, health_status, ...)
```

## Gotchas
- `docker exec` starts a *new* process in the container, separate from PID 1, so it is not a
  test of how the main process handles signals.
- A `restart: always`/`unless-stopped` policy means the container you're inspecting may
  already be a *new* instance of a crash loop — check `docker inspect --format
  '{{.RestartCount}}'` before concluding "it's fine now," it might just be mid-loop.

## Verify
After fixing, `docker inspect --format '{{.RestartCount}} {{.State.Status}}'` stays stable
(no incrementing RestartCount) over several minutes of observation, not just one clean
`docker ps` snapshot.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23): `docker run` exit-code section, dual logging page, `docker debug` and `docker container run` reference data, `docker events` types (oom, health_status). Confirmed: 125/126/127 definitions, any-other-code rule, dual logging behaviour, docker debug semantics, `--pid=container:`/`--net=container:` forms and the `SYS_PTRACE` example. Removed as unconfirmed: the 0/139 interpretations, the architecture-mismatch bullet, the claim that non-json-file drivers make `docker logs` empty (outdated by dual logging), `docker top` host-view claim, tool lists for netshoot, the PID-1 signal explanation, jq pipelines.
Method: documentation only; no commands were run.
