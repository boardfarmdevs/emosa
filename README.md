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

## Status and quick start

The Python foundation and direct semantic component evaluation are implemented.
The real OVSDB simulator uses the pinned OpenSync schema and a separate manager
process. Wire provisioning, physical-pod mapping and independent-controller
acceptance remain gated; simulator passes do not establish interoperability.

```sh
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run pytest -m unit
bash scripts/build-ovsdb.sh
uv run pytest -m ovsdb
uv run emosa-lab run scenarios/component-bss-change.json --backend ovsdb-sim
uv run emosa-lab run scenarios/component-lost-reply.json --backend ovsdb-sim
uv run emosa-lab report RUN_ID --format json
uv run emosa-lab watch RUN_ID
uv run emosa-lab inspect RUN_ID --operation OPERATION_ID
uv run emosa-lab compare RUN_A RUN_B --format html
```

`--backend model` runs deterministic model scenarios without OVSDB binaries or
privileged resources. Each run retains its journal, effective inputs, redacted
observations, HTML/Markdown timeline and artifact hashes under `.lab/runs/`.
Fault scenarios cover conflicts, partial/withheld application, lost responses,
controller/server restart and multi-pod isolation. `--ssid`, `--seed`, `--repeat`
and `--apply-seconds` create parameterized reruns with new identities.

`scenarios/provision-one-bss.json` and `scenarios/lost-reply.json` explicitly
require genuine EasyMesh provisioning. They currently produce blocked reports,
exit 5, and perform no semantic fallback. `pytest -m wire`, `-m hardware` or
`-m external` fails explicitly at its missing gate instead of reporting success
with no applicable tests. Default CI runs unit and OVSDB component suites only.

Prepare actual pod evidence without changing it using
[read-only qualification](docs/pod-qualification.md). Review
[deployment](deploy/README.md), [mapping scope](docs/operation-mappings.md),
[dependency/R0 findings](docs/dependency-qualification.md),
[open inputs](docs/open-inputs.md), and [traceability](docs/traceability.json).
The Ubuntu 24.04 LXD reference layout has scripts and pinned candidate image
fingerprints; runtime/package qualification and retained VM exports are pending.
