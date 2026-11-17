---
id: computing-software.web-development.gin.gin-upload-single-file
name: gin-upload-single-file
category: computing-software
field: web-development
product: gin
tags: [gin, upload-file, formfile, saveuploadedfile, maxmultipartmemory, multipart]
level: practitioner
status: docs-checked
description: "Receive one multipart upload in Gin with c.FormFile and c.SaveUploadedFile, tune router.MaxMultipartMemory, and sanitize file.Filename with filepath.Base."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/single-file.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin single file upload

Goal: accept one file from a multipart/form-data request and save it to disk.

Gin gives `gin.Context` three upload helpers: `c.FormFile(name)` (one file by form field name), `c.MultipartForm()` (whole form, all files and fields) and `c.SaveUploadedFile(file, dst)` (save to a path).

```go
router := gin.Default()
// Set a lower memory limit for multipart forms (default is 32 MiB)
router.MaxMultipartMemory = 8 << 20 // 8 MiB

router.POST("/upload", func(c *gin.Context) {
  file, err := c.FormFile("file")
  if err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  log.Println(file.Filename)

  dst := filepath.Join("./files/", filepath.Base(file.Filename))
  c.SaveUploadedFile(file, dst)

  c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
})
router.Run(":8080")
```

Try it:

```sh
curl -X POST http://localhost:8080/upload \
  -F "file=@/path/to/your/file.zip" \
  -H "Content-Type: multipart/form-data"
# Output: 'file.zip' uploaded!
```

## Memory limit
`router.MaxMultipartMemory` defaults to 32 MiB. Data within the limit is buffered in memory; files larger than it are stored in temporary files on disk.

## Gotcha
Never trust `file.Filename` from the client. Sanitize it before using it in file paths; `filepath.Base` strips directory components and prevents path traversal.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/upload-file/single-file.md and routing/upload-file/index.md. Confirmed: FormFile, MultipartForm and SaveUploadedFile descriptions, the 32 MiB default and temporary-file behaviour, the example and output, and the never-trust-file.Filename caution. Trimmed nothing.

Method: documentation only; no commands were run.
