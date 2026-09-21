# MODULEMAP-PB06 — Module Map & Vertical Slice
### AI Tóm Tắt & Trích Xuất Hợp Đồng (MVP)

> **Phiên bản:** 1.2 · **Ngày:** 2026-09-06
> **Input:** `SCOPE-PB06.md` **v3.2** (✅ signed off 2026-09-06) · `SPEC-PB06.md` **v1.1** (✅ signed off 2026-09-06)
> **Mục đích:** Xác định tầng móng vs bề mặt, thứ tự build, và lát cắt dọc ứng viên.

---

## Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.2** | 2026-09-06 | Đồng bộ SCOPE v3.2 + SPEC v1.1 sau đánh giá cổng [2] (`DEVBOOK` DB-11). **A1** S3 tách trục nhãn độ tin cậy vs trạng thái (§3.0/A6). **A2** L0-ResultStore thêm trạng thái theo trường + đa giá trị/đa đoạn + con trỏ theo câu. **A3** L0-AIpipeline validator tách D6-a/D6-b, thêm `insufficient_grounding`. **A4** thêm **Slice 1b** đo neo-theo-câu vs DoD-1. **B1** §0 đồng bộ 3 dòng out-of-scope với SCOPE §5. **B2** chốt độ dài sprint. **B3** chú thích ngữ nghĩa `not_found` trong slice. |
| **1.1** | 2026-07-31 | Bản nhận được — viết trên SCOPE v3.0 / SPEC v1.0 (tụt phiên bản, xem DB-11). |

---

## 0. MVP Scope Commitment

> Đoạn này dành cho stakeholder đọc nhanh. Mọi chi tiết ở các section sau.

**MVP bắt buộc gồm — tất cả phải ship:**

Layer 0: `L0-Auth` · `L0-Gateway` · `L0-ResultStore` · `L0-AuditLog` · `L0-PDFIngestion` · `L0-AIpipeline`

Surface: `S1-ContractEntry` · `S2-AnalysisTrigger` · `S3-ResultView` · `S4-EditApprove` · `S5-Reanalyze` · `S6-AuditUI`

**Không build trong MVP này:**

| Tính năng | Lý do loại |
|---|---|
| Admin field editor | D2: schema động làm phức tạp prompt + validation |
| Legal advice / đánh giá rủi ro | Sản phẩm khác, cần liability framework riêng |
| Auto renewal / workflow downstream | Cần `approved` data đủ chính xác trước |
| Auto signing | Hành động pháp lý — cần trust vào data trước |
| Full-text search từ AI text | D4: text thô không persist |
| External party access | OI-01 chưa trả lời — auth model chưa xác định |
| Đa ngôn ngữ ngoài VI/EN | Chưa có baseline đánh giá accuracy (SCOPE §5) |
| SLA xử lý PDF scan mờ/hỏng nặng/thiếu trang | Giới hạn kỹ thuật OCR, không phải scope cut (SCOPE §5) |
| Tóm tắt tự do không neo nguồn | D6-b: miễn trừ tóm tắt khỏi grounding là lỗ hổng lớn nhất của tính năng (SCOPE §5, thêm ở v3.1) |

---

## 1. Nguyên tắc phân tầng

| Tầng | Định nghĩa | Dấu hiệu nhận |
|---|---|---|
| **Layer 0 — Móng** | Module không có UI người dùng thấy trực tiếp; module khác phụ thuộc vào nó để **tồn tại hoặc đúng** | Nếu thiếu → surface module compile được nhưng **sai về bảo mật, dữ liệu, hoặc nghiệp vụ** |
| **Surface — Bề mặt** | Module tạo ra màn hình / endpoint mà người dùng tương tác; tiêu thụ output của Layer 0 | Nếu thiếu → người dùng không thấy tính năng, nhưng **hệ thống không vỡ** |

> **Bẫy thường gặp:** build surface đẹp trước khi có móng → compile xong nhưng không enforce auth, không có schema để ghi, không có audit trail → phải xây lại.

---

## 2. Layer 0 — Móng dùng chung

> Tất cả module Layer 0 phải hoàn thành **trước khi** bất kỳ surface module nào được ship.

