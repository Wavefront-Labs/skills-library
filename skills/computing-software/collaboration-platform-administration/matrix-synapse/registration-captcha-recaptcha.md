---
id: computing-software.collaboration-platform-administration.matrix-synapse.registration-captcha-recaptcha
name: registration-captcha-recaptcha
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, captcha, recaptcha, registration, bots, enable-registration-captcha, x-forwarded]
level: practitioner
status: docs-checked
description: "Enable reCAPTCHA v2 checkbox on Synapse registration: key setup, the two config keys, unticking origin verification, and passing the real client IP with x_forwarded."
sources:
  - https://element-hq.github.io/synapse/latest/CAPTCHA_SETUP.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A captcha helps stop bots registering accounts. Synapse uses Google reCAPTCHA, which needs API keys from Google, and only the reCAPTCHA v2 "I'm not a robot" Checkbox type works.

Steps from the docs:

1. Create a site at the reCAPTCHA admin console, choose any label, and select reCAPTCHA v2 with the checkbox option.
2. Add your server's public hostname, as set in `public_baseurl`, to the authorized domains. If `public_baseurl` is unset, use `server_name`.
3. Accept the terms and submit, then copy the site key and secret key into `homeserver.yaml`:

```yaml
recaptcha_public_key: YOUR_SITE_KEY
recaptcha_private_key: YOUR_SECRET_KEY
```

4. Turn the captcha on for new registrations:

```yaml
enable_registration_captcha: true
```

5. In the settings page of the CAPTCHA you just created, untick "Verify the origin of reCAPTCHA solutions" so any client can display it. If you leave it ticked you must list the domain of every client allowed to show the CAPTCHA.

The reCAPTCHA API requires the IP address of the user who solved the challenge. If clients reach Synapse through a proxy or load balancer, the origin IP is the proxy's, so the `X-Forwarded-For` header must be used instead. Enable that with the `x_forwarded` directive on the relevant listener in `homeserver.yaml`; the reverse proxy skill shows where to set it.

## Checked

2026-11-04. Confirmed against the Synapse CAPTCHA setup page: reCAPTCHA v2 checkbox only, authorized domains, key settings, enable_registration_captcha, origin verification checkbox, x_forwarded. Removed a generic closing paragraph.
Method: documentation only; no commands were run.
