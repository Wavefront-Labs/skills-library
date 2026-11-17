---
id: computing-software.software-engineering.perl.plack-psgi-middleware
name: plack-psgi-middleware
category: computing-software
field: software-engineering
product: perl
tags: [perl, psgi, plack, plackup, plack-middleware, plack-builder, plack-psgi-middleware]
level: advanced
status: docs-checked
description: "Write a PSGI app, understand the env, response and streaming rules, and compose middleware with Plack::Builder (enable, enable_if, mount)."
sources: ["https://metacpan.org/pod/PSGI", "https://metacpan.org/pod/Plack", "https://metacpan.org/pod/Plack::Builder"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSGI, Plack and middleware

**Goal:** understand the layer under Perl web frameworks and wrap apps with middleware.

```perl
# app.psgi
use strict; use warnings; use Plack::Builder;
my $app = sub {
    my $env = shift;                                   # PSGI environment hash ref
    return ['200', ['Content-Type' => 'text/plain'], ["Hello World"]];   # status, header pairs, body
};
builder {
    enable "Deflater";                                 # loads Plack::Middleware::Deflater
    enable_if { $_[0]->{REMOTE_ADDR} eq '127.0.0.1' } 'StackTrace', force => 1;
    $app;                                              # builder returns the wrapped app
};
```

## The application contract (PSGI spec)
- An app is a code ref taking exactly one argument, the environment, and returning an array ref of exactly three values, or a code ref for a delayed or streaming response.
- The environment is a hash ref. It must include `REQUEST_METHOD` (never empty), `SCRIPT_NAME`/`PATH_INFO` (one must be set), `QUERY_STRING` (always present, may be empty), `SERVER_NAME`, `SERVER_PORT`, plus `psgi.version`, `psgi.url_scheme`, `psgi.input`, `psgi.errors` and the boolean `psgi.multithread`, `psgi.multiprocess`, `psgi.run_once`, `psgi.nonblocking`, `psgi.streaming`.
- Request headers appear as `HTTP_*` keys (upper case, hyphens to underscores); `CONTENT_TYPE` and `CONTENT_LENGTH` are separate keys and `HTTP_CONTENT_TYPE`/`HTTP_CONTENT_LENGTH` must not appear.
- Custom env keys must contain a dot and be uniquely prefixed; `psgi.` and `psgix.` prefixes are reserved.
- Status is an integer >= 100. Headers are an array ref of key/value pairs (even count), not a hash; repeated keys are sent as separate lines (for example several `Set-Cookie`).
- `Content-Type` is required except for status 1xx, 204 and 304, where `Content-Type` and `Content-Length` must not be present.
- The body is an array ref of byte strings or a handle-like object (servers call `getline` and `close`). It must be encoded and must not contain wide characters (> 255).
- Read `psgi.input` with `$input->read($buf, $len)` as a method rather than the built-in `read` or `<$fh>`.
- Delayed response: return `sub { my $responder = shift; ... }` and call `$responder->([...])`. Omit the body from that array to get a writer with `write` and `close` methods (streaming). Servers set `psgi.streaming` true when supported.
- Middleware is an app that wraps an app. To the server it looks like an app; to the inner app it is the server. It must behave exactly like an app and should pass through response types it does not understand (for example streaming).

## Plack toolkit pieces (Plack POD)
- `.psgi` file: loaded with Perl's `do`; its return value must be the app code ref. Frameworks usually generate one (for example `sub { MyApp->run_psgi(@_) }`).
- `plackup` runs a `.psgi` file via Plack::Loader and Plack::Handler adapters (standalone HTTP::Server::PSGI, CGI, FCGI, Apache1/2, HTTP::Server::Simple in core; many more on CPAN).
- Plack::Request and Plack::Response wrap `$env` and the response array; Plack::Test tests an app with HTTP::Request/HTTP::Response pairs; Plack::Test::Suite tests new server backends.
- Namespaces: middleware goes under `Plack::Middleware::` (subclass Plack::Middleware); endpoint-style components under `Plack::App::` (subclass Plack::Component), for example Plack::App::File. Do not name a new application or framework under `Plack::`.

## Plack::Builder (POD)
- `enable "Name", %opts` pushes middleware (prefix `Plack::Middleware::` added; prefix with `+` for a full class name). Enable from outer to inner: the stack is reversed when wrapping, so the first `enable` is outermost.
- Inline middleware: `enable sub { my $app = shift; sub { my $env = shift; ...; $app->($env) } }`.
- `enable_if { condition on $_[0] } 'Name', %opts` enables it conditionally.
- `mount "/path" => $app` maps paths via Plack::App::URLMap. Once you use `mount`, every path including root must use it: end with `mount "/" => $app`, not a bare `$app` (it is ignored with a warning). Builder blocks nest, so `mount "/foo" => builder { mount "/bar" => $app }` serves `$app` at `/foo/bar`.
- `builder { ... }` returns a new app, so it should normally be the last statement in the `.psgi` file.
- OO form: `Plack::Builder->new`, `add_middleware`, `add_middleware_if`, `mount`, `wrap($app)`, `to_app`.

## Self-check
- [ ] The `.psgi` file ends with the `builder` block or the app code ref.
- [ ] Response bodies are byte strings and headers are a flat list of pairs.

## Checked
Method: 2026-11-08 read the full PSGI, Plack and Plack::Builder POD text (MetaCPAN API plain-text export). Removed claims the pages do not state: plackup auto-reload flags, Starman/Twiggy/Gazelle options and worker flags, nginx/TLS and PLACK_ENV deployment advice, the AccessLog middleware, `Plack::Request->param`, and the Windows note. The `psgi.streaming` example and Builder behaviour are as documented.
