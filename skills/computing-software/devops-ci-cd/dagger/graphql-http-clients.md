---
id: computing-software.devops-ci-cd.dagger.graphql-http-clients
name: graphql-http-clients
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, graphql, http, curl, dagger-query, rust, php]
level: practitioner
status: docs-checked
description: "Call the Dagger API over raw GraphQL HTTP with curl, Rust, PHP or dagger query, using the session port and basic-auth token that dagger run provides."
sources: [https://docs.dagger.io/0.21/getting-started/api/http]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger API over HTTP and GraphQL (Dagger 0.21 docs)

Goal: send GraphQL queries to the Dagger Engine from a shell or a non-SDK language. This is optional; SDKs and the CLI are the normal route.

## Endpoint and auth

- Every Dagger session has a local endpoint: `http://127.0.0.1:$DAGGER_SESSION_PORT/query`.
- Auth is HTTP Basic with `DAGGER_SESSION_TOKEN` as the user and an empty password. Treat the token as a credential.
- The page runs every client under `dagger run`, which initializes or reuses a local Dagger Engine and executes the command against it.

## curl

```shell
echo '{"query":"{
  container {
    from(address:\"alpine:latest\") {
      file(path:\"/etc/os-release\") {
        contents
      }
    }
  }
}"}'|   dagger run sh -c 'curl -s \
    -u $DAGGER_SESSION_TOKEN: \
    -H "content-type:application/json" \
    -d @- \
    http://127.0.0.1:$DAGGER_SESSION_PORT/query'
```

## Language clients

Rust uses `gql_client` (setup: `cargo init`, then separate `cargo add` for `gql_client@1.0.7`, `serde_json@1.0.125`, `tokio@1.39.3 -F full`, `base64@0.22.1`). PHP uses `composer require gmostafa/php-graphql-client`.

PHP core of `client.php`: read `DAGGER_SESSION_PORT` and `DAGGER_SESSION_TOKEN` from the environment, then

```php
$client = new Client(
  'http://127.0.0.1:' . $sessionPort . '/query',
  ['Authorization' => 'Basic ' . base64_encode($sessionToken . ':')]
);
$results = $client->runRawQuery($query);
print_r($results->getData()->container->from->withExec->stdout);
```

with query `container { from (address: "alpine:latest") { withExec(args:["uname", "-nrio"]) { stdout } } }`. The Rust version builds the same header (`authorization: Basic base64(token:)`) with `Client::new_with_headers`. Run with `dagger run cargo run` or `dagger run php client.php`.

## dagger query

`dagger query` sends raw GraphQL from stdin. The page's `build.sh` does two queries: the first returns a content-addressed directory id (`git(url:...){ branch(name:"master"){ tree{ id }}}`, extracted with `jq -r .git.branch.tree.id`); the second interpolates that id into `withDirectory(path:"/src", directory:"$source")`, sets `withWorkdir(path:"/src/hello")`, runs `withExec(args:["go","build","-o","dagger-builds-hello","."])` in `golang:latest` and calls `file(...){ export(path:"./dagger-builds-hello") }`. Then `chmod +x ./build.sh && ./build.sh`.

## Gaps

The page does not document API schema details beyond these examples; see the API reference for fields.

## Checked

2026-11-07

Read getting-started/api/clients-http.mdx in full (live slug /getting-started/api/http; the old .../clients-http URL returned 404, fixed in sources) and all three embedded snippet files (build.sh, client.php, main.rs). Confirmed the session endpoint and DAGGER_SESSION_PORT, the Basic-auth token warning, the curl example, the pinned cargo add versions, the composer package name, the PHP and Rust header construction, the run commands and the dagger query build.sh flow. Corrections: the claim that the variables exist only inside a session was replaced by what the page states about dagger run; the build.sh description now includes the withWorkdir step that the snippet contains.

Method: documentation only; no commands were run.
