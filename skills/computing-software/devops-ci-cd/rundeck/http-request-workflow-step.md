---
id: computing-software.devops-ci-cd.rundeck.http-request-workflow-step
name: http-request-workflow-step
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, http-request, workflow-step, oauth2, response-code-check]
level: practitioner
status: docs-checked
description: "Call HTTP or HTTPS endpoints from a Rundeck workflow with the HTTP Request step: method, headers, auth, expected response code, proxy and unsafe characters."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-plugins/workflow-steps/http-request.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The HTTP Request workflow step executes an HTTP/S request against a remote endpoint.

Key settings:
- Remote URL: must begin with `http://` or `https://`.
- HTTP Method: GET, POST, PUT, DELETE, HEAD, OPTIONS or PATCH.
- Headers: YAML list of name/value pairs or JSON.
- Body, Request Timeout (milliseconds), Validate SSL Certificates.
- Authentication: Basic or OAuth 2.0. Username/Client ID, and Password/Client Secret chosen from Key Storage; for OAuth also the Token URL and Validate URL.
- Check Response Code? with an expected Response Code: the step fails if the code differs.
- Print Response?, Print Response to File? (with File Path), Print Response Code?.
- Use Proxy Settings? with Proxy IP and Port.

Header YAML:

```yaml
- name: "Content-Type"
  value: "application/json"
```

To use JVM-level proxy settings, set `useJvmProxySettings=true` under `project.plugin.WorkflowNodeStep.edu.ohio.ais.rundeck.HttpWorkflowNodeStepPlugin.` in project properties, or `framework.plugin.WorkflowNodeStep.edu.ohio.ais.rundeck.HttpWorkflowNodeStepPlugin.` in framework properties.

Gotcha: the error `Illegal character in scheme name at index` means an unsafe character is in the URL; encode all unsafe characters.

## Checked

2026-11-04. Confirmed against the Rundeck docs page HTTP Request Workflow Step: URL scheme rule, the seven HTTP methods, YAML or JSON headers, body, timeout in milliseconds, SSL validation, Basic or OAuth 2.0 authentication fields, response code check, print options, proxy fields and the useJvmProxySettings property names, and the Illegal character in scheme name tip. Removed the unconfirmed log-filter pairing advice.

Method: documentation only; no commands were run.
