---
id: computing-software.web-development.dioxus.dioxus-file-input-handling
name: dioxus-file-input-handling
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, file-input, files, read-string, directory, multiple, accept, onchange]
level: intro
status: docs-checked
description: "Pick files and folders in Dioxus with input type file: accept, multiple, directory, evt.files(), file.name() and async file.read_string()."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/event_handlers.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/input_fileengine.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/input_fileengine_async.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/input_fileengine_folder.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File inputs in Dioxus

Goal: let the user choose files or a folder and read them.

Use an `input` of type `file`. It supports `multiple`; add `directory` to select a folder (Dioxus maps it to browser-specific attributes because there is no standard way). The `FormData` event exposes the selection through `evt.files()`.

## List filenames

```rust
let mut filenames: Signal<Vec<String>> = use_signal(Vec::new);
rsx! {
    input {
        type: "file",
        accept: ".txt,.rs",   // accepted extensions
        multiple: true,       // pick several files
        onchange: move |evt| {
            for file in evt.files() {
                filenames.write().push(file.name());
            }
        }
    }
}
```

## Read content asynchronously

Read file content in an async closure so the UI stays interactive:

```rust
onchange: move |evt| {
    async move {
        for file in evt.files() {
            if let Ok(file) = file.read_string().await {
                files_uploaded.write().push(file);
            }
        }
    }
}
```

## Select a folder

```rust
input {
    type: "file",
    directory: true,
    onchange: move |evt| {
        for file in evt.files() {
            println!("{}", file.name());
        }
    }
}
```

## Gotchas

- Extracting files differs from typical JavaScript: use `evt.files()` on the event rather than reading a DOM list.
- The prose on the page mentions a `FileEngine` struct; the included 0.7 example code iterates `evt.files()` directly.

## Checked
Checked 2026-11-07 against the 0.7 Handling User Input page (Handling files section) and the input_fileengine, input_fileengine_async and input_fileengine_folder snippet files (all read in full). Confirmed: type file with accept, multiple and directory, evt.files(), file.name(), async read_string(), and the FileEngine prose vs code difference. Nothing removed.
Method: documentation only; no commands were run.
