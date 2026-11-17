---
id: computing-software.software-engineering.rust.axum-routing-extractors-and-shared-state
name: axum-routing-extractors-and-shared-state
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-web-services, rust-axum, axum, routing, extractors, state, web]
level: practitioner
status: docs-checked
description: "Build an axum service: Router, handlers with extractors, typed State and FromRef, IntoResponse error types, body limits and debug_handler."
sources:
  - https://docs.rs/axum/latest/axum/
  - https://docs.rs/axum/latest/axum/extract/index.html
  - https://docs.rs/axum/latest/axum/extract/struct.DefaultBodyLimit.html
  - https://docs.rs/axum/latest/axum/attr.debug_handler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# axum routing, extractors and shared state

**Goal:** a small, testable HTTP service.

```rust
#[derive(Clone)]
struct AppState { db: sqlx::PgPool, cfg: Arc<Config> }

async fn get_user(State(s): State<AppState>, Path(id): Path<i64>) -> Result<Json<User>, AppError> {
    let u = find_user(&s.db, id).await?.ok_or(AppError::NotFound)?;
    Ok(Json(u))
}
async fn create(State(s): State<AppState>, Json(body): Json<NewUser>) -> impl IntoResponse {
    (StatusCode::CREATED, Json(s.insert(body).await))
}

enum AppError { NotFound, Db(sqlx::Error) }
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        match self {
            AppError::NotFound => StatusCode::NOT_FOUND.into_response(),
            AppError::Db(e) => { tracing::error!(%e, "db"); StatusCode::INTERNAL_SERVER_ERROR.into_response() }
        }
    }
}
impl From<sqlx::Error> for AppError { fn from(e: sqlx::Error) -> Self { AppError::Db(e) } }

let app = Router::new()
    .route("/users/{id}", get(get_user))        // path parameters use {id} in the current docs
    .route("/users", post(create))
    .with_state(state);
let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app).await?;
```

- A handler is an async function taking zero or more extractors (types implementing `FromRequest` or `FromRequestParts`) and returning something that implements `IntoResponse`. `Path`, `Query` and `Json` deserialize their input.
- Extractors run in parameter order. The request body can be consumed once, so only one extractor may consume it (`Json`, `String`, `Bytes`) and it must be the last argument; otherwise you get a compile error.
- Share state with the `State` extractor and `Router::with_state`. State is cloned per request, so wrap it in `Arc` or derive `Clone` when all fields are cheap to clone. `FromRef` (derive needs the `macros` feature) lets a handler extract only a substate.
- `Router<S>` with `S` other than `()` is missing state; `with_state` supplies it and the resulting `Router<()>` is what `serve` accepts.
- Alternatives to `State`: `Extension` (runtime 500 error if missing), closure captures (verbose) and task-local variables. The docs prefer `State` as more type safe.
- axum has no middleware system of its own; it uses `tower::Service`, so tower and tower-http layers (timeouts, tracing, compression) apply.
- `Bytes` and extractors built on it (`String`, `Json`, `Form`) accept bodies up to 2MB by default; raise or lower the limit with `DefaultBodyLimit`.

## Gotchas
- Handler type errors are long and cryptic; apply `#[axum::debug_handler]` (needs the `macros` feature) during development for better messages.
- `axum::serve` needs the `tokio` feature (default) and `http1` or `http2`.
- Cargo features for `ws`, `multipart`, `macros` and `http2` are off by default.

## Verify
`curl -i localhost:3000/users/1` returns the expected status; confirm a body-consuming extractor not placed last fails to compile.

## Checked
Method: docs-checked 2026-11-09 against the axum crate root, extract module, DefaultBodyLimit and debug_handler pages on docs.rs. Dropped unconfirmed claims about graceful shutdown, tower oneshot testing, 422 on malformed JSON and version-pinning advice.
