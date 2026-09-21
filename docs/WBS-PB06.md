# WBS-PB06 — Work Breakdown Structure & Rolling-Wave
### AI Tóm Tắt & Trích Xuất Hợp Đồng (MVP)

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-06
> **Input:** `SCOPE-PB06.md` **v3.2** (signed off) · `SPEC-PB06.md` **v1.1** (signed off) · `MODULEMAP-PB06.md` **v1.2** · `ARCH-PB06.md` **v1.4** (draft — chờ Architecture Review)
> **Trạng thái:** ✅ **Có hiệu lực** — đã qua cổng hiểu bước [4] ngày 2026-09-06 (hồ sơ: `DEVBOOK` DB-13)
> **Ràng buộc cứng:** 8 tuần (A7) · sprint = 1 tuần (MODULEMAP §4) · team 4 người: 1 PM · 1 AI engineer · 1 BE · 1 FE · **0 QA** (gap đã ghi ở risk)
> Artefact bước **[4] WBS + Rolling-Wave** · Capstone Playbook · drill EX-02

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.1** | 2026-09-06 | Sửa theo phát hiện của PM tại cổng hiểu [4] (`DEVBOOK` DB-13): ① hoán vị W1-15 ↔ W1-16 — S1 đứng trước S2 theo luồng người dùng, S2 nhận thêm phụ thuộc W1-15; ② viết thành văn **ranh giới thang build S3** (W1-17 khung → W1-21 summary → F-03 phần còn lại) để chặn mạ-vàng-bản-mỏng và làm-lại-việc-đã-làm. |
| **1.0** | 2026-09-06 | Bản đầu: 3 wave / 8 sprint. Wave 1 (S0–S2) 22 task grain 0.5–2 ngày, đích = Slice 1 + Slice 1b xanh; Wave 2 (S3–S5) 9 feature; Wave 3 (S6–S7) 5 epic. §5 việc PM thêm/bớt kèm lý do; §6 truy vết "việc hay sót"; §7 phụ thuộc ngoài team; §8 kiểm tải thô. |

---

## 1. Nguyên tắc cấu trúc

**Rolling-wave — độ mịn theo khoảng cách:**

| Wave | Sprint (tuần) | Grain | Vì sao |
|---|---|---|---|
| **Wave 1** | S0 – S2 | Task **0.5–2 ngày** | Việc tuần tới phải bẻ tới mức giao được cho một người trong ≤2 ngày |
| **Wave 2** | S3 – S5 | Feature | Bẻ sâu bây giờ = đoán; sẽ bẻ lại đầu S3 khi có kết quả Slice 1b |
| **Wave 3** | S6 – S7 | Epic | Chỉ giữ hình khối + điều kiện vào |

**Quy ước:** mỗi task gắn pha SDLC `[REQ] [DES] [DEV] [TEST] [DEPLOY] [OPS]` · cột **Phụ thuộc** dùng ID task · cột **Leash** chỉ ghi khi khác mức A mặc định · ước lượng ở đây là **thô để xếp lịch** — 3-point + kết luận khả thi thuộc bước [5] `EST-PB06`.

**Nguyên tắc xếp việc (kế thừa MODULEMAP):** móng trước – bề mặt sau · **Slice 1 + Slice 1b xanh rồi mới mở rộng ngang** · surface bản-mỏng-phục-vụ-slice trước, làm dày sau. Điểm khác với lịch module thuần của MODULEMAP §4: S1/S2/S3 xuất hiện sớm ở Wave 1 nhưng chỉ ở **bản mỏng cho 1 trường** — lát cắt cắt *ngang* qua module, không đợi module *xong*.

---

## 2. WAVE 1 — Sprint 0–2 · Móng + Lát cắt (grain 0.5–2 ngày)

**Đích ra khỏi Wave 1:** Slice 1 + Slice 1b chạy end-to-end trên staging, số đo p95 nằm trong Dev Book, quyết định 200-vs-120-từ đã chốt.

### Sprint 0 (tuần 1) — Nền, hợp đồng API, khơi thông phụ thuộc ngoài

