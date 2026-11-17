---
id: computing-software.ai-ml-engineering.open-webui.schedule-follow-ups-with-chat-timers
name: schedule-follow-ups-with-chat-timers
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, chat-features, timers, subagents, scheduling]
level: advanced
status: docs-checked
description: "Enable and use the Open WebUI timer builtin tool for one-shot chat follow-ups, including time formats, cancel_on events, restart behaviour and limits."
sources:
  - https://docs.openwebui.com/features/chat-conversations/chat-features/timers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Schedule follow-ups with chat timers

Goal: have a model send a prompt back into the same chat later, one time.

## Enable
Timers have no toggle of their own. They ride on Sub-agents: set `ENABLE_SUBAGENTS` (off by default) AND enable the per-model **Sub-agents** builtin tools category. The `timer` tool shares the gate with `delegate_task`, needs native function calling in a chat started from the interface, and is unavailable for direct connections and inside sub-agent chats.

## Setting one
The model calls `timer` with a prompt, a time and optional `cancel_on`. Time is either a relative offset (`10s`, `5m`, `1h`, `2d`, `+10s`, `in 10 seconds`, `5 minutes`, `2 hours`) or an RFC 3339 timestamp with an explicit timezone; a timestamp without timezone is rejected, and the time must be in the future. The scheduler polls each second; `TIMER_POLL_INTERVAL` can raise (not lower below 1 s) the interval.

## When it fires
The prompt is appended to the original chat and answered with the model, workspace tools, skills, filters and settings captured when the timer was set. The system prompt is rebuilt at fire time. If the chat is busy generating it waits. Firing does not notify you; pair with Notifications so the prompt leads the model to call `notify`.

## Cancelling
`cancel_on` accepts `chat.read` (you open the chat) and `chat.user_message` (you send a message). There is no UI to list or cancel timers; without `cancel_on` it fires. The only trace is a collapsible Timer row in the chat.

## Operator notes
- Stored in the database; survive restarts and fire late after downtime rather than being skipped.
- Disabling Sub-agents later does not cancel pending timers, it only blocks new ones.
- The scheduler claims up to 10 due timers per poll; no per-user limit exists (unlike automations, which have `AUTOMATION_MAX_COUNT` and `AUTOMATION_MIN_INTERVAL`).
- Each fired timer costs a model call.

## Gotcha
A user's own direct tool-server connections (Settings > Integrations) are not carried over to a fired timer; admin-configured tool servers are. For recurring schedules use Automations instead.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/chat-features/timers (read in full). Removed: the claim that temporary chats and channels lack timers, and the past-time wording; the page states only that a timestamp without timezone is rejected and the time must be in the future.
Method: documentation only; no commands were run.
