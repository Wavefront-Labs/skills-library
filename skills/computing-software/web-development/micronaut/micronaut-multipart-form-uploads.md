---
id: computing-software.web-development.micronaut.micronaut-multipart-form-uploads
name: micronaut-multipart-form-uploads
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, uploads, multipart, form-data, file-upload, streaming-file-upload, formdata]
level: practitioner
status: docs-checked
description: "Receive forms and file uploads in Micronaut controllers using FormData/FileUpload, CompletedFileUpload, StreamingFileUpload and publisher arguments, with limits and cleanup rules."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/uploads.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/formData.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/formUploads.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/form/formBinding.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forms and file uploads in Micronaut

Set `consumes = MediaType.MULTIPART_FORM_DATA` on the route (`@Post(consumes = ...)`). Argument names match the form field names; use `@Part("name")` when they differ. Plain `application/x-www-form-urlencoded` forms bind like JSON (Jackson) to POJOs or directly to parameters (`@Nullable`/`Optional` supported).

## CompletionStage API (experimental): FormData, FileUpload, FormPart, FormParts
```java
@Controller(value = "/profile", consumes = MediaType.MULTIPART_FORM_DATA)
public class ProfileController {
    @Post("/form")
    public CompletionStage<String> form(FormData form) {
        String name = form.getString("name");
        int age = form.getInt("age", 18);
        FileUpload avatar = form.getFile("avatar");
        return avatar.bytes(64 * 1024)
            .thenApply(bytes -> name + " (" + age + ") sent " + avatar.fileName() + " of " + bytes.length + " bytes");
    }

    @Post("/arguments")
    public CompletionStage<String> arguments(String name, @Part("avatar") FileUpload picture,
                                             @Nullable FileUpload cover, List<FileUpload> documents) {
        return picture.transferTo(uploads.resolve(UUID.randomUUID().toString()))
            .thenApply(done -> name + " sent " + picture.fileName());
    }

    @Post("/video")
    public CompletionStage<String> video(String title, FormPart video) {   // streamed as it arrives
        return video.transferTo(uploads.resolve(UUID.randomUUID().toString()))
            .thenApply(done -> title + " stored " + video.fileName());
    }
}
```
- A missing required field or unconvertible value gives `400`; a file over `micronaut.server.multipart.max-file-size` gives `413`.
- Consume an upload once: `bytes(max)`, `text(max)`, `transferTo(path)` (target must not exist, directory must exist), `transferTo(outputStream)`, or `takeBody()`. A second consumption throws `IllegalStateException`.
- Do the work inside the returned stage. Unconsumed or running work is aborted and released when the request ends; do not wrap an async operation in try-with-resources.
- `fileName()` is client-supplied: never use it as a path unsanitized.
- `FormPart`: text fields the method needs must be sent before the part, else `400`. `FormParts` with `forEach` (and `part(name, consumer)`) walks parts in order; each part is owned until its stage completes.
- Limits: text fields share `micronaut.server.max-request-buffer-size`; whole request `micronaut.server.max-request-size`; Netty `form-max-fields` and `form-max-buffered-bytes`. Combining `FormParts` with any other form argument, or `FormData` with `CompletedFileUpload`/`FormPart`/`FormParts`, gives `500`.
- Filters can read `FormData`, `FileUpload` or `@Part` arguments and leave the same form for the route.

## Publisher-style API
- `StreamingFileUpload` (a `Publisher<PartData>` with metadata): the controller can run before the whole upload arrives; you must consume it, and `transferTo(File)` / `transferTo(OutputStream)` return a publisher:
  The argument name matches the form attribute name (for example `<input type="file" name="file">`). The returned `Mono` subscribes to the publisher from `transferTo` and answers once the upload completes, without blocking. File reading is offloaded to the IO thread pool.
```java
@Post(consumes = MediaType.MULTIPART_FORM_DATA)
public Publisher<HttpResponse<String>> upload(StreamingFileUpload file) {
    // Mono.from(file.transferTo(someFile)) then map the outcome to an HttpResponse
}
```
- `CompletedFileUpload` (or `byte[]`, `String`): the route waits for the whole upload. To buffer large files to disk set `micronaut.server.multipart.mixed: true` and `threshold: 10MB` (default threshold 10MB; unconfigured files stay in memory). The file is deleted when the controller ends unless you `transferTo` or `moveResource()`. If you do not read a `CompletedFileUpload`, call `discard`.
- Several parts with the same name: use `Publisher<StreamingFileUpload>`, `Publisher<CompletedFileUpload>`, `Publisher<CompletedPart>`, or `Publisher<Publisher<PartData>>`. A `Publisher<CompletedFileUpload>` is read fully immediately (no backpressure).
- A `StreamingFileUpload` before normal fields in the request deadlocks; the server raises an error. Use publisher parameters for the later fields.
- `@Body MultipartBody` is a publisher of every `CompletedPart` when part names are unknown; close each part.
- `CompletedFileUpload.transferTo` may block (the page's example runs the controller on an IO thread), and reading a `StreamingFileUpload` through an `InputStream` may block, so run those on an IO thread.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against all four cited pages: the multipart `consumes` setting, `@Part`, the experimental `FormData`, `FileUpload`, `FormPart` and `FormParts` types and their accessors, status codes 400, 413 and 500, one-shot consumption rules, the cleanup and `fileName()` warnings, the limit settings, `StreamingFileUpload` and `CompletedFileUpload` behaviour, the `mixed` and `threshold` YAML, same-name publisher types, `MultipartBody` and filter support. Removed: the streaming-upload code body (temp file, `CONFLICT` response) and the `@ExecuteOn(TaskExecutors.BLOCKING)` claim, which the pages do not state.
