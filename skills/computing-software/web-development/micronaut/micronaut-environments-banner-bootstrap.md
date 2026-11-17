---
id: computing-software.web-development.micronaut.micronaut-environments-banner-bootstrap
name: micronaut-environments-banner-bootstrap
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, environments, banner, bootstrap, application-context, distributed-configuration]
level: practitioner
status: docs-checked
description: "Activate Micronaut environments, customize or disable the startup banner, and set up the bootstrap context for distributed configuration."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/environments.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/banner.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/bootstrap.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control which environments are active, the startup banner, and whether a bootstrap context loads configuration before the main context.

## Environments

The `Environment` interface models the application environment; one or many unique names are given when creating the `ApplicationContext`:

```java
ApplicationContext applicationContext = ApplicationContext.run("test", "android");
Environment environment = applicationContext.getEnvironment();

assertTrue(environment.getActiveNames().contains("test"));
assertTrue(environment.getActiveNames().contains("android"));
```

Active names select `application-{environment}.{extension}` files and drive `@Requires` on beans and `@Configuration` packages.

- Inside a Spock or JUnit test the `Environment.TEST` environment is activated automatically.
- Add more at launch with the `micronaut.environments` system property or the `MICRONAUT_ENVIRONMENTS` environment variable (comma-separated):

```bash
java -Dmicronaut.environments=foo,bar -jar myapp.jar
```

- Cloud-environment detection is off by default since Micronaut 4 (see the Cloud Configuration section of the guide).

## Banner

A banner showing the Micronaut version prints at startup (since 2.3, enabled by default). To replace it, create `src/main/resources/micronaut-banner.txt` with plain ASCII art. To disable it:

```java
public class Application {
    public static void main(String[] args) {
        Micronaut.build(args)
                 .banner(false)
                 .start();
    }
}
```

## Bootstrap context

A bootstrap context can be created before the main context to hold the configuration needed to fetch more configuration (typically remote). It is enabled by the first of these that applies, checked in order:

1. The `micronaut.bootstrap.context` system property.
2. The `ApplicationContextBuilder.bootstrapEnvironment` option.
3. A `BootstrapPropertySourceLocator` bean being present (normally from `micronaut-discovery-client`). If you supply a custom `ConfigurationClient`, make sure that dependency is on the classpath.

Bootstrap files (`bootstrap.yml` etc.) are read with the same rules as application configuration, with the prefix `bootstrap` instead of `application`. Change the prefix with the `micronaut.bootstrap.name` system property.

- Bootstrap values carry over to the main context and take precedence over main-context values, so a property needed in both places belongs in the bootstrap configuration.
- A bean can be resolved in the bootstrap context only if annotated `@BootstrapContextCompatible`; annotate every bean that takes part in retrieving distributed configuration.

## Checked
2026-11-07. Checked against the environments, banner and bootstrap pages. Removed the JMX line, which is on a page not cited.

Method: documentation only; no commands were run.
