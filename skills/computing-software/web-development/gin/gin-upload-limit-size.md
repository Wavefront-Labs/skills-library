---
id: computing-software.web-development.gin.gin-upload-limit-size
name: gin-upload-limit-size
category: computing-software
field: web-development
product: gin
tags: [gin, upload-file, maxbytesreader, maxbyteserror, parsemultipartform, 413]
level: practitioner
status: docs-checked
description: "Cap Gin upload size with http.MaxBytesReader around c.Request.Body and return 413 when ParseMultipartForm reports *http.MaxBytesError."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/limit-bytes.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin upload size limit

Goal: reject oversized uploads so clients cannot exhaust server memory or disk (denial of service).

Wrap `c.Request.Body` with `http.MaxBytesReader`; once the client sends more than the cap, the reader stops and returns an error. Trigger the read with `c.Request.ParseMultipartForm`, and check for `*http.MaxBytesError` to answer `413 Request Entity Too Large`.

```go
const MaxUploadSize = 1 << 20 // 1 MB

func uploadHandler(c *gin.Context) {
  c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, MaxUploadSize)

  if err := c.Request.ParseMultipartForm(MaxUploadSize); err != nil {
    if _, ok := err.(*http.MaxBytesError); ok {
      c.JSON(http.StatusRequestEntityTooLarge, gin.H{
        "error": fmt.Sprintf("file too large (max: %d bytes)", MaxUploadSize),
      })
      return
    }
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }

  file, _, err := c.Request.FormFile("file")
  if err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": "file form required"})
    return
  }
  defer file.Close()

  c.JSON(http.StatusOK, gin.H{"message": "upload successful"})
}

r := gin.Default()
r.POST("/upload", uploadHandler)
r.Run(":8080")
```

Test it:

```sh
curl -X POST http://localhost:8080/upload -F "file=@/path/to/small-file.txt"
# Output: {"message":"upload successful"}
curl -X POST http://localhost:8080/upload -F "file=@/path/to/large-file.zip"
# Output: {"error":"file too large (max: 1048576 bytes)"}
```

## Gotcha
`router.MaxMultipartMemory` (default 32 MiB) only decides how much of a multipart form is buffered in memory before spilling to temporary files; `MaxBytesReader` is the strict cap shown here.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/upload-file/limit-bytes.md and routing/upload-file/index.md. Confirmed: MaxBytesReader around c.Request.Body, ParseMultipartForm, the *http.MaxBytesError 413 path, the curl outputs, and the 32 MiB MaxMultipartMemory default from the index page. Trimmed nothing.

Method: documentation only; no commands were run.
