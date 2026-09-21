# DOR-PB06 — Definition of Ready · Lát cắt dọc đầu tiên
### AI Tóm Tắt & Trích Xuất Hợp Đồng (MVP)

> **Phiên bản:** 1.0 · **Ngày:** 2026-09-06
> **Input:** `SCOPE` v3.2 ✅ · `SPEC` v1.1 ✅ · `MODULEMAP` v1.2 · `ARCH` v1.4 *(chờ N6)* · `WBS` v1.1 · `EST` v1.1 · `RISK` v1.1 · `DELEGATION-MAP` v1.1 · `DEVBOOK` DB-01→16
> **Trạng thái:** ✅ **Có hiệu lực** — đã qua cổng hiểu bước [7] ngày 2026-09-06, qua sạch (hồ sơ: `DEVBOOK` DB-17). Nhịp rà: mỗi standup Sprint 0 tới khi lớp 🔴/🟠 sạch
> **Phạm vi:** DoR cho **Slice 1** (trường ① end-to-end) và **Slice 1b** (tóm tắt + neo-theo-câu + đo p95) — KHÔNG phải DoR cho cả MVP.
> Artefact bước **[7] Definition of Ready** · Capstone Playbook
> **Luật đọc bảng:** trạng thái chỉ có PASS/FAIL — *chưa xác minh = FAIL* (fail-closed áp cho chính checklist). FAIL không phải tin xấu; FAIL vô hình mới là tin xấu.

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.0** | 2026-09-06 | Bản đầu: 18 điều kiện / 5 nhóm — **7 PASS · 11 FAIL**, mỗi FAIL gắn task giải quyết + owner + hạn + phạm vi chặn; phân loại FAIL 3 lớp; DoR riêng cho Slice 1b; kết luận *chưa Ready — đủ điều kiện khởi động Sprint 0 theo luật tiền-đề*. |

---

## 1. Checklist — 18 điều kiện

### A. Đặc tả & kế hoạch

| # | Điều kiện | Trạng thái | Căn cứ / Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D1 | SCOPE v3.2 signed off (D6-a/b + A6) | ✅ PASS | Sign-off 2026-09-06 |
| D2 | SPEC v1.1 signed off; AC của slice (AC-01-1→3 · AC-03-1/2 · AC-05-3 · AC-15-1a) đọc lên nói được ca nào pass/fail | ✅ PASS | Sign-off 2026-09-06; AC đã qua cổng [1] |
| D3 | Slice định nghĩa xong + ranh giới thang S3 chốt (không mạ vàng bản mỏng) | ✅ PASS | MODULEMAP v1.2 §7 + WBS v1.1 |
| D4 | ARCH v1.4 qua **Architecture Review** (N6) | ❌ FAIL | Tech Lead review — hạn Sprint 0–1. Chặn: **D5**. Không chặn: skeleton (W1-03), migration draft (W1-04) — đã tách bởi G8 |
| D5 | API contract **LOCKED** | ❌ FAIL | Theo D4. Chặn: **FE merge code gọi endpoint** (cổng C4); FE vẫn build local trên spec draft |
| D6 | Kế hoạch + ước lượng hiệu lực (WBS v1.1 · EST v1.1 · trigger T1/T2 chốt sẵn) | ✅ PASS | Cổng [4][5] đã đóng |

### B. Môi trường & dữ liệu

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D7 | Repo + CI + quyền truy cập đủ cho cả 4 người | ❌ FAIL *(chưa xác minh)* | BE xác nhận **ngày 1 Sprint 0**. Chặn: mọi task code |
| D8 | Staging sẵn sàng (G5 của EST) | ❌ FAIL *(chưa xác minh)* | BE xác nhận với platform, hạn trong Sprint 0. Chặn: W1-18 ghép slice · W1-22 đo p95 |
| D9 | Egress control khả thi trên hạ tầng SaaS (tiền đề W1-11) | ❌ FAIL *(chưa xác minh)* | BE spike nửa buổi Sprint 0. Chặn: W1-11; nếu hạ tầng không cho app-level egress → đuôi P của W1-11 kích hoạt |
| D10 | Bộ 5 hợp đồng synthetic sẵn (W1-06) — **nhiên liệu hợp pháp duy nhất** khi OI-02 chưa chốt | ❌ FAIL | PM soạn tuần 1 (0.5d). Chặn: W1-12 trở đi (mọi việc cho model ăn dữ liệu) |

