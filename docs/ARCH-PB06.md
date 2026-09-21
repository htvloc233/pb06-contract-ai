# ARCH-PB06 — Thiết kế kiến trúc kỹ thuật MVP
### AI Tóm Tắt & Trích Xuất Hợp Đồng

> **Phiên bản:** 1.4 · **Ngày:** 2026-09-06
> **Input tham chiếu:** `SPEC-PB06.md` **v1.1** (signed off) · `MODULEMAP-PB06.md` **v1.2** · `SCOPE-PB06.md` **v3.2** (signed off)
> **Trạng thái:** Draft for Architecture Review
> **Mục tiêu:** Thiết kế đủ rõ để bắt đầu code MVP: sơ đồ container, data model, API contract, tech stack, mô hình phân quyền.

---

## Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.4** | 2026-09-06 | Đồng bộ `SPEC` v1.1 + `MODULEMAP` v1.2 (`DEVBOOK` DB-12). **AD-01 → AD-01b** + bảng mới `analysis_summary_sources` (neo-theo-câu, D6-b) và `analysis_field_items` (đa giá trị ①/đa đoạn ⑤). Enum trạng thái field tách khỏi trạng thái sửa (`grounded/uncertain/not_found` + `is_edited`); nhãn độ tin cậy bỏ `uncertain` (A6 v3.2). Bỏ `failed` khỏi `analysis_results.status`. API: 4.5 `items[]` + summary `status`/`sentences[]`; thêm **4.8b** PATCH summary; 4.3 thêm `pdf_type`; polling timeout theo nhánh (NFR-P2). Chốt thứ tự 6 hàng (UI-owned). `users.display_name` → Confidential. §8 thêm **Slice 1b**. Bỏ Apache PDFBox. |
| **1.3** | 2026-08-03 | Bản nhận được (văn bản tham chiếu) — viết trên SPEC v1.0 / MODULEMAP v1.1. |

---

## 1. Nguyên tắc kiến trúc

1. **Human-in-the-loop by default**
   AI chỉ tạo `draft_ai`. Kết quả chỉ trở thành dữ liệu chính thức khi user có quyền bấm **"Xác nhận & Lưu"** để chuyển sang `approved`. Downstream API/report chỉ đọc bản `approved`, không đọc trực tiếp `draft_ai`.

2. **Fail-closed grounding — hai nhánh (D6-a / D6-b)**
   *Trường trích xuất ①→⑤ (D6-a):* mỗi **giá trị** phải có `value + source_excerpt + page_number` khớp verbatim, hoặc nhãn `not_found`/`uncertain`; trường đa giá trị/đa đoạn: **mỗi giá trị một span** (AC-15-1a). *Trường tổng hợp ⑥ (D6-b):* mỗi **câu chứa dữ kiện** của tóm tắt phải có ≥1 con trỏ nguồn; câu không neo bị cắt; phần còn lại không đủ nghĩa → `insufficient_grounding` (AC-15-1b). Không có đường thứ ba. Nhãn độ tin cậy Cao/TB/Thấp là **thuộc tính hiển thị**, chỉ trên trường `grounded`, không bao giờ quyết định trạng thái (SCOPE A6 v3.2).

3. **API Gateway là cổng bắt buộc giữa Surface và Layer 0**
   UI không gọi trực tiếp AI service. Mọi request đi qua `L0-Gateway`, nơi kiểm tra auth, permission, chuẩn hóa request/response và route nội bộ đến AI service.

4. **Không persist raw contract text sau xử lý**
   File PDF gốc vẫn nằm trong storage hiện tại, nhưng text thô sau khi extract/OCR không được lưu dài hạn trong DB. DB chỉ lưu kết quả, metadata nguồn, source excerpt cần thiết, trạng thái, version và audit metadata.

5. **Audit-first, không retrofit sau**
   Các hành động `ai_job_triggered`, `ai_job_completed`, `field_edited`, `result_approved`, `ai_job_rerun` phải ghi audit log ngay từ đầu. Audit log là append-only, không xóa, không chứa full text hợp đồng.

---

## 2. Sơ đồ container

```text
+------------------------------------------------------------------+
|                         End Users                                |
|                                                                  |
|  Legal / Business User                  PM / Admin               |
|  - chọn/upload PDF                      - xem audit log          |
|  - chạy AI                              - nghiệm thu DoD         |
|  - review/edit/approve                                           |
+--------------------------+-------------------+-------------------+
                           |
                           v
+------------------------------------------------------------------+
|                  SaaS Web App - ReactJS                          |
|                                                                  |
|  S1 ContractEntry                                                |
|  S2 AnalysisTrigger                                              |
|  S3 ResultView                                                   |
|  S4 EditApprove                                                  |
|  S5 Reanalyze                                                    |
|  S6 AuditUI                                                      |
+--------------------------+---------------------------------------+
                           |
                           | HTTPS / Existing SaaS session or JWT
                           v
+------------------------------------------------------------------+
|              Existing SaaS Backend + L0-Gateway                  |
|                                                                  |
|  - Auth/session validation                                       |
|  - Contract-level permission check                               |
|  - REST API boundary: /analyze, /results, /approve, /audit       |
|  - Internal routing to AI Service                                |
|  - Blocks unauthorized direct behavior                           |
+----------------+---------------------+---------------------------+
                 |                     |
                 v                     v
+----------------------------+     +-------------------------------+
| PostgreSQL - Existing DB   |     | Object Storage                |
|                            |     |                               |
| Existing:                  |     | - Contract PDF files          |
| - users                    |     | - Existing uploaded files     |
| - contracts                |     |                               |
| - contract_files           |     +-------------------------------+
|                            |
| New MVP tables:            |
| - analysis_jobs            |
| - analysis_results         |
| - analysis_result_fields   |
| - analysis_field_items     |
| - analysis_field_sources   |
| - analysis_summary_sources |
| - audit_logs               |
| - ai_model_runs            |
+----------------------------+
                 |
                 | Internal network only
                 v
+------------------------------------------------------------------+
|                     AI Service - FastAPI                         |
|                                                                  |
|  L0-PDFIngestion                                                 |
|  - text-layer extraction                                         |
|  - OCR for scanned PDF                                           |
|  - page_number / char_offset metadata                            |
|                                                                  |
|  L0-AIpipeline                                                   |
|  - provider-agnostic LLM wrapper                                 |
|  - grounding validator                                           |
|  - egress guard                                                  |
|  - VI/EN handling                                                |
+--------------------------+---------------------------------------+
                           |
                           | Config-gated / whitelist only
                           v
+------------------------------------------------------------------+
|            LLM Runtime - Chưa chốt                               |
|                                                                  |
|  Option A: Self-hosted model                                     |
|  Option B: External LLM API after DPA + Legal/Security approval  |
+------------------------------------------------------------------+
```

