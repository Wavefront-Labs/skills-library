---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-rolling-updates-rollback-and-task-diagnosis
name: swarm-rolling-updates-rollback-and-task-diagnosis
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, swarm-service, rolling-update, update-parallelism, update-delay, failure-action, service-rollback, rollback-config, service-ps, service-logs, task-state]
level: advanced
description: "Tune Swarm rolling updates (parallelism, delay, order, monitor, failure-action), automatic and manual rollback, and diagnose stuck tasks with service ps and logs."
sources: ["https://docs.docker.com/reference/cli/docker/service/update/", "https://docs.docker.com/reference/cli/docker/service/rollback/", "https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/", "https://docs.docker.com/engine/swarm/how-swarm-mode-works/swarm-task-states/", "https://docs.docker.com/reference/cli/docker/service/ps/", "https://docs.docker.com/reference/cli/docker/service/logs/", "https://github.com/compose-spec/compose-spec/blob/main/deploy.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm rolling updates, rollback and task diagnosis

## Update config
```yaml
deploy:
  replicas: 6
  update_config:
    parallelism: 2          # tasks updated at once (0 = all)
    delay: 10s              # wait between batches
    order: start-first      # start new before stopping old (needs spare capacity/ports)
    monitor: 30s            # watch each new task this long for failure
    failure_action: rollback    # pause (default) | continue | rollback
    max_failure_ratio: 0.1
  rollback_config:
    parallelism: 0          # roll back everything at once
    order: stop-first
```
CLI: `docker service update --update-parallelism 2 --update-delay 10s --update-order start-first
--update-monitor 30s --update-failure-action rollback --image app:1.5.0 shop_api`.

- Each updated task is watched for failure for `monitor`; under the default action a task that returns FAILED pauses the update. Without a
  health check, a broken-but-running app is not detected - define one.
- Default `failure_action: pause` leaves the service half-updated; you must notice.

## Rollback
```sh
docker service rollback shop_api        # to the previous version of the service
docker service update --rollback shop_api
```
For explicit versioning, redeploy a known tag via `docker stack deploy`.

## Diagnosing tasks
```sh
docker service ls                                   # REPLICAS 4/6 = trouble
docker service ps shop_api --no-trunc               # task history incl. errors
docker service ps shop_api -f desired-state=running --format '{{.Name}} {{.Node}} {{.CurrentState}} {{.Error}}'
docker service logs -f --tail 100 --timestamps shop_api
docker service logs --raw shop_api.3                # one task
docker inspect <task-id> -f '{{json .Status}}'
```
Task states: `new -> pending -> assigned -> accepted -> ready -> preparing -> starting -> running`, ends
`complete | failed | shutdown | rejected | orphaned | remove`.
| Stuck in | Look at |
|---|---|
| `pending` | no node can meet the service's resource reservations (the service stays pending) |
| `preparing` | Docker is preparing the task, for example pulling the image; private registries need `--with-registry-auth` |
| `rejected` | the worker node rejected the task; read the error column |
| `failed` repeatedly | app crash/health - check `service logs` |

## Verify
`docker service inspect shop_api -f '{{json .UpdateStatus}}'` shows the update state (for example `paused` with a message after a failed update); `docker service ps` shows old tasks Shutdown.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `--update-parallelism` (0 = all), `--update-delay`, `--update-order`, `--update-monitor`, `--update-failure-action` (`pause`, `continue`, `rollback`; default `pause`), `--rollback-*` flags; `docker service rollback` and `docker service update --rollback`; compose keys under `update_config` and `rollback_config`; `docker service logs` flags `--raw`, `--tail`, `--timestamps`, `-f`; task states new, pending, assigned, accepted, ready, preparing, starting, running, complete, failed, shutdown, rejected, orphaned, remove; a paused update shows state `paused` in `service inspect`; `--with-registry-auth` for private registries. Removed: single-level and toggle rollback claim, `.PreviousSpec` field, rollback_completed state, host-port start-first failure, stuck-state causes beyond documented ones.
Method: documentation only; no commands were run.