| ID | Task | Module | SDLC | Phụ thuộc | Owner | Thô (d) | Ra gì — neo AC/DoD |
|---|---|---|---|---|---|---|---|
| W1-01 | Xác nhận **tên role SaaS thật** + chốt bảng mapping permission (ARCH 6.3 đang là ví dụ) | L0-Auth | [REQ] | team SaaS | PM+BE | 0.5 | Bảng mapping chốt — mở khoá W1-02 |
| W1-02 | L0-Auth: permission resolver JWT → `contract:read/write/none` + unit test mọi ca 403/404 | L0-Auth | [DEV][TEST] | W1-01 | BE | 2 | NFR-A1/A2; nền mọi AC "403" |
| W1-03 | L0-Gateway: skeleton controller + **lock API contract** (12 endpoint ARCH §4, OpenAPI spec) | L0-Gateway | [DES][DEV] | W1-02 | BE | 1.5 | Contract locked trước khi FE build (MODULEMAP checklist) |
| W1-04 | Migration đợt 1: **8 bảng** (jobs · results+summary cols · fields · **items** · field_sources · **summary_sources** · audit_logs · model_runs) + CHECK constraints + trigger append-only | L0-ResultStore · L0-AuditLog | [DEV] | ARCH v1.4 §3 | BE | 2 | Schema review xong · **Leash A+** — đổi schema, chờ người duyệt |
| W1-05 | Audit writer helper: ghi log **atomic cùng transaction** nghiệp vụ + test UPDATE/DELETE bị chặn ở DB level | L0-AuditLog | [DEV][TEST] | W1-04 | BE | 1 | DoD-5; MODULEMAP checklist |
| W1-06 | Dựng **bộ hợp đồng synthetic**: 5 PDF text-layer tiếng Việt tự soạn, không dữ liệu thật | — | [REQ] | — | PM | 0.5 | Nhiên liệu hợp pháp cho pipeline khi OI-02 chưa chốt (luật cứng #2) |
| W1-07 | **OI-01 + OI-02 escalation**: văn bản câu hỏi + hạn chót gửi PO và Legal/Security; lịch bám đuổi hằng tuần | — | [REQ] | — | PM | 0.5 | Việc treo → task có owner; OI-02 kéo hồ sơ ĐGTĐ có deadline pháp lý riêng |
| W1-08 | ❗ Chốt **owner gold set** + lịch gán nhãn với pháp chế (30–50 HĐ, khởi động tuần 2) | — | [REQ] | — | PM | 0.5 | Không có gold set thì go/no-go không đo được (DB-11 B4) |
| W1-09 | Verify upload flow SaaS hiện có: định dạng lỗi non-PDF, quyền tạo hợp đồng (A2 — **không build mới**) | S1 | [TEST] | — | FE | 0.5 | AC-02-2/-3; nếu SaaS thiếu → kích hoạt điều kiện mở lại scope A2 |

### Sprint 1 (tuần 2) — Pipeline móng, một trường

| ID | Task | Module | SDLC | Phụ thuộc | Owner | Thô (d) | Ra gì — neo AC/DoD |
|---|---|---|---|---|---|---|---|
| W1-10 | L0-PDFIngestion: trích text-layer pdfplumber, giữ `page + char_offset` **mức từ** + unit test 3 ca (text / corrupt / password) | L0-PDFIngestion | [DEV][TEST] | — | AI | 2 | AC-13-1/-3; móng trace nguồn |
| W1-11 | Provider-agnostic LLM wrapper + **egress guard** (whitelist config, mặc định đóng) + egress test tự động | L0-AIpipeline | [DEV][TEST] | — | AI | 1.5 | DoD-4, D5, NFR-S1/S2 · **Leash A+** — ranh giới dữ liệu |
| W1-12 | Prompt + JSON schema trích trường ① (đa giá trị — mỗi bên một span, theo `items`) | L0-AIpipeline | [DES][DEV] | W1-10 | AI | 1 | AC-15-1a · prompt = logic nghiệp vụ, PM đọc từng dòng (L2) |
| W1-13 | Validator D6-a: khớp verbatim + parse kiểu + gán trạng thái; **transaction 8 bước** ARCH 3.4 | L0-AIpipeline | [DEV][TEST] | W1-04, W1-12 | AI | 2 | DoD-2 nhánh D6-a — cổng fail-closed |
| W1-14 | Tech Lead **chốt job worker** (A/B/C — ARCH 4.4) + dựng khung async 202 + poll | L0-Gateway | [DES][DEV] | W1-03, Tech Lead | BE | 1 | Interface bất biến dù chọn option nào |
| W1-15 | S1 bản mỏng: hiện/ẩn nút theo quyền + có PDF | S1 | [DEV] | W1-03 | FE | 1 | AC-01-1/-2/-3 |
| W1-16 | S2 bản mỏng: nút phân tích + polling **theo nhánh** `pdf_type` (40s/70s) + disable chống double-submit | S2 | [DEV] | W1-03, W1-15 | FE | 1.5 | AC-03-1/-2; NFR-P3 — nút của S2 sống trong màn S1 |
| W1-17 | S3 bản mỏng: bảng **đủ 6 hàng** — hàng ① có items + excerpt + page, 5 hàng not_found. **Ranh giới:** CHỈ layout + dữ liệu trường ① — không nhãn tin cậy, không styling trạng thái (phần đó thuộc F-03) | S3 | [DEV] | W1-03 | FE | 2 | AC-05-3 (render đủ hàng dù thiếu field) |

> **Thang build S3 — ba nấc, không chồng lấn:** W1-17 (khung 6 hàng + trường ①) → W1-21 (summary + con trỏ theo câu) → F-03 (đủ 6 trường + hai trục nhãn). Mỗi nấc chỉ làm phần chưa có.

### Sprint 2 (tuần 3) — Slice 1 xanh · Slice 1b + phép đo đã cam kết

| ID | Task | Module | SDLC | Phụ thuộc | Owner | Thô (d) | Ra gì — neo AC/DoD |
|---|---|---|---|---|---|---|---|
| W1-18 | Ghép **Slice 1** end-to-end trên staging + demo nội bộ + ghi Dev Book | tất cả | [TEST][DEPLOY] | W1-02→17 | cả team | 1 | MODULEMAP §7 — cổng vào mở rộng |
| W1-19 | Prompt sinh tóm tắt ~200 từ (VI) | L0-AIpipeline | [DES][DEV] | W1-12 | AI | 0.5 | US-04 |
| W1-20 | ⭐ **Kiểm neo-theo-câu**: tách câu → phát hiện câu dữ kiện → đối chiếu verbatim → cắt câu không neo → `insufficient_grounding` + ghi `summary_sources` | L0-AIpipeline | [DEV][TEST] | W1-19, W1-13 | AI | 2 | AC-15-1b — **cấu phần rủi ro nhất toàn dự án** |
| W1-21 | S3: render summary + con trỏ nguồn theo câu + nhãn trạng thái **thay** tóm tắt khi insufficient | S3 | [DEV] | W1-17, W1-20 | FE | 1 | AC-04-4/-5 |
| W1-22 | 📏 **Đo p95 Slice 1b** (trường ①+⑥, HĐ ~20 trang) → quyết định 200 vs 120 từ → ghi Dev Book | — | [TEST] | W1-18→21 | AI+PM | 0.5 | Điểm quyết định DB-03; đòn bẩy đã chốt, không nới D6-b |
| W1-23 | Gold set đợt 1: pháp chế gán nhãn 10 HĐ đầu (PM điều phối, làm song song) | — | [REQ] | W1-08 | **Ngoài team** | — | Nhiên liệu cho F-06 |

---

## 3. WAVE 2 — Sprint 3–5 · Mở rộng ngang (grain feature)

> **Điều kiện vào:** Slice 1 + 1b xanh (W1-18, W1-22). **Bẻ sâu lại đầu Sprint 3** với số đo thật trong tay.

| ID | Feature | Module | Sprint dự kiến | Phụ thuộc | Neo AC/DoD |
|---|---|---|---|---|---|
| F-01 | 4 trường còn lại ②③④⑤ (prompt + validator; ⑤ đa đoạn theo items) + tiếng Anh + song ngữ hỗn hợp | L0-AIpipeline | S3 | W1-13 | AC-15-1a; US-16; NFR-L1/L2 |
| F-02 | Nhánh OCR: detect scan → engine (Tech Lead benchmark Tesseract/PaddleOCR trên gold set) → `pdf_type=scan` → best-effort | L0-PDFIngestion | S3–S4 | W1-10; gold set đợt 1 | US-14; NFR-P2; AC-14-2 |
| F-03 | S3 đầy đủ: nhãn tin cậy **chỉ trên `grounded`**, nhãn trạng thái, hiển thị đủ items đa giá trị/đa đoạn — **phần còn lại của thang S3, không làm lại những gì W1-17/W1-21 đã có** | S3 | S4 | F-01 | AC-05-2/-4; AC-06-2; A6 v3.2 |
| F-04 | S4 Edit & Approve: inline edit + **4.8b sửa tóm tắt** + cảnh báo unsaved + approve + audit field_edited/result_approved | S4 | S4 | W1-05, F-03 | US-07/08; DoD-3, DoD-5 |
| F-05 | S5 Reanalyze + version selector (không diff view — post-MVP) | S5 | S5 | F-04 | US-09; D7; AC-09-2/-4 |
| F-06 | 🎯 **Eval harness + chạy gold set**: precision/recall per-field + tỷ lệ câu không neo — báo cáo go/no-go | — | S4–S5 | W1-23 (≥30 HĐ) | Go/no-go của Problem Statement; DoD-7(b) |
| F-07 | S6 Audit UI (PM-only, chặn 403, query theo contract_id) | S6 | S5 | W1-05 | US-11 |
| F-08 | ⚖️ Hồ sơ ĐGTĐ chuyển dữ liệu ra nước ngoài — **chỉ kích hoạt nếu OI-02 = external** | — | ngay khi OI-02 chốt | W1-07; Legal | Deadline pháp lý riêng, không theo lịch dự án |
| F-09 | Bộ test negative + phân quyền theo role + **DB schema audit kiểm D4** (không cột nào chứa text thô) | — | S5 | F-01→05 | NFR-S3; chuẩn bị SIT — *đội không có QA: PM cầm, cả team góp* |

---

## 4. WAVE 3 — Sprint 6–7 · Khép & nghiệm thu (grain epic)

| ID | Epic | Điều kiện vào | Neo DoD |
|---|---|---|---|
| E-01 | **SIT**: happy + negative + phân quyền + egress test + append-only test | F-01→09 xong | DoD-2/3/4/5 |
| E-02 | **UAT** trên mẫu ≥5 hợp đồng thực tế (user review DoD-7a + kiểm neo DoD-7b) | E-01; có căn cứ dùng HĐ thật nội bộ | DoD-6/7 |
| E-03 | Hardening + đo lại p95 **đủ 6 trường** (text-layer + scan) | E-01 | DoD-1; NFR-P2 |
| E-04 | Nghiệm thu DoD-1→7 + RTM + Dev Book + telemetry + demo (nối bước [9][10] Playbook) | E-01→03 | 3 cổng tốt nghiệp |
| E-05 | Buffer nửa cuối S7 + **van xả scope** nếu trượt: rút tóm tắt 120 từ (đã chốt) → giảm gold set đợt nghiệm thu → S6 lùi cuối S7. **Không cắt:** grounding, human gate, audit — lõi giá trị (EX-03 sẽ tính lại chi tiết) | — | — |

---

## 5. Việc PM chủ động THÊM / BỚT — kèm lý do *(EX-02)*

**Thêm — 4 việc không nằm trong ARCH/MODULEMAP:**

| Task | Vì sao thêm |
|---|---|
| W1-06 bộ hợp đồng synthetic | OI-02 chưa chốt + luật cứng #2 ⇒ build chỉ được chạy dữ liệu tự tạo. Không có task này, pipeline **không có gì để chạy hợp pháp** trong 3 tuần đầu — và không ai nhận ra cho tới khi cần |
| W1-07 · W1-08 escalation OI + owner gold set | Biến "việc treo" thành task có owner + hạn. Bài học từ Dev Book: **phụ thuộc ngoài team là loại việc trễ nhất** vì không nằm trong standup của ai |
| F-06 eval harness + gold set run | Nằm trong danh sách "WBS hay sót" của chính đề bài; thiếu nó thì *"trích đúng ở mức chấp nhận"* là câu cảm thán, không phải tiêu chí |
| F-09 kiểm D4 bằng DB schema audit | NFR-S3 có ngưỡng "kiểm bằng DB schema audit" nhưng chưa từng có task nào làm việc kiểm đó — cổng viết ra mà không ai chạy = cổng không tồn tại |

**Bớt — 4 việc cố ý KHÔNG có trong WBS:**

| Không làm | Vì sao bớt |
|---|---|
| Build upload flow mới | A2: dùng upload sẵn có của SaaS — chỉ giữ W1-09 (verify, 0.5d). Nếu verify fail → mở lại scope theo đúng luật A2, không lặng lẽ build |
| Diff view giữa các version | AC-09-2 chỉ đòi *chuyển đổi*; diff là post-MVP (MODULEMAP S5) — dev rất muốn làm, phải ghi thành văn |
| Admin field editor · auto-approve · full-text search · auto-renewal · auto-signing | Out-of-scope SCOPE §5 — liệt kê lại đúng một dòng để không ai "tiện tay" |
| Standalone gateway service (Kong/nginx) | D1: Gateway là controller layer trong backend hiện tại |

---

## 6. "Việc hay sót" của đề — đã nằm ở đâu

| Bẫy đề cài | Task phủ |
|---|---|
| Hiển thị nguồn trích | W1-17 · W1-21 · F-03 |
| Bước đánh giá chất lượng trích xuất | W1-08 · W1-23 · F-06 |
| Xử lý PDF lỗi / scan kém | W1-10 (3 ca lỗi) · F-02 (best-effort) |
| Phân quyền & negative test | W1-02 · W1-09 · F-09 · E-01 |
| Migration/di trú dữ liệu | Không áp dụng (tính năng mới, không di trú) — ghi rõ để khỏi bị hỏi |

---

## 7. Phụ thuộc NGOÀI team — theo dõi riêng, rủi ro trễ cao nhất

| # | Phụ thuộc | Chặn task | Owner ngoài | Hạn |
|---|---|---|---|---|
| N1 | Tên role SaaS thật (ARCH 6.3) | W1-02 | Team SaaS | Sprint 0 |
| N2 | `OI-01` external access | Threat model nếu Yes | Product Owner | Trước Sprint 0 kết thúc |
| N3 | `OI-02` external LLM / self-host | F-08 + cấu hình egress | Legal/Security | Trước Sprint 0 kết thúc ⚠️ deadline pháp lý riêng nếu external |
| N4 | Gold set 30–50 HĐ gán nhãn | F-06, F-02 benchmark | Pháp chế (owner: **chưa có tên** ❗) | Đợt 1 tuần 2 · đủ 30 trước S4 |
| N5 | Quyết định job worker A/B/C | W1-14 | Tech Lead | Sprint 1 |
| N6 | Architecture Review ARCH v1.4 | không chặn code Wave 1, chặn khoá contract | Tech Lead | Sprint 0–1 |

---

## 8. Kiểm tải thô Wave 1 — cảnh báo sớm cho bước [5]

Ngày công liệt kê / ngày công có (3 tuần ≈ 15 ngày/người, chưa trừ họp + rework):

| Người | Ngày liệt kê | Tải danh nghĩa | Đọc số |
|---|---|---|---|
| **AI engineer** | ~9.5 | **~63%** | Cộng họp + rework + hỗ trợ ghép slice ⇒ **critical path, đúng SPOF đã ghi ở risk**. Bắt buộc pair 1 buổi/tuần với BE; W1-20 không được giao kèm việc khác |
| BE | ~7.5 | ~50% | Còn đệm cho option worker + sửa migration |
| FE | ~6.5 | ~43% | Đệm dùng cho polish S3 khi schema đổi |
| PM | ~2.5 + điều phối | — | N1–N6 là việc thật của PM, không phải "chờ" |

> Con số này là **thô để xếp lịch** — bước [5] `EST-PB06` làm 3-point, cộng Wave 2/3, đối chiếu mốc 8 tuần và ra kết luận cắt/không cắt.

---

*WBS-PB06 v1.0 · trạng thái `draft_ai` — hiệu lực sau khi PM qua cổng hiểu bước [4] và review. Thay đổi chạm A1–A7/D1–D7 → mở lại scope theo quy định `SCOPE-PB06`.*
