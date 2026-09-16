# EMOSA — EasyMesh OVSDB Adapter

![EMOSA — エモさ — Emotional resonance: a Japanese riverside at sunset](assets/emosa-banner.png)

EMOSA is an evaluation platform for exploring whether a controller-side adaptation layer can make **unchanged OpenSync pods work seamlessly with an EasyMesh controller**.

The goal is to demonstrate what works, expose compatibility gaps, and provide repeatable experiments with clear visibility into protocol exchanges, configuration changes, and actual device behavior.

The name also echoes **エモさ (*emosa*)**, a Japanese expression for emotional resonance, often with a nostalgic feeling. The banner illustrates this wordplay; see [Sanseido's explanation of エモい (*emoi*)](https://dictionary.sanseido-publ.co.jp/topic/shingo2016/2016Best10.html), from which エモさ is formed.

## Architecture

```text
EasyMesh controller
        │ Real IEEE 1905 / EasyMesh messages
        ▼
EMOSA virtual agent + OVSDB adapter
        │ Existing OVSDB management interface
        ▼
Unchanged OpenSync pods
```

All adaptation runs in the controller environment. Pods require no firmware changes or additional software; configuration uses their existing authorized management interfaces. EasyMesh procedures terminate at EMOSA's virtual agents, while the physical pods remain OpenSync devices.

## Planned evaluation capabilities

- Real EasyMesh message handling and translation into supported OpenSync operations.
- Physical-pod testing over wired and wireless management paths.
- Deterministic simulations and an optional backend using selected OpenSync core components.
- Configurable scenarios, fault injection, repeatable runs, and result comparisons.
- Live status and correlated evidence across EasyMesh messages, OVSDB transactions, pod state, and independent Wi-Fi client checks.
- Evaluation with independent EasyMesh controllers.

Success is assessed per procedure, controller version, and pod firmware. Unsupported behavior and negative results are part of the evaluation; full EasyMesh interoperability or certification is not assumed.

## Implementation direction

- **Language:** Python for the controller tools and adapter.
- **Reference lab:** an LXD VM with Ubuntu LXD containers.
- **Initial device target:** existing OpenSync 6.6.0 pods.
- **Dependencies:** no prplMesh build-time or runtime dependency in EMOSA.

The first milestone is one supported provisioning flow to an existing BSS, followed by a failure-and-recovery experiment, with independently verifiable results.

## Status

**Design stage.** Implementation, protocol compatibility, and hardware behavior have not yet been validated. This repository is intended to develop and evaluate the adaptation approach, with production suitability assessed from the resulting evidence.
