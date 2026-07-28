"""quotes.txt에서 무작위 한 줄을 골라 README.md 마커 구간을 갱신한다."""
import random
import re
from pathlib import Path

MARKER = re.compile(r"(<!-- QUOTE:START -->\n).*?(\n<!-- QUOTE:END -->)", re.S)


def update(readme: Path, quotes: Path) -> str:
    lines = [l for l in quotes.read_text(encoding="utf-8").splitlines() if l.strip()]
    quote = random.choice(lines)
    text, n = MARKER.subn(lambda m: m[1] + quote + m[2], readme.read_text(encoding="utf-8"))
    if n != 1:
        raise SystemExit("README.md에 QUOTE:START/END 마커가 정확히 하나 있어야 한다")
    readme.write_text(text, encoding="utf-8")
    return quote


if __name__ == "__main__":
    root = Path(__file__).parent
    print(update(root / "README.md", root / "quotes.txt"))
