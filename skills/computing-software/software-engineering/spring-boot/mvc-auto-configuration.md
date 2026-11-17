---
id: computing-software.software-engineering.spring-boot.mvc-auto-configuration
name: mvc-auto-configuration
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, spring-mvc, webmvcconfigurer, enablewebmvc, httpmessageconverters, conversion-service, webmvcregistrations]
level: practitioner
status: docs-checked
description: "What Spring MVC auto-configuration adds, extending it with WebMvcConfigurer or WebMvcRegistrations, taking full control with @EnableWebMvc, converters and formats."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot auto-configures Spring MVC, replacing the need for `@EnableWebMvc` (the two cannot be used together). Beyond MVC defaults it adds: `ContentNegotiatingViewResolver` and `BeanNameViewResolver` beans, static resources including WebJars, automatic registration of `Converter`, `GenericConverter` and `Formatter` beans, `HttpMessageConverters` support, `MessageCodesResolver`, static `index.html`, and use of a `ConfigurableWebBindingInitializer` bean if you define one.

Extend while keeping Boot's customizations: add a `@Configuration` class implementing `WebMvcConfigurer` without `@EnableWebMvc` (interceptors, formatters, view controllers). To supply custom `RequestMappingHandlerMapping`, `RequestMappingHandlerAdapter` or `ExceptionHandlerExceptionResolver`, declare a `WebMvcRegistrations` bean; instances still get further configuration, and a `WebMvcConfigurer` can override it. For total control, add a `@Configuration` with `@EnableWebMvc` (or a `DelegatingWebMvcConfiguration`).

Conversion service: MVC uses a different `ConversionService` than property binding. `Period`, `Duration` and `DataSize` converters are unavailable and `@DurationUnit` / `@DataSizeUnit` are ignored. Customize through a `WebMvcConfigurer.addFormatters` method (can delegate to `ApplicationConversionService` statics) or `spring.mvc.format.date`, `.time`, `.date-time` (defaults `ofLocalizedDate/Time/DateTime(FormatStyle.SHORT)`).

HTTP message converters: JSON via Jackson, XML via the Jackson XML extension if available, otherwise JAXB; strings are UTF-8. Any `HttpMessageConverter` bean is added, and defaults can be overridden. Declare `ClientHttpMessageConvertersCustomizer` or `ServerHttpMessageConvertersCustomizer` beans to add converters before the defaults (`addCustomConverter`) or replace a default (`withJsonConverter`).

Message codes: set `spring.mvc.message-codes-resolver-format` to `PREFIX_ERROR_CODE` or `POSTFIX_ERROR_CODE` for Boot to create a `MessageCodesResolver`.

Functional style (WebMvc.fn): define any number of `RouterFunction` beans; they can be ordered for precedence.

## Checked

2026-11-07. Read web/servlet.html (Spring MVC Auto-configuration, HttpMessageConverters) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Reworded the XML converter line to say the Jackson XML extension is used if available, otherwise JAXB, as the page states. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
