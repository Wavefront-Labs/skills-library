---
id: computing-software.web-development.fastify.content-type-parsers
name: content-type-parsers
category: computing-software
field: web-development
product: fastify
tags: [fastify, content-type, parsers, body, add-content-type-parser]
level: practitioner
status: docs-checked
description: "Add parsers for non-JSON bodies with addContentTypeParser, including parseAs, bodyLimit, regexes and the catch-all."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/ContentTypeParser.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Warnings.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fastify natively parses `application/json` and `text/plain`; the result lands in `request.body`. Any other content type returns 415 with `FST_ERR_CTP_INVALID_MEDIA_TYPE`.

Add a parser:

```js
fastify.addContentTypeParser('application/jsoff', function (request, payload, done) {
  jsoffParser(payload, (err, body) => done(err, body))
})

// let Fastify buffer the body first
fastify.addContentTypeParser('text/json', { parseAs: 'string', bodyLimit: 1024 }, (req, body, done) => {
  try { done(null, JSON.parse(body)) } catch (err) { err.statusCode = 400; done(err) }
})

// catch-all
fastify.addContentTypeParser('*', (request, payload, done) => done(null, payload))
```

Details:
- `parseAs`: `'string'` or `'buffer'`; the `payload` argument is then the buffered value instead of a stream.
- `bodyLimit` per parser.
- A string content type matches before a RegExp; overlapping types match last-in-first-out.
- `removeContentTypeParser(typeOrArray)` (string or RegExp), `removeAllContentTypeParsers()` and `hasContentTypeParser(type)` exist; `getDefaultJsonParser` and `defaultTextParser` expose the built-ins.
- GET and HEAD bodies are never parsed; OPTIONS and DELETE only if a content-type is sent.
- Parsers are encapsulated.

Security: anchor RegExp content types by starting with `^` or including `;?`, for example `/^application\/([\w-]+);?/`; an unanchored one triggers FSTSEC001, a possible CORS bypass (Warnings.md).

Gotcha: do not `await` route registration around `addContentTypeParser` inside `register`. v5 also rejects DELETE with `Content-Type: application/json` and an empty body.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (ContentTypeParser.md, Getting-Started.md, Warnings.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: the unanchored-looking regex example, replaced by the page's own anchored example; the invented Verify step.

Method: documentation only; no commands were run.
