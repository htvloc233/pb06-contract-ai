# REPO-SETUP-PB06 — Dựng Repo + CI để lật PASS điều kiện DoR D7

> **Mục tiêu:** D7 chuyển FAIL → PASS **bằng bằng chứng hành vi**, không bằng "đã tạo xong".
> **Thời lượng:** 1–2 giờ. **Ai làm:** PM tự dựng được — phân vai theo `DELEGATION-MAP` v1.1: tài khoản/token/secret = **Human-do** (dòng #11), file config CI = **AI-draft + Human-review** (L2–L3).

---

## 0. Chọn đường — quyết trong 1 ngày, không chờ vô hạn

| Đường | Khi nào | Cách |
|---|---|---|
| **A — GitHub free (mặc định)** | Học bootcamp / không có hạ tầng sẵn / đường B không trả lời trong 1 ngày | Làm theo §1–§4 dưới |
| **B — Hạ tầng công ty** (GitLab/DevOps nội bộ) | Tổ chức có sẵn + policy bắt buộc dùng nội bộ | Gửi Tech Lead/PMO đúng một câu hỏi: *"Xin 1 project space private cho PB-06: quyền cho [danh sách người], branch protection trên main, CI runner Python 3.11. Hạn cần: ngày X."* — có hạn chót, quá hạn 1 ngày → chuyển đường A (đúng luật escalation N-list) |

> **Nếu bạn học một mình (Customer Zero):** "4 người" là đội trong kịch bản đề. D7 diễn giải theo **đội thật**: mọi người thật tham gia build (bạn + Coach/mentor nếu có quyền review) truy cập được. Khi lật PASS, ghi rõ diễn giải này vào dòng bằng chứng của DOR — minh bạch, không lặng lẽ đổi điều kiện.

---

## 1. Tạo repo + commit đầu tiên = chính bộ hồ sơ giấy

```bash
# Trên github.com: New repository → tên: pb06-contract-ai → Private → KHÔNG tick README
git clone https://github.com/<user>/pb06-contract-ai.git
cd pb06-contract-ai

# Cấu trúc đúng quy ước CLAUDE.md §13
mkdir -p docs src tests .github/workflows
touch src/.gitkeep

# Copy 10 artefact .md đã có vào đúng chỗ:
#   CLAUDE.md, DEVBOOK-PB06.md, telemetry.md (nếu có)  → gốc repo
#   SCOPE/SPEC/MODULEMAP/ARCH/WBS/EST/RISK/DELEGATION-MAP/DOR-PB06.md → docs/
```

Tạo `.gitignore` ở gốc — **dòng `.env` là luật cứng #2 bằng config**:

```gitignore
.env
*.env
__pycache__/
*.pyc
.venv/
node_modules/
.DS_Store
*.local.*
```

Tạo `tests/test_smoke.py` — smoke test **có nghĩa** (kiểm cấu trúc repo, không phải `assert True` — đó là "test giả" mà Delegation #7 cấm):

```python
from pathlib import Path

REQUIRED = [
    "CLAUDE.md",
    "docs/SCOPE-PB06.md", "docs/SPEC-PB06.md", "docs/ARCH-PB06.md",
    "docs/WBS-PB06.md", "docs/DOR-PB06.md",
    "DEVBOOK-PB06.md",
]

def test_repo_structure():
    missing = [p for p in REQUIRED if not Path(p).exists()]
    assert not missing, f"Thiếu artefact bắt buộc: {missing}"

def test_no_env_committed():
    assert not Path(".env").exists(), "Luật cứng #2: .env không được nằm trong repo"
```

Đặt file `ci.yml` (kèm sẵn trong bộ này) vào `.github/workflows/ci.yml`, rồi:

```bash
git add -A
git commit -m "chore: hồ sơ [0]→[7] làm commit #1 — docs-as-code, luật ghim phiên bản kiểm bằng git log"
git push origin main
```

> **Vì sao commit #1 là bộ .md:** từ đây, "luật ghim phiên bản" (CLAUDE.md §7, sinh từ DB-08/DB-11) kiểm được bằng `git log` thay vì bằng trí nhớ — mỗi lần artefact đổi version là một commit có dấu thời gian.

---

## 2. Branch protection — luật cứng #1 trở thành config, hết là lời hứa

GitHub → repo → **Settings → Branches → Add branch protection rule** cho `main`:

- ✅ **Require a pull request before merging** + ≥1 approval
- ✅ **Require status checks to pass** → chọn check `lint-test` (hiện sau lần CI chạy đầu)
- ✅ **Do not allow bypassing** (áp cả admin)

Kết quả: *"AI không tự push/merge/release"* và *"người cũng không"* — mọi thay đổi đi qua PR + review + CI xanh. Đây chính là kênh-bằng-chứng mà bạn dựng ở cổng [6] (RISK A7): kết quả tính theo artifact của runner trên PR, không theo lời ai.

---

## 3. Cấp quyền

Settings → **Collaborators** → mời từng người (đội thật) quyền `Write`. Mỗi người xác nhận bằng **hành vi**: clone → tạo branch → mở 1 PR chào sân (sửa một dòng README) → CI chạy → người khác approve → merge. Một vòng PR trọn vẹn cho mỗi người = bằng chứng, "đã nhận lời mời" thì chưa.

**Secret/token:** PAT hoặc deploy key ai tạo người đó giữ — không dán vào chat, không commit, không đưa AI đọc (Delegation #11, L0).

---

## 4. Checklist bằng chứng lật PASS D7 — tick đủ 5, mỗi ô là hành vi kiểm được

| ✔ | Bằng chứng | Cách kiểm |
|---|---|---|
| ☐ | Repo private tồn tại, đúng cấu trúc, commit #1 = bộ artefact | Mở URL + `git log --oneline` |
| ☐ | CI **xanh trên commit đầu** (lint + smoke test) | Tab Actions: run xanh |
| ☐ | Direct push vào `main` **bị chặn** | Thử `git push origin main` từ branch thường → bị từ chối — *một lần fail cố ý là bằng chứng đẹp nhất* |
| ☐ | Mỗi người thật hoàn thành 1 vòng PR trọn vẹn | Danh sách PR đã merge, mỗi người ≥1 |
| ☐ | `.env` không thể lọt | `test_no_env_committed` xanh + `.gitignore` có dòng `.env` |

---

## 5. Sau khi tick đủ

Báo lại kèm **URL repo + link CI run xanh** (hoặc dán output `git log` + trạng thái Actions). Nhận được bằng chứng, DOR D7 lật PASS với dòng: *bằng chứng + ngày + người xác nhận* — và Dev Book nhận thêm một mục nhỏ: D7 đóng bằng hành vi, không bằng tuyên bố.

**Việc kế cận cùng cụm hạ tầng** (làm luôn cho trọn buổi): D9 — spike nửa buổi kiểm egress control khả thi (giả lập: một test gọi ra domain ngoài whitelist phải bị chặn — sau này thành job `egress-test` đã để chỗ sẵn trong `ci.yml`).

---

*REPO-SETUP-PB06 v1.0 · đường A mặc định · nguyên tắc xuyên suốt: mọi ô PASS đổi bằng hành vi kiểm được.*