### Ý nghĩa kiến trúc

- `SaaS Web App` chỉ chứa các module bề mặt mà user/PM nhìn thấy.
- `SaaS Backend + L0-Gateway` là cổng bắt buộc để enforce auth/permission và route nội bộ.
- `AI Service` xử lý PDF, OCR, gọi LLM và validate grounding.
- `PostgreSQL` lưu job, result, field, source metadata, version và audit log.
- LLM external vẫn **chưa chốt**, chỉ bật sau DPA và phê duyệt Legal/Security.

---

## 3. Data model

### 3.0 ERD — Relationship overview

```
[users] ──────────────────────────────────────────────────────────┐
   │ 1                                                             │
   │ N                                                             │
[analysis_jobs] ──────── N:1 ──── [contracts] ──── 1:N ── [contract_files]
   │ 1                                │ 1                          │ 1
   │                                  │                            │ (file_id FK
   │ 0..1                             │ N                          │  in jobs/results)
   │                                  │
[analysis_results] ◄── job_id FK    [audit_logs] (contract_id FK)
   │ 1
   │ N
[analysis_result_fields]
   │ 1
   │ N
[analysis_field_items]
   │ 1
   │ N
[analysis_field_sources]

[analysis_results] ── 1:N ── [analysis_summary_sources]
                              (con trỏ nguồn theo câu của tóm tắt — D6-b)

[analysis_jobs] ── 1:N ── [ai_model_runs]
```

**Ghi chú cardinality:**

| Relationship | Cardinality | Ghi chú |
|---|---|---|
| users → analysis_jobs | 1:N | 1 user có thể trigger nhiều job |
| contracts → analysis_jobs | 1:N | 1 contract có thể có nhiều lần phân tích |
| contracts → analysis_results | 1:N | N versions per contract (D7) |
| contracts → audit_logs | 1:N | Toàn bộ hành động ghi vào log |
| analysis_jobs → analysis_results | 1:0..1 | 1 job tạo tối đa 1 result; job failed thì không có result |
| analysis_results → analysis_result_fields | 1:N | Đúng 5 rows per result (5 trường cố định) |
| analysis_result_fields → analysis_field_items | 1:N | Đơn trị ②③④: đúng 1 item; đa giá trị ①/đa đoạn ⑤: ≥1 item (AC-05-4, AC-15-1a) |
| analysis_field_items → analysis_field_sources | 1:N | Item của field `grounded` có ≥1 source; field `not_found`/`uncertain` có 0 source |
| analysis_results → analysis_summary_sources | 1:N | 1 row per **câu dữ kiện** của tóm tắt (D6-b); `insufficient_grounding` → 0 rows |
| analysis_jobs → ai_model_runs | 1:N | 1 job có thể có nhiều model run (retry) |

---

### 3.1 Phân loại độ nhạy dữ liệu

| Mức | Ý nghĩa | Ví dụ |
|---|---|---|
| Public | Không nhạy cảm | Không dùng trong MVP này |
| Internal | Metadata vận hành | job status, timestamps, model version |
| Confidential | Dữ liệu nghiệp vụ khách hàng | contract metadata, approved extracted fields |
| Restricted | Dữ liệu hợp đồng nhạy cảm | PDF file, source excerpt, penalty clause, contract value |

---

### 3.2 Existing tables giả định

#### `users`

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `user_id` | UUID | Internal | Existing SaaS user ID |
| `email` | varchar | Confidential | Dùng auth/session |
| `display_name` | varchar | **Confidential** | Tên người thật = **dữ liệu cá nhân** (Luật BVDLCN 91/2025/QH15); hiển thị audit/UI có kiểm soát |
| `status` | enum | Internal | active/inactive |

#### `contracts`

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `contract_id` | UUID | Internal | Existing contract ID |
| `title` | varchar | Confidential | Tên hợp đồng |
| `owner_user_id` | UUID | Internal | Owner |
| `status` | enum | Internal | active/archived |
| `created_at` | timestamp | Internal | Existing |

#### `contract_files`

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `file_id` | UUID | Internal | Existing file ID |
| `contract_id` | UUID | Internal | FK |
| `file_name` | varchar | Confidential | File name có thể lộ thông tin |
| `mime_type` | varchar | Internal | Must be `application/pdf` |
| `storage_uri` | varchar | Restricted | Không expose trực tiếp ra client |
| `uploaded_by` | UUID | Internal | User ID |
| `uploaded_at` | timestamp | Internal | Existing |

---

### 3.3 New MVP tables

#### `analysis_jobs`

Lưu trạng thái xử lý mỗi lần user bấm phân tích hoặc phân tích lại.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `job_id` | UUID | Internal | PK |
| `contract_id` | UUID | Internal | FK to contracts |
| `file_id` | UUID | Internal | FK to contract_files |
| `triggered_by` | UUID | Internal | User who triggered |
| `job_type` | enum | Internal | `initial_analysis`, `reanalyze` |
| `status` | enum | Internal | `queued`, `processing`, `completed`, `failed`, `blocked` |
| `error_code` | varchar | Internal | `pdf_unreadable`, `llm_timeout`, `invalid_response`, etc. |
| `error_message` | text | Internal | Only system-generated sanitized message from controlled enum/template |
| `error_detail_ref` | varchar | Internal/Confidential | reference to secure log, if needed |
| `started_at` | timestamp | Internal | For SLA |
| `completed_at` | timestamp | Internal | For SLA |
| `created_at` | timestamp | Internal | Audit support |

#### `analysis_results`

