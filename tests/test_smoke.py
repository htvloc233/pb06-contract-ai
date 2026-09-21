from pathlib import Path

REQUIRED = [
    "CLAUDE.md",
    "docs/SCOPE-PB06.md", "docs/SPEC-PB06.md", "docs/MODULEMAP-PB06.md",
    "docs/ARCH-PB06.md", "docs/WBS-PB06.md", "docs/EST-PB06.md",
    "docs/RISK-PB06.md", "docs/DELEGATION-MAP-PB06.md", "docs/DOR-PB06.md",
    "DEVBOOK-PB06.md",
]

def test_repo_structure():
    missing = [p for p in REQUIRED if not Path(p).exists()]
    assert not missing, f"Thieu artefact bat buoc: {missing}"

def test_no_env_committed():
    assert not Path(".env").exists(), "Luat cung #2: .env khong duoc nam trong repo"
