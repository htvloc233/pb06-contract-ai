# DECISION-D11-PB06 — Chốt tên role SaaS & mapping permission AI
### Quyết định một trang · lật điều kiện DoR **D11** (N1)

> **Phiên bản:** 1.0 · **Ngày:** 2026-09-21 · **Trạng thái:** ✅ **APPROVED** — PM duyệt nguyên trạng 2026-09-21 *(tuyên bố trong phiên · hồ sơ: `DEVBOOK` DB-19)*
> **Input:** `ARCH-PB06.md` v1.4 §6 (mapping ví dụ, ghi chú "cần xác nhận team SaaS") · `SPEC-PB06.md` v1.1 §2 + NFR-A1/A2 · `DOR-PB06.md` D11
> **Người quyết:** PM — với tư cách **product owner của SaaS trong kịch bản** *(chế độ solo/Customer-Zero: không có team SaaS thật; quyết định này thay cho bước "xác nhận với team SaaS" của N1, ghi minh bạch thay vì lặng lẽ bỏ qua)*

---

## 1. Quyết định

**Năm role chính thức** — dùng đúng các tên này trong code, test và tài liệu từ nay:

| SaaS role | Phạm vi gắn | AI permission (ARCH 6.2) | Được làm | Bị chặn |
|---|---|---|---|---|
| `contract_owner` | **theo từng hợp đồng** | `contract:write` | Chạy AI · sửa 6 trường (kể cả tóm tắt, 4.8b) · approve · re-analyze · xem draft+approved · upload/tạo HĐ mới | — |
| `contract_editor` | theo từng hợp đồng | `contract:write` | Như owner (kể cả upload/tạo HĐ mới) | — |
| `contract_viewer` | theo từng hợp đồng | `contract:read` | Xem **chỉ bản `approved`** + source excerpt | Trigger · sửa · approve · re-analyze · xem draft (**404**, không phải 403 — chống lộ tồn tại) |
| `pm_admin` | **toàn cục** | `contract:read` + `audit:read` | Xem approved mọi HĐ · query audit log | Sửa/approve thay user (UC-03 ma trận SPEC §5.0) |
| `system:ai_service` | internal | `system:ai_service` | Gọi nội bộ qua Gateway | Mọi endpoint public |
| *(không có role trên HĐ)* | — | `contract:none` | — | Mọi thứ → 403/**404** |

## 2. Ba quyết định con — chỗ ARCH để mở, nay chốt

| # | Câu hỏi mở | Chốt | Căn cứ |
|---|---|---|---|
| Q1 | Quyền gắn toàn cục hay theo hợp đồng? | **Theo từng hợp đồng** cho owner/editor/viewer (đọc từ bảng phân quyền HĐ sẵn có của SaaS); `pm_admin` toàn cục | NFR-A2 *"kế thừa phân quyền hợp đồng hiện tại"* — chọn per-contract vì đó là mô hình phổ biến của SaaS quản lý HĐ và là ca **chặt hơn**; nếu SaaS thật đơn giản hơn thì nới xuống rẻ, làm ngược lại thì đắt |
| Q2 | Ai được upload/tạo HĐ mới (AC-02-3)? | `contract_owner` + `contract_editor`; `contract_viewer` bị 403 và ẩn nút upload | US-02, AC-02-3 |
| Q3 | Approve có tách quyền riêng không? | **Không tách trong MVP** — approve thuộc `contract:write` | Khớp ARCH 6.2; tách approve-riêng là permission mới → chạm scope, để Post-MVP nếu khách thật đòi |

## 3. Ràng buộc kế thừa (nhắc lại, không định nghĩa mới)

L0-Auth đọc role từ JWT/session SaaS và **resolve theo `contract_id` từng request** (NFR-A1/A2); không tạo hệ permission mới. Nhãn tin cậy, trạng thái trường, human gate không đổi — R7 (AI tự approve) vẫn **L5 không cấp** bất kể role.

## 4. Điều kiện mở lại quyết định này

- Cắm vào một SaaS **thật** → mapping phải re-verify với team sở hữu SaaS đó; quyết định này chỉ có hiệu lực trong phạm vi capstone/kịch bản.
- OI-01 trả lời **Yes** (external parties) → thêm role ngoài = mở lại scope theo A1, không vá tay vào bảng trên.

## 5. Hệ quả khi PM duyệt

D11 lật **PASS** trong `DOR` (kèm dòng bằng chứng trỏ file này) → **W1-01 hoàn thành** → W1-02 (L0-Auth resolver) đủ điều kiện start theo luật tiền-đề. File này commit vào `docs/` qua **một vòng PR** (đường duy nhất vào `main`).

---

**✍️ Phán quyết của PM:** ☑ **Duyệt nguyên trạng** · ⬜ Duyệt có chỉnh · ⬜ Bác — *Ngày:* **2026-09-21** *(tuyên bố trong phiên — ký tay khi in hồ sơ viva)*