Lưu một version kết quả AI hoặc kết quả đã approved.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `result_id` | UUID | Internal | PK |
| `contract_id` | UUID | Internal | FK |
| `job_id` | UUID | Internal | FK |
| `version_no` | integer | Internal | Increment per contract |
| `status` | enum | Internal | `draft_ai`, `approved` — **bỏ `failed`** (job lỗi không sinh result: AC-15-4, AC-03-3, và chính ERD 1:0..1 ở §3.0); không có `rejected` trong MVP |
| `summary_text` | text | Restricted | Tóm tắt hợp đồng, tối đa ~200 từ; `NULL` khi `summary_status='insufficient_grounding'` (AC-04-5) |
| `summary_status` | enum | Internal | `grounded`, `insufficient_grounding` (D6-b) — do kiểm tra neo-theo-câu quyết định, **không do model tự khai** |
| `summary_confidence` | enum | Internal | `high`, `medium`, `low` — **nullable**, chỉ có giá trị khi `summary_status='grounded'` (A6 v3.2: `uncertain` là trạng thái, không phải nhãn) |
| `user_summary_text` | text | Restricted | Bản tóm tắt do người sửa (US-07 áp cho cả trường ⑥ — API 4.8b); nullable |
| `summary_edited_by` | UUID | Internal | Nullable |
| `summary_edited_at` | timestamp | Internal | Nullable |
| `created_by_ai` | boolean | Internal | true for AI-generated |
| `approved_by` | UUID | Internal | Nullable until approved |
| `approved_at` | timestamp | Internal | Nullable |
| `created_at` | timestamp | Internal | Version timestamp |
| `updated_at` | timestamp | Internal | Last update |

#### Architecture Decision — Summary storage (AD-01b, thay thế AD-01)

> **Quyết định giữ nguyên từ AD-01:** summary lưu **result-level** tại `analysis_results`, không tạo hàng thứ 6 trong `analysis_result_fields`. Lý do gốc vẫn đúng: summary là thuộc tính của toàn bộ kết quả, và tránh special-case row với `field_key` ngoài 5 trường của D2.
>
> **Bổ sung v1.4 — vì sao AD-01 chưa đủ:** `SPEC` v1.1 §3.0 định nghĩa trường ⑥ là loại **Tổng hợp** với trạng thái và grounding riêng (D6-b). Bản AD-01 để summary thành trường duy nhất **không có grounding**: `analysis_field_sources` trỏ vào `field_id` mà summary không có field row ⇒ con trỏ nguồn theo câu không có chỗ nằm, AC-15-1b/AC-04-4 không implement được. Vá đúng phần thiếu, không đảo quyết định:
>
> - Thêm cột `summary_status` (`grounded` / `insufficient_grounding`) vào `analysis_results`
> - Thêm bảng **`analysis_summary_sources`** — 1 row per câu dữ kiện của tóm tắt
> - `summary_confidence` bỏ `uncertain`; nullable, chỉ khi `summary_status='grounded'`
> - Người sửa tóm tắt qua `user_summary_text` (API 4.8b)
>
> **Hệ quả cho API và UI:**
> - DB lưu: summary + status + sentence sources ở result-level; 5 trường theo chuỗi fields → items → sources
> - API trả: `summary` object (`text` · `status` · `confidence` · `sentences[]`) + `fields[]` (5 phần tử, mỗi field có `items[]`)
> - UI render: ghép thành 6 hàng theo thứ tự cố định (xem 4.5 design rule)
> - Dev **không** tạo 6 rows trong `analysis_result_fields`

#### `analysis_result_fields`

Lưu 5 extracted fields cố định và trạng thái từng field. Summary lưu ở `analysis_results` — xem AD-01b ở trên. Giá trị chi tiết của trường đa giá trị ①/đa đoạn ⑤ nằm ở `analysis_field_items` (**nguồn sự thật**); các cột value ở đây là bản render tổng hợp để đọc nhanh.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `field_id` | UUID | Internal | PK |
| `result_id` | UUID | Internal | FK |
| `field_key` | enum | Internal | `parties`, `effective_date`, `expiry_date`, `contract_value`, `penalty_clause` |
| `ai_value` | text | Restricted | Value AI đề xuất |
| `user_value` | text | Restricted | Value sau khi user sửa |
| `display_value` | text | Restricted | Prefer `user_value` nếu có |
| `status` | enum | Internal | `grounded`, `uncertain`, `not_found` — **chỉ trạng thái grounding** (§3.0 SPEC; đổi tên `extracted`→`grounded` cho khớp từ vựng). **Bỏ `edited`**: sửa nằm ở `is_edited`/`user_value` — nếu status nhảy sang `edited`, thông tin "AI từng `uncertain`" mất vĩnh viễn, đúng thứ audit và viva cần giữ |
| `confidence_label` | enum | Internal | `high`, `medium`, `low` — **nullable**, chỉ có giá trị khi `status='grounded'` (A6 v3.2) |
| `is_edited` | boolean | Internal | UI marking |
| `edited_by` | UUID | Internal | Nullable |
| `edited_at` | timestamp | Internal | Nullable |
| `created_at` | timestamp | Internal |  |

#### `analysis_field_items` *(mới ở v1.4)*

Giá trị đơn vị của mỗi trường — cho phép đa giá trị ① / đa đoạn ⑤ mà mỗi giá trị vẫn có span riêng (AC-05-4, AC-15-1a). Trường đơn trị ②③④ có đúng 1 item — mô hình đồng nhất, không special-case.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `item_id` | UUID | Internal | PK |
| `field_id` | UUID | Internal | FK to `analysis_result_fields` |
| `item_value` | text | Restricted | Một bên / một điều khoản / một giá trị đơn |
| `ord` | integer | Internal | Thứ tự hiển thị; UNIQUE (field_id, ord) |
| `created_at` | timestamp | Internal |  |

#### `analysis_field_sources`

Lưu đoạn nguồn cho **từng item** để grounding (D6-a).

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `source_id` | UUID | Internal | PK |
| `item_id` | UUID | Internal | FK to `analysis_field_items` |
| `contract_id` | UUID | Internal | FK |
| `file_id` | UUID | Internal | FK |
| `page_number` | integer | Internal | Page in PDF |
| `char_start` | integer | Internal | Optional |
| `char_end` | integer | Internal | Optional |
| `source_excerpt` | text | Restricted | Tối đa khoảng 3 dòng, chứa text hợp đồng |
| `source_hash` | varchar | Confidential | Hash để trace/integrity |
| `created_at` | timestamp | Internal |  |

