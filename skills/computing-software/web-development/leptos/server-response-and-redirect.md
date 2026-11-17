---
id: computing-software.web-development.leptos.server-response-and-redirect
name: server-response-and-redirect
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, response-options, redirect, cookies, server-functions]
level: practitioner
status: docs-checked
description: "Set HTTP status, headers and cookies from a Leptos server function with ResponseOptions, and redirect with leptos_axum::redirect or leptos_actix::redirect."
sources: [https://book.leptos.dev/server/27_response.html, https://book.leptos.dev/islands.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modify the HTTP response and redirect from a server function

Goal: set a status code, set a cookie or header, or redirect, from inside a server function.

## ResponseOptions

`ResponseOptions` (types exist in both `leptos_actix` and `leptos_axum`) is provided via context during the initial server render and during every server function call. Pull it from context and mutate it:

```rust
#[server]
pub async fn tea_and_cookies() -> Result<(), ServerFnError> {
    use actix_web::{cookie::Cookie, http::header::HeaderValue, http::{header, StatusCode}};
    use leptos_actix::ResponseOptions;

    let response = expect_context::<ResponseOptions>();
    response.set_status(StatusCode::IM_A_TEAPOT);

    let cookie = Cookie::build("biscuits", "yes").finish();
    if let Ok(cookie) = HeaderValue::from_str(&cookie.to_string()) {
        response.insert_header(header::SET_COOKIE, cookie);
    }
    Ok(())
}
```

## redirect

Both integrations expose a `redirect` function. After validating credentials:

```rust
leptos_axum::redirect("/");
Ok(())
```

(The page's `login` example gets a DB pool and auth object from context, verifies the password, calls `auth.login_user`, then redirects, and returns `ServerFnError::ServerError("Invalid credentials".into())` on failure.)

## With forms

`redirect` works with the progressively enhanced `<ActionForm/>`: without JS/WASM the browser follows the status code and header; with JS/WASM the form detects the redirect in the server function response and navigates client-side. See computing-software.web-development.leptos.action-form.

## Gotcha

Without a client-side router (as in an islands app that keeps routing out of the client), you lose the ability to call `redirect()` from server functions and have it redirect on the client; the islands page says you can provide a minimal version by calling `set_redirect_hook`. See computing-software.web-development.leptos.islands-server-children-and-context.

## Checked

2026-11-07: Read in full: server/27_response.md (ResponseOptions provided via context during initial render and server function calls, tea_and_cookies and login examples, redirect with ActionForm) and, in islands.md, only the section 'Replacing the Client-Side Router' (the page is large; the rest was not re-read for this skill). Replaced the unsourced 'islands has no client router' gotcha with the islands page's statement that without a client-side router redirect() from server functions does not redirect on the client and set_redirect_hook can provide a minimal version; added islands.html to sources. Not opened: the docs.rs ResponseOptions and redirect pages.

Method: documentation only; no commands were run.
