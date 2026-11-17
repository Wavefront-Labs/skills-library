---
id: computing-software.web-development.gin.gin-write-log-to-file
name: gin-write-log-to-file
category: computing-software
field: web-development
product: gin
tags: [gin, logging, gin-defaultwriter, io-multiwriter, lumberjack, log-rotation, disableconsolecolor]
level: practitioner
status: docs-checked
description: "Redirect Gin request logs to a file, to file plus console with io.MultiWriter, or to a lumberjack rotating file by setting gin.DefaultWriter before creating the router."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/write-log.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write Gin logs to a file

Goal: persist request logs. By default Gin writes all log output to `os.Stdout`; set `gin.DefaultWriter` before creating the router.

```go
gin.DisableConsoleColor() // no console colour needed in a file

f, _ := os.Create("gin.log")
gin.DefaultWriter = io.MultiWriter(f)

router := gin.Default()
```

## File and console together
`io.MultiWriter` duplicates writes to every writer you pass:

```go
f, _ := os.Create("gin.log")
gin.DefaultWriter = io.MultiWriter(f, os.Stdout)
```

Every log entry then goes to both `gin.log` and the console.

## Rotation in production
`os.Create` truncates the file on each app start. For production, append and rotate by size or time, for example with lumberjack:

```go
import "gopkg.in/natefinch/lumberjack.v2"

gin.DisableConsoleColor()
gin.DefaultWriter = &lumberjack.Logger{
    Filename:   "gin.log",
    MaxSize:    100, // megabytes
    MaxBackups: 3,
    MaxAge:     28, // days
}
router := gin.Default()
```

## Gotchas
- Set `gin.DefaultWriter` before creating the router, as the docs do.
- `os.Create` truncates `gin.log` each time the application starts.
- Disable console colour when writing to a file.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: logging/write-log.md. Confirmed: stdout default, DefaultWriter set before the router, DisableConsoleColor, io.MultiWriter, os.Create truncating, and the lumberjack settings. Trimmed nothing.

Method: documentation only; no commands were run.