#### `analysis_summary_sources` *(mới ở v1.4)*

Con trỏ nguồn theo **câu dữ kiện** của tóm tắt (D6-b, AC-15-1b, AC-04-4). `summary_status='insufficient_grounding'` → bảng này 0 rows cho result đó.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `source_id` | UUID | Internal | PK |
| `result_id` | UUID | Internal | FK to `analysis_results` |
| `sentence_index` | integer | Internal | Vị trí câu trong tóm tắt (0-based) |
| `sentence_hash` | varchar | Confidential | Hash câu — phát hiện tóm tắt bị sửa lệch khỏi nguồn đã kiểm |
| `page_number` | integer | Internal | Trang PDF |
| `char_start` | integer | Internal | Optional |
| `char_end` | integer | Internal | Optional |
| `source_excerpt` | text | Restricted | Đoạn gốc, tối đa ~3 dòng |
| `created_at` | timestamp | Internal |  |

#### `audit_logs`

Append-only log cho mọi hành động quan trọng.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `audit_id` | UUID | Internal | PK |
| `actor_user_id` | UUID | Internal | User thực hiện |
| `actor_role` | varchar | Internal | User/PM/System |
| `contract_id` | UUID | Internal | FK |
| `result_id` | UUID | Internal | Nullable |
| `job_id` | UUID | Internal | Nullable |
| `action_type` | enum | Internal | `ai_job_triggered`, `ai_job_completed`, `ai_job_failed`, `field_edited`, `result_approved`, `ai_job_rerun`, `unauthorized_attempt` |
| `field_key` | varchar | Internal | Nullable |
| `before_value` | text | Restricted | Chỉ field-level, không full contract text |
| `after_value` | text | Restricted | Chỉ field-level |
| `metadata_json` | jsonb | Confidential | request_id, error_code, page reference |
| `created_at` | timestamp | Internal | Append-only |

#### `ai_model_runs`

Lưu metadata model/pipeline để debug và audit kỹ thuật, không lưu prompt full contract text.

| Field | Type | Sensitive | Note |
|---|---|---|---|
| `model_run_id` | UUID | Internal | PK |
| `job_id` | UUID | Internal | FK |
| `provider_type` | enum | Internal | `self_hosted`, `external_api` |
| `provider_name` | varchar | Confidential | Chưa chốt |
| `model_name` | varchar | Confidential | Chưa chốt |
| `pipeline_version` | varchar | Internal | Version |
| `prompt_template_version` | varchar | Internal | Template version only |
| `egress_allowed` | boolean | Internal | From egress guard |
| `latency_ms` | integer | Internal | Performance |
| `token_count_in` | integer | Internal | Không bắt buộc nếu self-host |
| `token_count_out` | integer | Internal | Không bắt buộc |
| `created_at` | timestamp | Internal |  |

---

### 3.4 Database constraints & indexes

Các constraints phải được implement ở DB level, không chỉ application level.

#### `analysis_results`

```sql
-- Không có 2 version trùng số trong cùng 1 contract
UNIQUE (contract_id, version_no)

-- Status chỉ nhận 2 giá trị hợp lệ trong MVP (job lỗi không sinh result — AC-15-4)
CHECK (status IN ('draft_ai', 'approved'))

-- Trạng thái tóm tắt (D6-b)
CHECK (summary_status IN ('grounded', 'insufficient_grounding'))

-- KHÔNG dùng UNIQUE partial index WHERE status='approved'
-- Lý do: D7 yêu cầu giữ toàn bộ lịch sử approved — nhiều bản approved
-- trên cùng 1 contract là hợp lệ (mỗi lần reanalyze + approve = 1 version mới).
--
-- Downstream lấy approved mới nhất bằng:
--   ORDER BY approved_at DESC LIMIT 1
--   hoặc ORDER BY version_no DESC LIMIT 1
--
-- Nếu sau này cần đánh dấu "approved hiện hành":
--   Thêm cột is_current_approved BOOLEAN DEFAULT FALSE vào analysis_results
--   Partial unique index: UNIQUE (contract_id) WHERE is_current_approved = TRUE
--   Cập nhật is_current_approved = FALSE trên bản cũ khi approve bản mới
-- (Tính năng này là post-MVP nếu downstream cần signal rõ ràng)
```

#### `analysis_result_fields`

```sql
-- Không trùng field_key trong cùng 1 result
UNIQUE (result_id, field_key)

-- Chỉ 5 field keys cố định
CHECK (field_key IN ('parties', 'effective_date', 'expiry_date', 'contract_value', 'penalty_clause'))

-- Status field = trạng thái grounding thuần, KHÔNG chứa trạng thái sửa
CHECK (status IN ('grounded', 'not_found', 'uncertain'))
```

#### `analysis_field_sources`

Grounding rule hai nhánh, enforce ở **service layer** (L0-AIpipeline validator) vì FK chỉ tồn tại sau INSERT — không kiểm trước được:

- **D6-a (trường ①→⑤):** field `status='grounded'` ⇒ **mọi item** của field phải có ≥1 source khớp verbatim.
- **D6-b (trường ⑥):** `summary_status='grounded'` ⇒ **mọi câu dữ kiện** có ≥1 row trong `analysis_summary_sources` (câu không neo đã bị pipeline cắt); không đủ nghĩa sau khi cắt ⇒ `summary_status='insufficient_grounding'`, `summary_text=NULL`.
- **Người sửa KHÔNG cần source:** `user_value` / `user_summary_text` là thẩm quyền của người — D6 áp cho output AI, không áp cho input người (human-in-the-loop).

**Thứ tự transaction đúng ở service layer (L0-AIpipeline):**

