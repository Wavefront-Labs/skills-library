---
id: computing-software.software-engineering.java.spring-multipart-uploads-and-streaming-downloads
name: spring-multipart-uploads-and-streaming-downloads
category: computing-software
field: software-engineering
product: java
tags: [java, spring-web, spring-file-upload, multipartfile, streamingresponsebody, upload-limits, owasp]
level: practitioner
status: docs-checked
description: "Accept multipart uploads and stream large downloads in Spring MVC: Boot multipart limits, safe file naming and validation per OWASP, StreamingResponseBody."
sources: ["https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html#mvc-ann-async-http-streaming", "https://docs.spring.io/spring-boot/appendix/application-properties/index.html#appendix.application-properties.web", "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multipart uploads and streaming downloads

## Limits (Spring Boot properties)
```yaml
spring.servlet.multipart:
  max-file-size: 10MB          # default 1MB
  max-request-size: 12MB       # default 10MB
  file-size-threshold: 1MB     # files above this are written to disk (default 0B)
```
Also available: `spring.servlet.multipart.enabled` (default `true`), `location` (intermediate location) and `resolve-lazily` (default `false`). Tomcat has its own `server.tomcat.max-swallow-size` (default 2MB) and `server.tomcat.max-http-form-post-size` (default 2MB).

## Upload
```java
@PostMapping(path = "/files", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
ResponseEntity<Void> upload(@RequestParam("file") MultipartFile f) throws IOException {
    if (f.isEmpty()) throw new ResponseStatusException(BAD_REQUEST);
    Path target = root.resolve(UUID.randomUUID() + ".bin").normalize();   // generated name, never the client name
    if (!target.startsWith(root)) throw new ResponseStatusException(BAD_REQUEST);
    try (InputStream in = f.getInputStream()) { Files.copy(in, target); }
    return ResponseEntity.created(URI.create("/files/" + target.getFileName())).build();
}
```

## Streaming download
`StreamingResponseBody` bypasses message conversion and writes straight to the response `OutputStream` (for example a file download); use it as the body of a `ResponseEntity` to set status and headers. Writes run on a thread from the configured `AsyncTaskExecutor`; the default executor is not suitable for production under load, so configure one with `configureAsyncSupport` on `WebMvcConfigurer`. The async timeout defaults to the Servlet container's value unless set.
```java
@GetMapping("/files/{id}")
ResponseEntity<StreamingResponseBody> download(@PathVariable String id) {
    Path p = root.resolve(id).normalize();
    if (!p.startsWith(root) || !Files.isRegularFile(p)) return ResponseEntity.notFound().build();
    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_OCTET_STREAM)
        .body(out -> Files.copy(p, out));
}
```
The Servlet API gives no notice when a client disconnects; the write simply fails.

## OWASP File Upload checklist (applies to any stack)
- Allow-list extensions the business needs; validate after decoding the filename; beware double extensions, null bytes, case tricks and NTFS alternate data streams (reject a colon).
- The `Content-Type` header is client-supplied and spoofable: use it only as a quick check, add file-signature validation, and never rely on either alone.
- Replace the filename with an application-generated one (for example a UUID); if names must be kept, cap the length and restrict characters.
- Set file size limits (after decompression for archives) and limit downloads too.
- Store files on another host, or outside the web root; if public, serve them through a handler that maps ids to files. Disable per-directory config overrides on upload directories.
- Only authenticated, authorized users upload; protect the endpoint from CSRF; scan with antivirus or a sandbox where possible; for images decode and re-encode.

## Verify
An oversize upload is rejected by the configured limit; a filename of `../../x` is stored under a generated name.

## Checked

Date: 2026-11-08

Read in full: the Spring Framework Asynchronous Requests page and the OWASP File Upload Cheat Sheet. Partially read: the Spring Boot application-properties appendix (about 235 KB), searched only for the multipart and Tomcat property names and defaults quoted above, which match. Removed because the cited pages do not state them: the 413 status, `Resource`-based Range and conditional request handling, the `nosniff` header, `ContentDisposition` usage, and presigned-URL advice.

Method: documentation only; no commands were run.
