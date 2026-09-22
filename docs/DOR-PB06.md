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
| *(cập nhật)* | 2026-09-22 | **D9 lật PASS** — egress guard + 6 test, hai môi trường xanh, cổng sống trong CI (DB-23). Bảng: **14 PASS · 4 FAIL**; 🟠 còn duy nhất **D8** |
| *(cập nhật)* | 2026-09-22 | **D12 lật PASS** — DECISION-D12 duyệt nguyên trạng: option C + 4 design rule (DB-22). Bảng: **13 PASS · 5 FAIL**; 🟠 còn D8 · D9 |
| *(cập nhật)* | 2026-09-22 | **D10 lật PASS** — bộ synthetic + answer key, PM review duyệt (DB-21). Bảng: **12 PASS · 6 FAIL**; 🟠 còn D8·D9·D12 |
| *(cập nhật)* | 2026-09-21 | **D4 + D5 lật PASS** — N6 đạt (PM kiêm Tech Lead, cổng [3] có chấm, DB-20) → contract LOCK theo G8. Bảng: **11 PASS · 7 FAIL**; 🟠 còn D8·D9·D10·D12 |
| *(cập nhật)* | 2026-09-21 | **D11 lật PASS** — `DECISION-D11-PB06.md` duyệt nguyên trạng (DB-19). **Lớp 🔴 = 0**. Bảng: **9 PASS · 9 FAIL** |
| *(cập nhật)* | 2026-09-21 | **D7 lật FAIL → PASS** bằng hành vi + bằng chứng xác minh (repo/CI/hàng rào/PR — DB-18). Lớp 🔴 còn **D11**. Bảng: 8 PASS · 10 FAIL |
| **1.0** | 2026-09-06 | Bản đầu: 18 điều kiện / 5 nhóm — **7 PASS · 11 FAIL**, mỗi FAIL gắn task giải quyết + owner + hạn + phạm vi chặn; phân loại FAIL 3 lớp; DoR riêng cho Slice 1b; kết luận *chưa Ready — đủ điều kiện khởi động Sprint 0 theo luật tiền-đề*. |

---

## 1. Checklist — 18 điều kiện

### A. Đặc tả & kế hoạch

| # | Điều kiện | Trạng thái | Căn cứ / Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D1 | SCOPE v3.2 signed off (D6-a/b + A6) | ✅ PASS | Sign-off 2026-09-06 |
| D2 | SPEC v1.1 signed off; AC của slice (AC-01-1→3 · AC-03-1/2 · AC-05-3 · AC-15-1a) đọc lên nói được ca nào pass/fail | ✅ PASS | Sign-off 2026-09-06; AC đã qua cổng [1] |
| D3 | Slice định nghĩa xong + ranh giới thang S3 chốt (không mạ vàng bản mỏng) | ✅ PASS | MODULEMAP v1.2 §7 + WBS v1.1 |
| D4 | ARCH qua **Architecture Review** (N6) | ✅ **PASS** *(2026-09-21)* | **Bằng chứng:** review bởi PM kiêm Tech Lead (solo, minh bạch), qua cổng hiểu [3] có chấm — câu stack đạt vòng 1 (blast radius · polling · *exact evidence grounding* vs vector DB), câu độ nhạy đạt vòng 2 (bắt nhãn hai mặt `error_detail_ref`, vá ở **ARCH v1.5**). Biên bản: `REVIEW-N6-PB06.md` · DB-20 |
| D5 | API contract **LOCKED** | ✅ **PASS** *(2026-09-21)* | LOCK ghi tại ARCH v1.5 §4 (theo G8). FE chính thức được merge code gọi endpoint; đổi shape từ nay = mở lại review |
| D6 | Kế hoạch + ước lượng hiệu lực (WBS v1.1 · EST v1.1 · trigger T1/T2 chốt sẵn) | ✅ PASS | Cổng [4][5] đã đóng |

