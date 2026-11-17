---
id: computing-software.devops-ci-cd.rundeck.api-run-job-with-options
name: api-run-job-with-options
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, api-run-job, auth-token, x-rundeck-auth-token, job-options-json]
level: practitioner
status: docs-checked
description: "Create a user API token and run a Rundeck job over the REST API with curl, passing option values as JSON."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/api/api_basics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a token: log in, click the user icon (upper right), **Profile**, click the "+" button, name the token and save it.

Run a job by its ID with POST to `/api/<version>/job/<job-id>/run`, sending the token in the `X-Rundeck-Auth-Token` header:

```bash
curl --request POST 'http://localhost:4440/api/41/job/<job-id>/run' \
  --header 'Accept: application/json' \
  --header 'X-Rundeck-Auth-Token: <token>' \
  --header 'Content-Type: application/json' \
  --data-raw ''
```

To pass options, send a JSON body with an `options` map:

```json
{"options": {"input_key": "HelloWorld"}}
```

Other checks: `GET /api/<version>/system/info` with `Accept: application/json` returns system info and is a good first call.

Verify: open the Activity page and look at the latest execution.

Tip from the page: in Postman, keep hostname, port, API version and token as collection variables so one change updates every request; the page uses version 41 at time of writing, so check what your server supports.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Getting Started with the API: token creation via user icon, Profile, the + button; POST /api/41/job/<id>/run with the X-Rundeck-Auth-Token header; JSON body with an options map; GET /api/<version>/system/info with Accept application/json; Postman collection variables; Activity page check. Nothing removed.

Method: documentation only; no commands were run.
