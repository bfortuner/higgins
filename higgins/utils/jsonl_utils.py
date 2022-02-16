from typing import Dict, List

import jsonlines


def save_jsonl(fpath: str, records: List[Dict]) -> None:
    with jsonlines.open(fpath, 'w') as writer:
        writer.write_all(records)


def open_jsonl(fpath: str) -> List[Dict]:
    lines = []
    with jsonlines.open(fpath) as reader:
        for row in reader:
            lines.append(row)
    return lines