### B. Môi trường & dữ liệu

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D7 | Repo + CI + quyền truy cập đủ cho cả 4 người | ✅ **PASS** *(2026-09-21)* | **Bằng chứng:** ① repo public đúng cấu trúc, commit #1 = bộ artefact — `github.com/htvloc233/pb06-contract-ai` *(AI xác minh độc lập)* · ② CI xanh — run `35555468221`, Status **Success**, job lint-test *(AI xác minh độc lập)* · ③ push thẳng `main` bị chặn `GH006 — Changes must be made through a pull request` — hàng rào **từng sập vì (a) Private+Free không enforce**, sửa bằng chuyển Public, kiểm lại bằng cú push cố tình thất bại *(output dán trong phiên)* · ④ vòng PR #1 trọn vẹn — PR + CI xanh trên PR *(AI xác minh)*, cú Merge *(ghi nhận theo tuyên bố PM 2026-09-21; kênh xác minh tự động bị cache/robots chặn — PM tự kiểm README hiển thị trên main)* · ⑤ `.env` chặn bởi `.gitignore` + `test_no_env_committed` trong run Success. **Diễn giải solo:** "4 người" theo đội thật — học viên (Coach thêm quyền khi tham gia review). Chi tiết: `DEVBOOK` DB-18 |
| D8 | Staging sẵn sàng (G5 của EST) | ❌ FAIL *(chưa xác minh)* | BE xác nhận với platform, hạn trong Sprint 0. Chặn: W1-18 ghép slice · W1-22 đo p95 |
| D9 | Egress control khả thi (tiền đề W1-11) | ✅ **PASS** *(2026-09-22)* | **Bằng chứng 3 mắt xích, xác minh độc lập:** ① guard thật `src/egress_guard.py` (mặc định đóng · chỉ https · không suy subdomain · bị chặn thì transport không bị chạm) — **6/6 test PASS trên máy PM** (Python 3.8, output dán trong phiên) · ② **CI run `35763287927` Success trên `main`** — job `egress-test` xanh (AI fetch xác minh) · ③ run chính là commit merge PR #6 ⇒ **merge đã xác minh**. Cổng DoD-4/B1 từ nay sống trong CI. Hai môi trường 3.8/3.11 cùng xanh. Chi tiết: DB-23 |
| D10 | Bộ 5 hợp đồng synthetic sẵn (W1-06) — **nhiên liệu hợp pháp duy nhất** khi OI-02 chưa chốt | ✅ **PASS** *(2026-09-22)* | **Bằng chứng:** bộ 5 PDF text-layer (máy kiểm word-offset + mọi giá trị answer key khớp verbatim) + `MANIFEST-SYNTH-PB06.md` v1.0 (answer key = mini gold set) + `gen_synth.py` tái lập được ⇒ chứng minh giả 100%. AI-draft (Delegation #13, L2), **PM review checklist §4 và duyệt** *(tuyên bố trong phiên)*. HD-04 19 trang thoả luôn DoR-1b B2. Chi tiết: DB-21 |

### C. Con người & quyết định

| # | Điều kiện | Trạng thái | Nếu FAIL: giải quyết bằng gì |
|---|---|:-:|---|
| D11 | Tên role SaaS thật + mapping permission chốt (N1) | ✅ **PASS** *(2026-09-21)* | **Bằng chứng:** `DECISION-D11-PB06.md` v1.0 — 5 role + 3 quyết định con (Q1 quyền per-contract · Q2 upload = owner/editor · Q3 approve ∈ write), **PM duyệt nguyên trạng** (tuyên bố trong phiên; chế độ solo — PM quyết với tư cách product owner kịch bản, điều kiện re-verify khi cắm SaaS thật tại §4 của quyết định). ⇒ W1-01 hoàn thành, W1-02 đủ điều kiện start |
| D12 | Job worker option chốt (N5) | ✅ **PASS** *(2026-09-22)* | **Bằng chứng:** `DECISION-D12-PB06.md` v1.0 APPROVED — **option C** (FastAPI BackgroundTasks) + 4 design rule: job state sống ở DB · stale-job sweep 10 phút → `failed` · interface 4.3/4.4 bất biến · trigger nâng cấp A **đo được**. B tự loại trong solo (không có SaaS tham chiếu). PM kiêm Tech Lead duyệt nguyên trạng *(tuyên bố trong phiên)*. ⇒ W1-14 hết chặn; [PROPOSAL] ARCH §4.4 đã giải |
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
| 🔴 **Chặn ngày-1** | ~~D7~~ ✅ · ~~D11~~ ✅ *(cả hai PASS 2026-09-21 — DB-18 · DB-19)* | **Lớp 🔴 SẠCH** — task code đầu tiên (W1-02 L0-Auth resolver) đủ điều kiện start theo luật tiền-đề |
| 🟠 **Chặn trong Sprint 0–1** | ~~D4~~ ✅ · ~~D5~~ ✅ · ~~D9~~ ✅ · ~~D10~~ ✅ · ~~D12~~ ✅ *(DB-20 → DB-23)* · **D8** | Còn **1 mục cuối cùng: staging** |
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
| B2 | Bộ synthetic có **≥1 hợp đồng ~20 trang** đúng chuẩn đo (điều kiện của DoD-1 p95) | ✅ Thoả bởi `HD-04` (19 trang, bảng 120 hạng mục + 3 phụ lục) — xem D10 | 
| B3 | Đòn bẩy T1 (200→120 từ) còn nguyên hiệu lực, người quyết có mặt khi đo | Đo xong phải quyết ngay và ghi Dev Book — số để qua đêm là số nguội |

---

*DOR-PB06 v1.0 · `draft_ai` — hiệu lực sau cổng hiểu bước [7]. FAIL trong bảng này là tài sản: mỗi cái là một sự cố tuần 3 được trả trước với giá tuần 1.*
