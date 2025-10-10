import csv
import io
from typing import List

from core.schemas import NameCard


def to_csv(cards: List[NameCard]) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "name",
        "territory",
        "distinctiveness",
        "pronounceability",
        "spellability",
        "uniqueness",
        "availability",
    ])
    for c in cards:
        writer.writerow([
            c.candidate.text,
            c.candidate.territory,
            f"{c.scores.distinctiveness:.2f}",
            f"{c.scores.pronounceability:.2f}",
            f"{c.scores.spellability:.2f}",
            f"{c.scores.seo_uniqueness:.2f}",
            f"{c.scores.domain_handle:.2f}",
        ])
    return buf.getvalue().encode("utf-8")


