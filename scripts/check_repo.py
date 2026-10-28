"""Guard against accidentally committing state or credentials."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DENY_FILENAMES = {"terraform.tfvars", "backend.hcl", ".env"}
DENY_PARTS = {".terraform", "__pycache__", ".git"}
DENY_PATTERNS = [
    re.compile(r"(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(client_secret|access_key|password)\s*=\s*[\"'][^\s\"']{12,}"),
]


def main() -> int:
    problems = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or set(path.parts).intersection(DENY_PARTS):
            continue
        if path.name in DENY_FILENAMES or path.suffix in (".tfstate", ".tfplan"):
            problems.append(f"Unsafe artifact: {path.relative_to(ROOT)}")
            continue
        if path.suffix not in (".tf", ".kql", ".py", ".json", ".md", ".yml", ".yaml"):
            continue
        try:
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in DENY_PATTERNS:
            if pattern.search(contents):
                problems.append(f"Potential credential in {path.relative_to(ROOT)}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print("Repository hygiene checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
