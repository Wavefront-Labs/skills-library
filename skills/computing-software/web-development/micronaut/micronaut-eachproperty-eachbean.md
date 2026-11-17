---
id: computing-software.web-development.micronaut.micronaut-eachproperty-eachbean
name: micronaut-eachproperty-eachbean
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, eachproperty, eachbean, named-beans, multiple-configurations, list-binding]
level: practitioner
status: docs-checked
description: "Create one configuration bean per sub-property with @EachProperty and one dependent bean per config with @EachBean, including list-based binding."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/eachProperty.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/eachBean.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define several named instances of a configuration (for example data sources) and a bean built from each.

## @EachProperty

Creates a `ConfigurationProperties` bean for each sub-property under the given name. The sub-property key becomes the bean name and qualifier, injected with `@Parameter`:

```java
@EachProperty("test.datasource")
public class DataSourceConfiguration {

    private final String name;
    private URI url = new URI("localhost");

    public DataSourceConfiguration(@Parameter String name) throws URISyntaxException {
        this.name = name;
    }
    public String getName() { return name; }
    public URI getUrl() { return url; }
    public void setUrl(URI url) { this.url = url; }
}
```

Configuration:

```java
ApplicationContext applicationContext = ApplicationContext.run(PropertySource.of(
        "test",
        CollectionUtils.mapOf(
        "test.datasource.one.url", "jdbc:mysql://localhost/one",
        "test.datasource.two.url", "jdbc:mysql://localhost/two")
));
```

Look up:

```java
Collection<DataSourceConfiguration> beansOfType = applicationContext.getBeansOfType(DataSourceConfiguration.class); // 2 beans
DataSourceConfiguration firstConfig = applicationContext.getBean(
        DataSourceConfiguration.class, Qualifiers.byName("one"));
```

Gotcha: config names are kebab-case: `@EachProperty("my-bean")` works, `@EachProperty("myBean")` fails.

## List-based binding

By default binding is map style (key = bean name). Set `list = true` to bind from a list; the index is passed with `@Parameter`, and implementing `Ordered` preserves order when retrieving:

```java
@EachProperty(value = "ratelimits", list = true)
public class RateLimitsConfiguration implements Ordered {
    private final Integer index;
    private Duration period;
    private Integer limit;

    RateLimitsConfiguration(@Parameter Integer index) { this.index = index; }

    @Override
    public int getOrder() { return index; }
    // getters and setters for period and limit
}
```

## @EachBean

Builds another bean for every bean of the given type, usually from a `@Factory`:

```java
@Factory
public class DataSourceFactory {

    @EachBean(DataSourceConfiguration.class)
    DataSource dataSource(DataSourceConfiguration configuration) {
        URI url = configuration.getUrl();
        return new DataSource(url);
    }
}
```

The parent bean must carry a `@Named` qualifier (as `@EachProperty` beans do), because each created bean inherits it. Pick one with `applicationContext.getBean(DataSource.class, Qualifiers.byName("one"))`; `getBeansOfType(DataSource.class)` returns both.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
