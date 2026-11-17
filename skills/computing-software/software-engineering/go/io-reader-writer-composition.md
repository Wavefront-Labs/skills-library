---
id: computing-software.software-engineering.go.io-reader-writer-composition
name: io-reader-writer-composition
category: computing-software
field: software-engineering
product: go
tags: [go, golang, io-reader, io-writer, streaming, io-copy, io-pipe, bufio, composition, go-io-files, go-bufio-scanner]
level: practitioner
status: verified
description: "Stream data in Go by composing io.Reader and io.Writer: io.Copy, TeeReader, MultiWriter, LimitReader, io.Pipe and bufio, with correct Read semantics and closing."
sources: ["https://pkg.go.dev/io", "https://pkg.go.dev/bufio", "https://go.dev/tour/methods/21"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# io.Reader / io.Writer composition

**Goal:** process files, network bodies and archives as streams with constant memory, by plugging
small readers and writers together instead of loading everything into `[]byte`.

## The contracts
- `Read(p)` returns `n > 0` bytes **and possibly an error in the same call**. Always process
  `p[:n]` before looking at `err`. `io.EOF` is the normal end, not a failure.
- A Read may return fewer bytes than `len(p)` even when more data is coming; use `io.ReadFull` when
  you need exactly N bytes.
- `Write` must return a non-nil error if `n < len(p)`.

## Building blocks
| Need | Tool |
|---|---|
| copy stream to stream | `io.Copy(dst, src)` (uses `WriterTo`/`ReaderFrom` fast paths when source or destination implements them) |
| cap input size | `io.LimitReader(r, max)`; for HTTP bodies `http.MaxBytesReader` |
| hash while copying | `io.TeeReader(r, h)` or `io.MultiWriter(file, h)` |
| concatenate | `io.MultiReader(header, body)` |
| connect a writer-producer to a reader-consumer | `io.Pipe()` |
| buffered line reading | `bufio.Scanner` / `bufio.Reader` |
| batch small writes | `bufio.NewWriter(w)` + `Flush()` |
| read from memory | `bytes.NewReader`, `strings.NewReader` |
| random access / section | `io.SectionReader`, `io.ReaderAt` |

## Example: upload, hash and gzip in one pass
```go
func store(dst io.Writer, src io.Reader) (string, error) {
    h := sha256.New()
    zw := gzip.NewWriter(dst)
    if _, err := io.Copy(zw, io.TeeReader(io.LimitReader(src, 100<<20), h)); err != nil {
        return "", err
    }
    if err := zw.Close(); err != nil { // Close flushes the gzip footer: check its error
        return "", err
    }
    return hex.EncodeToString(h.Sum(nil)), nil
}
```

## io.Pipe: stream into an API that wants a Reader
```go
pr, pw := io.Pipe()
go func() {
    enc := json.NewEncoder(pw)
    err := enc.Encode(bigValue)
    pw.CloseWithError(err)      // nil err closes normally -> reader sees EOF
}()
req, _ := http.NewRequestWithContext(ctx, "POST", url, pr)
```
Pipes are synchronous and unbuffered; if the reader stops reading, the writer goroutine blocks
forever, so always close one side on error.

## Scanner limits
`bufio.Scanner` fails with `bufio.Scanner: token too long` on lines over 64 KB. Raise with
`sc.Buffer(make([]byte, 0, 1<<20), 10<<20)` or use `bufio.Reader.ReadString('\n')`. Always check
`sc.Err()` after the loop.

## Writing your own
Accept the narrowest interface (`io.Reader`, not `*os.File`) and return concrete types. Implement
`io.WriterTo` / `io.ReaderFrom` only when you can do better than a buffer copy.

## Gotchas
- Forgetting to `Close` writers that buffer (gzip, zip, bufio Flush, csv Flush) produces truncated
  output with no error until you check.
- `ioutil` is deprecated; use `io.ReadAll` / `os.ReadFile`. `io.ReadAll` on untrusted input needs a
  `LimitReader` first.
- HTTP response bodies must be read to EOF and closed for connection reuse.

## Verify
- [ ] Memory stays flat when processing a file larger than RAM.
- [ ] Truncated or oversized input returns an error, not partial success.
- [ ] Every buffering writer's Close/Flush error is checked.

## Checked
2026-10-21 on Go 1.27.3 (Windows): `store` (TeeReader + LimitReader + gzip + sha256) round-tripped; a gzip writer that was not closed produced a stream that failed to read with `unexpected EOF`; `bufio.Scanner` on a 70,000-byte line failed with `token too long` and `sc.Buffer(make([]byte,0,1<<20), 10<<20)` fixed it; `iotest.DataErrReader` returned 3 bytes plus EOF in one call, `OneByteReader` returned short reads and `io.ReadFull` returned 4 bytes (or `unexpected EOF` on short input); `io.Pipe` with `CloseWithError(nil)` gave EOF and with an error returned it to the reader; `MultiWriter`/`MultiReader`/`SectionReader` ran; `http.MaxBytesReader` returned `http: request body too large`; an unflushed `bufio.Writer` had written 0 bytes until `Flush`; the `Write`/`Read` contracts and the `ioutil` deprecation (Go 1.16) read from `go doc`. The 'sendfile' remark was dropped because it was not verified.