| ID | Tên Module | Stories / NFR | Trách nhiệm cốt lõi | MVP? |
|---|---|---|---|---|
| **L0-Auth** | Auth & Phân quyền | NFR-A1, A2, A3; mọi AC có "403" (US-01~09) | Reuse JWT/session SaaS. Xác thực JWT, tra quyền đọc/ghi/approve của user trên từng hợp đồng. Cung cấp permission context cho L0-Gateway gọi. | ✅ |
| **L0-Gateway** | API Boundary / SaaS↔AI | NFR-S1, S2, S7; AC-03-4, AC-08-4, AC-09-3 | Expose REST endpoints AI feature trong SaaS backend (`POST /analyze`, `GET /results`, `POST /approve`…). Enforce auth+permission bằng cách gọi L0-Auth trước khi forward request vào AI service. Routing SaaS backend → AI service qua internal network (không public internet). Chuẩn hóa request/response contract giữa surface và pipeline. **Không phải standalone gateway service** (Kong/nginx) — là controller layer trong SaaS backend hiện tại (D1). | ✅ |
| **L0-ResultStore** | Data Model Kết quả | US-08, US-09; D3, D7; **SPEC §3.0** | Schema `analysis_results`: trạng thái bản ghi `draft_ai` / `approved`, versioning per contract, FK đến hợp đồng. **Trạng thái theo trường** `grounded` / `uncertain` / `not_found` / `insufficient_grounding` (§3.0). Cấu trúc chứa **đa giá trị** (trường ①) và **đa đoạn** (trường ⑤) — mỗi giá trị/đoạn một span riêng (AC-05-4, AC-15-1a) — và **con trỏ nguồn theo câu** cho trường ⑥ (D6-b, AC-15-1b). Không ép 6 trường về một khuôn `field: value + span`. Là nguồn sự thật duy nhất cho mọi surface module đọc/ghi. | ✅ |
| **L0-AuditLog** | Audit Log | US-11; NFR-S5, S6; DoD-5 | Append-only event store: `user_id, action_type, contract_id, field_name, before_value, after_value, timestamp`. Không chứa text hợp đồng. Viết được từ mọi layer khác. | ✅ |
| **L0-PDFIngestion** | Trích Xuất PDF | US-13, US-14 | Nhận PDF → detect text-layer hoặc scan → trích text kèm `page_number + char_offset` (pdfplumber / Tesseract OCR). Output là structured text cho pipeline tiêu thụ — không persist text thô (D4). | ✅ |
| **L0-AIpipeline** | Pipeline AI & Grounding | US-15, US-16; D5, **D6-a/D6-b**; DoD-2, DoD-4 | Gọi LLM qua provider-agnostic wrapper. Egress guard chặn mọi endpoint ngoài whitelist. **Validator fail-closed hai nhánh:** *(D6-a, trường ①→⑤ — AC-15-1a)* mỗi giá trị phải có `(giá trị + source_excerpt + page)` khớp **verbatim** HOẶC nhãn `uncertain`/`not_found`; trường đa giá trị/đa đoạn: mỗi giá trị một span. *(D6-b, trường ⑥ — AC-15-1b)* kiểm **neo-theo-câu**: câu dữ kiện không neo bị cắt, không viết mềm đi; sau cắt không đủ nghĩa → trạng thái `insufficient_grounding`. Không có đường thứ ba. Xử lý VI/EN và không crash với ngôn ngữ khác. | ✅ |

---

## 3. Surface — Module bề mặt (người dùng thấy)

