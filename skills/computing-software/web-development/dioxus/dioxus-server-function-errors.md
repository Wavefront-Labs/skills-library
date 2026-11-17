---
id: computing-software.web-development.dioxus.dioxus-server-function-errors
name: dioxus-server-function-errors
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, serverfnerror, orhttperror, httperror, asstatuscode, errorboundary, commit-error-status]
level: practitioner
status: docs-checked
description: "Return HTTP status codes from Dioxus server functions with ServerFnError, HttpError, OrHttpError and AsStatusCode, and keep them in an ErrorBoundary."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/server_functions.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handle errors and status codes in Dioxus fullstack

Goal: return meaningful errors from server functions and render fallback UI without losing the HTTP status.

Server functions must return `Result<T>`. The prelude exports a `Result<T>` that re-exports anyhow's. Accepted error types: `anyhow::Error`, `ServerFnError`, `CapturedError` (cheaply-cloneable anyhow wrapper), `StatusCode`, `HttpError` (status plus message) and custom errors implementing `Serialize + Deserialize + AsStatusCode`. Errors that do not downcast to a status-code-like type default to `500 INTERNAL SERVER ERROR`. With plain `Result<T>`, the client can only downcast errors to `ServerFnError`; use `ServerFnError` itself to match variants such as `ServerError { code, .. }`.

## OrHttpError

Extension methods on `Result<T>`, `Option<T>` and `bool` that return `Err(HttpError)`:

```rust
authenticate_user().or_unauthorized("You must be logged in to view this resource")?;
authenticate_user().or_http_error(StatusCode::UNAUTHORIZED, "Log in first!")?;
```

## Custom error

```rust
#[derive(thiserror::Error, Debug, Serialize, Deserialize)]
enum MyCustomError {
    #[error("bad request")] BadRequest { custom_name: String },
    #[error("not found")] NotFound,
    #[error("internal server error: {0}")] ServerFnError(#[from] ServerFnError),
}
impl AsStatusCode for MyCustomError {
    fn as_status_code(&self) -> StatusCode {
        match self {
            MyCustomError::BadRequest { .. } => StatusCode::BAD_REQUEST,
            MyCustomError::NotFound => StatusCode::NOT_FOUND,
            MyCustomError::ServerFnError(e) => e.as_status_code(),
        }
    }
}
```

## Status codes bubble to the root

Dioxus downcasts errors that bubble to the root component. If you catch the error with an `ErrorBoundary`, you must set the status yourself with `FullstackContext::commit_error_status`:

```rust
ErrorBoundary {
    handle_error: move |err| {
        let http_error = FullstackContext::commit_error_status(err.error().unwrap());
        rsx! { "An error occurred! {http_error:?}" }
    },
    Post {}
}
```

With the router, put the `ErrorBoundary` around `Outlet::<Route> {}` in a layout (`#[layout(ErrorLayout)]`) and match on `http_error.status` (e.g. `StatusCode::NOT_FOUND`) so only part of the page shows the error.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 fullstack pages server_functions.md and errors.md: accepted error types, the 500 default, the anyhow-backed prelude Result and ServerFnError downcast, OrHttpError methods, the custom error and AsStatusCode code, status bubbling to the root, commit_error_status inside an ErrorBoundary, and the ErrorLayout router pattern. Nothing removed.

Method: documentation only; no commands were run.
