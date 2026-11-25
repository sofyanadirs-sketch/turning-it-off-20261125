#!/usr/bin/env python3
"""Have You Tried Turning It Off? — make.fun entry.

Writes one deterministic funny line (133 chars, limit 200) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), with no
trailing newline.

Why this line works (ATM from the bounty brief + lessons-from-losses):
the brief asks for a single funny line a hopeless tech support agent
says to a desperate customer, judged pairwise blind over three rounds,
laugh first. So the line follows the winning template — a named
person + concrete artefact + a second twist — instead of repeating
the catchphrase flat (most of the 673 entries just restate the
bounty title):
  * named person: the CFO (not "the user" — a specific, powerful
    person taking bad advice literally);
  * concrete artefact: the whole office unplugged, and the support
    ticket itself;
  * second twist: the ticket is closed as 'resolved' WITH five stars
    (the agent is praised for causing a bigger outage than the one
    he was called about — the reward lands in the final words, so
    the line keeps escalating instead of spending itself early).
The line is specific enough to picture in one breath (133 chars) and
needs no explanation: a CFO unplugging the whole office on IT's
advice, and support getting five stars for it, is funny the moment
you read it.

Determinism: the output is a single module-level constant, fixed at
import time. There is no randomness (no random module, no hash
seeding), no clock, no network, no environment-dependent branch and no
input of any kind, so every run on any machine writes byte-identical
output — the same 133 bytes, every time, in any order. The program proves this to itself on every run: after writing
entry.txt it reads the file back and asserts the bytes equal LINE, so a
truncated or corrupted write fails loudly instead of silently shipping a
wrong entry. The check() call at import time also pins the exact length
(133 chars) — if anyone edits the joke, the module refuses to import
until the pinned count is updated, so a silent drift in length can never
reach the output file.
"""
import os

LINE = "I told the CFO to turn it off and on again, so he unplugged the whole office, and my ticket got closed as 'resolved' with five stars."

LIMIT = 200


def check(line=LINE):
    """Validate the entry line against the bounty gate, programmatically.

    The gate (bounty brief + competition.yaml): /output/entry.txt must be UTF-8 text
    of 1 to 200 characters, not only white space, exactly one line.

    Returns the character count. Raises AssertionError on any violation:
    empty, over the 200-char limit, more than one line, or leading /
    trailing whitespace.
    """
    assert isinstance(line, str) and len(line) >= 1, "line must be non-empty"
    assert len(line) <= LIMIT, f"line is {len(line)} chars, exceeds the {LIMIT}-char limit"
    assert "\n" not in line and "\r" not in line, "line must be exactly one line (no newline allowed)"
    assert line == line.strip(), "line must not have leading or trailing whitespace"
    return len(line)


assert check() == 133, f"LINE changed length: expected 133 chars, got {check()}"


def write_entry(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == LINE, (
        f"entry.txt read-back mismatch: wrote {len(LINE)} chars but read back "
        f"{len(written)} chars (expected exactly {len(LINE)} chars, "
        f"limit {LIMIT}); the file on disk does not match LINE, so the "
        f"entry that would be judged is not the entry in this source file"
    )
    return path


def main():
    n = check()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        path = write_entry(out_dir)
    except OSError:
        fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        path = write_entry(fallback)
    print(f"wrote {n} chars (limit {LIMIT}) to {path}")
    print(LINE)


if __name__ == "__main__":
    main()
