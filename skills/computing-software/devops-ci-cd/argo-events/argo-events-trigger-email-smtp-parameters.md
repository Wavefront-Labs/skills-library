---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-email-smtp-parameters
name: argo-events-trigger-email-smtp-parameters
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, email-trigger, smtp, parameters, secret, notification]
level: practitioner
status: docs-checked
description: "Send email notifications from a Sensor via SMTP, setting recipients, from, subject and body dynamically with parameters."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/email-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger email smtp parameters

The Email trigger sends a custom email to a set of addresses through an SMTP server, intended for pipeline notifications. Prerequisites: an EventBus, an SMTP server and, if it needs auth, a Secret holding the password:

```sh
kubectl create secret generic smtp-secret --from-literal=password=$SMTP_PASSWORD
```

Update `email.host`, `email.port` and `email.username` in the sensor (`examples/sensors/email-trigger.yaml`); if the server needs no authentication, omit `email.username` and `email.smtpPassword`.

Static recipients: set `email.to` as a list. Dynamic recipients use parameters:

```yaml
parameters:
  - src: {dependencyName: test-dep, dataKey: body.to}
    dest: email.to.0
  - src: {dependencyName: test-dep, dataKey: body.to}
    dest: email.to.-1
  - src: {dependencyName: test-dep, dataKey: body.from}
    dest: email.from
  - src: {dependencyName: test-dep, dataKey: body.subject}
    dest: email.subject
  - src: {dependencyName: test-dep, dataKey: body.emailBody}
    dest: email.body
```

- `email.to.<index>` overwrites the address at that index.
- `email.to.-1` appends an address.
- `email.from`, `email.subject` and `email.body` set those fields.

To send to the static addresses, remove the `email.to.0` parameterization. Test: POST `{"name":"Luke","to":"your@email.com"}` to the webhook EventSource.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/email-trigger.md. Confirmed: prerequisites, smtp-secret command, host/port/username note, parameter destinations email.to.N, email.to.-1, from, subject, body. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
