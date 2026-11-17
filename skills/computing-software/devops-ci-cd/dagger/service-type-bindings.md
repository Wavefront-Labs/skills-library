---
id: computing-software.devops-ci-cd.dagger.service-type-bindings
name: service-type-bindings
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, service, service-binding, ports, endpoint, integration-testing]
level: practitioner
status: docs-checked
description: "Create Dagger Services from containers, bind them to other containers by alias, expose them to the host with up, reach host services, and run tests against a database."
sources: [https://docs.dagger.io/0.21/getting-started/types/service]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger Service type and bindings (Dagger 0.21 docs)

Goal: run a TCP service (web server, database) alongside a workflow. A `Service` has `endpoint`, `hostname`, `ports` and `up` (tunnel from the caller's network).

## Create and bind

```go
func (m *MyModule) HttpService() *dagger.Service {
	return dag.Container().
		From("python").
		WithWorkdir("/srv").
		WithNewFile("index.html", "Hello, world!").
		WithExposedPort(8080).
		AsService(dagger.ContainerAsServiceOpts{Args: []string{"python", "-m", "http.server", "8080"}})
}

func (m *MyModule) Get(ctx context.Context) (string, error) {
	return dag.Container().
		From("alpine").
		WithServiceBinding("www", m.HttpService()).
		WithExec([]string{"wget", "-O-", "http://www:8080"}).
		Stdout(ctx)
}
```

`dagger call get`. The binding alias (`www`) becomes the hostname.

## Expose to the host

```shell
dagger call http-service up
curl localhost:8080
dagger call http-service up --ports 9000:8080
curl localhost:9000
```

## Use a host service in a function

Accept `svc *dagger.Service`, bind it (`WithServiceBinding("db", svc)`), and call `dagger call user-list --svc=tcp://localhost:3306`. The service must already be listening on the host, outside Dagger.

## Start manually and read the endpoint

```go
service, err := dag.Container().From("nginx").WithExposedPort(80).AsService().Start(ctx)
endpoint, err := service.Endpoint(ctx, dagger.ServiceEndpointOpts{Scheme: "http", Port: 80})
return dag.HTTP(endpoint).Contents(ctx)
```

## Transient service for tests

Start MariaDB with `WithEnvVariable("MARIADB_USER", ...)` and others, `WithExposedPort(3306)`, `AsService(dagger.ContainerAsServiceOpts{UseEntrypoint: true})`. Bind into the app container as `db`, set `SIMPLETEST_DB=mysql://user:password@db/drupal`, then run PHPUnit kernel tests via `WithExec`. The docs example uses Drupal `drupal:10.0.7-php8.2-fpm` and `mariadb:10.11.2`.

Related: computing-software.devops-ci-cd.dagger.container-type-and-caching.

## Checked

2026-11-07

Read getting-started/types/service.mdx in full (live slug /getting-started/types/service matches the cited URL). The page only imports partials, so I also read partials/types/_service.mdx and the five cookbook service partials (_use-service, _expose-service-to-host, _expose-host-service-to-function, _use-service-endpoints, _create-service-for-test), plus the five Go snippets they embed (bind-services, expose-dagger-services-to-host, expose-host-services-to-dagger, use-endpoint, test-against-db-service); the Python, TypeScript and PHP tabs were not opened. Confirmed the Service fields, WithServiceBinding with the www alias, up and --ports 9000:8080 with the curl checks, the host service example and its note that the service must already be listening, the manual Start and Endpoint example, and the MariaDB/Drupal test example including SIMPLETEST_DB and the image tags. No corrections needed.

Method: documentation only; no commands were run.
