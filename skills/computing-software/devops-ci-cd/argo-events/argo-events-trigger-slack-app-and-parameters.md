---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-slack-app-and-parameters
name: argo-events-trigger-slack-app-and-parameters
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, slack-trigger, oauth, bot-token, scopes, channel, parameters]
level: practitioner
status: docs-checked
description: "Send Slack messages from a Sensor: create a Slack app with the right bot scopes, store the token in a Secret and parameterize channel and message."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/slack-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger slack app and parameters

Slack trigger sends a message to a channel for notifications such as build pipelines.

Create the Slack app: on api.slack.com/apps choose Create New App, then Features, OAuth and Permissions. Add Bot Token Scopes `channels:join`, `channels:read`, `groups:read` and `chat:write`, install the app to the workspace and copy the OAuth access token. Store it:

```sh
kubectl create secret generic slack-secret --from-literal=token=$SLACK_OAUTH_TOKEN
```

Apply `examples/sensors/slack-trigger.yaml`. By default it posts "hello world" to the `#general` channel; change `triggers.slack.channel` and `message` as needed.

Dynamic channel and message:

```yaml
parameters:
  - src:
      dependencyName: test-dep
      dataKey: body.channel
    dest: slack.channel
  - src:
      dependencyName: test-dep
      dataKey: body.message
    dest: slack.message
```

`src` has `dependencyName`, `dataKey` (event data) and `contextKey` (event context); if both keys are given, `dataKey` wins. POSTing `{"channel":"random","message":"test message"}` to the webhook EventSource posts to #random. Complex payload structures can be built using sjson path syntax.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/slack-trigger.md. Confirmed: app creation steps, four bot scopes, slack-secret, default #general hello world, parameters, src keys and dataKey precedence, sjson. The page's own parameters example writes contextKey for the message; the skill uses dataKey because the value comes from the request body (event data). Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
