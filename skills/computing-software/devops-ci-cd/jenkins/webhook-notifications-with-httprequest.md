---
id: computing-software.devops-ci-cd.jenkins.webhook-notifications-with-httprequest
name: webhook-notifications-with-httprequest
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, http-request-step, notifications, post-conditions]
level: practitioner
status: docs-checked
description: "Send build notifications to Discord, generic webhooks or incident tools from Jenkins with the httpRequest step: JSON bodies, auth headers, timeouts and failure handling."
sources: ["https://plugins.jenkins.io/http_request/", "https://www.jenkins.io/doc/pipeline/steps/http_request/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook notifications with httpRequest

Plugin: `http_request`. Useful when no dedicated plugin exists (incoming webhooks, custom deploy trackers).

```groovy
post {
  failure {
    script {
      def body = groovy.json.JsonOutput.toJson([
        content: "FAILED ${env.JOB_NAME} #${env.BUILD_NUMBER} ${env.BUILD_URL}"
      ])
      withCredentials([string(credentialsId: 'discord-webhook', variable: 'HOOK')]) {
        httpRequest url: HOOK, httpMode: 'POST', contentType: 'APPLICATION_JSON',
          requestBody: body, validResponseCodes: '200:299',
          timeout: 15, consoleLogResponseBody: false, quiet: true
      }
    }
  }
}
```

## Auth headers
```groovy
httpRequest url: 'https://api.example.com/notify', httpMode: 'POST',
  contentType: 'APPLICATION_JSON', requestBody: payload,
  customHeaders: [[name: 'Authorization', value: "Bearer ${API_TOKEN}", maskValue: true]]
```
Or `authentication: '<key name>'` to use an authentication defined in the plugin's global configuration.

## Gotchas
- `JsonOutput.toJson` instead of string concatenation, so quotes in commit messages do not break JSON.
- Default `validResponseCodes` is `100:399` (4xx and 5xx fail the step); `100:599` accepts any code. In `post`, wrap in
  `catchError(buildResult: null, stageResult: null)` or `try/catch` so a notification outage does
  not mark green builds failed.
- If Jenkins restarts after the request is sent but before the response arrives, the request fails. `timeout` is in seconds (default 0 = none).
- Script approval may be required for `JsonOutput` in the sandbox.
- Alternative without plugin: `sh "curl -fsS -X POST -H 'Content-Type: application/json' -d @payload.json \"$HOOK\""` on an agent.

## Verify
- [ ] Forced failure posts one message; webhook outage does not change the build result.

## Checked
2026-11-02. Confirmed against the httpRequest step reference and plugin page: parameters url, httpMode, contentType values, requestBody, customHeaders (name, value, maskValue), authentication from global configuration, validResponseCodes format and 100:399 default, timeout seconds default 0, quiet, consoleLogResponseBody, restart behaviour. Removed: PagerDuty example (its API takes a routing key in the body), controller-execution claim.
Method: documentation only; no commands were run.