```
BEGIN TRANSACTION
  1. INSERT analysis_result_fields            → nhận field_id (5 rows)
  2. INSERT analysis_field_items              → nhận item_id
     (đơn trị: 1 item; ①⑤: mỗi giá trị/điều khoản 1 item)
  3. INSERT analysis_field_sources            (item_id)
  4. INSERT analysis_results.summary_text + summary_status
     + analysis_summary_sources               (mỗi câu dữ kiện 1 row)
  5. VALIDATE D6-a: mỗi field status='grounded'
     → mọi item có ≥1 source, source_excerpt khớp verbatim text nguồn
  6. VALIDATE D6-b: summary_status='grounded'
     → mỗi câu dữ kiện có ≥1 row summary_sources
  7. IF validation fails → ROLLBACK toàn bộ transaction,
                           trả lỗi có cấu trúc về SaaS backend (AC-15-4)
  8. IF validation passes → COMMIT
END TRANSACTION

-- Field status IN ('not_found', 'uncertain'): items/sources optional, không validate
```

#### `audit_logs` — Append-only enforcement

Nói "append-only" ở mức tài liệu là không đủ; phải enforce ở một trong hai cách:

| Cơ chế | Cách làm | Trade-off |
|---|---|---|
| **DB trigger (recommended)** | `BEFORE UPDATE OR DELETE ON audit_logs RAISE EXCEPTION` | Enforce cứng nhất, không bypass được từ application |
| **Application DB role** | Role dùng cho app chỉ có `INSERT` trên `audit_logs`, không có `UPDATE/DELETE` | Dễ setup, nhưng DBA vẫn có thể bypass |
| **Row-level security** | PostgreSQL RLS policy cho phép INSERT, deny UPDATE/DELETE | Phù hợp nếu SaaS đã dùng RLS |

> Chọn ít nhất 1 cơ chế trước khi ship. Recommended: DB trigger + application role giới hạn.

---

## 4. API contract chính

### 4.1 Auth convention

- Tất cả endpoint dùng session/JWT hiện tại của SaaS.
- `L0-Gateway` gọi `L0-Auth` để kiểm tra quyền theo `contract_id`.
- Response lỗi phân quyền dùng `403`.
- Không expose `storage_uri`, raw PDF path hoặc AI service URL ra client.

---

### 4.2 — POST /api/contracts/{contract_id}/ai-analysis

Trigger phân tích AI.

**Permission:** user phải có quyền `write` hoặc quyền tương đương cho phép chạy AI trên hợp đồng. Read-only user bị chặn.

**Request**

```json
{
  "file_id": "uuid",
  "mode": "initial_analysis"
}
```

**Response 202**

```json
{
  "job_id": "uuid",
  "contract_id": "uuid",
  "status": "queued",
  "message": "AI analysis job created"
}
```

**Errors**

```json
{ "error": "forbidden", "message": "You do not have permission to analyze this contract" }
```

```json
{ "error": "job_already_running", "message": "Analysis is already in progress" }
```

---

### 4.3 — GET /api/ai-analysis/jobs/{job_id}

Lấy trạng thái job để UI hiển thị progress.

**Permission:** user phải có quyền đọc hợp đồng liên quan đến job.

**Response 200**

```json
{
  "job_id": "uuid",
  "contract_id": "uuid",
  "status": "processing",
  "pdf_type": "text_layer",
  "started_at": "2026-07-31T10:00:00Z",
  "completed_at": null,
  "error_code": null
}
```

> `pdf_type`: `text_layer` · `scan` · `null` (trước khi detect xong). Client dùng trường này để chọn timeout theo nhánh — xem 4.4.

---

### 4.4 Async job mechanism (S2-AnalysisTrigger)

**Luồng:**

```
UI  →  POST /analyze  →  202 + job_id
UI  →  GET /jobs/{job_id}  (polling)  →  status: processing
                                       →  status: completed  →  fetch results
                                       →  status: failed     →  show error
```

**Polling spec:**

- Interval: 3 giây.
- Timeout client-side **theo nhánh** (đọc `pdf_type` từ `GET /jobs/{job_id}`): **40 giây** cho PDF text-layer (buffer trên p95 30s — DoD-1); **70 giây** cho PDF scan (buffer trên target 60s — NFR-P2). Nếu không phân nhánh: job scan thành công ở giây 55 nhưng UI đã báo lỗi từ giây 40.
- Nếu timeout → UI hiển thị *"Phân tích mất nhiều thời gian hơn dự kiến — vui lòng thử lại"*; không tự retry.
- Nút "Phân tích bằng AI" bị disabled trong suốt thời gian polling (AC-03-2, AC-09-4).

**Backend job worker — [PROPOSAL, chưa chốt]:**

> ⚠️ Đây là kiến trúc đề xuất. Quyết định cuối do **Tech Lead / Platform team** chốt trước Sprint 1 dựa trên hạ tầng SaaS hiện tại.

| Option | Mô tả | Chọn khi |
|---|---|---|
| **A (Recommended):** Celery + Redis | Celery worker nhận job từ Redis queue, gọi AI Service, ghi kết quả về PostgreSQL. AI Service là FastAPI stateless. | SaaS chưa có job framework sẵn |
| **B:** Existing SaaS job framework | Dùng background job system đã có trong SaaS (Sidekiq, Resque, Bull…) nếu có | SaaS đã có job framework đang chạy — tránh thêm infra mới |
| **C:** FastAPI BackgroundTasks | Chạy job ngay trong AI Service process sau khi nhận request | Chỉ dùng nếu MVP scale nhỏ, không cần retry hoặc monitoring job |

Dù chọn option nào, interface contract không đổi: `POST /analyze` → 202 + `job_id` → `GET /jobs/{job_id}` để poll.

**Lý do chọn polling thay vì WebSocket/SSE:**
SaaS backend hiện tại là REST-based; thêm WebSocket làm tăng complexity infra trong MVP. 40–70s timeout + 3s interval tạo tối đa 13–23 request — chấp nhận được ở MVP scale.

---

### 4.5 — GET /api/contracts/{contract_id}/ai-results/latest

Lấy kết quả AI mới nhất để render S3-ResultView.

**Permission:** user phải có quyền đọc contract. Draft chỉ hiển thị trong UI review cho user có quyền phù hợp; downstream/report chỉ đọc approved.

**Response 200**

