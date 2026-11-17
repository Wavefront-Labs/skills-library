---
id: computing-software.software-engineering.scala.sc-files-os-lib
name: sc-files-os-lib
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-text-io, files-os-lib]
level: practitioner
status: draft
description: "Read and write files with java.nio, Using and os-lib and run processes safely."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# scala.io.Source, java.nio.file and os-lib
- `Using(Source.fromFile(path, "UTF-8"))(_.getLines().toList)` closes the file; `Source` takes the default charset otherwise.
- `java.nio.file.Files.readString(Path.of(p))`, `Files.write`, `Files.walk` (close the stream).
- os-lib: ``os.read(os.pwd / "a.txt")``, ``os.proc("ls", "-l").call().out.text()``, ``os.write.over``; paths are typed and absolute.
- `scala.sys.process` runs processes with `"ls".!`; the `!!` throws on a non-zero exit code.
Verify: tests use a temporary directory.
