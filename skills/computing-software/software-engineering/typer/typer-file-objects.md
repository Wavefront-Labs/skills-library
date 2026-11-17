---
id: computing-software.software-engineering.typer.typer-file-objects
name: typer-file-objects
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, file, filetext, binary, mode, atomic]
level: advanced
status: docs-checked
description: "Receive file-like objects in Typer with FileText, FileTextWrite, FileBinaryRead and FileBinaryWrite, and tune mode, encoding, lazy and atomic."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/file.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial004_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial005_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer file-like parameters

Most of the time `Path` is enough. Use the file types when you want a file-like object (what `open()` returns), for example when migrating an existing application.

## The four types

- `typer.FileText`: read text, you get `str` (decoded, e.g. non-English text arrives as characters, not bytes). Default `mode="r"`.
- `typer.FileTextWrite`: write human text. Default `mode="w"`. It is a convenience class equal to `FileText` with `mode="w"`.
- `typer.FileBinaryRead`: read binary, you get `bytes`. `mode="rb"`.
- `typer.FileBinaryWrite`: write binary, pass `bytes` to `.write()`, not `str`; encode strings first. `mode="wb"`.

```python
@app.command()
def main(config: Annotated[typer.FileText, typer.Option()]):
    for line in config:
        print(f"Config line: {line}")
```

Verify: with `config.txt` containing `some settings` and `some more settings` lines, `--config config.txt` prints `Config line: some settings` then `Config line: some more settings`.

Write text:

```python
@app.command()
def main(config: Annotated[typer.FileTextWrite, typer.Option()]):
    config.write("Some config written by the app")
    print("Config written")
```

Read binary (chunks are `bytes`):

```python
@app.command()
def main(file: Annotated[typer.FileBinaryRead, typer.Option()]):
    processed_total = 0
    for bytes_chunk in file:
        # Process the bytes in bytes_chunk
        processed_total += len(bytes_chunk)
        print(f"Processed bytes total: {processed_total}")
```

Write binary (encode `str` first):

```python
@app.command()
def main(file: Annotated[typer.FileBinaryWrite, typer.Option()]):
    first_line_str = "some settings\n"
    # You cannot write str directly to a binary file, you have to encode it to get bytes
    first_line_bytes = first_line_str.encode("utf-8")
    # Then you can write the bytes
    file.write(first_line_bytes)
    # This is already bytes, it starts with b"
    second_line = b"la cig\xc3\xbce\xc3\xb1a trae al ni\xc3\xb1o"
    file.write(second_line)
    print("Binary file written")
```

## Configuration parameters

Pass these to `typer.Option()` or `typer.Argument()`:

- `mode`: the open mode; set automatically by the class.
- `encoding`: force e.g. `"utf-8"`.
- `lazy`: delay I/O. Default is `lazy=True` for writing (file not created until you write) and `lazy=False` for reading. Set `lazy=False` to override.
- `atomic`: writes go to a temporary file, moved to the destination on completion; useful for files modified frequently by several users or programs.

## Overriding mode

`mode="a"` appends:

```python
@app.command()
def main(config: Annotated[typer.FileText, typer.Option(mode="a")]):
    config.write("This is a single line\n")
    print("Config line written")
```

Because you set the mode manually, either `FileText` or `FileTextWrite` works. Verify: running three times then `cat config.txt` shows `This is a single line` three times.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/file.md with its five example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