```json
{
  "result_id": "uuid",
  "contract_id": "uuid",
  "version_no": 3,
  "status": "draft_ai",
  "summary": {
    "text": "Short summary...",
    "status": "grounded",
    "confidence": "medium",
    "is_edited": false,
    "sentences": [
      {
        "index": 0,
        "sources": [
          { "page_number": 1, "source_excerpt": "This agreement is made between..." }
        ]
      }
    ]
  },
  "fields": [
    {
      "field_key": "parties",
      "label": "Các bên",
      "status": "grounded",
      "confidence": "high",
      "is_edited": false,
      "user_value": null,
      "display_value": "Company A · Company B",
      "items": [
        { "value": "Company A", "source": { "page_number": 1, "source_excerpt": "...between Company A..." } },
        { "value": "Company B", "source": { "page_number": 1, "source_excerpt": "...and Company B..." } }
      ]
    }
  ]
}
```

**Design rules (v1.4):**

- **Đa giá trị:** mỗi field trả `items[]`, mỗi item mang value + source riêng (AC-05-4). Trường đơn trị: `items[]` có đúng 1 phần tử.
- **Summary:** `status='insufficient_grounding'` ⇒ `text=null`, `sentences=[]` — UI hiển thị **nhãn trạng thái thay cho tóm tắt** (AC-04-5). `sentences[]` là dữ liệu để UI làm con trỏ nguồn theo câu (AC-04-4).
- **Nhãn độ tin cậy:** `confidence` chỉ xuất hiện khi `status='grounded'`; trường ở trạng thái khác hiển thị **nhãn trạng thái**, không hiển thị confidence (SCOPE A6 v3.2).

**Design rule — 6-row rendering (AC-05-3):**
API trả về `summary` object riêng và mảng `fields[]` gồm 5 trường. UI ghép thành 6 hàng theo thứ tự cố định:

| Thứ tự | Nguồn trong response | Hiển thị |
|---|---|---|
| 1 | `summary` | Tóm tắt (~200 từ) |
| 2 | `fields[field_key=parties]` | Các bên |
| 3 | `fields[field_key=effective_date]` | Ngày hiệu lực |
| 4 | `fields[field_key=expiry_date]` | Ngày hết hạn |
| 5 | `fields[field_key=contract_value]` | Giá trị hợp đồng |
| 6 | `fields[field_key=penalty_clause]` | Điều khoản phạt |

> **Chốt thứ tự (đối chiếu SPEC):** AC-05-1 liệt kê 6 trường theo mã ①→⑥ (Tóm tắt cuối) nhưng chỉ kiểm *đủ 6 hàng*, không kiểm thứ tự hiển thị. Thứ tự HIỂN THỊ chốt tại đây — **Tóm tắt hàng 1**, vì người dùng cần overview trước khi tra trường. Mọi tài liệu khác tham chiếu bảng này.

Nếu một field vắng mặt trong response → UI tự điền `{ status: "not_found" }`, không ẩn hàng.

---

### 4.6 — GET /api/contracts/{contract_id}/ai-results

Liệt kê tất cả versions kết quả của một hợp đồng. Dùng cho version selector ở S5-Reanalyze (AC-09-2).

**Permission:** user phải có quyền đọc contract.

**Response 200**

```json
{
  "contract_id": "uuid",
  "items": [
    { "result_id": "uuid", "version_no": 3, "status": "draft_ai", "created_at": "2026-07-31T10:00:00Z", "approved_by": null, "approved_at": null },
    { "result_id": "uuid", "version_no": 2, "status": "approved", "created_at": "2026-07-30T09:00:00Z", "approved_by": "uuid", "approved_at": "2026-07-30T09:30:00Z" }
  ]
}
```

**Design rule:** Sắp xếp theo `version_no` giảm dần (mới nhất lên đầu). Downstream API chỉ đọc bản `approved` mới nhất — không expose `draft_ai` ra ngoài UI review flow (NFR-A3).

---

### 4.7 — GET /api/ai-results/{result_id}

Lấy nội dung một version cụ thể. Dùng khi user chọn version khác trong selector (AC-09-2).

**Permission:** user phải có quyền đọc contract liên quan.

**Response 200** — cùng schema với 4.5 (`GET /ai-results/latest`), thêm trường `is_latest`:

```json
{
  "result_id": "uuid",
  "contract_id": "uuid",
  "version_no": 2,
  "status": "approved",
  "is_latest": false,
  "summary": { "text": "...", "status": "grounded", "confidence": "high" },
  "fields": [ "..." ],
  "approved_by": "uuid",
  "approved_at": "2026-07-30T09:30:00Z"
}
```

**Design rule:** `draft_ai` version chỉ trả về cho user có `contract:write`; user `contract:read` chỉ thấy `approved` versions.

---

### 4.8 — PATCH /api/ai-results/{result_id}/fields/{field_key}

User chỉnh sửa field trong bản draft_ai.

**Permission:** user phải có quyền `write`.

**Request**

```json
{ "user_value": "Corrected value" }
```

**Response 200**

```json
{
  "field_key": "contract_value",
  "status": "grounded",
  "is_edited": true,
  "display_value": "Corrected value",
  "edited_at": "2026-07-31T10:15:00Z"
}
```

**Audit:** ghi `field_edited` với before/after field-level value.

**Design rule (v1.4):** `status` giữ nguyên trạng thái grounding — **kể cả `uncertain`** — việc sửa chỉ bật `is_edited` và ghi `user_value`, để không mất dấu "AI từng không chắc". `user_value` là bản ghi đè cấp trường do người nhập, **không yêu cầu source** (D6 áp cho output AI, không áp cho người); `items[]` giữ nguyên bản ghi AI để đối chiếu và audit.

---

### 4.8b — PATCH /api/ai-results/{result_id}/summary *(mới ở v1.4)*

User chỉnh sửa tóm tắt trong bản draft_ai — US-07 áp cho **cả 6 trường**, trường ⑥ không thể không có đường sửa.

**Permission:** user phải có quyền `write`.

**Request**

```json
{ "user_summary": "Bản tóm tắt đã người sửa..." }
```

**Response 200**

```json
{
  "result_id": "uuid",
  "summary_status": "grounded",
  "is_edited": true,
  "display_text": "Bản tóm tắt đã người sửa...",
  "edited_at": "2026-07-31T10:18:00Z"
}
```

**Audit:** ghi `field_edited` với `field_key='summary'`, before/after áp rule truncate 500 ký tự (xem 4.11).

