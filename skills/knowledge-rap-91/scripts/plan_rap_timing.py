#!/usr/bin/env python3
"""Create a deterministic planned 91 BPM rap grid from Chinese text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HAN = re.compile(r"[\u3400-\u9fff]")
LATIN = re.compile(r"[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*")
TOKEN_RE = re.compile(r"[\u3400-\u9fff]|[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*|[，、；：。！？,.!?;:]")
def token_slots(token: str) -> int:
    if HAN.fullmatch(token):
        return 1
    if token in "，、；：,;:":
        return 1
    if token in "。！？.!?":
        return 2
    if LATIN.fullmatch(token):
        # Acronyms naturally map to one slot per spoken letter. Longer Latin
        # words are capped and should be manually reviewed for pronunciation.
        return max(1, min(6, len(token)))
    return 1


def srt_time(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--bpm", type=float, default=91.0)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--srt", type=Path)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    slot_seconds = 60.0 / args.bpm / 4.0
    cursor = args.start
    slot_index = 0
    events = []
    line_no = 0

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or (line.startswith("[") and line.endswith("]")):
            if events:
                cursor += slot_seconds * 2
                slot_index += 2
            continue
        line_no += 1
        for token in TOKEN_RE.findall(line):
            slots = token_slots(token)
            start = cursor
            end = start + slots * slot_seconds
            is_rest = token in "，、；：。！？,.!?;:"
            events.append(
                {
                    "token": token,
                    "kind": "rest" if is_rest else "word",
                    "line": line_no,
                    "start": round(start, 4),
                    "end": round(end, 4),
                    "duration": round(end - start, 4),
                    "bar": slot_index // 16 + 1,
                    "slotInBar": slot_index % 16 + 1,
                    "slots": slots,
                }
            )
            cursor = end
            slot_index += slots
        cursor += slot_seconds * 2
        slot_index += 2

    words = [event for event in events if event["kind"] == "word"]
    payload = {
        "schemaVersion": 1,
        "timingType": "planned",
        "bpm": args.bpm,
        "timeSignature": "4/4",
        "slot": "sixteenth-note",
        "slotSeconds": round(slot_seconds, 6),
        "fps30FramesPerSlot": round(slot_seconds * 30, 3),
        "totalSeconds": round(cursor, 3),
        "totalBars": (slot_index + 15) // 16,
        "wordCount": len(words),
        "events": events,
    }
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.srt:
        blocks = []
        for index, event in enumerate(words, 1):
            blocks.append(
                f"{index}\n{srt_time(event['start'])} --> {srt_time(event['end'])}\n{event['token']}\n"
            )
        args.srt.write_text("\n".join(blocks), encoding="utf-8")

    print(
        json.dumps(
            {
                "bpm": args.bpm,
                "slotSeconds": round(slot_seconds, 6),
                "wordCount": len(words),
                "totalBars": payload["totalBars"],
                "totalSeconds": payload["totalSeconds"],
                "timingType": "planned",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
