from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

CREDIT_MEMO_DIR = Path("data/outputs/credit_memos")


@dataclass(frozen=True)
class CreditMemoFile:
    filename: str
    path: str
    size_bytes: int
    modified_at: datetime


def list_credit_memos(output_dir: Path = CREDIT_MEMO_DIR) -> list[CreditMemoFile]:
    if not output_dir.exists():
        return []

    files = []

    for path in sorted(output_dir.glob("*.pdf")):
        stat = path.stat()
        files.append(
            CreditMemoFile(
                filename=path.name,
                path=str(path),
                size_bytes=stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime),
            )
        )

    return files