**Design rule:** `user_summary_text` là thẩm quyền của người — **không yêu cầu sentence sources** (D6-b áp cho output AI); `summary_status` và `analysis_summary_sources` giữ nguyên bản ghi AI để đối chiếu. Display ưu tiên `user_summary_text` khi có.

---

### 4.9 — POST /api/ai-results/{result_id}/approve

Chuyển draft_ai thành approved.

**Permission:** user phải có quyền `write/approve`.

**Request**

```json
{ "confirm_reviewed": true }
```

**Response 200**

```json
{ "result_id": "uuid", "status": "approved", "approved_by": "uuid", "approved_at": "2026-07-31T10:20:00Z" }
```

**Errors**

```json
{ "error": "invalid_state", "message": "Only draft_ai result can be approved" }
```

```json
{ "error": "forbidden", "message": "You do not have permission to approve this result" }
```

**Design rule:** không có route nào được tạo `approved` nếu không qua confirm endpoint này.

---

### 4.10 — POST /api/contracts/{contract_id}/ai-analysis/reanalyze

Chạy lại AI, tạo version draft_ai mới.

**Permission:** user phải có quyền `write`.

**Request**

```json
{ "file_id": "uuid", "reason": "manual_rerun" }
```

**Response 202**

```json
{ "job_id": "uuid", "contract_id": "uuid", "new_version_status": "pending", "message": "Re-analysis job created" }
```

**Errors**

```json
{ "error": "job_already_running", "message": "Analysis is already in progress" }
```

---

### 4.11 — GET /api/contracts/{contract_id}/audit-logs

PM/Admin xem audit log.

**Permission:** PM/Admin only. Legal/Business user bị 403.

**Query params**

```text
?from=2026-07-01&to=2026-07-31&action_type=field_edited
```

**Response 200**

```json
{
  "items": [
    {
      "audit_id": "uuid",
      "actor_user_id": "uuid",
      "actor_role": "legal_user",
      "action_type": "field_edited",
      "contract_id": "uuid",
      "result_id": "uuid",
      "field_key": "expiry_date",
      "before_value": "2027-01-01",
      "after_value": "2027-03-31",
      "created_at": "2026-07-31T10:15:00Z"
    },
    {
      "audit_id": "uuid",
      "actor_user_id": "uuid",
      "actor_role": "legal_user",
      "action_type": "result_approved",
      "contract_id": "uuid",
      "result_id": "uuid",
      "field_key": null,
      "before_value": null,
      "after_value": null,
      "created_at": "2026-07-31T10:20:00Z"
    }
  ]
}
```

**Design rule — before/after value:** `before_value` và `after_value` chỉ có giá trị với `action_type=field_edited` (AC-11-1). Với các action type khác (`ai_job_triggered`, `result_approved`…) hai trường này là `null`. Response không chứa full text hợp đồng — chỉ field-level value (NFR-S6, AC-11-3).

**Design rule — Long-text field truncation (Issue 7):**
Các field như `penalty_clause` có thể có giá trị dài và bản chất là nội dung hợp đồng. Để tránh audit log chứa đoạn văn bản hợp đồng dài (vi phạm tinh thần NFR-S6), áp dụng rule sau khi ghi `before_value` / `after_value`:

| Field type | Rule |
|---|---|
| Short fields (`parties`, `effective_date`, `expiry_date`, `contract_value`) | Ghi nguyên giá trị |
| Long-text fields (`penalty_clause`, `summary`) | Truncate tại **500 ký tự**, append `…[truncated]` nếu vượt ngưỡng |

```
audit_log.before_value = truncate(field.old_value, max_length=500)
audit_log.after_value  = truncate(field.new_value, max_length=500)
```

Không bao giờ ghi `source_excerpt` hoặc đoạn văn bản thô từ PDF vào audit log.

---

## 5. Tech stack đề xuất

| Layer | Stack đề xuất | Lý do |
|---|---|---|
| Web App | ReactJS | Phù hợp SaaS web hiện tại và surface modules: ContractEntry, AnalysisTrigger, ResultView, EditApprove, Reanalyze, AuditUI |
| SaaS Backend / Gateway | Existing SaaS backend controller layer | Tránh tạo gateway service mới ngoài scope; `L0-Gateway` là controller/API boundary trong backend hiện tại |
| AI Service | Python FastAPI | Phù hợp xử lý PDF/OCR/LLM theo service riêng |
| DB | PostgreSQL | Dùng DB SaaS hiện tại, lưu job/result/field/source/audit/version |
| Object Storage | Existing object storage / blob storage | Lưu PDF gốc, DB chỉ lưu metadata và kết quả |
| PDF text extraction | pdfplumber | Cần trích text-layer + metadata trang/offset **mức từ** cho grounding và trace nguồn. *(v1.4: bỏ Apache PDFBox — thư viện Java, lạc giữa stack Python)* |
| OCR | Tesseract/PaddleOCR hoặc OCR service nội bộ | PDF scan là capability bắt buộc, scan chất lượng kém là best-effort |
| LLM runtime | Provider-agnostic wrapper | External LLM chưa chốt; cần egress guard và whitelist |
| Async job worker | **[PROPOSAL]** Celery + Redis (recommended) hoặc existing SaaS job framework nếu có — xem 4.4 | Chưa chốt; decision owner: Tech Lead. Interface contract (202 + poll) không đổi dù chọn option nào |
| Deployment | Docker | Phù hợp tách AI service và Celery worker khỏi SaaS backend, triển khai nội bộ |
| Secret management | Existing secret manager | API key/secret không được hardcode trong source code |

---

## 6. Mô hình phân quyền

### 6.1 Role

| Role | Mô tả |
|---|---|
| Legal/Business User | Người dùng chính: chọn/upload hợp đồng, chạy AI, xem kết quả, sửa và duyệt nếu có quyền write |
| PM/Admin | Xem audit log, nghiệm thu DoD, không sửa/duyệt kết quả AI thay user trong MVP |
| AI Service | System role nội bộ, không có UI, chỉ được gọi qua SaaS backend/Gateway |

### 6.2 Permission model

