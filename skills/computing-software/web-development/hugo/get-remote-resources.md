---
id: computing-software.web-development.hugo.get-remote-resources
name: get-remote-resources
category: computing-software
field: web-development
product: hugo
tags: [resources-getremote, remote-data, try-statement, http-security, json]
level: practitioner
status: docs-checked
description: "Fetch remote data or files with resources.GetRemote: options, try error handling, 404 returns nil, disk caching and the security.http allowlist."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/resources/GetRemote.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`resources.GetRemote` fetches a remote resource from a URL and returns a `resource.Resource`, or `nil` if none is found. The `Err` method was removed in v0.141.0; use `try`.

Options (a `dict`):

- `body`: data to send.
- `headers`: request headers; use a slice for several values under one key.
- `key`: a custom cache key.
- `method`: such as `GET`, `POST` or `HEAD`.
- `responseHeaders`: headers to extract, read through `Data.Headers` (v0.143.0; case-insensitive).
- `timeout`: a duration string such as `"10s"` (v0.157.0); default is 2 minutes.

Uses:

- Remote JSON or other data, parsed with `transform.Unmarshal`. If the server sends a wrong Content-Type, pass `.Content` instead.
- Publishing remote images or files with `Permalink`, `RelPermalink` or `Publish`. Hugo adds a hash to the filename to keep cache keys unique.

Errors: wrap the call in `try` to catch HTTP errors. Unhandled errors fail the build. A 404 is not an error; the result is `nil`, so check it with `with`.

Caching: results are cached on disk. The default key derives from the arguments; the `key` option controls how often Hugo refetches.

Security: Hugo checks the response Content-Type, file extension and content against a media type allowlist. Add regular-expression entries under `[security.http]`; they are added to the list, not substituted.

## Checked

2026-11-04. Confirmed against the Hugo docs page resources.GetRemote: the `Err` removal in v0.141.0, the six options with their version notes and the 2 minute timeout default, the `transform.Unmarshal` and Content-Type note, hash-suffixed published filenames, `try` error handling, the 404 returning `nil`, disk caching and the `key` option, and the `security.http` media type allowlist being additive. Nothing removed.

Method: documentation only; no commands were run.
