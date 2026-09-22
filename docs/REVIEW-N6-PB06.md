# REVIEW-N6-PB06 — Biên bản Architecture Review
### ARCH-PB06 · một trang

> **Ngày:** 2026-09-21 · **Đối tượng:** `ARCH-PB06.md` v1.4 → **v1.5**
> **Reviewer:** PM kiêm vai Tech Lead *(chế độ solo/Customer-Zero — ghi minh bạch; đạt qua cổng hiểu [3] có Coach-AI chấm, không tự đóng dấu)* · Hồ sơ chấm: `DEVBOOK` DB-20
> **Verdict:** ✅ **APPROVE with fix** — một phát hiện, đã vá tại v1.5

---

## 1. Câu cổng #1 — Stack (đạt vòng 1)

Reviewer bảo vệ 3 quyết định bằng phương án bị loại:

| Chọn | Thay vì | Nếu chọn vế kia thì hỏng |
|---|---|---|
| AI service FastAPI tách riêng | Viết thẳng vào SaaS backend | Lỗi/tải AI kéo sập SaaS đang nuôi khách (NFR-AV1); mất scale + release độc lập |
| Polling 202+poll | WebSocket/SSE | Thêm hạ tầng cho một trạng thái đơn giản; phục hồi sau rớt mạng phức tạp hơn — poll tiếp là xong |
| PostgreSQL thuần | + Vector DB | MVP là **exact evidence grounding** — similarity trả đoạn *"giống giống"*, **ngược thiết kế** D6-a (đòi verbatim); scope truy trong 1 hợp đồng, và D4 không persist text ⇒ không có corpus để index |

## 2. Câu cổng #2 — Độ nhạy (đạt vòng 2)

- Vòng 1: `field_key` — **không đạt**: nhầm *cái khoá* với *cái giá trị* (enum tên cột giống nhau mọi hợp đồng, không mang thông tin). Bài học schema-vs-data ghi DB-20.
- Vòng 2: **đạt** — bắt `analysis_jobs.error_detail_ref` gắn nhãn hai mặt *"Internal/Confidential"*: nhãn không chọn phe ⇒ mỗi dev tự chọn phe hộ, lọt qua security review.

**Fix (v1.5):** chốt **Confidential** theo nguyên tắc *nhãn con trỏ đi theo cái nó mở được* + 2 design rule: không trả ref ra client API; secure log đích tự gác mức Restricted-capable — không cam kết được thì ref ăn nhãn đích.

## 3. Hệ quả

| | |
|---|---|
| ARCH | v1.5 — **Approved** |
| API contract §4 | 🔒 **LOCKED 2026-09-21** (G8): FE được merge code gọi endpoint; đổi shape = mở lại review |
| DoR | **D4 ✅ · D5 ✅** — lớp 🟠 còn D8 (staging) · D9 (egress) · D10 (synthetic) · D12 (worker) |
| Điều kiện mở lại | Cắm SaaS thật → re-review §6 permission cùng DECISION-D11; OI-02 chốt external → rà lại LLM runtime box |

---

**✍️ Reviewer xác nhận:** ☑ Approve with fix — 2026-09-21 *(tuyên bố trong phiên; ký tay khi in hồ sơ viva)*
