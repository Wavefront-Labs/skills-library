---
id: computing-software.devops-ci-cd.dagger.services-ephemeral
name: services-ephemeral
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, services, service-container, as-service, networking, integration-testing, mariadb]
level: practitioner
status: docs-checked
description: "Use Dagger ephemeral service containers: return an HTTP service to the host, bind a host database service into a function, and run built images with as-service."
sources: [https://docs.dagger.io/0.21/features/services, https://docs.dagger.io/0.21/getting-started/quickstarts/ci]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral services in Dagger

Goal: run databases, test targets or sidecars as containers during a workflow (Dagger 0.21 docs).

## Characteristics

Service containers have a canonical content-addressed hostname and optional exposed ports; they are started just-in-time, de-duplicated, stopped when no longer needed, and health checked before clients run. Typical uses: a database for tests, end-to-end integration tests, sidecars. Directions supported: container-to-container, container-to-host, host-to-container.

## Return a service to the host (Go)

```go
func (m *MyModule) HttpService() *dagger.Service {
	return dag.Container().
		From("python").
		WithWorkdir("/srv").
		WithNewFile("index.html", "Hello, world!").
		WithExposedPort(8080).
		AsService(dagger.ContainerAsServiceOpts{Args: []string{"python", "-m", "http.server", "8080"}})
}
```

## Use a service from a function (host service in)

Accept a `*dagger.Service` argument and bind it under a hostname:
```go
func (m *MyModule) UserList(ctx context.Context, svc *dagger.Service) (string, error) {
	return dag.Container().
		From("mariadb:10.11.2").
		WithServiceBinding("db", svc).
		WithExec([]string{"/usr/bin/mysql", "--user=root", "--password=secret", "--host=db", "-e", "SELECT Host, User FROM mysql.user"}).
		Stdout(ctx)
}
```
The container reaches the service at host `db`.

## Run a built image locally

From the CI quickstart, in Dagger Shell:
```shell
build | as-service | up --ports=8080:80
```
By default each exposed container port maps to the same host port; `--ports 8080:80` remaps. The quickstart calls this similar to Docker Compose, except that you use code instead of YAML.

The page's "Learn more" list names further topics (services as arguments, create and return services, expose host services, start and stop, persist state) but has no content for them.

Related: `computing-software.devops-ci-cd.dagger.ci-workflow-quickstart`.

## Checked

2026-11-07

Read introduction/features/services.mdx (live slug /features/services; the cited /introduction/features/services URL is a file path that 404s, fixed in sources) and getting-started/quickstarts/ci/index.mdx (live slug /getting-started/quickstarts/ci, trailing slash removed in sources) in full, plus the Go services-1 and services-2 snippets (Python, TypeScript, PHP and Java tabs, the videos and the CI quickstart code snippets were not opened). Confirmed the service container characteristics, the three networking directions, the use cases, the HttpService and UserList Go examples, the as-service and up --ports=8080:80 command with the default same-port mapping, and that the Learn more list is bare placeholders. Replaced the unqualified Docker Compose analogue claim with the quickstart's own wording.

Method: documentation only; no commands were run.
