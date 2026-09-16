# Read-only physical-pod qualification

`emosa qualify-pod` runs on the controller machine. It uses only schema retrieval,
basic OVSDB monitor requests and echo/connection handling. Its session rejects
modifying transactions. It installs nothing on the pod and never changes Config,
State, manager endpoints, cloud settings or firmware.

Create a private directory (`0700`) for existing credentials and trust material.
Files must be owned by the CLI user, regular files, mode `0600`, with no symlinks.
Start from `deploy/qualification.example.json`, replace its placeholders with
the authorized endpoint/database/direction and secret **references**, and put
the existing CA/client certificate/private key in that directory. Obtain the
expected peer certificate SHA-256 from the trusted provisioning channel; do not
learn a pin by accepting an unauthenticated connection.

```sh
uv run emosa qualify-pod --connection /private/lab-pod-01.json \
  --output .lab/qualification/lab-pod-01-first-read
```

The output directory must be new. It contains `schema.json`,
`draft-profile.json` and `artifact-manifest.json`. Treat identifiers and SSIDs as
private lab information; review/sanitize them before publishing. Wi-Fi keys and
security maps are not selected by the monitor, and certificate/private-key
contents are never placed in the report. Keep the original schema artifact/hash
for future mapping qualification.

The draft reports available firmware/model/serial fields, schema version and
fingerprint, Config/State radio/VIF relationships, active security flags and
candidate configuration representations. Missing columns and unknown fields
remain explicit. Column presence does not prove usable behavior. Expected
identifier mismatches retain the draft and give a nonzero CLI result.

Supported connection preparation:

- Dialing mutual TLS uses the upstream OVS client with mandatory CA validation
  and an explicit peer certificate pin. A pin supplies endpoint identity binding
  because the upstream client disables DNS hostname matching. Minimum TLS is
  1.2; there is no insecure fallback. TLS qualification runs in its own short-lived
  process because upstream certificate file settings are process-global.
- An existing owned private Unix socket can be read locally, for example an
  already configured authorized tunnel. Its remote-pod binding still needs
  qualification.
- A database-initiated listening-manager connection can use an existing
  authenticated tunnel into a loopback listener. Set direction `listen`, endpoint
  `ptcp:PORT:127.0.0.1`, trust kind `existing-tunnel`, and a private `evidence_ref`
  describing the existing trust setup. The report hashes that reference and
  explicitly leaves external tunnel verification pending. The collector creates
  no tunnel or pod endpoint setting.

Native listening TLS is not qualified by the selected Python client. A remote
plaintext TCP endpoint is rejected; supply the existing authenticated access path
instead of weakening it for collection. Test certificates are generated only for
local TLS regression tests, never for a physical pod.

The draft is always `writable=false`. Remaining M0 work includes physical
identity/trust binding, specific managed resources, existing writer controls and
their reboot/reconnect behavior, shared radio/management dependencies, recovery,
actual manager/security semantics and independent client observations. EasyMesh
6.1 §7.1 provisioning operates on the radio's requested BSS set: the one-BSS
experiment needs a sole existing BSS on that radio or a complete-radio mapping.

The eventual acceptance path remains **real EasyMesh messages → EMOSA → unchanged
physical pod → independent observed behavior**. This collector and the simulator
are preparation and component evidence, respectively.
