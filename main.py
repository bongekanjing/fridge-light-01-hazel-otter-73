#!/usr/bin/env python3
"""Validate LINE.txt and write it to the output directory.

The line lives in LINE.txt so the bytes judged are the bytes committed:
nothing is assembled at run time and nothing is fetched over the network.

The destination directory comes from MAKEFUN_OUTPUT_DIR and defaults to
/output, where the gate looks for entry.txt.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = os.path.join(HERE, "LINE.txt")
OUT_NAME = "entry.txt"

MIN_CHARS = 1
# 140 is this bounty's character cap.
MAX_CHARS = 140


def die(message):
    sys.stderr.write("error: %s\n" % message)
    sys.exit(1)


def main():
    try:
        with open(LINE, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        die("cannot read %s: %s" % (LINE, exc))

    # A file that is not valid UTF-8 fails the gate: name the problem here
    # rather than half-decode it into something that happens to fit.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        die("LINE.txt is not valid UTF-8: %s" % exc)

    # A byte-order mark is an encoding artefact, not part of the line.
    if text.startswith("\ufeff"):
        text = text[1:]

    # Trailing newlines end the file; they are not part of the line.
    line = text.rstrip("\r\n")

    if not line.strip():
        die("LINE.txt is empty or only white space")
    if "\n" in line or "\r" in line:
        die("LINE.txt holds more than one line")

    count = len(line)
    if count < MIN_CHARS or count > MAX_CHARS:
        die("%d characters, outside the %d-%d allowed" % (count, MIN_CHARS, MAX_CHARS))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        die("cannot create output dir %s: %s" % (out_dir, exc))

    target = os.path.join(out_dir, OUT_NAME)
    try:
        with open(target, "w", encoding="utf-8", newline="") as handle:
            handle.write(line + "\n")
    except OSError as exc:
        die("cannot write %s: %s" % (target, exc))

    print(count)


if __name__ == "__main__":
    main()
