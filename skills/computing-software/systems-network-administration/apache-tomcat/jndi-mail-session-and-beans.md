---
id: computing-software.systems-network-administration.apache-tomcat.jndi-mail-session-and-beans
name: jndi-mail-session-and-beans
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jndi, jakarta-mail, mail-session, smtp, beanfactory, javabean-resource, mail-smtp-host]
level: practitioner
status: docs-checked
description: "Provide a Jakarta Mail Session and generic JavaBean resources through Tomcat 10.1 JNDI: Context Resource XML, jar placement, BeanFactory behaviour and singleton=false."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/jndi-resources-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mail session and JavaBean resources

Jakarta Mail Session, in `META-INF/context.xml`:
```xml
<Resource name="mail/Session" auth="Container" type="jakarta.mail.Session"
          mail.smtp.host="smtp.example.com"/>
```
plus in web.xml a `<resource-ref>` with `res-ref-name` `mail/Session`, `res-type` `jakarta.mail.Session`, `res-auth` `Container`.
- Extra attributes become properties passed to `Session.getInstance(Properties)`.
- If `password` is set together with `mail.smtp.user` or `mail.user`, an `Authenticator` is added automatically.
- Install `jakarta.mail-api-2.1.0.jar` and an implementation jar in `$CATALINA_HOME/lib`. Do not also put the API jar in the web app's `lib` (error).
- Lookup: `envCtx.lookup("mail/Session")`.

Generic JavaBean (`org.apache.naming.factory.BeanFactory`): any class with a no-arg constructor and `setFoo()` setters.
```xml
<Resource name="bean/MyBeanFactory" auth="Container" type="com.mycompany.MyBean"
          factory="org.apache.naming.factory.BeanFactory" bar="23"/>
```
with `<resource-env-ref>` in web.xml (`resource-env-ref-name` `bean/MyBeanFactory`).
- Strings go straight to setters; primitives and wrappers convert automatically. For other types add a String-taking setter with the same name or lookup fails with `NamingException`.
- A new instance per lookup only with `singleton="false"`. `forceString` was removed.

Custom factory: implement `javax.naming.spi.ObjectFactory`, put classes in `$CATALINA_HOME/lib`, set `factory="com.mycompany.MyBeanFactory"`.

Verify: a servlet sends a test mail, or reads `bean.getBar()` equal to 23.

## Checked

2026-11-04. Read the Tomcat 10.1 JNDI Resources How-To (jndi-resources-howto.html): confirmed the mail/Session Resource and resource-ref pattern, attributes passed to Session.getInstance, the automatic Authenticator rule, jakarta.mail-api-2.1.0.jar in CATALINA_HOME/lib, BeanFactory behaviour (setters, String conversion, NamingException, singleton=false, forceString removed), resource-env-ref and the custom ObjectFactory. Removed the unsupported restart instruction.

Method: documentation only; no commands were run.
