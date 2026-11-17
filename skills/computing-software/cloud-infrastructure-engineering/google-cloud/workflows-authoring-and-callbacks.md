---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workflows-authoring-and-callbacks
name: workflows-authoring-and-callbacks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workflows, workflows-yaml, workflows-steps, workflows-connectors, workflows-callbacks, long-running-workflows, orchestration]
level: practitioner
status: docs-checked
description: "Author Google Cloud Workflows in YAML (steps, switch, parallel, retries, connectors), deploy and run them, and pause executions on HTTP callbacks."
sources: ["https://cloud.google.com/workflows/docs/reference/syntax", "https://cloud.google.com/workflows/docs/reference/googleapis", "https://cloud.google.com/workflows/docs/creating-callback-endpoints", "https://cloud.google.com/workflows/docs/reference/syntax/retrying"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Workflows authoring and callbacks

## 1. A workflow with parallel work
```yaml
main:
  params: [args]
  steps:
  - init:
      assign:
        - files: '${args.files}'
  - process_all:
      parallel:
        for:
          value: f
          in: '${files}'
          steps:
          - call_worker:
              try:
                call: http.post
                args:
                  url: https://worker.example.com/process
                  body: {file: '${f}'}
                result: r
              retry: '${http.default_retry}'
  - done:
      return: '${"processed " + string(len(files))}'
```
Connectors (`googleapis.<service>.<version>...`) call Google APIs and poll long-running
operations; see the connectors reference. `parallel` branches can only assign outer variables
that are declared in a `shared: [...]` list.

## 2. Deploy and run
```bash
gcloud workflows deploy ingest --source=ingest.yaml --location=europe-west2 \
  --service-account=wf-ingest@<P>.iam.gserviceaccount.com --call-log-level=log-errors-only
gcloud workflows run ingest --location=europe-west2 --data='{"files":["a.csv","b.csv"]}'
gcloud workflows executions list ingest --location=europe-west2 --limit=5
```

## 3. Callbacks (human approval, external systems)
```yaml
  - create_cb:
      call: events.create_callback_endpoint
      args: {http_callback_method: POST}
      result: cb
  - notify:
      call: http.post
      args: {url: https://chat.example.com/hook, body: {text: '${"Approve: " + cb.url}'}}
  - wait:
      call: events.await_callback
      args: {callback: '${cb}', timeout: 86400}
      result: cb_req
  - decide:
      switch:
        - condition: '${cb_req.http_request.body.approved == true}'
          next: deploy
```
`events.create_callback_endpoint` creates a URL expecting the given HTTP method;
`events.await_callback` blocks until it is called or the timeout passes. The incoming request is
available as `http_request`. Callers send an `Authorization: Bearer` access token with the request.
A callback endpoint has one slot: if several requests arrive before `await_callback`, only the
first is accepted and later ones get `RESOURCE_EXHAUSTED`.

## Gotchas
- Retries on non-idempotent POSTs can duplicate work; use `http.default_retry_non_idempotent` or a custom predicate.
- Handle a timeout from `await_callback` with try/except and take a "no response" path.

## Verify
- [ ] `gcloud workflows executions describe <ID> --workflow=ingest --location=<R>` shows `SUCCEEDED` with the expected result.
- [ ] An approval callback sent with an access token resumes the run.

## Checked
2026-10-28. Confirmed against the Workflows syntax reference (`shared`), the callbacks page (call names, `http_callback_method`, `timeout`, `http_request`, bearer token, single slot and `RESOURCE_EXHAUSTED`), the connectors reference and the retry page (`http.default_retry`). gcloud commands checked with check_commands.py. Removed: the BigQuery connector step, `concurrency_limit`, OIDC/OAuth2 auth advice, `roles/workflows.invoker` for callbacks, execution length and per-step cost claims, variable size limits.
Method: documentation only; no commands were run.