| ID | Tên Module | Stories | Trách nhiệm cốt lõi | Phụ thuộc Layer 0 | MVP? |
|---|---|---|---|---|---|
| **S1-ContractEntry** | Chọn / Upload HĐ | US-01, US-02 | Hiển thị nút "Phân tích bằng AI" nếu có PDF và user có quyền. Ẩn/disable khi không có PDF hoặc read-only. Upload PDF mới qua flow SaaS hiện tại. | L0-Gateway · L0-Auth | ✅ |
| **S2-AnalysisTrigger** | Kích hoạt Phân tích | US-03 | Gọi job async, hiển thị progress indicator, disable nút tránh double-submit. Error toast nếu pipeline lỗi. UI phản hồi < 2s (NFR-P3). | L0-Gateway · L0-Auth · L0-ResultStore · L0-PDFIngestion · L0-AIpipeline | ✅ |
| **S3-ResultView** | Xem Kết quả AI | US-04, US-05, US-06 | Render tóm tắt ≤200 từ + bảng 6 trường cố định. Hiển thị source excerpt + page. **Hai trục nhãn tách bạch (SPEC §3.0, SCOPE A6):** nhãn độ tin cậy **Cao/Trung bình/Thấp** chỉ trên trường `grounded`; trường `uncertain` / `not_found` / `insufficient_grounding` hiển thị **nhãn trạng thái**, không hiển thị nhãn độ tin cậy. Trường ⑥ ở `insufficient_grounding` → nhãn trạng thái **thay cho** tóm tắt (AC-04-5). Trường đa giá trị ①/đa đoạn ⑤ hiển thị **đủ mọi giá trị**, mỗi giá trị một span đối chiếu được (AC-05-4). Luôn render đủ 6 hàng dù API thiếu field (AC-05-3). | L0-Gateway · L0-Auth · L0-ResultStore | ✅ |
| **S4-EditApprove** | Chỉnh sửa & Duyệt | US-07, US-08 | Inline edit từng trường. Đánh dấu trường đã sửa khác với giá trị AI. Cảnh báo unsaved khi rời trang. Nút "Xác nhận & Lưu" chuyển `draft_ai → approved`. Read-only lock với user không có quyền write. | L0-Gateway · L0-Auth · L0-ResultStore · **L0-AuditLog** | ✅ |
| **S5-Reanalyze** | Chạy lại AI | US-09 | Tạo version `draft_ai` mới, giữ nguyên bản `approved` cũ. Từ chối nếu đang có job đang chạy (AC-09-4). Version selector cho phép **chuyển đổi** giữa draft/approved versions; compare/diff view nếu có là post-MVP. | L0-Gateway · L0-Auth · L0-ResultStore · L0-PDFIngestion · L0-AIpipeline | ✅ |
| **S6-AuditUI** | Audit Trail (PM) | US-11 | PM-only: query log theo `contract_id` hoặc `user_id`, xem timeline hành động. Chặn 403 với mọi role khác. | L0-Gateway · L0-Auth · **L0-AuditLog** | ✅ |

---

## 4. Sơ đồ phụ thuộc & Thứ tự build

```
┌──────────────────────────────────────────────────────────────┐
│                      LAYER 0 — MÓNG                          │
│                                                              │
│  L0-Auth ──────────────────────────────┐                    │
│                                        │                    │
│  L0-ResultStore ───────────────────┐  │                    │
│                                    │  │                    │
│  L0-AuditLog ──────────────────┐  │  │                    │
│                                │  │  │                    │
│  L0-PDFIngestion ─► L0-AIpipeline ─┤  │  │                    │
│                                │  │  │                    │
│  L0-Gateway  ◄─────────────────┘  │  │                    │
│  (SaaS backend API layer)         │  │                    │
│                                   │  │                    │
└───────────────────────────────────┼──┼────────────────────┘
                                    │  │
┌───────────────────────────────────┼──┼────────────────────┐
│  SURFACE                          ▼  ▼                     │
│                                                            │
│  S1-ContractEntry   ◄──── L0-Gateway + L0-Auth            │
│  S2-AnalysisTrigger ◄──── L0-Gateway + pipeline           │
│  S3-ResultView      ◄──── L0-Gateway + L0-ResultStore     │
│  S4-EditApprove     ◄──── L0-Gateway + L0-AuditLog        │
│  S5-Reanalyze       ◄──── L0-Gateway + pipeline           │
│  S6-AuditUI         ◄──── L0-Gateway + L0-AuditLog        │
└────────────────────────────────────────────────────────────┘
```

**Thứ tự build bắt buộc:**

```
Sprint 0-1 │ L0-Auth → L0-Gateway → L0-ResultStore → L0-AuditLog
           │   L0-Auth trước: Gateway cần gọi Auth để check permission
           │   L0-Gateway song song L0-ResultStore: định nghĩa API contract
           │   L0-AuditLog phải có trước khi bất kỳ surface action nào xảy ra
           │
Sprint 1-2 │ L0-PDFIngestion → L0-AIpipeline
           │   (pipeline không chạy được nếu không có text + metadata)
           │
Sprint 2-3 │ S1-ContractEntry + S2-AnalysisTrigger
           │   (entry point + job trigger — user thấy tính năng lần đầu)
           │   L0-AuditLog đã sẵn sàng để ghi ai_job_completed từ S2
           │
Sprint 3-4 │ S3-ResultView
           │   (giá trị thực sự user nhận được)
           │
Sprint 4-5 │ S4-EditApprove + S5-Reanalyze
           │   (human gate — DoD-3 bắt buộc trước khi ship)
           │
Sprint 5-6 │ S6-AuditUI
           │   (cần L0-AuditLog có đủ data từ các bước trên)
```

