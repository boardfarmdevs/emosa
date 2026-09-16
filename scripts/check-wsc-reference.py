"""Rebuild synthetic WSC vectors with pinned upstream hostap, independently of EMOSA.

Needs a C compiler and OpenSSL development headers. No daemon or radio is started.
Without --archive, downloads the pinned official release into a temporary directory.
"""

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/protocol/wsc"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="existing digest-matching hostapd-2.11.tar.gz")
    args = parser.parse_args()
    provenance = json.loads((FIXTURE / "provenance.json").read_text())
    with tempfile.TemporaryDirectory(prefix="emosa-wsc-reference-") as directory:
        work = Path(directory)
        archive = args.archive
        if archive is None:
            archive = work / "hostapd-2.11.tar.gz"
            with urllib.request.urlopen(provenance["source_url"], timeout=30) as response:
                archive.write_bytes(response.read(16 * 1024 * 1024))
        if hashlib.sha256(archive.read_bytes()).hexdigest() != provenance["source_sha256"]:
            raise SystemExit("hostap archive digest mismatch")
        with tarfile.open(archive) as source:
            source.extractall(work, filter="data")
        source_root = work / "hostapd-2.11"
        for name, digest in provenance["source_files"].items():
            if hashlib.sha256((source_root / name).read_bytes()).hexdigest() != digest:
                raise SystemExit("hostap source file digest mismatch")
        executable = work / "reference"
        command = [
            "cc",
            "-O2",
            "-ffunction-sections",
            "-fdata-sections",
            "-DCONFIG_WPS",
            "-DCONFIG_SHA256",
            "-DCONFIG_NO_STDOUT_DEBUG",
            "-I",
            str(source_root / "src"),
            "-I",
            str(source_root / "src/utils"),
            str(FIXTURE / "reference.c"),
            *[str(source_root / name) for name in provenance["compiled_sources"]],
            "-Wl,--gc-sections",
            "-lcrypto",
            "-o",
            str(executable),
        ]
        subprocess.run(command, check=True, timeout=60)
        result = subprocess.run(
            [str(executable)], check=True, capture_output=True, text=True, timeout=30
        )
        cases = []
        for line in result.stdout.splitlines():
            key, value = line.split("=", 1)
            if key == "case":
                cases.append({"name": value})
            else:
                cases[-1][key] = value
        if cases != json.loads((FIXTURE / "vectors.json").read_text())["cases"]:
            raise SystemExit("independent hostap output differs from retained vectors")
        print(f"Independent hostap reference: {len(cases)} cases match retained expected bytes")


if __name__ == "__main__":
    main()
