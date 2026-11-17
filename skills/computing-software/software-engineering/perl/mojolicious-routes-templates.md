---
id: computing-software.software-engineering.perl.mojolicious-routes-templates
name: mojolicious-routes-templates
category: computing-software
field: software-engineering
product: perl
tags: [perl, mojolicious, mojolicious-lite, morbo, hypnotoad, mojo-routes, mojolicious-routes-templates, perl-web-frameworks]
level: practitioner
status: draft
description: "Build a Mojolicious app: Lite and full apps, routes, templates, helpers, tests with Test::Mojo, and morbo/hypnotoad servers."
sources: ["https://docs.mojolicious.org", "https://metacpan.org/pod/Mojolicious::Guides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mojolicious routes, controllers and server

**Goal:** a small web app and how to run it.

```perl
use Mojolicious::Lite -signatures;
get '/' => sub ($c) { $c->render(text => 'Hello') };
get '/user/:id' => [id => qr/\d+/] => sub ($c) { $c->render(json => { id => $c->param('id') }) };
post '/items' => sub ($c) {
    my $data = $c->req->json or return $c->render(json => { error => 'bad json' }, status => 400);
    $c->render(json => $data, status => 201);
};
helper db => sub ($c) { state $db = connect_db() };
app->secrets(['change-me-and-rotate']);
app->start;
```
```bash
perl app.pl daemon -l http://*:3000        # development server
morbo script/my_app                          # auto-reloading dev server
hypnotoad script/my_app                      # production prefork server (zero-downtime reload by re-running)
mojo generate app MyApp                      # full app layout: lib/, templates/, public/, t/
perl app.pl routes; perl app.pl get /user/5  # introspection and request from CLI
```

## Rules
- Full apps use controllers in `lib/MyApp/Controller/*.pm` and `$r->get('/path')->to('controller#action')` in `startup`.
- Templates (`*.html.ep`, Embedded Perl) escape output by default (`<%= %>` escapes, `<%== %>` does not); layouts in `templates/layouts`.
- `$c->stash`, `$c->session` (signed cookie: needs `secrets`), `$c->flash`, `$c->param`, `$c->render_later` for async.
- Config via `Mojolicious::Plugin::Config` (`my_app.conf`), modes (`MOJO_MODE=production`).
- Behind a reverse proxy set `MOJO_REVERSE_PROXY=1` (or `$app->config(...)`) so the app sees the real client IP and scheme.
- Testing: `use Test::Mojo; my $t = Test::Mojo->new('MyApp'); $t->get_ok('/')->status_is(200)->content_like(qr/Hello/);`
- Never keep the default secret in production; rotate by prepending new secrets.
- Version differences: signatures in apps need Perl 5.20+ with `-signatures`; check the Mojolicious changelog for removals before upgrading.

## Self-check
- [ ] `perl app.pl get /` prints `Hello` and the Test::Mojo test passes.
