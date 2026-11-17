---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-slack-threads-attachments-blocks
name: argo-events-trigger-slack-threads-attachments-blocks
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, slack-trigger, threads, attachments, blocks, sender, block-kit]
level: advanced
status: docs-checked
description: "Customize Slack trigger messages with a sender identity, thread aggregation keys, attachments and Block Kit blocks."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/slack-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger slack threads attachments blocks

Beyond channel and message, the `slack` trigger offers:

Sender identity:

```yaml
slack:
  sender:
    username: "Cool Robot"
    icon: ":robot_face:"      # emoji or an image URL
```

Threads: messages sharing a key land in the same Slack thread.

```yaml
slack:
  thread:
    messageAggregationKey: "abcdefg"
    broadcastMessageToChannel: true   # also broadcast the thread message to the channel
```

Attachments (Slack Attachments API): `attachments` takes a JSON array string with fields like `title`, `title_link`, `color` and `fields` (each with `title`, `value`, `short`):

```yaml
slack:
  message: "hello world!"
  attachments: |
    [{"title": "Attachment1!", "color": "#18be52",
      "fields": [{"title": "Hello1", "value": "Hello World1", "short": true}]}]
```

Blocks (Block Kit): `blocks` takes a JSON array string of blocks, for example an `actions` block containing a `datepicker`, an `overflow` menu and a `button`, each with an `action_id`.

See the SlackTrigger API spec for all fields.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/slack-trigger.md. Confirmed: sender, thread keys, attachments and blocks snippets. Removed or changed: the claim that attachments and blocks must be valid JSON (not stated) and reworded the broadcast comment to match the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
