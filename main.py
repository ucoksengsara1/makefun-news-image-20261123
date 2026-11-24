#!/usr/bin/env python3
"""Deliver THE MORNING MERIDIAN — akun8's page for 23 November 2026.

What sits in this repository is a finished newspaper front page drawn
as a single PNG: twelve numbered cards (the burning Russian cargo ship
off Finland first), a strip of the day's binding numbers, a dotted map
with a pin per card, a date-check box naming seven stories that belong
to other days, and twenty-six briefs underneath.

The job of this script is only to hand that page over, untouched. It
relies on nothing beyond the standard library: the PNG is read from
the script's own directory, its length and SHA-256 digest are compared
with the values sealed at render time, and the verified bytes are then
written to MAKEFUN_OUTPUT_DIR (falling back to /output). Any mismatch
stops the run with a message rather than shipping a damaged page, so
the copy that lands in the output directory is guaranteed to be the
page that was drawn, sealed and checked in this repository.
"""

import hashlib
import os
import sys

SEALED_BYTES = 292639
SEALED_SHA256 = "a8d712a75e8efdf34c9a699908057a961c38a567a13bf0d53f8993d73df05120"
MAGIC = b"\x89PNG\r\n\x1a\n"
ONE_MIB = 1048576


def read_page():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as fh:
        return fh.read()


def check_page(blob):
    if len(blob) == 0:
        sys.exit("entry.png is empty — nothing to deliver")
    if blob[:8] != MAGIC:
        sys.exit("entry.png is not a PNG file")
    if len(blob) > ONE_MIB:
        sys.exit("entry.png exceeds the 1 MiB competition cap")
    if len(blob) != SEALED_BYTES:
        sys.exit(
            "entry.png has %d bytes; the sealed page has %d"
            % (len(blob), SEALED_BYTES)
        )
    if hashlib.sha256(blob).hexdigest() != SEALED_SHA256:
        sys.exit("entry.png digest differs from the sealed digest")


def main():
    page = read_page()
    check_page(page)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(page)
    sys.stderr.write(
        "delivered THE MORNING MERIDIAN: %d bytes, sha256 %s\n"
        % (len(page), hashlib.sha256(page).hexdigest())
    )


if __name__ == "__main__":
    main()
