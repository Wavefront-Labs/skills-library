---
id: computing-software.web-development.dioxus.dioxus-server-function-custom-io
name: dioxus-server-function-custom-io
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, intorequest, fromrequest, intoresponse, fromresponse, server-functions, websocketoptions]
level: sme
status: docs-checked
description: "Build custom Dioxus server function inputs and outputs with FromRequest, IntoRequest, IntoResponse and FromResponse implementations."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/server_functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom inputs and outputs for Dioxus server functions

Goal: send or return a type that is not obviously serializable, as the built-in `WebsocketOptions` / `Websocket` pair does.

Non-query arguments must be a group of serializable types or a single type implementing both Axum's `FromRequest` (server side) and Dioxus' `IntoRequest` (client side). The return type must be serializable or implement Axum's `IntoResponse` plus Dioxus' `FromResponse`.

## Input: FromRequest + IntoRequest

If unsure which `Rejection` to use, the built-in `ServerFnError` integrates with fullstack.

```rust
impl<S: Send> FromRequest<S> for WebSocketOptions {
    type Rejection = axum::response::Response;
    fn from_request(request: Request, state: &S)
        -> impl Future<Output = Result<Self, Self::Rejection>> + Send { async move { /* .. */ } }
}
```

`IntoRequest` is generic over a hidden state type (default `ClientResponse`). For websockets a custom state, `UpgradingWebsocket`, carries the request stream so the response can initialize from it:

```rust
impl IntoRequest<UpgradingWebsocket> for WebSocketOptions {
    fn into_request(self, request: ClientRequest)
        -> impl Future<Output = std::result::Result<UpgradingWebsocket, RequestError>> + 'static {
        async move { let stream = send_request(request).await?; Ok(UpgradingWebsocket { /* stream */ }) }
    }
}

pub trait IntoRequest<R = ClientResponse>: Sized {
    fn into_request(self, req: ClientRequest)
        -> impl Future<Output = Result<R, RequestError>> + 'static;
}
```

## Output: IntoResponse + FromResponse

`IntoResponse` just builds an Axum `Response`; it is passed to the client untouched (Dioxus may add headers). `FromResponse` mirrors it and should use the same state parameter as the request type:

```rust
pub trait FromResponse<R = ClientResponse>: Sized {
    fn from_response(res: R) -> impl Future<Output = Result<Self, ServerFnError>>;
}
impl FromResponse<UpgradingWebsocket> for Websocket { /* from_response(res) */ }
```

The error type is `ServerFnError` so client code can downcast failures to a standard error.

Usage then stays simple: `_ = get_updates(WebsocketOptions::new()).await?;`

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 server functions page (read in full): argument and return type rules, FromRequest and IntoRequest with the hidden state type, UpgradingWebsocket, IntoResponse and FromResponse, ServerFnError, and the final usage line.

Method: documentation only; no commands were run.
