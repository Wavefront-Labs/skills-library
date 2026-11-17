---
id: computing-software.software-engineering.quarkus.quarkus-qute-checked-templates
name: quarkus-qute-checked-templates
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, qute, templates, type-safe, checked-template, java]
level: practitioner
status: docs-checked
description: "Define build-time validated Qute templates in Quarkus with parameter declarations, @CheckedTemplate classes, template records, fragments and path customization."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/qute-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type-safe Qute templates in Quarkus

Qute checks expressions at build time when it knows the Java type behind the first part of an expression. A bad expression fails the build.

## Option 1: parameter declaration in the template

Bind a type to a name at the top of the template. Use fully qualified names (only `java.lang` types may drop the package).

```html
{@org.acme.Foo foo}
{@java.util.List<String> strings}
{@String name="Quarkus"}
<h1>{foo.message.toLowerCase}</h1>
```

- Wildcards are ignored; only the bound is used.
- `{@int age=10}`: the default after `=` is used when the key is `null` or not found. Its type must be assignable to the declared type (`{@org.acme.Foo foo=1}` fails the build).
- A section can shadow the name: inside `{#for foo in baz.foos}` the loop alias is not validated against the declaration.
- Avoid `{#with}` in type-safe templates; it blocks validation. Use `{#let it=item.parent}` instead.

## Option 2: @CheckedTemplate class

Annotate a class with `@io.quarkus.qute.CheckedTemplate`; each `static native` method returning `TemplateInstance` is a template. Parameters become parameter declarations.

```java
@Path("item")
public class ItemResource {
    @CheckedTemplate
    public static class Templates {
        public static native TemplateInstance item(Item item);
    }
    @GET @Path("{id}") @Produces(MediaType.TEXT_HTML)
    public TemplateInstance get(Integer id) {
        return Templates.item(service.findItem(id));
    }
}
```

A nested class uses `templates/ItemResource/item.html`; a top-level class uses `templates/hello.txt` style paths. Only type-safe expressions are allowed by default; relax with `@CheckedTemplate(requireTypeSafeExpressions = false)`.

## Option 3: template record

```java
record Hello(String name) implements TemplateInstance {}
```

Located at `templates/HelloResource/Hello.html` when nested in `HelloResource`. A record without `@CheckedTemplate` is treated as default `@CheckedTemplate`.

## Details

- Names come from `-parameters` metadata; use `@CheckedTemplateParam("name")` on a parameter or record component to set the name explicitly (must be a valid Java identifier).
- Path: `@CheckedTemplate(basePath = "items", defaultName = CheckedTemplate.HYPHENATED_ELEMENT_NAME)` turns `itemAndOrder` into `items/item-and-order`.
- Type-safe fragment: a method or record whose name contains `$`, e.g. `static native TemplateInstance items$item(Item item);` The part after the last `$` is the `{#fragment id=item}` identifier; fragment parameters are validated. `ignoreFragments=true` disables this.
- `@TemplateContents("Hello {name}!")` on a method or record supplies the template text in Java.
- Global variables (`@TemplateGlobal`) are overridden automatically by a type-safe template parameter of the same name.

## Checked

2026-11-07. Matched against the text (with includes) of: qute-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
