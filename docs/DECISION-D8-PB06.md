# DECISION-D8-PB06 — Chốt định nghĩa Staging (chế độ solo)
### Quyết định một trang · lật điều kiện DoR **D8** (G5/G8 của EST)

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-23 · **Trạng thái:** ✅ **APPROVED** — PM duyệt nguyên trạng 2026-09-23, bằng chứng chạy đủ 3 ô *(hồ sơ: `DEVBOOK` DB-24)*
> **v1.1 — sửa theo ràng buộc phần cứng thật:** máy PM chạy macOS 10.15.5; Docker Desktop hiện hành đòi macOS 14+, các bản cũ tương thích Catalina **không còn link tải chính thức** → thi hành staging trên máy này chuyển sang **phương án B (native)**. Đúng tinh thần §4 của mọi DECISION: quyết định gặp thực tế thì sửa quyết định có hồ sơ — không ép công cụ, không cài bản không được vá lên máy đang giữ credential
> **Input:** `DOR` D8 · `EST` v1.1 G5/G8 · `ARCH` v1.5 §2 (container) · `DECISION-D12` (worker C chạy trong AI service) · tiền lệ D11/D12 (vai kiêm minh bạch)
> **Người quyết:** PM kiêm vai hạ tầng *(solo — không có team platform; quyết định này thay cho "staging của tổ chức tồn tại")*

---

## 1. Quyết định

**Hai tầng định nghĩa (v1.1):**

- **Định nghĩa chuẩn** vẫn là docker-compose hai container dưới đây — áp cho CI và mọi máy đủ điều kiện; file compose **giữ trong repo**.
- **Thi hành trên máy PM hiện tại — phương án B (native):** AI service chạy trong **venv Python 3.12** (installer chính chủ python.org) bằng `./staging-up.sh`; PostgreSQL chạy bằng **Postgres.app** bản tương thích Catalina (PG 12/13 — chính Postgres.app build PG 13 trên macOS 10.15). Cùng cấu trúc, khác vỏ:

| Container | Ảnh | Vai |
|---|---|---|
| `db` | postgres:16-alpine | L0-ResultStore/AuditLog — nơi migration W1-04 sẽ đổ vào; volume persist, reset sạch bằng `docker compose down -v` |
| `ai-service` | build từ Dockerfile (python:3.11-slim + FastAPI) | Khung W1-F01; **egress guard nằm sẵn trong image** vì copy cả `src/` |

Mọi lần chữ "staging" xuất hiện trong hồ sơ (W1-18 ghép slice · W1-22 đo p95 · E2E · G5/G8) từ nay trỏ vào **một nguồn sự thật này** — không có "chạy tạm chỗ khác".

## 2. Bốn design rule — điều kiện của chữ duyệt

1. **Secret chỉ sống trong `.env` local** — `.env.example` commit, `.env` không bao giờ (luật cứng #2; smoke test `test_no_env_committed` đang gác bằng máy).
2. **`EGRESS_ALLOWED_HOSTS` rỗng mặc định** ngay trong `.env.example` — staging sinh ra đã đóng cổng; muốn mở phải là hành động có chủ đích, sau OI-02.
3. **Chỉ dữ liệu synthetic (D10) được vào staging này** cho tới khi OI-02 chốt — hợp đồng thật chạm compose này là vi phạm B1.
4. **Python của app cố định ≥3.11** — trong image (compose) hoặc trong venv 3.12 (phương án B); máy trần chạy 3.8 không còn liên quan (giải ghi sổ DB-23).
5. **Lệch phiên bản PG được ghi nhận và khoanh vùng (v1.1):** staging-B chạy PG 12/13, chuẩn compose/CI là PG 16 → **migration Wave 1 chỉ dùng tính năng cổ điển** (bảng, kiểu chuẩn, CHECK, UNIQUE, trigger — đều có từ trước PG 12); skew tự hết khi chuyển máy/OS/staging thật. Vi phạm khoanh vùng = mở lại quyết định.

## 3. Bằng chứng để lật D8 — hành vi, không phải lời

| ✔ | Bằng chứng | Lệnh |
|---|---|---|
| ☐ | AI service trả lời thật | `curl http://localhost:8000/health` → JSON `"status":"ok"` |
| ☐ | PostgreSQL sống và có DB dự án | `psql -d pb06 -c "select version();"` (psql của Postgres.app) → dòng `PostgreSQL 12.x/13.x` |
| ☐ | Kit A (compose — định nghĩa chuẩn) + Kit B (script native) vào repo qua PR, **KHÔNG kèm `.env`** | vòng PR thường lệ |

*(Máy đủ điều kiện Docker sau này: bộ bằng chứng gốc `docker compose ps` áp trở lại.)*

## 4. Điều kiện mở lại

Cắm SaaS thật → staging thật của tổ chức họ, compose này giáng cấp thành dev-local; cần multi-user/E2E tải thật → tách môi trường. Mở `EGRESS_ALLOWED_HOSTS` → chỉ sau OI-02 + (nếu external) hồ sơ ĐGTĐ — ghi Dev Book từng lần đổi giá trị.

---

**✍️ Phán quyết của PM:** ☑ **Duyệt nguyên trạng** *(v1.1 — hai tầng định nghĩa + 5 design rule)* · ⬜ Duyệt có chỉnh · ⬜ Bác — *Ngày:* **2026-09-23** *(tuyên bố trong phiên — ký tay khi in hồ sơ viva)*
