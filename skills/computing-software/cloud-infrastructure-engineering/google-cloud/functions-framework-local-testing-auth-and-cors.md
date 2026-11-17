---
id: computing-software.cloud-infrastructure-engineering.google-cloud.functions-framework-local-testing-auth-and-cors
name: functions-framework-local-testing-auth-and-cors
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, functions-framework-local, local-testing, functions-auth, functions-cors, identity-tokens, cloudevents]
level: practitioner
status: docs-checked
description: "Run and test functions locally with the Functions Framework (HTTP and CloudEvents), call private functions with ID tokens, and handle CORS preflight correctly for browser clients."
sources: ["https://docs.cloud.google.com/run/docs/authenticating/service-to-service", "https://github.com/GoogleCloudPlatform/functions-framework-python", "https://github.com/GoogleCloudPlatform/functions-framework-nodejs", "https://docs.cloud.google.com/functions/docs/securing/authenticating", "https://docs.cloud.google.com/functions/docs/samples/functions-http-cors", "https://docs.cloud.google.com/sdk/gcloud/reference/auth/print-identity-token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions Framework local testing, auth and CORS

## 1. Run locally
```bash
pip install functions-framework
functions-framework --target=handle --port=8080 --debug          # Python
npx @google-cloud/functions-framework --target=handle             # Node.js
```
HTTP: `curl localhost:8080 -d '{"x":1}' -H 'Content-Type: application/json'`.
For CloudEvent functions start the framework with the CloudEvent target and send a CloudEvent in structured or binary mode (the Functions Framework README shows the invocation).
Unit-test handlers by calling them directly with fake request/CloudEvent objects; use the
Pub/Sub emulator for integration tests (`gcloud beta emulators pubsub start`).

## 2. Call a private function
```bash
gcloud functions add-invoker-policy-binding api --region=<R> --member=serviceAccount:caller@<P>.iam.gserviceaccount.com
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" <FUNCTION_URL>
```
Service-to-service: fetch an ID token for the function URL as audience from the metadata server
(`.../instance/service-accounts/default/identity?audience=<URL>`) or the client library
`google.oauth2.id_token.fetch_id_token`.

## 3. CORS
```python
@functions_framework.http
def handle(request):
    headers = {"Access-Control-Allow-Origin": "https://app.example.com"}
    if request.method == "OPTIONS":
        headers.update({"Access-Control-Allow-Methods": "GET,POST",
                        "Access-Control-Allow-Headers": "Content-Type,Authorization",
                        "Access-Control-Max-Age": "3600"})
        return ("", 204, headers)
    return ({"ok": True}, 200, headers)
```
The Google sample handles the preflight `OPTIONS` request in function code and caches it with `Access-Control-Max-Age`. A function that requires IAM authentication needs the caller to send an identity token (see section 2).

## Gotchas
- `gcloud auth print-identity-token --audiences=<URL>` sets the token audience (only one audience is accepted); `--impersonate-service-account` mints it as a service account.
- Local runs authenticate with Application Default Credentials, not the function's service account.

## Checked
2026-10-31. Confirmed against the Functions Framework Python and Node.js READMEs (`pip install functions-framework`, `--target`, `--port` default 8080, `--debug`, npx invocation), the `gcloud auth print-identity-token` reference (`--audiences`, one audience, `--impersonate-service-account`), and the Google CORS sample (preflight handling, Access-Control-Max-Age, ADC for local runs). Commands were verified by check_commands. Removed unconfirmed: CloudEvent curl block, 403-on-preflight claim, API Gateway/LB advice, wildcard-credentials gotcha and the incorrect claim that audiences need impersonation.
Method: documentation only; no commands were run.

## Verify
- [ ] A local CloudEvent request triggers the handler with parsed data.
- [ ] Browser fetch from the allowed origin succeeds; from another origin fails CORS.
