---
id: computing-software.ai-ml-engineering.langchain.langgraph-platform-deployment
name: langgraph-platform-deployment
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph-platform, langgraph-json, langgraph-cli, langsmith-deployment, agent-server, deployment]
level: practitioner
status: docs-checked
description: "Deploy LangGraph apps to LangSmith Deployment: langgraph.json keys, langgraph dev/build/up, uv lockfile installs, store and checkpointer TTL, multiple graphs, SDK call."
sources:
  - https://docs.langchain.com/langgraph-platform/application-structure
  - https://docs.langchain.com/langsmith/cli
  - https://docs.langchain.com/oss/python/langgraph/deploy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying with langgraph.json and LangSmith Deployment

The docs now call this LangSmith Deployment; the Agent Server runs your graphs.

## Application structure
A deployable app has one or more graphs, a `langgraph.json`, a dependency file (`requirements.txt`, `pyproject.toml` or `package.json`) and an optional `.env`. Node bodies may contain arbitrary code, so non-LangGraph frameworks can be wrapped in a minimal `StateGraph` (docs) and deployed.
```json
{
  "dependencies": ["."],
  "graphs": {"support_agent": "./my_agent/support.py:agent",
             "research_agent": "./my_agent/research.py:agent"},
  "env": "./.env"
}
```
- `graphs` is required: graph ID -> `path:variable` (a compiled graph) or `path:make_graph` (a function taking a `RunnableConfig` and returning a graph). All graphs share the deployment's dependencies, env and image; Agent Server creates a default assistant per graph, so clients pass the graph ID as `assistant_id`.
- `dependencies`: `"."` for local packages, a directory holding `pyproject.toml`/`setup.py`/`requirements.txt` (give the directory, not the filename), or a package name. Required unless `source` is set.
- `env`: path to a `.env` file or a mapping. For production, set variables in the deployment environment (docs).
- Other keys: `python_version` (3.11, 3.12, 3.13; default 3.11), `node_version: 20` for JS, `image_distro` (debian default; wolfi, bookworm, bullseye), `base_image`, `dockerfile_lines`, `auth`, `http` (custom Starlette/FastAPI `app`, CORS, route-disable flags), `webhooks`, `api_version`, `ui`, `pip_installer`.
- uv lockfile: `"source": {"kind": "uv"}` (with `python_version`, no `dependencies`) installs from `uv.lock` via `uv export --frozen`. Without it, `"dependencies": ["."]` re-resolves from `pyproject.toml` at build time and ignores `uv.lock`.
- `store`: `index` (`embed`, `dims`, optional `fields`) enables semantic search on the built-in store; `ttl` (`refresh_on_read` default true, `default_ttl` in minutes for new items only, `sweep_interval_minutes`, no sweeping if unset).
- `checkpointer`: `backend` default is PostgreSQL (`mongo` or `custom` possible); `ttl` (`strategy`, `sweep_interval_minutes`, `default_ttl`) expires checkpoints; `serde` tunes deserialization (`allowed_json_modules`, `pickle_fallback`).

## CLI
```bash
pip install -U "langgraph-cli[inmem]"
langgraph dev                  # no Docker; hot reload; default 127.0.0.1:2024; state persisted to a local directory
langgraph build -t my-agent    # -t/--tag is required; builds the API server Docker image
langgraph up                   # Docker; default port 8123; needs a LangSmith API key locally, a license key for production
langgraph dockerfile ./Dockerfile
```
- `langgraph dev` needs Python 3.11+ and the `inmem` extra; options include `--port`, `--no-reload`, `--no-browser`, `--debug-port`, `--tunnel`. `langgraph up` options include `--postgres-uri`, `--watch`, `--docker-compose`, `--image`.
- `langgraph deploy` (beta) builds and pushes an image and creates or updates a LangSmith deployment in one step; its option details were not read.
- Keep the compiled graph free of a checkpointer in code: the server supplies persistence (my reading of the persistence docs; not stated on these pages).

## Deploy to Cloud and call it
Push the app to a GitHub repo, then in LangSmith choose Deployments > New Deployment, link the repo and submit (docs say it can take about 15 minutes). Test in Studio, copy the API URL, then:
```python
from langgraph_sdk import get_sync_client   # get_client for async
client = get_sync_client(url="<deployment-url>", api_key="<langsmith-api-key>")
for chunk in client.runs.stream(None, "agent", input={"messages": [{"role": "human", "content": "hi"}]},
                                stream_mode="updates"):
    print(chunk.event, chunk.data)
```
The first argument `None` is a threadless run; the second is the graph name from `langgraph.json`. REST: POST `<url>/runs/stream` with `X-Api-Key`.

## Topologies
The deployment page names LangSmith Cloud, hybrid, standalone servers and self-hosted with control plane. Production use of `langgraph up` needs a license key (see CLI above).

## Verify
- [ ] `langgraph dev` and the built image answer the same SDK smoke test.
- [ ] Config validates against the schema referenced in the CLI docs (`"$schema": "https://langgra.ph/schema.json"`).

## Checked
Method: 2026-11-08 read the application-structure and deploy pages in full as markdown; read the CLI page's config table, examples (to the checkpointer serde example) and the dev, build, up and dockerfile sections, not the deploy command section or the remaining examples. Removed unsupported claims from the draft (Redis in production, double-texting strategies, cron jobs, assistants as versioned config, thread-restart check) and added the product rename, uv, TTL and Cloud steps. One item is flagged as inference (no checkpointer in code).