> **Độ dài sprint: 1 tuần lịch** — để 6 sprint + đệm nằm trong mốc 8 tuần của A7. Nếu team chạy sprint 2 tuần, lộ trình trên là ~12 tuần → **vượt A7 ⇒ mở lại scope** theo quy định cuối `SCOPE-PB06`. Con số cuối chốt ở bước [4]/[5] (WBS + Estimation), nhưng ràng buộc 8 tuần không thương lượng ở tầng module map.

---

## 5. Cổng hiểu — Móng nào PHẢI xong trước và tại sao

### L0-Auth — Bắt buộc xong trước L0-Gateway và MỌI surface module

**Vì sao bề mặt không chạy được nếu thiếu:**
L0-Gateway gọi L0-Auth để kiểm tra permission trước khi forward request — nếu Auth chưa có, Gateway không biết user có quyền gì trên hợp đồng. Hệ quả dây chuyền: S1 hiển thị nút "Phân tích bằng AI" với mọi user kể cả view-only (AC-01-3, AC-03-4). S4 cho phép bất kỳ ai approve (vi phạm DoD-3). S2 có thể bị gọi trực tiếp qua API bỏ qua UI check. Surface hoạt động theo góc nhìn UI nhưng **sai về bảo mật từ gốc** — phải viết lại toàn bộ API layer.

### L0-Gateway — Bắt buộc xong trước MỌI surface module

**Vì sao bề mặt không chạy được nếu thiếu:**
Surface module gọi các REST endpoint mà L0-Gateway expose (`POST /analyze`, `GET /results`, `POST /approve`…). Chưa có Gateway thì không có endpoint để gọi — surface module không có điểm kết nối với Layer 0. Quan trọng hơn: Gateway là nơi enforce "user chỉ phân tích được hợp đồng họ có quyền đọc" (NFR-A2) và "AI service chỉ nhận request từ SaaS backend qua internal network" (NFR-S7). Nếu thiếu Gateway, mọi enforcement này chỉ tồn tại trên UI — bất kỳ ai biết endpoint AI service cũng có thể gọi trực tiếp bỏ qua auth.

### L0-ResultStore — Bắt buộc xong trước S2, S3, S4, S5

**Vì sao bề mặt không chạy được nếu thiếu:**
S2 không có bảng nào để ghi job status và kết quả. S3 không biết đọc `draft_ai` từ đâu. S4 không thể transition state `draft_ai → approved`. S5 không thể tạo version mới mà không ghi đè bản cũ. Đây là điểm suy sụp dây chuyền: thiếu schema → surface module không có nguồn sự thật → viết mock data → phải bỏ khi có schema thật.

### L0-AuditLog — Bắt buộc xong trước S2, S4 và S5

**Vì sao bề mặt không chạy được nếu thiếu:**
DoD-5 yêu cầu **100% hành động** (chạy AI / sửa trường / duyệt) có log — ba action này nằm ở ba module khác nhau:

- **S2** tạo action `ai_job_triggered` và `ai_job_completed` — ghi ngay khi user bấm phân tích.
- **S4** tạo action `field_edited` (before/after value) và `result_approved` — phức tạp nhất, cần atomic write.
- **S5** tạo action `ai_job_rerun` khi user chạy lại.

Nếu L0-AuditLog chưa có khi S2 được build: action chạy AI không có log → DoD-5 fail ngay từ sprint đầu tiên có surface, không phải chờ đến S4. Retrofit audit log vào sau khi surface đã build: mỗi action phải wrap lại để đảm bảo atomic write (business logic + log hoặc không gì cả) — **patch-in sau sẽ bỏ sót case** và không đảm bảo atomicity.

### L0-PDFIngestion — Bắt buộc xong trước L0-AIpipeline

**Vì sao pipeline không chạy được nếu thiếu:**
L0-AIpipeline nhận input là **structured text kèm page_number + char_offset** — không phải raw PDF bytes. Không có metadata trang thì grounding (AC-15-1, DoD-2) không làm được: LLM trả về giá trị nhưng không link được về đoạn nguồn → toàn bộ fail-closed validator bị vô hiệu hóa.

---

## 6. Bác sai tầng — Hai phân loại sai phổ biến

### ❌ Sai #1: Xếp L0-AIpipeline vào Surface

**Lập luận sai:** "AI Pipeline là *tính năng AI* — user bấm nút thì AI chạy, đây là thứ user thấy giá trị nhất, vậy nó là module bề mặt."

