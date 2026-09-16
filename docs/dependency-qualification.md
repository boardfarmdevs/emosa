# Dependency qualification

The recorded development host is Ubuntu 22.04.5 x86-64, with CPython 3.13.7,
uv 0.11.17 and LXD client/server 6.9. The pinned Ubuntu 24.04 image fingerprints
in `deploy/images.lock.json` were resolved from the Ubuntu LXD remote. The later
[dedicated-VM evidence](evidence/peer/qualification-summary.json) records Ubuntu
24.04 component runtime compatibility, installed packages and a retained base
image export. Final runtime image exports and full procedure reruns remain
pending. Only the project-owned `emosa-lab` VM and its inner containers were
configured for this experiment.

## Open vSwitch experiment

The maintained upstream `ovs==4.0.0` Python package is used for JSON-RPC,
connections, echo, reconnect and OVSDB datum/schema validation. One bounded
worker per session isolates its synchronous interface. No alternative client or
custom full OVSDB protocol stack was needed. See the upstream
[OVSDB connection documentation](https://docs.openvswitch.org/en/stable/ref/ovsdb.7/)
and [RFC 7047](https://www.rfc-editor.org/rfc/rfc7047.html).

The locally built `ovsdb-server` and `ovsdb-tool` are version 4.0.0. Source archive
and binary digests are in `docs/evidence/bootstrap.json`. Building just these
targets first requires the upstream `BUILT_SOURCES`; the supplied build script
generates them before linking. There is no `make install`, system daemon or
switching datapath. TLS is disabled in this **simulation-only** binary build.

The integration suite checks schema retrieval, initial monitor snapshots,
incremental update/delete/reference handling, set/map/optional values, guarded
transactions, row counts, reconnect, independent manager application, lost
responses, conflicts, resource exhaustion and four independent sessions.
Both dialing via Unix sockets and database-initiated TCP to a listening manager
are exercised. Two narrow upstream compatibility accommodations are required:

- Python `PassiveStream` interprets `ptcp:HOST:PORT`, unlike the C client's
  `ptcp:PORT:HOST`. The public session configuration retains the latter syntax;
  its adapter converts to the Python form.
- Python 4.0.0 creates a blocking TCP listening socket. The wrapper makes that
  socket nonblocking immediately after creation, preserving the documented
  nonblocking accept behavior and preventing a worker from stalling.

These workarounds live in `src/emosa/opensync/session.py`, with a real
listening-manager regression test. No files in the installed dependency are
patched. Application/connection generations are independent of reusable wire
request IDs; the durable attempt ID is assigned before submission.

The measured schema response was 131,161 decoded JSON bytes for the selected
server build; snapshots depend on cardinality and enabled columns. The initial
16 MiB parser admission/decoded-message budget and 10,000-row cache bound are
engineering resource limits, **not** OpenSync or EasyMesh protocol limits.
Exhaustion marks the observation cache unready and forces full resynchronization.
Larger physical schemas/snapshots and authenticated TLS remain unqualified.

## Provisioning crypto

The separately scoped [WSC component](wsc-component.md) selects WPS 2.0.10 and
pins `cryptography==50.0.1` for DH group 5 and AES-CBC. CPython's standard
library supplies SHA-256, HMAC and randomness. The group-5 exchange, KDF,
authentication tags and encrypted settings match two independently generated
hostap 2.11 cases. Negative tests cover malformed TLVs, nonce/MAC binding,
out-of-range/nonmember public keys, altered tags, IV/ciphertext and padding.

[Cryptography 50.0.1](https://cryptography.io/en/50.0.1/hazmat/primitives/asymmetric/dh/)
still supports finite-field DH but deprecates it for removal in a future release.
WPS requires this group; silently substituting ECDH would change the protocol.
The dependency is pinned, its deprecation warnings remain visible, and upgrading
requires requalification. This bounded compatibility result is not a security
audit or completion of P0. The component is not yet wired to an exchange state
machine or pod operations. HMAC used by the operation journal remains separate
from the WSC session keys.

## R0 native OpenSync experiment

The separate checkout is pinned to
`78d8a7194d5e77635877cc456231e7be5cf03d68`. The upstream script expects a `core/`
directory in a device tree. The local experiment supplies that layout with a
symlink, builds only `src/owm` and `ovsdb-create`, and does not run upstream boot
scripts or managers on the host.

The initial build lacked `kconfiglib`. An isolated uv environment with
`kconfiglib==14.1.0` got past Kconfig. Supplying the locally built `ovsdb-tool`
got past database creation; `jinja2==3.1.6` got past seed templating. Compilation
then stopped at **`protoc-c: No such file or directory`**. Logs and Kconfig hash
are retained in `docs/evidence/r0-*`. Additional compiled dependencies and
platform requirements may surface after that blocker is resolved.

The dummy-driver API was inspected: an actual backend needs registration,
PHY/VIF/client seeding and configuration callbacks that publish driver feedback.
No native manager, dummy-driver harness or platform stub was executed or
qualified. N01–N03 remain blocked; N04 has isolated build evidence only. Next R0
work belongs in a dedicated Ubuntu 24.04 LXD container with pinned C build
dependencies. It does not gate the real-pod path once P0 and M0 are ready.
