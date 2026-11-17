---
id: computing-software.devops-ci-cd.gitea.webhooks
name: webhooks
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-webhook-payload, gitea, webhook-signature, x-gitea-signature, webhook-branch-filter, webhook-events, webhook-redelivery, hmac-sha256]
level: advanced
status: docs-checked
description: "Configure Gitea webhooks at repository, org, user and system scope, verify X-Gitea-Signature HMAC-SHA256, use branch filter globs, event groups and delivery headers."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/repository/webhooks.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea webhooks

Repository webhooks live at `/:username/:reponame/settings/hooks` (repository admin). Scopes: repository, organization, user, and system (all eligible activity). Admin **default webhooks** are not another scope: they are copied into newly created repositories and then act as repository hooks. Integrations: Gitea, Gogs, Slack, Discord, Dingtalk, Telegram, Microsoft Teams, Feishu, Matrix, Wechatwork, Packagist; Gitea and Gogs send the generic payload, the others a service-specific body.

## Options
`Target URL`, `HTTP Method` (generic: POST or GET, POST normal), `POST Content Type` (`application/json`, or `application/x-www-form-urlencoded` which sends a form field named `payload`), `Secret` (HMAC of the raw body), `Authorization Header` (separate from the secret, for endpoints needing app-level auth), `Branch Filter`, `Trigger On` (Push Events, All Events, or custom), `Active`. Current versions do not put the secret in the payload; verify signatures instead.

## Branch filter
gobwas glob: empty, `*` or `**` matches everything; `main`; full refs like `refs/tags/v*`; braces like `{main,release/*}`. Applies only to events carrying a git ref (`create`, `delete`, `push`); issue and release events ignore it.

## Delivery headers
`X-Gitea-Delivery` (UUID per attempt), `X-Gitea-Event` (normalised, e.g. `issues`), `X-Gitea-Event-Type` (exact trigger, e.g. `issue_assign`; use it when you need precision), `X-Gitea-Signature` (lowercase hex HMAC-SHA256, no prefix), `X-Gitea-Hook-Installation-Target-Type`. Compatibility: `X-Gogs-*`, `X-GitHub-*`, `X-Hub-Signature` (`sha1=`), `X-Hub-Signature-256` (`sha256=`). Without a secret the signature headers are still sent with empty digests.

## Verify
Read the raw body unmodified, compute HMAC-SHA256 with the secret, compare to `X-Gitea-Signature` or `X-Hub-Signature-256` in constant time, and only then parse JSON. PHP form: `hash_hmac('sha256', $payload, $secret)` compared with `hash_equals` against `$_SERVER['HTTP_X_GITEA_SIGNATURE']`.

## Events
Repository: `create`, `delete`, `fork`, `push`, `wiki`, `repository`, `release`, `package`, `status` (no `action` field, uses `state`). Issue: `issues`, `issue_assign`, `issue_label`, `issue_milestone`, `issue_comment`. Pull request: `pull_request`, `pull_request_assign`, `_label`, `_milestone`, `_comment`, `_review_approved`, `_review_rejected`, `_review_comment`, `_sync`, `_review_request`; `pull_request_review` is only a subscription umbrella with no payload of its own. Workflow: `workflow_run`, `workflow_job` (`queued`, `waiting`, `in_progress`, `completed`).

## Debugging
Each hook page has `Test Delivery` (a synthetic `push`, with a fake commit on empty repositories), `Recent Deliveries` (request and response) and `Redelivery`. Admins can restrict hosts, timeouts and cleanup in the `[webhook]` config section.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page webhooks.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
