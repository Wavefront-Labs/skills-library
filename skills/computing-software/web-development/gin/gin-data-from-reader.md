---
id: computing-software.web-development.gin.gin-data-from-reader
name: gin-data-from-reader
category: computing-software
field: web-development
product: gin
tags: [gin, datafromreader, io-reader, streaming, proxy, content-disposition, extraheaders]
level: practitioner
status: docs-checked
description: "Stream a remote or generated io.Reader to the client in Gin with c.DataFromReader, passing status, length, content type and extra headers."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/serving-data-from-reader.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/serving-data-from-file.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin DataFromReader: stream an io.Reader to the response

Goal: forward data from any `io.Reader` to the client without buffering it all in memory.

Signature: `c.DataFromReader(code, contentLength, contentType, reader, extraHeaders)` where `extraHeaders` is an optional `map[string]string` (for example `Content-Disposition` for downloads).

Use cases: proxying remote resources (cloud storage, CDN), streaming generated content such as CSV exports, and serving large files read in chunks.

```go
router.GET("/someDataFromReader", func(c *gin.Context) {
  response, err := http.Get("https://raw.githubusercontent.com/gin-gonic/logo/master/color.png")
  if err != nil || response.StatusCode != http.StatusOK {
    c.Status(http.StatusServiceUnavailable)
    return
  }

  reader := response.Body
  contentLength := response.ContentLength
  contentType := response.Header.Get("Content-Type")

  extraHeaders := map[string]string{
    "Content-Disposition": `attachment; filename="gopher.png"`,
  }

  c.DataFromReader(http.StatusOK, contentLength, contentType, reader, extraHeaders)
})
```

The example fetches an image from GitHub and streams it to the client as a downloadable attachment; bytes flow from the upstream response body to the client without being accumulated in a buffer.

## Gotcha
The page notes that `response.Body` is closed automatically by the HTTP server after the handler returns, since `DataFromReader` reads it to completion while writing the response.

## Comparison
For files already on disk use `c.File`, `c.FileFromFS` or `c.FileAttachment`. Reach for `c.DataFromReader` when the bytes come from an `io.Reader` such as a remote URL or dynamically generated content, and you want to set the content length and MIME type yourself.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Serving data from reader and Serving data from file (DataFromReader signature, use cases, File/FileFromFS/FileAttachment).
Removed or corrected: fixed broken source URL; reworded Body-close note to match the page.

Method: documentation only; no commands were run.
