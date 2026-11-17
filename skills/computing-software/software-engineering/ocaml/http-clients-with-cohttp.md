---
id: computing-software.software-engineering.ocaml.http-clients-with-cohttp
name: http-clients-with-cohttp
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, cohttp-client, cohttp, http-client, cohttp-lwt, tls]
level: practitioner
status: docs-checked
description: "Make HTTP requests with cohttp-lwt-unix, read bodies, add timeouts, follow redirects manually and pick a TLS backend."
sources: ["https://github.com/mirage/ocaml-cohttp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP clients

```ocaml
(* libraries: cohttp-lwt-unix *)
open Lwt
open Cohttp
open Cohttp_lwt_unix

let main =
  Client.get (Uri.of_string "http://example.org/") >>= fun (resp, body) ->
  let code = resp |> Response.status |> Code.code_of_status in
  Printf.printf "Response code: %d\n" code;
  body |> Cohttp_lwt.Body.to_string >|= fun body ->
  Printf.printf "Body of length: %d\n" (String.length body);
  body

let () = ignore (Lwt_main.run main)
```

## Notes
- `Client.call` is the most general; `get`, `post` and the like are specialised. `Client.get` takes optional arguments for headers. The response is a tuple of the response (status, headers, version) and the body.
- Backends: `Cohttp_lwt_unix` (Lwt, ocaml-tls), `Cohttp_async` (Async, async_ssl), `Cohttp_lwt_jsoo` (XMLHttpRequest), `Cohttp_curl` (libcurl via ocurl), `Cohttp_eio` (Eio, OCaml 5). Install the backend you want, e.g. `opam install cohttp-lwt-unix`.
- HTTPS with `Cohttp_lwt_unix`: install `tls-lwt` (ocaml-tls) or `lwt_ssl` (ocaml-ssl). `lwt_ssl` is the default when both are installed; set `CONDUIT_TLS=native` to force ocaml-tls.
- Timeouts: use `Lwt.pick [ (f () >|= fun v -> `Done v); (Lwt_unix.sleep time >|= fun () -> `Timeout) ]` around the request. With `cohttp-async` use Async `Clock.with_timeout`.
- Redirects are not followed automatically. Write a loop that reads the `location` header and counts remaining redirects. Drain unconsumed bodies of non-OK responses with `Cohttp_lwt.Body.drain_body`, otherwise memory or connections leak.
- Cookies and sessions are not supported by cohttp (the `session` library is compatible). Multipart form data needs an external library such as `multipart_form`.
- A server handler has type `conn -> Http.Request.t -> Cohttp_lwt.Body.t -> (Http.Response.t * Cohttp_lwt.Body.t) Lwt.t`; the request body is raw binary you must decode yourself.
- Debugging: set `COHTTP_DEBUG` to any value other than `0` or `false` for a default debug logger on stdout. Cohttp and Conduit use `Logs`; sources include `cohttp.lwt.io` and `cohttp.lwt.server`.

## Self-check
- [ ] A request to an HTTP echo server returns status 200.

## Checked

2026-11-08. Read in full: the ocaml-cohttp README (client tutorial, TLS note, timeouts, sessions, multipart, redirects, server, debugging).
Removed: `Lwt_unix.with_timeout` advice, JSON and Content-Type advice, piaf/httpaf claims, ocaml.org and Dream landing sources.
Method: documentation only; no commands were run.
