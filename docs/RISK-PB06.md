# RISK-PB06 — Risk Register (MVP)
### AI Tóm Tắt & Trích Xuất Hợp Đồng

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-06
> **Input:** `EST-PB06.md` **v1.1** · `WBS-PB06.md` **v1.1** · `ARCH-PB06.md` **v1.4** · `SPEC-PB06.md` **v1.1** · `SCOPE-PB06.md` **v3.2** · `DEVBOOK` DB-01→15
> **Trạng thái:** ✅ **Có hiệu lực** — đã qua cổng hiểu bước [6] ngày 2026-09-06 (hồ sơ: `DEVBOOK` DB-16)
> Artefact bước **[6a] Risk** · Capstone Playbook · drill EX-04
> **Nguyên tắc:** mitigation phải có **cổng kiểm được** (máy chạy hoặc thủ tục có chữ ký) — mitigation chỉ là lời hứa thì không tính.

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.1** | 2026-09-06 | Thêm **A7 — AI báo "passed ảo"** (nguồn: PM bắt tại cổng hiểu [6], DB-16); cổng = kênh bằng chứng artifact-của-runner. Register lên 15 rủi ro. |
| **1.0** | 2026-09-06 | Bản đầu: 14 rủi ro / 3 nhóm (A rủi-ro-AI bắt buộc · B dữ liệu-pháp lý · C delivery), thang L×I 5×5, điểm inherent + residual sau cổng, Top-5, nhịp vận hành register. Nguồn: risk nền từ phân tích đề + phát sinh qua DB-01→15 (C4 do chính PM phát hiện tại cổng [5]). |

---

## 1. Thang đo

**L (Likelihood)** 1–5: 1 hiếm · 3 có thể · 5 gần chắc chắn. **I (Impact)** 1–5: 1 khó chịu · 3 trễ sprint/lỗi phải sửa · 5 mất trust khách hàng / vi phạm pháp lý / trượt go-no-go.
**Điểm = L×I** (inherent — trước cổng). **Residual** = mức còn lại *sau khi* cổng chạy: 🟢 thấp · 🟡 trung bình · 🔴 cao.
Ngưỡng hành động: ≥15 = theo dõi hằng tuần, có owner tên riêng; 8–14 = review 2 tuần/lần; <8 = ghi nhận.

---

## 2. NHÓM A — Rủi ro AI *(bắt buộc theo EX-04)*

