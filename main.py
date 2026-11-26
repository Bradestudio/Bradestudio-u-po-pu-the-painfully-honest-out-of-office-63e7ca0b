"""The Painfully Honest Out-of-Office — make.fun bounty entry.

Writes one out-of-office auto-reply (188 chars) to entry.txt in
MAKEFUN_OUTPUT_DIR (fallback /output). Stdlib only, no network,
no clock, no local imports, no hardcoded paths.

The line is a single sentence that admits, in public, what an
employee would only say privately: the inbox stopped being opened
because every reply bred three more. The turn is the breeding —
each answer multiplies the work — and the close stays warm and
professional: resting until Monday, answering properly then.
"""

import os
import sys

ENTRY = (
    "I'm out of office and being honest: I stopped opening my inbox "
    "because every reply bred three more, so I'm resting until Monday "
    "and will answer properly then \u2014 thank you for your patience."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 200:
        sys.exit("entry line must be 1-200 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if line.count(".") != 1 or not line.endswith("."):
        sys.exit("entry line must be exactly one sentence")
    if len(line.split()) < 20:
        sys.exit("entry line too short to land the admission, got %d words"
                 % len(line.split()))
    if "bred three more" not in line:
        # The turn of phrase is the admission's engine: every reply
        # breeding three more is why the inbox stopped being opened.
        sys.exit("entry line must keep the breeding-replies turn")
    if not line.startswith("I'm out of office"):
        # It must read as a real away message first, not a joke about one.
        sys.exit("entry line must open as an out-of-office reply")
    if "thank you" not in line.lower():
        # The polite close is what lets the brutal admission stand:
        # honesty without it is just rudeness, and loses.
        sys.exit("entry line must keep its polite close")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file is exactly the gated line, no newline.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
