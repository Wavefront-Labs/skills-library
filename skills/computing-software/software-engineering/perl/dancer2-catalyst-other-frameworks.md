---
id: computing-software.software-engineering.perl.dancer2-catalyst-other-frameworks
name: dancer2-catalyst-other-frameworks
category: computing-software
field: software-engineering
product: perl
tags: [perl, dancer2, catalyst, framework-choice, web-app-structure, dancer2-plugin, dancer2-catalyst-other-frameworks]
level: advanced
status: draft
description: "Create apps with Dancer2 (route DSL on PSGI) or Catalyst (MVC), and choose among Mojolicious, Dancer2, Catalyst and Web::Simple."
sources: ["https://metacpan.org/pod/Dancer2", "https://metacpan.org/pod/Dancer2::Manual", "https://metacpan.org/pod/Catalyst::Manual"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dancer2, Catalyst and choosing a framework

**Goal:** pick and start a framework quickly.

## Dancer2
```bash
dancer2 gen -a MyApp         # skeleton; run with: plackup -r bin/app.psgi
```
```perl
package MyApp;
use Dancer2;
get '/' => sub { template 'index' => { title => 'Home' } };
get '/user/:id' => sub { my $id = route_parameters->get('id'); return to_json({ id => $id }) };   # or: content_type 'application/json'
post '/save' => sub { my $data = body_parameters->get('name'); redirect '/'; };
hook before => sub { ... };
true;
```
Config in `config.yml` and `environments/*.yml`; plugins like `Dancer2::Plugin::Database`, `Dancer2::Plugin::DBIC`, `Dancer2::Session::*`. Dancer2 runs on PSGI so any Plack server works.

## Catalyst
```bash
catalyst.pl MyApp           # creates the MVC skeleton (lib/MyApp/Controller, Model, View, root/)
script/myapp_server.pl -r   # restart on change
```
```perl
package MyApp::Controller::Root;
use Moose; use namespace::autoclean; BEGIN { extends 'Catalyst::Controller' }
sub index :Path :Args(0) { my ($self, $c) = @_; $c->stash(template => 'index.tt'); }
sub item :Local :Args(1) { my ($self, $c, $id) = @_; $c->response->body("item $id"); }
sub end :ActionClass('RenderView') {}
```
Catalyst is full-stack and mature (models, views, authentication plugins); its attribute-based dispatch has a learning curve.

## Choosing
| Need | Pick |
|---|---|
| async, WebSocket, all-in-one, active development | Mojolicious |
| minimal route DSL, PSGI ecosystem | Dancer2 |
| large existing MVC apps, plugin ecosystem | Catalyst |
| tiny services | Web::Simple or bare PSGI |

## Rules
- Do not mix framework session/auth systems; use the framework's secret management.
- Escape output in templates; Template Toolkit auto-escape is off by default (use `| html`), see the templating skill.
- CGI.pm was removed from the core distribution in Perl 5.22; legacy CGI scripts need `CGI` installed from CPAN or a PSGI wrapper (`CGI::Emulate::PSGI`, `Plack::App::WrapCGI`).

## Self-check
- [ ] `plackup` serves the skeleton and `curl /` returns HTML.