**Tại sao sai:**
L0-AIpipeline không có UI. Nó là internal FastAPI service nhận text và trả JSON — không có màn hình nào, không có interaction nào trực tiếp với người dùng. Quan trọng hơn: **S2, S3, S5 đều phụ thuộc vào output của L0-AIpipeline** — nếu xếp nó là surface thì ba surface module kia không có dependency để consume. Dấu hiệu nhận chuẩn: nếu xóa L0-AIpipeline, S2 và S3 sụp hoàn toàn (không phải chỉ mất chức năng). Đây là đặc trưng của móng, không phải bề mặt.

**Hệ quả nếu xếp sai tầng:** Team build S3 (ResultView UI đẹp) trước khi L0-AIpipeline ổn định → S3 dùng hardcode mock data → khi pipeline thật trả về response shape khác (vì chưa locked contract) → phải refactor S3 lần hai.

---

### ❌ Sai #2: Xếp S6-AuditUI vào Layer 0

**Lập luận sai:** "Audit là bắt buộc về compliance, log phải có từ ngày đầu, vậy toàn bộ audit module là Layer 0."

**Tại sao sai:**
*L0-AuditLog* (event store, append-only writer) đúng là Layer 0 vì các surface module khác gọi nó để ghi. Nhưng *S6-AuditUI* (màn hình PM đọc log) là bề mặt thuần túy — không có module nào phụ thuộc vào S6 để hoạt động. Nếu xóa S6, L0-AuditLog vẫn ghi đầy đủ, S4 vẫn approve đúng, DoD-5 vẫn đạt (log tồn tại trong DB, chỉ chưa có UI để xem). S6-AuditUI có thể build sau khi có đủ data từ các sprint trước mà không ảnh hưởng gì đến pipeline.

**Hệ quả nếu xếp sai tầng:** Đưa S6 lên Sprint 0-1 chiếm bandwidth của L0-AuditLog và L0-ResultStore thực sự cần build trước → surface có UI đẹp nhưng không có data để hiển thị.

---

## 7. Lát cắt dọc ứng viên

> Lát cắt mỏng nhất đi xuyên từ móng lên một tính năng bề mặt hoàn chỉnh. Dùng để validate toàn bộ stack trước khi build rộng.

### Slice: "Trích xuất trường **Các bên** từ PDF text-layer và hiển thị kèm nguồn"

```
[S1-ContractEntry]
  Nút "Phân tích bằng AI" active vì có PDF và user có quyền
        │
        ▼
[S2-AnalysisTrigger]
  User bấm nút → UI gọi POST /analyze
        │
        ▼
[L0-Gateway]
  Nhận request từ SaaS UI/backend
  Gọi L0-Auth để check permission
  Chặn request không hợp lệ (403 nếu thiếu quyền)
  Forward request qua internal network đến AI service (NFR-S7)
        │
        ▼
[L0-Auth]
  Xác nhận user có quyền đọc hợp đồng → cho phép tiếp tục
        │
        ▼
[L0-PDFIngestion]
  Nhận PDF text-layer → trích text → trả page_number + char_offset
        │
        ▼
[L0-AIpipeline]
  Gọi LLM với prompt chỉ yêu cầu trường "Các bên"
  Egress guard kiểm tra endpoint
  Validator D6-a: phải có (giá trị + source_excerpt + page, verbatim) HOẶC not_found
  (slice này chỉ chạy trường ① — nhánh D6-b đo ở Slice 1b)
        │
        ▼
[L0-ResultStore]
  Lưu draft_ai với 1 trường "Các bên"
        │
        ▼
[L0-AuditLog]
  Ghi event: user_id · action=ai_job_triggered · contract_id · timestamp
  Ghi event: user_id · action=ai_job_completed · contract_id · timestamp
        │
        ▼
[S3-ResultView]
  Bảng 6 hàng render: hàng "Các bên" có giá trị + source_excerpt + page
  5 hàng còn lại hiển thị not_found (đúng — chưa trích)
```

> **Lưu ý ngữ nghĩa (chỉ áp cho slice):** `not_found` ở 5 hàng này nghĩa là *chưa được yêu cầu trích* (render field thiếu theo AC-05-3), **khác** nghĩa production ở §3.0 (*không có span khớp verbatim trong văn bản*). Không mang ngữ nghĩa slice vào production — MVP thật luôn trích đủ 6 trường trong một lần chạy.

**Tại sao đây là slice đúng:**

