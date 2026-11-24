#!/usr/bin/env python3
"""THE MORNING MERIDIAN — entry program for news-image-20261123 (akun8).

The artwork beside this file, entry.png, is a one-page newspaper for
Monday 23 November 2026: twelve main cards led by the Russian cargo
ship still burning off Finland, a day-in-numbers strip, a dotted world
map, a date-check box and twenty-six briefs — 38 stories in all.

This program is deliberately boring. It uses only the Python standard
library, reads entry.png from its own folder, verifies the byte count
and the SHA-256 fingerprint that were recorded when the page was
rendered, and then writes an identical copy into the output directory
(MAKEFUN_OUTPUT_DIR, default /output). No network, no image libraries,
no surprises: two runs always produce the same bytes, and a tampered
or truncated entry.png is refused instead of being passed along.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 292639
EXPECTED_SHA256 = "a8d712a75e8efdf34c9a699908057a961c38a567a13bf0d53f8993d73df05120"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576  # the competition caps an entry at 1 MiB


def load_entry():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as fh:
        return fh.read()


def verify(blob):
    if not blob:
        sys.exit("entry.png is empty")
    if blob[:8] != PNG_HEADER:
        sys.exit("entry.png does not start with the PNG magic bytes")
    if len(blob) > HARD_LIMIT:
        sys.exit("entry.png is over the 1 MiB cap: %d bytes" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size drifted: got %d bytes, expected %d"
            % (len(blob), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png fingerprint mismatch: %s" % digest)
    return digest


def main():
    blob = load_entry()
    digest = verify(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(blob)
    sys.stderr.write(
        "THE MORNING MERIDIAN entry copied: %d bytes sha256=%s\n"
        % (len(blob), digest)
    )


if __name__ == "__main__":
    main()
