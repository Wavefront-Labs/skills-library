---
id: computing-software.web-development.gin.gin-upload-multiple-files
name: gin-upload-multiple-files
category: computing-software
field: web-development
product: gin
tags: [gin, upload-file, multipartform, saveuploadedfile, multipart, maxmultipartmemory]
level: practitioner
status: docs-checked
description: "Handle several uploaded files in one request with c.MultipartForm and form.File, saving each with c.SaveUploadedFile and a filepath.Base-sanitized name."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/multiple-file.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/upload-file/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin multiple file upload

Goal: receive several files in one request and save each one.

Use `c.MultipartForm()`. Files are grouped by form field name, so give every file you want to upload together the same field name (here `files`) and read them from `form.File["files"]`.

```go
router := gin.Default()
// Set a lower memory limit for multipart forms (default is 32 MiB)
router.MaxMultipartMemory = 8 << 20 // 8 MiB

router.POST("/upload", func(c *gin.Context) {
  form, err := c.MultipartForm()
  if err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  files := form.File["files"]

  for _, file := range files {
    log.Println(file.Filename)
    dst := filepath.Join("./files/", filepath.Base(file.Filename))
    c.SaveUploadedFile(file, dst)
  }
  c.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))
})
router.Run(":8080")
```

Test it:

```sh
curl -X POST http://localhost:8080/upload \
  -F "files=@/path/to/test1.zip" \
  -F "files=@/path/to/test2.zip" \
  -H "Content-Type: multipart/form-data"
# Output: 2 files uploaded!
```

## Gotchas
- `c.MultipartForm()` parses the entire form, giving access to both files and field values.
- The client-supplied `file.Filename` should not be trusted; sanitize it (the example uses `filepath.Base`).
- Default memory limit for multipart parsing is 32 MiB (`router.MaxMultipartMemory`); larger parts go to temporary files on disk.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/upload-file/multiple-file.md and routing/upload-file/index.md. Confirmed: MultipartForm with form.File["files"], the 8 MiB MaxMultipartMemory example, filepath.Base sanitising, the curl output, and the 32 MiB default with temporary files from the index page. Trimmed nothing.

Method: documentation only; no commands were run.
