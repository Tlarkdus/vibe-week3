"""quotes.txt에서 무작위 한 줄을 골라 README.md 마커 구간을 갱신한다."""
import random
import re
from pathlib import Path

MARKER = re.compile(r"(<!-- QUOTE:START -->\n)(.*?)(\n<!-- QUOTE:END -->)", re.S)


def update(readme: Path, quotes: Path) -> str:
    text = readme.read_text(encoding="utf-8")
    current = MARKER.search(text)
    if not current:
        raise SystemExit("README.md에 QUOTE:START/END 마커가 정확히 하나 있어야 한다")

    lines = [l for l in quotes.read_text(encoding="utf-8").splitlines() if l.strip()]
    # 오늘 문구가 어제와 같으면 커밋할 게 없어지므로 현재 문구는 후보에서 뺀다
    candidates = [l for l in lines if l != current[2].strip("\n")] or lines
    quote = random.choice(candidates)

    readme.write_text(MARKER.sub(lambda m: m[1] + quote + m[3], text), encoding="utf-8")
    return quote


if __name__ == "__main__":
    root = Path(__file__).parent
    print(update(root / "README.md", root / "quotes.txt"))