| Permission | Ý nghĩa | Được phép | Không được phép |
|---|---|---|---|
| `contract:none` | Không có quyền trên contract | — | Mọi thứ → 403/404 |
| `contract:read` | Xem contract và **chỉ bản `approved`** | Xem `approved` result, source excerpt, status | Xem `draft_ai` · trigger AI · edit · approve · reanalyze |
| `contract:write` | Toàn quyền trên AI feature | Xem `draft_ai` và `approved` · trigger AI · edit field · approve · reanalyze | — |
| `audit:read` | Xem audit log | Xem toàn bộ audit log theo contract_id | Sửa/xóa log |
| `system:ai_service` | Service-to-service internal call | Gọi AI service qua internal network | Mọi endpoint public |

> **Rule quan trọng — draft visibility:** `contract:read` **không được** xem `draft_ai` result. `GET /ai-results/latest` và `GET /ai-results/{result_id}` phải kiểm tra permission trước khi trả về — nếu user là `contract:read` và result là `draft_ai` thì trả 404 (không phải 403 để tránh lộ sự tồn tại của draft). Chỉ `contract:write` mới thấy draft (NFR-A3).

### 6.3 Mapping permission AI → SaaS role hiện tại (NFR-A2)

Permission AI feature được suy ra từ role SaaS hiện tại — không tạo permission system mới. L0-Auth đọc role từ JWT/session SaaS và map sang permission AI:

| SaaS role (ví dụ) | AI permission | Hành động được phép |
|---|---|---|
| `contract_owner` | `contract:write` | Chạy AI, sửa, approve, re-analyze |
| `contract_editor` | `contract:write` | Chạy AI, sửa, approve, re-analyze |
| `contract_viewer` | `contract:read` | Xem result và source — không trigger, không sửa, không approve |
| Không có quyền | `contract:none` | 403/404 trên mọi endpoint |
| `pm_admin` | `contract:read` + `audit:read` | Xem result (không sửa/approve) + xem audit log |
| AI Service (internal) | `system:ai_service` | Gọi AI service qua internal network — không có UI |

> **Ghi chú:** Tên SaaS role cụ thể (`contract_owner`, `contract_editor`, `contract_viewer`) cần xác nhận với team SaaS hiện tại trước khi implement L0-Auth. Mapping trên là ví dụ — bản chốt phải đồng bộ với permission model của SaaS.

### 6.4 Use-case × role mapping

| Use case | Legal/Business User | PM/Admin | AI Service |
|---|---|---|---|
| UC-01: Phân tích hợp đồng từ danh sách | Allowed nếu có `contract:write`; read-only chỉ được xem, không trigger | Không có UI access | Không |
| UC-02: Upload và phân tích hợp đồng mới | Allowed nếu có quyền upload/create contract | Không có UI access | Không |
| UC-03: Review, sửa và duyệt kết quả | Allowed nếu có `contract:write`; read-only bị khóa edit/approve | Xem được nếu được cấp read, không sửa/duyệt | Không |
| UC-04: Chạy lại AI | Allowed nếu có `contract:write` và không có job đang chạy | Không | Không |
| UC-05: Kiểm tra audit trail | Không, bị 403 | Allowed với `audit:read` | Không |
| UC-06: Xử lý PDF và gọi LLM | Không | Không | Allowed, internal only |

---

## 7. Phần chưa chốt

1. **LLM deployment mode chưa chốt** — Chưa quyết định external LLM API hay self-host. External chỉ được bật sau DPA + Legal/Security approval. Hiện kiến trúc giữ provider-agnostic và egress guard đóng mặc định.
2. **External party access chưa chốt** — Đối tác/khách hàng bên ngoài chưa thuộc MVP vì auth model, phân quyền theo hợp đồng và threat model chưa xác định.
3. **OCR engine cụ thể chưa chốt** — MVP cần OCR capability cho PDF scan, nhưng engine cụ thể như Tesseract, PaddleOCR hay OCR service managed cần benchmark thêm theo dữ liệu thật.
4. **Confidence calibration chưa chốt** — MVP dùng nhãn heuristic `Cao/Trung bình/Thấp`, **chỉ hiển thị trên trường `grounded`** (`uncertain` là *trạng thái*, không phải nhãn — SCOPE A6 v3.2), không phải xác suất đúng đã hiệu chỉnh. Cấu hình **ngưỡng hiển thị nhãn** là post-MVP (US-12).
5. **Retention policy chi tiết chưa chốt** — Kiến trúc đã chốt không persist raw extracted text sau pipeline, nhưng retention cho `source_excerpt`, approved fields, audit log và model metadata cần Legal/Security xác nhận thêm.
6. **Mobile app không nằm trong MVP hiện tại** — Container diagram có thể mở rộng cho mobile sau này, nhưng SPEC và module map hiện chỉ mô tả SaaS web app surface modules.

---

## 8. Vertical slice đầu tiên để bắt đầu code

Lát cắt đầu tiên nên là:

> **Trích xuất field "Các bên" từ PDF text-layer và hiển thị kèm source.**

Flow tối thiểu:

```text
S1 ContractEntry
→ S2 AnalysisTrigger
→ L0-Gateway
→ L0-Auth
→ L0-PDFIngestion
→ L0-AIpipeline
→ L0-ResultStore
→ L0-AuditLog
→ S3 ResultView
```

Slice này đủ mỏng nhưng validate toàn bộ móng: auth, gateway, PDF ingestion, AI grounding (nhánh D6-a), result store, audit log và UI render 6 hàng.

**Slice 1b — bắt buộc ngay sau Slice 1 (MODULEMAP v1.2 §7):** cùng hợp đồng, thêm trường ⑥ — sinh tóm tắt → kiểm neo-theo-câu (AC-15-1b) → ghi `analysis_summary_sources` + `summary_status` → S3 render nhãn trạng thái thay tóm tắt nếu `insufficient_grounding` (AC-04-5) → **đo p95 end-to-end** (trường ① + ⑥). Vượt 30s → áp đòn bẩy đã chốt: rút tóm tắt ~200 → ~120 từ, *không* nới D6-b. Ghi kết quả đo + quyết định vào Dev Book.

Cả hai slice xanh rồi mới mở rộng chiều ngang: thêm 4 trường trích xuất còn lại, OCR, edit/approve, re-analyze và Audit UI — không làm thay đổi kiến trúc lõi.
