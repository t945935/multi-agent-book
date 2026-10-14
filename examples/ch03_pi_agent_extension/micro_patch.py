from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PatchResult:
    changed: bool
    content: str
    occurrences: int

def replace_once(content: str, old: str, new: str) -> PatchResult:
    occurrences = content.count(old)
    if occurrences != 1:
        return PatchResult(False, content, occurrences)
    return PatchResult(True, content.replace(old, new, 1), occurrences)

def normalize_fullwidth_punctuation(text: str) -> str:
    table = str.maketrans({",": "，", ":": "："})
    return text.translate(table)
