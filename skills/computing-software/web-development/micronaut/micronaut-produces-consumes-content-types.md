---
id: computing-software.web-development.micronaut.micronaut-produces-consumes-content-types
name: micronaut-produces-consumes-content-types
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, produces-annotation, consumes-annotation, content-type, plain-text, text-plain]
level: practitioner
status: docs-checked
description: "Change the media types a Micronaut controller consumes and produces, return text/plain, and extend codec content types."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/producesAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/consumesAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/plainTextResponses.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Produces, consumes and plain text

Goal: serve or accept something other than `application/json`, the default for both directions.

## Produces

A controller action produces `application/json` by default. Change the response `Content-Type` with the `@Produces` annotation, or with the `produces` member of the HTTP method annotations (`@Get(value = "/x", produces = ...)`).

```java
@Controller("/produces")
public class ProducesController {
    @Get                                   // default content type: JSON
    public HttpResponse index() { ... }

    @Produces(MediaType.TEXT_HTML)         // annotation form
    @Get("/html")
    public String html() { ... }
}
```

## Consumes

A controller action consumes `application/json` by default. `@Consumes` takes a `String[]` of supported media types for an incoming request; any HTTP method annotation also has a `consumes` member.

```java
@Consumes({MediaType.APPLICATION_FORM_URLENCODED, MediaType.APPLICATION_JSON})
@Post("/multiple")
public HttpResponse multipleConsumes() { ... }
```

## Plain text responses

Annotate the method with `@Produces` for `text/plain` and return a `String`; the page's example converts the data with `toString()`.

Note from the page: in Micronaut Framework 4.x, `text/plain` responses are more restrictive about allowed types than 3.x. For anything other than `java.lang.String`, call `toString()` yourself. Setting `micronaut.http.legacy-text-conversion` to `true` restores the old 3.x behaviour, which the page calls not recommended.

## Extra content types per codec

JSON parsing normally happens only for `application/json`; other `MediaTypeCodec` classes likewise have predefined content types. To extend the list a codec processes, provide configuration stored in `CodecConfiguration`:

```yaml
micronaut:
  codec:
    json:
      additional-types:
        - text/javascript
```

The supported configuration prefixes are `json`, `json-stream`, `text` and `text-stream`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the three cited pages: defaults for produces and consumes, the `@Consumes` `String[]` type, the `consumes` and `produces` members, the 4.x text/plain note and `micronaut.http.legacy-text-conversion`, the codec `additional-types` YAML and the four prefixes. Removed: the `/xml`, `/member` and `/date` example routes and the `Calendar` snippet, because the pages only embed those from source files that were not readable.
