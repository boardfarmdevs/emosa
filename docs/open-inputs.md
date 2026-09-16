# Open input gates

| Gate | Missing input | Affected work | Independent work |
| --- | --- | --- | --- |
| P0 | Full IEEE 1905.1-2013/1905.1a-2014 and applicable 802.11-2024 text; final profile selection, complete rule matrix and independent vectors. EasyMesh 6.1 and WPS 2.0.10 were obtained from their publisher. | I3, I4, wire tests/provisioning | I0–I2, component evaluation |
| M0 | Named pod/build, actual schema, endpoint direction/trust, managed radio/VIF, writer evidence, management/recovery and client profile | I5 and hardware writes | Simulators, package, reports |
| X1 | The prplMesh candidate now starts and sends discovery to the EMOSA container; actual EMOSA exchanges, profile/BSS policy and shutdown/recovery remain unqualified | I7 | [Peer baseline and startup commands](../deploy/peer/README.md) |
| LXD | Ubuntu 24.04 component tests and VM-driven scenarios passed; base image export retained. Final runtime images and clean full-procedure reruns remain pending | Full reference deployment acceptance | Component and peer baselines now exercised in the dedicated VM |

`qualified` requires referenced evidence and compatible current configuration.
No boolean in an input manifest enables hardware writes. The upstream schema is
a simulation reference. Complete protocol frames remain pending; the separately
selected [WSC cryptographic component](wsc-component.md) has synthetic payload
vectors independently checked with hostap 2.11.

The user confirmed that no specification editions or actual pod profile have yet
been selected/supplied. See [the proposed corpus and access details](protocol-inputs.md).
The read-only collector in [pod-qualification.md](pod-qualification.md) can produce
a draft once real connection inputs arrive. Existing direct access and the ability
to disable/redirect cloud writers are confirmed intentions, not verified lab setup.
The operator explicitly confirmed that **no private connection configuration has
been provided or created**. Credentials-free TLS, tunnel and Unix examples are
available; populate the selected copy outside this repository on the EMOSA
machine, then provide only its absolute path. Physical connection stays pending.

R0 stopped at missing `protoc-c` after isolated Python build dependencies and the
local OVSDB tools were supplied. Its native container, further C dependencies and
driver harness remain unqualified; see the preserved build evidence.
