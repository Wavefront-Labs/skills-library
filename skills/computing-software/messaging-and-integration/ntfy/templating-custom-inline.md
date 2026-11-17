---
id: computing-software.messaging-and-integration.ntfy.templating-custom-inline
name: templating-custom-inline
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, template, inline-template, custom-template, globoff]
level: advanced
status: docs-checked
description: "Write custom ntfy template files (.yml) or inline templates in the URL, including the curl --globoff requirement."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom and inline templates

## Custom file

- Put `myapp.yml` in `template-dir` (default `/etc/ntfy/templates`). The extension must be `.yml`, not `.yaml`.
- Keys: `title`, `message`, `priority`; each is interpreted as a Go template over the JSON body.
- Use it with `?template=myapp`:

```
curl -sT- "https://ntfy.example.com/mytopic?template=myapp" < payload.json
```

## Inline

Set `tpl=yes` (or `template=yes`/`1`) and give the fields as query parameters `t` (title), `m` (message), `p` (priority) in Go template syntax. Use `curl --globoff` so `{` and `}` are not treated as URL globs, and URL-encode where required.

The docs example renders a title like `phil-pc: A severe error has occurred`, and sets priority 5 if the level is "severe", else 3.

## Gotchas

- Templates apply to `message`, `title`, `priority` only.
- Size and runtime limits from templating-basics apply (32 KB, HTTP 400 on timeout).
- `fromJSON` returns an empty string on invalid JSON; `mustFromJSON` returns an error (see the template-functions skill).
- The docs recommend trying templates in the Go Template Playground (repeatit.io) first.

## Checked

2026-11-04. Checked against publish.md: template-dir files, tpl/template, t/m/p parameters, --globoff and the phil-pc example match.
Method: documentation only; no commands were run.
