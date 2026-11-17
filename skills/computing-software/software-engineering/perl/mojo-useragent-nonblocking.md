---
id: computing-software.software-engineering.perl.mojo-useragent-nonblocking
name: mojo-useragent-nonblocking
category: computing-software
field: software-engineering
product: perl
tags: [perl, mojo-useragent, get-p, dom-scraping, websocket-client, mojo-useragent-nonblocking]
level: practitioner
status: docs-checked
description: "Use Mojo::UserAgent for blocking, callback and promise requests, JSON and form bodies, and Mojo::DOM CSS-selector scraping."
sources: ["https://docs.mojolicious.org/Mojo/UserAgent", "https://docs.mojolicious.org/Mojo/DOM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mojo::UserAgent blocking and non-blocking requests

**Goal:** a modern client that fits event-loop code. Mojo::UserAgent is a non-blocking I/O HTTP and WebSocket user agent with TLS, proxies, keep-alive, connection pooling, timeouts, cookies, gzip and promises.

```perl
use Mojo::UserAgent;
my $ua = Mojo::UserAgent->new;
$ua->max_redirects(5)->connect_timeout(3)->request_timeout(5);
$ua->transactor->name('MyUA 1.0');                      # change the user-agent name

my $res = $ua->get('https://example.org/api' => {Accept => 'application/json'})->result;  # dies on connection errors
my $data  = $res->json;
my $title = $res->dom->at('title')->text;
say $res->dom->find('h2 > a')->map('text')->join("\n");   # CSS selectors

$ua->post($url => json => {a => 1});                      # JSON body
$ua->post($url => form => {q => 'mojo'});                 # form body

$ua->get($url => sub ($ua, $tx) { say $tx->result->dom->at('title')->text });   # non-blocking callback
my $p = $ua->get_p($url);                                  # promise; combine several with Mojo::Promise
$ua->websocket('wss://example.org/ws' => sub ($ua, $tx) {
  say 'WebSocket handshake failed!' and return unless $tx->is_websocket;
});
```

## Rules (Mojo::UserAgent and Mojo::DOM docs)
- `->result` is the "fine grained response handling" form and dies on connection errors.
- `connect_timeout`, `request_timeout` and `max_redirects` are attributes you set on the user agent (the docs show `$ua->max_redirects(0)->connect_timeout(3)->request_timeout(5)`).
- `$ua->insecure(1)` disables TLS certificate verification; the docs show it only for testing. Its default comes from the `MOJO_INSECURE` environment variable.
- `$ua->cookie_jar` holds cookies; `$ua->cookie_jar->ignore(sub { 1 })` ignores all.
- Non-blocking methods take a callback; the `_p` variants return promises (`get_p`, `delete_p`, ...).
- `Mojo::DOM` `at` returns the first matching element (undef if none) and `find` returns a Mojo::Collection; both take CSS selectors, and HTML semantics mean tags and attribute names are lowercased, so selectors must be lowercase too.
- Mojo::DOM interprets broken markup in its own relaxed way that can differ from a browser: do not use it for validation or sanitization.
- Optional modules (EV, Net::DNS::Native, IO::Socket::Socks, IO::Socket::SSL) are used automatically if present; `MOJO_NO_NNR`, `MOJO_NO_SOCKS` and `MOJO_NO_TLS` disable features.

## Checked
2026-11-09. Read the Mojo::UserAgent synopsis, attributes and method listing (connect_timeout, request_timeout, max_redirects, insecure, cookie_jar, transactor) and Mojo::DOM description, `at`, `find`, selector notes by search. Removed as not confirmed on these pages: `is_success`/`message`/`code` usage, `$tx->error` semantics, the 4xx/5xx result claim, charset decoding via `text`, blocking-inside-loop warning, Mojo::URL advice, scraping etiquette and the `perl -Mojo` self-check.
Method: documentation only; no commands were run.
