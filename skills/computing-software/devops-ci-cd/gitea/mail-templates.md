---
id: computing-software.devops-ci-cd.gitea.mail-templates
name: mail-templates
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-mail-template, gitea, mail-subject-templates, templates-mail, notification-email]
level: advanced
status: docs-checked
description: "Customize Gitea notification email subjects and bodies by overriding templates under the custom templates/mail directory."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/administration/mail-templates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea mail templates

Override the subject and body of notification mails. Templates are read from the custom dir at startup, so restart after editing. Path: `custom/templates/mail/{issue|pull}/{action}.tmpl`.

## Actions
`new`, `comment`, `close`, `reopen`, `review`, `approve`, `reject`, `code` (single PR code comment), `assigned`, `default`. Fallback order, first existing wins: type+action, `issue`+action, type+`default`, `issue`+`default`. Only `issue/default` is mandatory and is embedded.

## File format
Optional subject, then a separator line of three or more dashes and nothing else, then the body:
```
[{{.Repo}}] @{{.Doer.Name}} updated #{{.Issue.Index}}: {{.Issue.Title}}
------------
<!DOCTYPE html><html><body>... {{.Body}} <a href="{{.Link}}">View it on Gitea</a></body></html>
```
Subject uses `text/template`; whitespace is collapsed to single spaces, trimmed and cut to 256 runes. An empty result, or no subject part, falls back to `{{.SubjectPrefix}}[{{.Repo}}] {{.Issue.Title}} (#{{.Issue.Index}})` (also exposed as `.FallbackSubject`). Body uses `html/template` (automatic escaping), sent as `multipart/alternative` with a tag-stripped text part. No attachments. Shared fragments live under `custom/mail` and are included relative to it, e.g. `{{template styles/base}}` for `custom/mail/styles/base.tmpl`.

## Context (case sensitive)
`.FallbackSubject`, `.Subject` (body only), `.Body` (rendered, sanitised Markdown, not the mail body), `.Link`, `.Issue` (use `.Issue.PullRequest` only for PRs, nil otherwise), `.Comment`, `.IsPull`, `.Repo` (owner/name), `.User`, `.Doer`, `.IsMention`, `.SubjectPrefix` (`Re: ` except on creation), `.ActionType`, `.ActionName`, `.ReviewComments` (text `.RenderedContent`, code `.Patch`).
Functions (call without a dot): `AppUrl`, `AppName`, `AppDomain`, `EllipsisString str n`, `SanitizeHTML` (body only). `{{.AppUrl}}` is wrong.

## Failure modes
Render errors surface only when a mail is sent: a failing subject falls back to the default, a failing body keeps what rendered before the error. Check Gitea's log (see `gitea-log-writers`).

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page mail-templates.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
