---
id: computing-software.game-programming.unity.collision-and-trigger-callbacks
name: collision-and-trigger-callbacks
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, oncollisionenter, ontriggerenter, collision-callbacks, triggers, contact-points, game-programming]
level: practitioner
status: docs-checked
description: "When Unity fires OnCollision and OnTrigger events: collision vs trigger conditions, non-kinematic Rigidbody note, Collision data, disabled MonoBehaviours, and the 2D equivalents."
sources: ["https://docs.unity3d.com/Manual/collider-interactions-other-events.html", "https://docs.unity3d.com/ScriptReference/Collider.OnCollisionEnter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collision and trigger callbacks

**Goal:** know which Unity collider events fire, and what the documentation guarantees about them.

## Two event types (Manual)
- **Collision events**: two colliders make contact and neither has Is Trigger enabled. Common functions:
  `Collider.OnCollisionEnter`, `OnCollisionStay`, `OnCollisionExit`.
- **Trigger events**: two colliders make contact, at least one has Is Trigger enabled, and at least one
  has a Rigidbody or ArticulationBody. Common functions: `Collider.OnTriggerEnter`, `OnTriggerStay`,
  `OnTriggerExit`.
- A collider with Is Trigger enabled does not physically collide; it creates a space that sends an event
  when other colliders pass through.
- Collider events need configuration via C# script; they cannot be set up with the UI alone.
- The 2D physics system has equivalents with `2D` appended (for example `OnCollisionEnter2D`); details
  are in the `MonoBehaviour` API docs (not opened).

## OnCollisionEnter(Collision other)
- Called when this collider/rigidbody has begun touching another rigidbody/collider.
- Unlike `OnTriggerEnter`, it is passed the `Collision` class, not a `Collider`. `Collision` contains
  information such as contact points and impact velocity.
- Collision events are only sent if one of the colliders also has a non-kinematic rigidbody attached.
- Collision events are sent to disabled MonoBehaviours, so you can enable Behaviours in response.
- Page example: loop `collision.contacts` drawing `Debug.DrawRay(contact.point, contact.normal, ...)`,
  and play an AudioSource when `collision.relativeVelocity.magnitude > 2`.

## Checked
Date: 2026-11-07

Read in full: the Manual page "Use collisions to trigger other events" and the `OnCollisionEnter`
reference page. The `OnTriggerEnter`, `Collision` and `ContactPoint` pages and the 2D docs were not
opened.

Removed because the pages do not confirm it: the "at least one of the pair must have a Rigidbody
(kinematic counts)" rule for triggers (the page says Rigidbody or ArticulationBody, kinematic status
not stated), kinematic pair settings (Contact Pairs Mode), the Layer Collision Matrix, delivery to the
Rigidbody's GameObject, `GetContacts`, `impulse`, Reuse Collision Callbacks, Stay-callback cost advice,
`attachedRigidbody` trigger sample, the silent failure checklist (signature typos, teleporting,
OnTriggerExit on disable, tunnelling) and the Verify list.

Method: documentation only; no commands were run.
