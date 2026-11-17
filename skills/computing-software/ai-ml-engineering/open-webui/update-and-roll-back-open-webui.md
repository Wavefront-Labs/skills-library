---
id: computing-software.ai-ml-engineering.open-webui.update-and-roll-back-open-webui
name: update-and-roll-back-open-webui
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [docker-updating, update, rollback, watchtower, diun, backup, migrations]
level: practitioner
status: docs-checked
description: "Update a Docker or pip Open WebUI install safely: back up, pull, verify, roll back by tag, and choose Diun, WUD or Watchtower for update alerts."
sources:
  - https://docs.openwebui.com/getting-started/updating
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/DockerUpdating
  - https://docs.openwebui.com/getting-started/quick-start/tab-python/PythonUpdating
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: update without losing data, and know how to go back.

## Before updating
1. Back up the data volume (all data lives in the `open-webui` volume: database, uploads, generated content):
```bash
docker run --rm -v open-webui:/data -v $(pwd):/backup alpine tar czf /backup/openwebui-$(date +%Y%m%d).tar.gz /data
```
2. Read the release notes on GitHub. After the update clear the browser cache (`Ctrl+F5` / `Cmd+Shift+R`).
3. Personal/homelab: `:main` and manual pulls. Shared: pin `:vX.Y.Z` and use Diun. Production: pin, read release notes, test in staging. Optionally run a `:dev` instance on its own volume and port to preview the next release.

## Update
- Docker run: `docker rm -f open-webui`, `docker pull ghcr.io/open-webui/open-webui:main`, then re-run the same `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data -e WEBUI_SECRET_KEY="your-secret-key" --name open-webui --restart always ghcr.io/open-webui/open-webui:main` (add `--gpus all` for CUDA).
- Compose: `docker compose pull` then `docker compose up -d`.
- pip: `pip install -U open-webui`, then `open-webui serve`.
- One-shot Watchtower: `docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --run-once open-webui`.

Keep a persistent `WEBUI_SECRET_KEY` (`openssl rand -hex 32`), or every recreated container invalidates all sessions.

## Verify
`docker logs open-webui 2>&1 | head -20` for the version, load the UI at http://localhost:3000. Migration errors in logs: check release notes and the connection-error troubleshooting page.

## Roll back
Pin the older tag (docs example `v0.8.3`): `docker rm -f open-webui`, `docker pull ghcr.io/open-webui/open-webui:v0.8.3`, re-run with that tag; Compose: change `image:` and pull/up; pip: `pip install open-webui==0.8.3`. Database migrations are one-way: if the newer version migrated the schema, the older version may not work, and you must restore the pre-update backup.

Restore (deletes everything in the volume first):
```bash
docker stop open-webui
docker run --rm -v open-webui:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/openwebui-YYYYMMDD.tar.gz -C /"
docker start open-webui
```

## Update notifications
- Diun: notify only (`crazymax/diun:latest`, mounts `/var/run/docker.sock:ro`, `DIUN_WATCH_SCHEDULE=0 */6 * * *`, `DIUN_PROVIDERS_DOCKER=true`, mail via `DIUN_NOTIF_MAIL_*`). Recommended for production.
- WUD: web UI, manual trigger.
- Watchtower: fully automated. `containrrr/watchtower` is unmaintained and fails on Docker 29+; use `nickfedor/watchtower`, e.g. `nickfedor/watchtower --interval 21600 open-webui` (every 6 h); `WATCHTOWER_CLEANUP=true` removes old images.

## Release-specific notes in the docs
- v0.11.4: personal tool servers sit behind the Direct Integrations switch (`ENABLE_DIRECT_INTEGRATIONS`, off by default), so users lose the Integrations tab until it is enabled.
- v0.12.1: a migration adds a sign-in record to accounts lacking one (mainly SCIM users); back up first.
- Multiple replicas: update all instances at once; stop all, let one instance migrate, then bring the rest up. `ENABLE_DB_MIGRATIONS=false` on the others only picks which instance migrates.
- pip with `UVICORN_WORKERS` above 1: run once with `UVICORN_WORKERS=1` until migrations finish.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: getting-started/updating and the Docker and Python updating pages. Removed: the Compose container-name remark; added the Python updating page to sources for the worker note.
Method: documentation only; no commands were run.