| ID | Rủi ro | L | I | Điểm | Mitigation + **CỔNG kiểm được** | Residual |
|---|---|:-:|:-:|:-:|---|:-:|
| **A1** | **AI bịa giá trị trường** — trả về ngày/số tiền/tên bên không có trong hợp đồng | 4 | 5 | **20** | Validator D6-a (W1-13): span phải khớp **verbatim** + parse đúng kiểu; **CỔNG:** transaction 8 bước — validate fail → ROLLBACK toàn bộ, không có đường ghi nửa vời (ARCH 3.4) | 🟢 |
| **A2** | **Tóm tắt sai nghĩa vụ/chế tài** — nguy hơn A1 vì câu sai đọc mượt, người khó phát hiện hơn ô dữ liệu sai | 3 | 5 | **15** | D6-b (W1-20): câu dữ kiện không neo bị CẮT, không viết mềm; **CỔNG:** không đủ nghĩa → `insufficient_grounding`, UI hiện nhãn **thay** tóm tắt (AC-04-5) — thà không có tóm tắt còn hơn tóm tắt trôi | 🟡 |
| **A3** | **Prompt injection trong chính hợp đồng** — đối tác nhúng chỉ dẫn vào PDF để làm sai trích xuất / giấu điều khoản phạt | 2 | 5 | **10** | Text tài liệu = **dữ liệu, không phải chỉ thị**; output theo schema cứng; span verification bắt phần lớn (giá trị bị lái vẫn phải có span khớp); **CỔNG:** bộ test negative F-09 có ≥3 mẫu injection, fail → không ship | 🟡 |
| **A4** | **Rubber-stamping tầng người dùng** — nhân viên duyệt bừa kết quả AI, human gate thành hình thức | 4 | 4 | **16** | Thiết kế precision>recall (thà trống hơn đoán — trống thì người phải điền, sai thì người dễ gật); nhãn tin cậy chỉ trên `grounded` (A6); **CỔNG-tín-hiệu:** audit log ghi thời gian duyệt — duyệt 6 trường <10s bị gắn cờ cho PM xem (thêm vào F-09) | 🟡 — hành vi người, cổng chỉ giảm |
| **A5** | **LLM variance phá estimate W1-20/W1-13** (P/O 4× — xác nhận bởi team tham khảo) | 3 | 4 | **12** | **CỔNG:** timebox 3 ngày cho W1-20 — chưa hội tụ thì hạ heuristic v1 (mọi câu có số/ngày/tên = dữ kiện; over-flag chấp nhận được vì fail-closed lệch về phía chặt) — quyết định ghi Dev Book, không gia hạn im lặng | 🟡 |
| **A6** | **Accuracy không đạt mức người duyệt chấp nhận** → go/no-go fail cuối kỳ | 3 | 5 | **15** | **CỔNG:** F-06 chạy eval trên gold set **giữa S4**, không đợi cuối — số xấu ở S4 còn 3 tuần xử lý, số xấu ở S7 là tin buồn không thuốc | 🟡 — phụ thuộc N4 |
| **A7** | **AI báo "passed ảo"** — khai xanh mà không chạy / chạy thiếu / sửa test cho xanh *(nguồn: PM bắt tại cổng [6] — DB-16)* | 2 | 4 | **8** | **CỔNG:** kết quả test chỉ tính theo **artifact của runner** (exit code + report máy sinh), không theo lời AI; cấm sửa test/lint cùng lượt chạy (Delegation #7/#8); spot-check đối chiếu report ↔ log | 🟢 |

---

## 3. NHÓM B — Dữ liệu & Pháp lý

| ID | Rủi ro | L | I | Điểm | Mitigation + **CỔNG** | Residual |
|---|---|:-:|:-:|:-:|---|:-:|
| **B1** | **Nội dung hợp đồng rời vùng cho phép** — chuyển dữ liệu cá nhân xuyên biên giới không căn cứ (Luật BVDLCN 91/2025/QH15, phạt tới 3 tỷ) | 4* | 5 | **20** | Egress guard whitelist, **mặc định ĐÓNG** (W1-11); build chạy synthetic tới khi OI-02 chốt (W1-06); nếu external → hồ sơ ĐGTĐ **trước khi mở cờ** (F-08); **CỔNG:** egress test tự động trong CI — request ngoài whitelist bị chặn = test pass (DoD-4) | 🟢 |
| **B2** | **Text thô hợp đồng bị persist trái D4** — dev "tiện tay" cache/log | 2 | 4 | **8** | **CỔNG:** DB schema audit trong F-09 — không cột nào ngoài danh mục ARCH được chứa text nguồn; audit log cấm source_excerpt (NFR-S6), truncate 500 ký tự | 🟢 |
| **B3** | **Lộ draft/lộ sự tồn tại draft cho read-only** | 2 | 3 | **6** | 404-not-403 (ARCH 6.2); **CỔNG:** test phân quyền theo role trong F-09/E-01 phủ mọi endpoint đọc | 🟢 |

*\*L của B1 tính ở trạng thái KHÔNG có guard — lý do phải build guard trước khi gọi model thật.*

---

## 4. NHÓM C — Delivery & Vận hành

| ID | Rủi ro | L | I | Điểm | Mitigation + **CỔNG** | Residual |
|---|---|:-:|:-:|:-:|---|:-:|
| **C1** | **SPOF AI engineer** — 100%/98% tải hai wave liên tiếp, mọi lệch đuôi bi quan ăn thẳng critical path | 4 | 5 | **20** | San W1-11→BE (đã áp EST v1.1); prompt/schema là **artefact có review**, không nằm trong đầu một người; pair AI–BE 1 buổi/tuần để truyền kiến thức; **CỔNG:** tải AI >110% hai tuần liên tiếp → bắn trigger T2 của EST (thủ tục mở scope) — có ngưỡng số, không cãi cảm tính | 🔴→🟡 |
| **C2** | **Gold set trễ / không có owner** — ❗ đến hôm nay vẫn chưa có tên | 4 | 4 | **16** | W1-08 chốt owner + lịch tuần 1; đợt 1 (10 HĐ) tuần 2, đủ 30 trước S4; **CỔNG:** F-06 và benchmark F-02 **không bắt đầu** nếu chưa đủ nguyên liệu — chặn cứng, để độ trễ hiện hình thay vì âm thầm chạy trên 3 hợp đồng | 🔴 tới khi có tên |
| **C3** | **Lỗi lọt do không có QA chuyên trách** | 3 | 4 | **12** | Thuế 0-QA hiện hình ở F-09 (PM soạn ca, dev chạy chéo); test tự động hoá tối đa từ Wave 1 (egress, append-only, validator); đề xuất xin QA part-time S5–S7 gửi kèm weekly; **CỔNG:** DoD chỉ nghiệm thu bằng test chạy được, không nghiệm thu bằng "đã kiểm tay" | 🟡 |
| **C4** | **ARCH review đổi shape API sau khi FE build** *(nguồn: PM bác W1-03 tại cổng [5] — DB-15)* | 3 | 4 | **12** | G8: skeleton làm ngay, **LOCK contract chỉ sau N6**; **CỔNG:** FE không merge code gọi endpoint chưa LOCK — kiểm ở review checklist | 🟢 |
| **C5** | **p95 vượt 30s** (DoD-1 vs D6-b cạnh tranh ngân sách) | 3 | 3 | **9** | **CỔNG:** phép đo bắt buộc W1-22 tại Slice 1b + trigger T1 đã chốt đòn bẩy (tóm tắt 120 từ) — biết ở tuần 3, không phải tuần 7 | 🟢 |
| **C6** | **Phụ thuộc ngoài (N1–N6) trễ dây chuyền** — loại việc trễ nhất vì không nằm trong standup của ai | 4 | 3 | **12** | Bảng N1–N6 theo dõi riêng (WBS §7), escalation có văn bản + hạn (W1-07); **CỔNG:** mỗi N có deadline; quá hạn 3 ngày → nâng lên sponsor, không chờ thêm im lặng | 🟡 |

---

## 5. TOP-5 — theo điểm inherent

| # | ID | Rủi ro | Điểm | Vì sao đứng đây |
|---|---|---|:-:|---|
| 1 | **B1** | Dữ liệu rời vùng cho phép | 20 | Impact pháp lý có định lượng tài chính + không đảo ngược được; cổng mạnh nhất register (egress fail-closed) nên residual 🟢 — nhưng inherent phải nhớ để **không ai tắt guard "cho tiện test"** |
| 2 | **A1** | AI bịa giá trị trường | 20 | Đánh thẳng vào lý do sản phẩm tồn tại; cổng D6-a là trái tim kiến trúc |
| 3 | **C1** | SPOF AI engineer | 20 | Rủi ro duy nhất trong top không cổng-hoá triệt để được — người không phải config; residual cao nhất top-5 |
| 4 | **C2** | Gold set không owner | 16 | Đang **hiện hành**, không phải giả định — L thực tế hôm nay là 4 vì chưa có tên |
| 5 | **A4** | Rubber-stamping người dùng | 16 | Rủi ro "đệ quy" của đề: sản phẩm chống duyệt-bừa mà để người dùng duyệt bừa thì thất bại về nghĩa |

---

## 6. Vận hành register

- Review **hằng tuần** cho mục ≥15 (gắn weekly report), 2 tuần/lần cho 8–14; mỗi mục ≥15 phải có **owner tên riêng** — hiện C1/C2 owner là PM cho tới khi phân lại.
- Trigger nâng hạng: sự kiện thật xảy ra (đo được/quan sát được), không nâng theo cảm giác; mọi thay đổi điểm ghi lý do một dòng.
- Rủi ro mới phát hiện giữa sprint → vào register trong ngày, không đợi họp — mẫu C4 (từ phản bác của PM) là tiền lệ đúng.

---

*RISK-PB06 v1.0 · `draft_ai` — hiệu lực sau cổng hiểu bước [6]. Mitigation không có cổng kiểm được = chưa được tính là mitigation.*
