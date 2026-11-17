---
id: computing-software.web-development.dioxus.dioxus-forms-and-multipart
name: dioxus-forms-and-multipart
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, forms, form, parsed-values, multipartformdata, next-field, formevent]
level: practitioner
status: docs-checked
description: "Submit HTML forms to Dioxus server functions with Form<T> and FormEvent::parsed_values, and handle file uploads with MultipartFormData and next_field."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/forms.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forms and multipart uploads in Dioxus fullstack

Goal: send form values and file inputs to a server function as typed Rust data.

## Simple forms

Wrap a struct implementing `Serialize + Deserialize` in Axum's typed `Form<T>` and take it as a server function argument:

```rust
#[derive(Deserialize, Serialize)]
pub struct LoginForm { username: String, password: String }

#[post("/api/login")]
async fn login(form: Form<LoginForm>) -> Result<()> {
    if form.0.username == "admin" && form.0.password == "password" { /* .. */ }
    Ok(())
}
```

On the client, `onsubmit` receives a `FormEvent`; call `.parsed_values()` to build your struct from the form's inputs (works with any form element that has `name` attributes):

```rust
form {
    onsubmit: move |evt: FormEvent| async move {
        evt.prevent_default(); // stop the browser navigating away
        let values: LoginForm = evt.parsed_values().unwrap();
        login(Form(values)).await;
    },
    input { r#type: "text", id: "username", name: "username" }
    input { r#type: "password", id: "password", name: "password" }
    button { "Login" }
}
```

Form elements must have a `name` attribute; it identifies fields during deserialization. `GET` requests encode form values in the URL, which may not suit complex data, so use `POST` endpoints for form data.

## Multipart (file uploads)

Forms with file inputs make the browser create a multi-part request. Dioxus provides `MultipartFormData`; on the client convert the event with `.into()`:

```rust
form {
    onsubmit: move |evt| async move { evt.prevent_default(); upload(evt.into()).await; },
    input { r#type: "file", name: "headshot", multiple: true, accept: ".png,.jpg,.jpeg" }
    input { r#type: "text", name: "name", placeholder: "Name" }
    input { r#type: "submit", name: "submit", value: "Submit your resume" }
}
```

On the server iterate the fields with `next_field()`:

```rust
#[post("/api/upload-multipart")]
async fn upload(mut form: MultipartFormData) -> Result<()> {
    while let Ok(Some(field)) = form.next_field().await {
        let name = field.name().unwrap_or("<none>").to_string();
        let file_name = field.file_name().unwrap_or("<none>").to_string();
        let content_type = field.content_type().unwrap_or("<none>").to_string();
        let bytes = field.bytes().await;
        // ...
    }
    Ok(())
}
```

## Checked
Checked 2026-11-07 against the 0.7 Forms and Multipart page (read in full; code is inline). Confirmed: Form<T> with Serialize and Deserialize, parsed_values(), name attributes, GET vs POST note, MultipartFormData with .into() on the client and next_field() on the server. Nothing removed.
Method: documentation only; no commands were run.
