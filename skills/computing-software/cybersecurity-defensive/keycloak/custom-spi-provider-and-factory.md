---
id: computing-software.cybersecurity-defensive.keycloak.custom-spi-provider-and-factory
name: custom-spi-provider-and-factory
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, spi, provider-factory, java, service-loader]
level: practitioner
status: docs-checked
description: "Implement a Keycloak SPI with a ProviderFactory, Provider and META-INF/services file, and configure it with --spi options."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/providers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom spi provider and factory
To implement a Keycloak SPI you implement its `ProviderFactory` and `Provider` interfaces and create a service configuration file. Example for the Theme Selector SPI:

Factory (Keycloak creates a single instance, so it can keep state across requests):
```java
public class MyThemeSelectorProviderFactory implements ThemeSelectorProviderFactory {
    public ThemeSelectorProvider create(KeycloakSession session) { return new MyThemeSelectorProvider(session); }
    public void init(Config.Scope config) { String themeName = config.get("theme"); }
    public void postInit(KeycloakSessionFactory factory) {}
    public void close() {}
    public String getId() { return "myThemeSelector"; }
}
```
Provider instances are created per request by `create`, so keep them light-weight. The service file `META-INF/services/org.keycloak.theme.ThemeSelectorProviderFactory` contains the factory class name.

Configure at start (the docs example maps `myThemeSelector` to `my-theme-selector` in option names):
```
bin/kc.sh --spi-theme-selector--my-theme-selector--enabled=true --spi-theme-selector--my-theme-selector--theme=my-theme
```
Return a unique id from `getId()`; the exception is overriding a built-in provider that must keep its id (for example `OIDCLoginProtocolFactory` keeps `openid-connect`): give your implementation a higher `order()` than the built-in one, and only the highest order is used.

Deploy: copy the JAR (and any extra dependencies) to the providers directory, then run `kc.sh build` or a non-optimized start. Provider JARs are not loaded in isolated classloaders, so do not include classes or resources that conflict with built-in ones. A provider can be disabled with `--spi-<spi>--<provider>--enabled=false` on a build, for example `--spi-user-cache--infinispan--enabled=false`.

## Checked
2026-11-03. Confirmed against server_development/topics/providers.adoc. Removed: the generic option-name template presented as a rule, the "review third-party JARs" and "revalidate on every upgrade" gotchas, and the log-based Verify step (none on the page).
Method: documentation only; no commands were run.
