---
id: computing-software.qa-testing-engineering.selenium.virtual-authenticator-webauthn
name: virtual-authenticator-webauthn
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [virtual-authenticator, webauthn, passkeys, credential-testing]
level: practitioner
status: verified
description: "Test WebAuthn/passkey login with Selenium's Virtual Authenticator: options (protocol, transport, resident keys, user verification), adding and reading credentials."
sources:
  - https://www.selenium.dev/documentation/webdriver/interactions/virtual_authenticator/
  - https://www.w3.org/TR/webauthn-2/#sctn-automation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual authenticator for WebAuthn

**Goal:** automate passkey/security-key registration and login without hardware.

```python
from selenium.webdriver.common.virtual_authenticator import VirtualAuthenticatorOptions, Credential

opts = VirtualAuthenticatorOptions()
opts.protocol = VirtualAuthenticatorOptions.Protocol.CTAP2
opts.transport = VirtualAuthenticatorOptions.Transport.INTERNAL   # platform authenticator (passkey)
opts.has_resident_key = True
opts.has_user_verification = True
opts.is_user_verified = True
driver.add_virtual_authenticator(opts)

# Registration via the UI
driver.find_element(By.ID, "register-passkey").click()
creds = driver.get_credentials()
assert len(creds) == 1 and creds[0].is_resident_credential

# Login
driver.find_element(By.ID, "login-passkey").click()
```

## Pre-seeding a credential
```python
cred = Credential.create_resident_credential(id=b"cred-1", rp_id="app.test", user_handle=b"user-1",
                                             private_key=pkcs8_private_key_bytes, sign_count=0)
driver.add_credential(cred)
```
Register the matching public key in the backend fixture so login works without a registration step.

## Scenarios to cover
- `is_user_verified = False` -> server must reject when UV is required.
- Remove credentials (`driver.remove_all_credentials()`) -> "no passkey" path.
- Sign count handling (cloned authenticator detection).
- Transports offered by `VirtualAuthenticatorOptions.Transport` are BLE, INTERNAL, NFC and USB (no cross-device/hybrid transport); protocols are CTAP2 and U2F.

## Gotchas
- Run on Chrome 156 here; other browsers were not tested.
- `rp_id` must match the page's effective domain; `localhost` works (ran), an IP host such as `127.0.0.1` fails with `SecurityError` in the page's `navigator.credentials.create`.
- Remove the authenticator in teardown (`driver.remove_virtual_authenticator()`).

## Verify
Registration then login passes headlessly (ran: register gave 1 resident credential, login worked, sign count rose to 2); the UV-false scenario fails with `NotAllowedError` (ran); a pre-seeded credential made from a `cryptography` P-256 PKCS8 key logged in (ran, the page does not verify the signature).
