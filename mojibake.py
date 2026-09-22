#!/usr/bin/env python3
"""
Repair common UTF-8 mojibake.

The program detects text which was originally UTF-8, incorrectly
decoded using a legacy single-byte encoding, and subsequently
encoded as UTF-8 again.

Examples:

    "JosÃ©"       -> "José"
    "├Ñ"          -> "å"
    "ÔÇÖ"         -> "’"
    "ÔÇ£"         -> "“"
    "ðŸ˜Š"        -> "😊"

Supported input encodings:

    UTF-8
    UTF-8 with BOM
    UTF-16 LE/BE
    UTF-32 LE/BE

Output is always UTF-8.

Command line:

    python mojibake.py input.txt output.txt
    python mojibake.py < input.txt > output.txt

Modify in place:

    python mojibake.py -m input.txt

Modify with backup:

    python mojibake.py -m -b input.txt
    python mojibake.py -m -b .orig input.txt

Options:

    -q, --quiet
        Do not report "no repair was made".

    -m, --modify
        Modify the input file in place. The second positional filename
        is ignored.

    -b, --backup [EXT]
        With --modify, rename the original to filename + EXT before
        replacing it. Defaults to ".bkp".

        Has no effect without --modify.
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile


# Encodings which are plausible sources of this type of corruption.
#
# cp1252 and latin-1 are common on Windows/Western European systems.
# cp437 and cp850 are common in DOS-era software and some terminals.
_ENCODINGS = (
    "cp1252",
    "cp437",
    "cp850",
    "latin-1",
    "iso-8859-15",
)


# Characters which are highly unusual in ordinary natural-language
# Unicode text and are frequently produced by mojibake.
#
# This is deliberately a fairly broad list. It is used as one signal
# among several, not as the sole detection mechanism.
_SUSPICIOUS_CHARS = set(
    # Western UTF-8 / CP1252 mojibake
    "ÃÂâÔÇ"
    # CP437 / CP850 box drawing
    "├┤┼│┌┐└┘─"
    "┬┴"
    "╔╗╚╝═║"
    # Block characters
    "░▒▓█"
)


# Particularly recognizable mojibake fragments.
_SUSPICIOUS_FRAGMENTS = (
    "Ã",
    "Â",
    "â€",
    "ÔÇ",
    "ðŸ",
    "Ã‚",
    "Ãƒ",
    "├",
    "┤",
    "┼",
    "┬",
    "┴",
    "┌",
    "┐",
    "└",
    "┘",
    "─",
)


# Unicode ranges which are usually suspicious when they occur in
# ordinary text. These aren't automatically errors, but they contribute
# to the score.
_SUSPICIOUS_RANGES = (
    (0x0080, 0x009F),  # C1 controls
    (0x2500, 0x257F),  # Box Drawing
    (0x2580, 0x259F),  # Block Elements
)


def _in_suspicious_range(codepoint: int) -> bool:
    return any(
        start <= codepoint <= end
        for start, end in _SUSPICIOUS_RANGES
    )


def mojibake_score(text: str) -> float:
    """
    Estimate how suspicious a Unicode string looks.

    Higher scores indicate text more likely to contain mojibake.

    The score intentionally combines several weak signals rather than
    relying on a single hard-coded sequence.
    """
    score = 0.0

    for ch in text:
        cp = ord(ch)

        if ch in _SUSPICIOUS_CHARS:
            score += 3.0

        if _in_suspicious_range(cp):
            score += 4.0

    for fragment in _SUSPICIOUS_FRAGMENTS:
        score += text.count(fragment) * 2.0

    # Replacement characters are almost always evidence of an earlier
    # decoding failure.
    score += text.count("\ufffd") * 10.0

    return score


def text_quality_score(text: str) -> float:
    """
    Estimate how plausible text is as ordinary Unicode text.

    This is deliberately conservative and language-independent.
    It does not try to identify a language.

    Higher is better.
    """
    if not text:
        return 0.0

    score = 0.0

    for ch in text:
        cp = ord(ch)

        # ASCII printable characters are generally a good sign.
        if 0x20 <= cp <= 0x7E:
            score += 1.0

        # Whitespace is also normal.
        elif ch in "\r\n\t":
            score += 0.5

        # Replacement character is strongly bad.
        elif ch == "\ufffd":
            score -= 10.0

        # C0/C1 controls are suspicious.
        elif cp < 0x20 or 0x7F <= cp <= 0x9F:
            score -= 4.0

        # Box drawing/block characters are unusual in prose.
        elif 0x2500 <= cp <= 0x259F:
            score -= 3.0

        # Private use characters are unusual in ordinary text.
        elif 0xE000 <= cp <= 0xF8FF:
            score -= 3.0

        else:
            # Normal Unicode letters, punctuation, symbols, emoji, etc.
            score += 0.5

    return score


def candidate_score(original: str, candidate: str) -> float:
    """
    Compare a repair candidate with the original.

    Positive values mean that the candidate looks better.
    """
    original_mojibake = mojibake_score(original)
    candidate_mojibake = mojibake_score(candidate)

    original_quality = text_quality_score(original)
    candidate_quality = text_quality_score(candidate)

    # Mojibake reduction is the strongest signal.
    improvement = (
        original_mojibake - candidate_mojibake
    ) * 10.0

    # Text-quality improvement provides a secondary signal.
    quality_improvement = (
        candidate_quality - original_quality
    )

    return improvement + quality_improvement


def decode_input(data: bytes) -> tuple[str, str]:
    """
    Decode input bytes.

    BOMs are preferred because they provide an unambiguous encoding.

    Returns:
        (decoded_text, encoding_name)
    """

    # UTF-32
    if data.startswith(b"\xff\xfe\x00\x00"):
        return data[4:].decode("utf-32-le"), "utf-32-le"

    if data.startswith(b"\x00\x00\xfe\xff"):
        return data[4:].decode("utf-32-be"), "utf-32-be"

    # UTF-16
    if data.startswith(b"\xff\xfe"):
        return data[2:].decode("utf-16-le"), "utf-16-le"

    if data.startswith(b"\xfe\xff"):
        return data[2:].decode("utf-16-be"), "utf-16-be"

    # UTF-8 BOM
    if data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8"), "utf-8"

    # Normal UTF-8
    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError as exc:
        raise ValueError(
            "input is not valid UTF-8 and has no recognized "
            "UTF-16/UTF-32 BOM"
        ) from exc


def _try_repair(
    text: str,
    encoding: str,
) -> str | None:
    """
    Try to reverse:

        UTF-8 -> <encoding> -> Unicode

    For example:

        "ÔÇÖ".encode("cp850").decode("utf-8")
        == "’"
    """
    try:
        return text.encode(encoding).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None


def _repair_once(
    text: str,
) -> tuple[str, str | None]:
    """
    Perform one repair pass.

    Every candidate encoding is tried. The candidate with the best
    score wins, but only if it improves the text sufficiently.
    """
    best_text = text
    best_encoding = None
    best_score = 0.0

    for encoding in _ENCODINGS:
        candidate = _try_repair(text, encoding)

        if candidate is None or candidate == text:
            continue

        score = candidate_score(text, candidate)

        if score > best_score:
            best_text = candidate
            best_encoding = encoding
            best_score = score

    # Require an actual meaningful improvement. This threshold is
    # intentionally greater than zero to avoid "repairs" caused by
    # tiny statistical differences.
    if best_encoding is None or best_score < 3.0:
        return text, None

    return best_text, best_encoding


def repair_text(
    text: str,
    max_passes: int = 3,
) -> str:
    """
    Repair common UTF-8 mojibake.

    Multiple passes allow text which has been corrupted repeatedly
    to be repaired.
    """
    for _ in range(max_passes):
        repaired, encoding = _repair_once(text)

        if encoding is None:
            break

        text = repaired

    return text


def repair_text_with_info(
    text: str,
    max_passes: int = 3,
) -> tuple[str, list[str]]:
    """
    Like repair_text(), but also returns the encodings used for each
    successful repair pass.

    This is useful for diagnostics and callers which want to know
    what happened.
    """
    encodings: list[str] = []

    for _ in range(max_passes):
        repaired, encoding = _repair_once(text)

        if encoding is None:
            break

        text = repaired
        encodings.append(encoding)

    return text, encodings


def _backup_name(
    filename: str,
    extension: str,
) -> str:
    """Return filename + extension, normalizing the leading dot."""
    if not extension.startswith("."):
        extension = "." + extension

    return filename + extension


def modify_file(
    filename: str,
    data: bytes,
    backup_extension: str | None,
) -> None:
    """
    Replace filename with data.

    A temporary file is created in the same directory first.

    If a backup was requested, the original is renamed to the backup
    only after the replacement data has been successfully written.
    """
    directory = os.path.dirname(os.path.abspath(filename))
    basename = os.path.basename(filename)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{basename}.",
        suffix=".tmp",
        dir=directory,
    )

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        if backup_extension is not None:
            backup_name = _backup_name(
                filename,
                backup_extension,
            )

            if os.path.exists(backup_name):
                raise FileExistsError(
                    f"backup file already exists: {backup_name}"
                )

            os.replace(filename, backup_name)

            try:
                os.replace(temp_name, filename)
            except Exception:
                # Try to restore the original.
                try:
                    os.replace(backup_name, filename)
                except Exception:
                    pass
                raise

        else:
            os.replace(temp_name, filename)

    finally:
        try:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair common UTF-8 mojibake."
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not report when no repair was made",
    )

    parser.add_argument(
        "-m",
        "--modify",
        action="store_true",
        help="modify the input file in place",
    )

    parser.add_argument(
        "-b",
        "--backup",
        nargs="?",
        const=".bkp",
        metavar="EXT",
        help=(
            "with --modify, backup input by appending EXT "
            "(default: .bkp)"
        ),
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="input file (default: stdin)",
    )

    parser.add_argument(
        "output",
        nargs="?",
        help="output file (ignored with --modify; default: stdout)",
    )

    args = parser.parse_args()

    # --modify requires a filename.
    if args.modify and not args.input:
        parser.error("--modify requires an input filename")

    # The second positional argument is explicitly ignored in modify mode.
    if args.modify and args.output and not args.quiet:
        print(
            "mojibake: output filename ignored with --modify",
            file=sys.stderr,
        )

    # ------------------------------------------------------------------
    # In-place mode
    # ------------------------------------------------------------------

    if args.modify:
        try:
            with open(args.input, "rb") as infile:
                data = infile.read()
        except OSError as exc:
            print(
                f"mojibake: cannot read {args.input}: {exc}",
                file=sys.stderr,
            )
            return 1

        try:
            text, input_encoding = decode_input(data)
        except ValueError as exc:
            print(f"mojibake: {exc}", file=sys.stderr)
            return 1

        repaired, repairs = repair_text_with_info(text)

        try:
            modify_file(
                args.input,
                repaired.encode("utf-8"),
                args.backup,
            )
        except OSError as exc:
            print(
                f"mojibake: cannot modify {args.input}: {exc}",
                file=sys.stderr,
            )
            return 1

        if not args.quiet:
            if repairs:
                print(
                    f"mojibake: {input_encoding} input; "
                    f"repair(s): {' -> '.join(repairs)}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"mojibake: no repair was made "
                    f"(input encoding: {input_encoding})",
                    file=sys.stderr,
                )

        return 0

    # ------------------------------------------------------------------
    # Normal input -> output / stdin -> stdout mode
    # ------------------------------------------------------------------

    infile = (
        open(args.input, "rb")
        if args.input
        else sys.stdin.buffer
    )

    outfile = (
        open(args.output, "wb")
        if args.output
        else sys.stdout.buffer
    )

    try:
        data = infile.read()

        try:
            text, input_encoding = decode_input(data)
        except ValueError as exc:
            print(f"mojibake: {exc}", file=sys.stderr)
            return 1

        repaired, repairs = repair_text_with_info(text)

        # Output is always UTF-8.
        outfile.write(repaired.encode("utf-8"))

        if not args.quiet:
            if repairs:
                print(
                    f"mojibake: {input_encoding} input; "
                    f"repair(s): {' -> '.join(repairs)}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"mojibake: no repair was made "
                    f"(input encoding: {input_encoding})",
                    file=sys.stderr,
                )

    except OSError as exc:
        print(f"mojibake: {exc}", file=sys.stderr)
        return 1

    finally:
        if args.input:
            infile.close()

        if args.output:
            outfile.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
