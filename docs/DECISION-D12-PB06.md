# DECISION-D12-PB06 — Chốt phương án Job Worker (N5)
### Quyết định một trang · lật điều kiện DoR **D12** · giải [PROPOSAL] tại ARCH §4.4

> **Phiên bản:** 1.0 · **Ngày:** 2026-09-22 · **Trạng thái:** ✅ **APPROVED** — PM duyệt nguyên trạng (C + 4 design rule) 2026-09-22 *(tuyên bố trong phiên · hồ sơ: `DEVBOOK` DB-22)*
> **Input:** `ARCH-PB06.md` v1.5 §4.4 (interface 202+poll đã **LOCK** — bất biến với mọi phương án) · `WBS` v1.1 W1-14 · `EST` v1.1 (giả định W1-14) · `RISK` v1.1 C1/C5
> **Người quyết:** PM kiêm vai Tech Lead *(solo — như tiền lệ D11/N6, minh bạch vai kiêm)*

---

## 1. Ba phương án — đặt trong bối cảnh solo

| | **A — Celery + Redis** | **B — Job framework của SaaS** | **C — FastAPI BackgroundTasks** |
|---|---|---|---|
| Hạ tầng thêm | Redis/broker + worker process riêng | Không (dùng đồ sẵn) | **Không — chạy trong chính AI service** |
| Công học/dựng | ~1–2 ngày dựng + vận hành | Phải học framework của SaaS | **~0 — vài chục dòng** |
| Độ bền job | ✅ Persist, retry, survive restart | Tuỳ SaaS | ⚠️ Job chết theo process, không retry |
| Song song hoá | ✅ Nhiều worker | Tuỳ SaaS | Giới hạn trong 1 process |
| Hợp Wave 1 (slice + đo p95) | Thừa cho 1 người dùng | — | ✅ Đủ và rẻ nhất |

**B tự loại trong bối cảnh solo:** không có SaaS thật thì "job framework của SaaS" không có vật tham chiếu — chọn B hôm nay là chọn một thứ không tồn tại. Ghi lại làm ứng viên tái xét **khi cắm SaaS thật** (§4). Bài toán còn lại là **A vs C**.

## 2. Đề xuất: **C cho Wave 1** — được phép chọn rẻ VÌ interface đã bất biến

Lý do cốt lõi: hợp đồng `202 + poll` đã LOCK nghĩa là client **không bao giờ biết** đằng sau là BackgroundTasks hay Celery — nâng cấp C → A sau này là chuyện nội bộ AI service, **không chạm contract, không chạm FE**. Chính vì đường lui rẻ nên chọn khởi đầu rẻ là hợp lý; nếu không có bất biến đó, C sẽ là món nợ.

**Bốn design rule bắt buộc đi kèm (điều kiện của chữ "duyệt"):**

1. **Trạng thái job sống ở DB** (`analysis_jobs`), không ở RAM — poll đọc DB, nên process nào trả lời cũng đúng.
2. **Stale-job sweep:** job ở `processing` quá **10 phút** → tự chuyển `failed` + `error_code='job_timeout'` — bịt ca process chết giữa chừng để job không treo "processing" vĩnh viễn (job *được phép* failed; result thì không — ARCH v1.4).
3. **Interface và JSON của 4.3/4.4 không đổi một ký tự** khi sau này thay worker.
4. **Trigger nâng cấp lên A — đo được, không cảm tính:** cần chạy >1 phân tích song song ổn định (multi-user thật) · hoặc cần retry/durability theo yêu cầu vận hành · hoặc p95 fail vì tuần tự hoá trong khi từng job vẫn nhanh. Chạm bất kỳ trigger nào → dựng Celery, ghi Dev Book, không vá cơi nới.

## 3. Hệ quả khi duyệt

D12 lật **PASS** → W1-14 hết chặn (khung async dựng bằng C ngay). **Lệch giả định EST ghi nhận minh bạch:** EST v1.1 W1-14 giả định *"chốt option A"* — quyết định này chọn C, effort **≤** ước lượng cũ (1.13 MD) nên con số giữ nguyên, lệch ghi tại đây + Dev Book thay vì đẩy version EST vì một dòng. [PROPOSAL] tại ARCH §4.4 coi như **đã giải bằng văn bản này**; gộp chú thích vào ARCH ở lần lên version kế tiếp.

## 4. Điều kiện mở lại

Chạm trigger §2.4 → nâng A. Cắm SaaS thật → tái xét B (dùng hạ tầng job sẵn có của họ có thể rẻ hơn vận hành Celery riêng).

---

**✍️ Phán quyết của PM:** ☑ **Duyệt nguyên trạng (C + 4 design rule)** · ⬜ Duyệt có chỉnh · ⬜ Chọn A ngay — *Ngày:* **2026-09-22** *(tuyên bố trong phiên — ký tay khi in hồ sơ viva)*