### C. Con người & quyết định

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D11 | Tên role SaaS thật + mapping permission chốt (N1) | ❌ FAIL | W1-01 — **ngày 1 Sprint 0**, PM+BE. Chặn: W1-02 |
| D12 | Job worker option chốt (N5) | ❌ FAIL | Tech Lead, hạn Sprint 1. Chặn: W1-14; interface 202+poll bất biến nên FE không chờ |
| D13 | **Owner gold set có TÊN** (N4) | ❌ FAIL — *nhắc lần 6* | PM chốt với pháp chế tuần 1 (W1-08). **Không chặn Slice 1**; chặn: lịch gán nhãn tuần 2 → dây chuyền F-02 benchmark · F-06 eval · A6/C2 của RISK |
| D14 | Đội hình giữ nguyên 8 tuần (A7/G3) | ✅ PASS | SCOPE signed; điều kiện mở lại scope nếu vỡ |

### D. Pháp lý & dữ liệu nhạy

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D15 | OI-02 (external LLM / self-host) trả lời | ❌ FAIL | Legal/Security, hạn trước hết Sprint 0. **Không chặn slice** — D5 của SCOPE đã cách ly (synthetic + egress đóng). Chặn: mở cờ external · E-02 UAT hợp đồng thật · F-08 |
| D16 | OI-01 (external parties) trả lời | ❌ FAIL | Product Owner, hạn trước hết Sprint 0. Không chặn MVP scope hiện tại; nếu Yes → mở lại scope (A1) |

### E. Quy trình & kỷ luật

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D17 | Delegation Map hiệu lực — cả team biết leash từng loại việc, 3 luật cứng, kênh bằng chứng test (#8) | ✅ PASS | v1.1, cổng [6] đóng; brief team ở kickoff Sprint 0 |
| D18 | Dev Book + telemetry đang chạy nhịp thật (không viết bù) | ✅ PASS | 16 mục, ghi cùng nhịp việc từ đầu |
| — | Rủi ro điểm ≥15 có **owner tên riêng** | ❌ FAIL *(soft)* | C1/C2 đang tạm PM; giải quyết cùng D13. Không chặn build; chặn chất lượng vận hành register |

---

## 2. Phân loại 11 FAIL — không phải FAIL nào cũng chặn như nhau

| Lớp | Mục | Ý nghĩa |
|---|---|---|
| 🔴 **Chặn ngày-1** | D7 (repo/CI) · D11 (role names) | Chưa xanh thì task code đầu tiên không start. Cả hai có resolving task xếp đúng ngày 1 |
| 🟠 **Chặn trong Sprint 0–1** | D4 · D5 · D8 · D9 · D10 · D12 | Có việc khác làm trong lúc chờ; mỗi mục có task + owner + hạn. Quá hạn → escalation N-list, không chờ im lặng |
| 🟡 **Không chặn slice — deadline riêng** | D13 · D15 · D16 · owner risk | Slice chạy được mà không có chúng, **nhưng Wave 2 thì không** — để trễ là mượn nợ của chính mình ba tuần sau |

---

## 3. Kết luận DoR

**Slice 1 hôm nay: CHƯA READY.** Và đó là câu trả lời đúng — DoR tồn tại để 11 cái FAIL này **hiện hình trước dòng code đầu tiên**, thay vì hiện hình ở tuần 3 dưới dạng "ơ, tưởng có staging rồi".

**Đủ điều kiện KHỞI ĐỘNG Sprint 0** theo **luật tiền-đề** (fail-closed áp vào lịch):

> Task chỉ được start khi **mọi điều kiện DoR nó phụ thuộc đã PASS**. FAIL còn đó thì task tương ứng đứng yên và độ trễ được nhìn thấy — không có "làm tạm trên giả định rồi tính".

Nhịp cập nhật: bảng này rà lại **mỗi standup Sprint 0** cho tới khi lớp 🔴 và 🟠 sạch; mỗi mục lật PASS ghi ngày + bằng chứng một dòng.

---

## 4. DoR riêng cho Slice 1b — 3 điều kiện

| # | Điều kiện | Vì sao |
|---|---|---|
| B1 | Slice 1 **xanh end-to-end trên staging** (W1-18) | 1b đo trên nền 1 — đo trên nền lung lay là số rác |
| B2 | Bộ synthetic có **≥1 hợp đồng ~20 trang** đúng chuẩn đo (điều kiện của DoD-1 p95) | Không có thì phép đo W1-22 không so được với ngưỡng 30s |
| B3 | Đòn bẩy T1 (200→120 từ) còn nguyên hiệu lực, người quyết có mặt khi đo | Đo xong phải quyết ngay và ghi Dev Book — số để qua đêm là số nguội |

---

*DOR-PB06 v1.0 · `draft_ai` — hiệu lực sau cổng hiểu bước [7]. FAIL trong bảng này là tài sản: mỗi cái là một sự cố tuần 3 được trả trước với giá tuần 1.*