| Tiêu chí | Đáp ứng |
|---|---|
| Đi qua tất cả 6 module Layer 0 (bao gồm L0-Gateway) | ✅ |
| Validate auth enforcement thực (không phải mock) | ✅ |
| Validate grounding fail-closed end-to-end | ✅ |
| Validate schema `draft_ai` đọc/ghi đúng | ✅ |
| Validate audit log ghi được từ pipeline | ✅ |
| Validate UI render đủ 6 hàng dù chỉ có 1 trường (AC-05-3) | ✅ |
| Scope nhỏ — chỉ cần 1 trường, text-layer PDF, không cần OCR | ✅ |

### Slice 1b — BẮT BUỘC ngay sau Slice 1: Tóm tắt + neo-theo-câu + đo p95

**Vì sao tồn tại:** `DEVBOOK` DB-03 chốt chi phí neo-theo-câu (D6-b) phải đo ở **lát cắt dọc đầu tiên**, vì nó cạnh tranh trực tiếp với DoD-1 (< 30s p95). Slice 1 cố tình không chạy tóm tắt để giữ tính tối giản validate stack — nên phép đo cần slice riêng, ngay kế tiếp, không lùi về sau.

**Phạm vi:** cùng hợp đồng của Slice 1, chỉ thêm trường ⑥:

1. Sinh tóm tắt (~200 từ)
2. Kiểm neo-theo-câu (AC-15-1b): câu dữ kiện không neo → **cắt**, không viết mềm đi
3. Sau cắt không đủ nghĩa → trạng thái `insufficient_grounding`
4. S3 render: nhãn trạng thái **thay cho** tóm tắt nếu insufficient (AC-04-5)
5. **Đo p95 end-to-end** cho cả pipeline (trường ① + ⑥)

**Điểm quyết định:** p95 vượt 30s → kích hoạt đòn bẩy đã chốt: **rút tóm tắt ~200 → ~120 từ**, *không* nới D6-b. Ghi kết quả đo + quyết định vào Dev Book.

**Ràng buộc:** Slice 1 **và** Slice 1b đều xanh trước khi mở rộng chiều ngang.

---

**Sau khi Slice 1 + Slice 1b chạy:** các story còn lại (thêm 4 trường trích xuất, OCR, edit, approve, re-analyze) là **mở rộng chiều ngang** — không thay đổi kiến trúc cốt lõi. Đây là tín hiệu slice đúng.

**Không chọn slice khác vì:**

- Slice "upload PDF mới" (US-02): phụ thuộc vào upload flow của SaaS hiện có, rủi ro integration cao hơn cần thiết cho bước đầu.
- Slice "edit & approve" (US-07, US-08): phụ thuộc vào S3-ResultView đã ổn định — không phải slice ứng viên đầu tiên.
- Slice "audit UI" (US-11): không validate pipeline, không có giá trị chứng minh stack core.

---

## 8. Checklist Done

- [ ] L0-Auth: permission model rõ ràng (read / write / none) per contract trước khi build Gateway
- [ ] L0-Gateway: API contract (endpoint, request/response schema) locked trước khi surface build
- [ ] L0-Gateway: test direct call vào AI service bị chặn nếu không qua Gateway
- [ ] L0-ResultStore: schema migration reviewed, versioning contract rõ ràng
- [ ] L0-AuditLog: append-only constraint enforce ở DB level (không chỉ application)
- [ ] L0-AuditLog: ghi được từ S2 (ai_job_triggered), S4 (field_edited, approved), S5 (ai_job_rerun) — không chỉ S4
- [ ] L0-PDFIngestion: unit test với PDF text-layer + PDF scan + PDF corrupt
- [ ] L0-AIpipeline: egress guard test — block request ra ngoài whitelist
- [ ] Slice dọc: chạy end-to-end trên môi trường staging trước khi mở rộng
- [ ] DoD-2: validator từ chối trường không có source VÀ không có nhãn
- [ ] DoD-3: không có route nào tạo bản `approved` mà không qua S4 confirm
- [ ] DoD-5: mọi action trong S2, S4, S5 ghi audit log atomically (không chỉ S4)
- [ ] L0-AIpipeline: test D6-b — câu dữ kiện không neo bị cắt; sau cắt không đủ nghĩa → `insufficient_grounding` (AC-15-1b)
- [ ] L0-ResultStore: schema chứa được trạng thái theo trường + đa giá trị ①/đa đoạn ⑤ + con trỏ theo câu ⑥ — review trước migration
- [ ] Slice 1b: đo p95 (trường ① + ⑥) trên staging; vượt 30s → áp đòn bẩy 200→120 từ, ghi Dev Book
