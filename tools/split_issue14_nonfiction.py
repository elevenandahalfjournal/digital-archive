from pathlib import Path
import re
import hashlib

IN_PATH = Path("Nonfiction Accepted Submissions.txt")  # if it's in project root
# If it's somewhere else, set the correct path, e.g. Path("tools/Nonfiction Accepted Submissions.txt")

OUT_DIR = Path("src/content/entries")

ISSUE_SLUG = "2026-issue-14"
ISSUE_NUMBER = 14
YEAR = 2026
GENRE = "nonfiction"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def safe_filename(base_slug: str, max_len: int = 60) -> str:
    # clip long slugs + add stable hash suffix so filenames never explode
    h = hashlib.md5(base_slug.encode("utf-8")).hexdigest()[:8]
    clipped = base_slug[:max_len].rstrip("-")
    return f"{clipped}-{h}"

def parse_blocks(raw: str):
    # Normalize newlines
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = raw.split("\n")

    i = 0
    blocks = []
    while i < len(lines):
        # skip leading empties
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        title = lines[i].strip()
        author = lines[i + 1].strip() if i + 1 < len(lines) else ""
        dedication = lines[i + 2].strip() if i + 2 < len(lines) else ""
        i += 3

        # expect a blank line after dedication (but don’t hard-fail if missing)
        if i < len(lines) and lines[i].strip() == "":
            i += 1

        body_lines = []
        # body continues until we hit the next "title/author/dedication" pattern
        # heuristic: next non-empty line + next line non-empty + next line non-empty,
        # AND there is a blank line after those three.
        while i < len(lines):
            # lookahead pattern
            if lines[i].strip() != "":
                if i + 3 < len(lines):
                    a = lines[i].strip()
                    b = lines[i + 1].strip()
                    c = lines[i + 2].strip()
                    d = lines[i + 3].strip()
                    if a and b and c and d == "":
                        # this looks like the next entry header
                        break
            body_lines.append(lines[i])
            i += 1

        body = "\n".join(body_lines).strip()
        blocks.append((title, author, dedication, body))

    return blocks

def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"Could not find input file: {IN_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = IN_PATH.read_text(encoding="utf-8", errors="replace")
    blocks = parse_blocks(raw)

    for idx, (title, author, dedication, body) in enumerate(blocks, start=1):
        base = f"{ISSUE_SLUG}-{slugify(title)}"
        fname = safe_filename(base) + ".md"
        out_path = OUT_DIR / fname

        fm = [
            "---",
            f'title: "{title}"',
            f'author: "{author}"' if author else 'author: ""',
            f'dedication: "{dedication}"' if dedication else 'dedication: ""',
            f'genre: "{GENRE}"',
            f'issueSlug: "{ISSUE_SLUG}"',
            f"issueNumber: {ISSUE_NUMBER}",
            f"year: {YEAR}",
            f"order: {idx}",
            "---",
            "",
        ]

        out_path.write_text("\n".join(fm) + body + "\n", encoding="utf-8")
        print("Wrote", out_path)

    print(f"\nDone. Generated {len(blocks)} nonfiction entries for {ISSUE_SLUG}.")

if __name__ == "__main__":
    main()
