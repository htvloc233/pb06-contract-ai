# SPEC-PB06 — Software Requirement Specification
### AI Tóm Tắt & Trích Xuất Hợp Đồng (MVP)

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-06
> **Input:** `SCOPE-PB06.md` **v3.2** (locked)
> **Trạng thái:** ✅ **Signed off** — BA + Tech Lead (2026-09-06 · ghi nhận theo xác nhận của PM trong phiên)
>
> Artefact bước **[1] SW Spec chi tiết (SRS)** · Capstone Playbook · đề `PB-06` · drill EX-01

---

## 0. Changelog & Trạng thái phục hồi

| Version | Ngày | Nội dung |
|---|---|---|
| **1.1** | 2026-09-06 | **Đồng bộ với `SCOPE-PB06` v3.1.** Thêm **§3.0 Mô hình trạng thái trường** làm chuẩn duy nhất (cardinality + trạng thái + vai trò nhãn độ tin cậy). Tách **AC-15-1 → AC-15-1a** (D6-a, trường ①→⑤) **+ AC-15-1b** (D6-b, trường ⑥ neo theo câu). Thêm **AC-04-4** (DoD-7 vế b), **AC-04-5** (`insufficient_grounding`), **AC-05-4** (đa giá trị/đa đoạn). Mở rộng **AC-05-2**. Sửa câu chữ **US-12**, **NFR-AV4**, §6 Mapping (US-04·05·15). Không thêm trường, màn hình hay role mới. |
| **1.0** | 2026-07-29 | Bản đầu: §1 Tổng quan · §2 Người dùng & Role · §3 US-01→US-16 (43 AC) · §4 NFR (Hiệu năng · Bảo mật · Phân quyền · Khả dụng · Ngôn ngữ) · §5 Use Case theo role + ma trận phân quyền · §6 Mapping Story→DoD · §7 Out-of-Scope Confirmation. Input: `SCOPE-PB06.md` **v3.0**. |

### ⚠️ Ghi chú phục hồi

Tài liệu được dựng lại từ bản sao bị lỗi: khối tiêu đề lặp theo trang của chính tài liệu bị chèn đè vào thân văn bản tại các điểm ngắt trang, **xoá mất chữ tại chỗ nó rơi vào**.

**Đã phục hồi — cơ học, không rủi ro.** Từ khóa `Given` / `When` / `Then` của toàn bộ **43 Acceptance Criteria**.

**Đã phục hồi — theo bằng chứng nội tại.** Bốn token trạng thái `draft_ai` · `approved` · `not_found` · `uncertain`, căn cứ vào AC-15-1 và AC-16-3 (còn nguyên vẹn) và `SCOPE-PB06` D3 · D6 · D7. Vị trí: AC-05-2 · AC-06-2 · AC-06-3 · AC-07-1 · AC-08-1→4 · AC-09-1 · AC-09-3 · AC-16-4 · NFR-A3 · UC-03 · UC-04.

**Đã bổ sung từ bản gốc (người dùng cung cấp) — không còn nhãn `[THIẾU]` nào trong thân tài liệu:**

| # | Vị trí | Nội dung đã điền |
|---|---|---|
| 1 | Header | Phiên bản **1.0** · ngày **2026-07-29** · Input `SCOPE-PB06.md` (locked) |
| 2 | §1 · §2 · §3 · §3.1 | Tổng quan · Người dùng & Role · câu dẫn ký hiệu [MVP] · tiêu đề mục |
| 3 | US-01 · US-02 | Story + 6 AC (AC-01-1→3, AC-02-1→3) |
| 4 | US-03 | Tiêu đề story · AC-03-1 · AC-03-2 (gạch đầu dòng `When` đã xác định) |
| 5 | AC-05-2 | Tiêu đề: *Trạng thái `not_found` và `uncertain` hiển thị rõ* |
| 6 | AC-06-2 | Nhãn độ tin cậy: **Cao / Trung bình / Thấp** |
| 7 | AC-14-2 | Nhãn cho trường không trích được: `not_found` / `uncertain` |
| 8 | US-09 · US-12 | Cụm thiếu trong câu Story: `approved` · `uncertain` |
| 9 | §5.0 | Câu dẫn: "được phép và **không được phép**" |
| 10 | UC-06 bước 8 | Trả `draft_ai` response *(bản gốc gõ "dratf_ai" — đã sửa chính tả)* |

**Bất thường về thứ tự đã sắp lại:** bản gốc để AC-06-3 trước AC-06-2, và §4.5 trước §4.4. Đã đưa về đúng thứ tự số.

### ✅ Đồng bộ phiên bản — đã xử lý ở v1.1

SPEC v1.0 viết trên SCOPE v3.0, tụt lại sau khi SCOPE lên v3.1 (tách D6 thành D6-a/D6-b). Bốn điểm lệch đã được đóng:

| # | Điểm lệch (v1.0) | Cách đóng ở v1.1 |
|---|---|---|
| 1 | **AC-15-1** đòi mỗi trong 6 trường có 1 `source_excerpt` hoặc nhãn — không đủ cho trường ⑥ | Tách **AC-15-1a** (D6-a) + **AC-15-1b** (D6-b, neo theo câu dữ kiện) |
| 2 | Trạng thái **`insufficient_grounding`** chưa xuất hiện ở đâu | Đưa vào đúng 3 chỗ: sinh ra (AC-15-1b) · hiển thị (**AC-04-5**) · render bảng (**AC-05-2**) |
| 3 | **AC-04-1** chỉ kiểm tóm tắt *đủ hiểu* | Thêm **AC-04-4** cho DoD-7 vế (b) — hai phép đo khác nhau nên tách hai AC |
| 4 | Cardinality 6 trường chưa vào SPEC | **§3.0** định nghĩa một lần; thêm **AC-05-4** cho đa giá trị/đa đoạn |

**Điểm mơ hồ nhãn-vs-trạng thái đã chốt tại §3.0, và được ghi thành văn ở `SCOPE` **A6** (v3.2):** nhãn độ tin cậy (Cao/Trung bình/Thấp) là **thuộc tính hiển thị**, chỉ áp cho trường `grounded`, và **không bao giờ quyết định trạng thái**. Căn cứ: D6 quy định cổng là grounding cơ học, A6 quy định confidence chỉ là chỉ báo heuristic — để một số heuristic làm cổng gác là trái cả hai.

> **Cổng vào bước [2]: MỞ.** Hết nhãn `[THIẾU]`, hết lệch phiên bản, hết mơ hồ nhãn-vs-trạng thái; **đã sign-off BA + Tech Lead (2026-09-06)** ⇒ đủ điều kiện làm input cho Module Map / Architecture.

---

## 1. Tổng quan

Tài liệu này mô tả các yêu cầu phần mềm cho tính năng AI tóm tắt và trích xuất trường hợp đồng, tích hợp vào SaaS quản lý hợp đồng hiện có. Mọi yêu cầu đều bám sát `SCOPE-PB06` và đề bài gốc `PB-06`.

**Nguyên tắc thiết kế xuyên suốt:**

- Con người chốt — AI chỉ là bản nháp chờ duyệt.
- Grounding bắt buộc — mọi trường phải có nguồn hoặc nhãn rõ.
- Fail-closed — không có nguồn thì không xuất trường.
- Mặc định không gửi hợp đồng ra ngoài vùng cho phép.

---

## 2. Người dùng & Role

| Role | Mô tả | Quyền chính |
|---|---|---|
| **Nhân viên pháp chế/kinh doanh (User)** | Người trực tiếp dùng tính năng AI hằng ngày | Upload/chọn HĐ, kích hoạt AI, review, sửa, duyệt |
| **Quản trị sản phẩm (PM/Admin)** | Người duyệt nghiệm thu, giám sát quy trình | Xem audit log, nghiệm thu DoD |
| **Hệ thống AI (Internal/System)** | FastAPI service xử lý PDF và gọi LLM | Trích text, OCR, gọi model, trả kết quả có grounding |

> Xem **OI-01** trong `SCOPE-PB06` nếu cần bổ sung role external parties sau này.

---

## 3. User Stories & Acceptance Criteria

Ký hiệu: **[MVP]** = thuộc phạm vi MVP 8 tuần. Story không có tag = post-MVP.

---

### 3.0 Mô hình trạng thái trường — chuẩn duy nhất

Nguồn: `SCOPE-PB06` v3.2 §4 (cardinality) + **D6-a** / **D6-b** (grounding) + **A6** (vai trò nhãn độ tin cậy). **Mọi AC trong §3 tham chiếu về bảng này, không định nghĩa lại.**

**Cardinality — nguồn bắt buộc theo loại trường**

| Loại | Trường | Nguồn bắt buộc |
|---|---|---|
| Đơn trị | ② Ngày hiệu lực · ③ Ngày hết hạn · ④ Giá trị hợp đồng | 1 span |
| Đa giá trị | ① Các bên | ≥1 span cho **mỗi bên** |
| Đa đoạn | ⑤ Điều khoản phạt | ≥1 span cho **mỗi điều khoản** |
| Tổng hợp | ⑥ Tóm tắt | ≥1 span cho **mỗi câu chứa dữ kiện** (D6-b) |

**Trạng thái — do kiểm tra grounding quyết định (cơ học, KHÔNG do model tự khai)**

| Trạng thái | Điều kiện | Áp dụng |
|---|---|---|
| `grounded` | span khớp verbatim + parse đúng kiểu + 1 ứng viên | ① → ⑤ |
| `uncertain` | có span nhưng nhiều ứng viên, hoặc kiểu dữ liệu mơ hồ | ① → ⑤ |
| `not_found` | không có span khớp verbatim | ① → ⑤ |
| `insufficient_grounding` | sau khi cắt câu không neo được, phần còn lại không đủ nghĩa | ⑥ |

**Nhãn độ tin cậy (Cao / Trung bình / Thấp) — thuộc tính HIỂN THỊ, không phải trạng thái:**

- Chỉ hiển thị trên trường ở trạng thái `grounded`.
- Là ước tính heuristic (A6) — **không bao giờ quyết định trạng thái**.
- Trường ở `uncertain` / `not_found` / `insufficient_grounding` hiển thị **nhãn trạng thái**, không hiển thị nhãn độ tin cậy.

---

### 3.1 Role: Nhân viên pháp chế / Kinh doanh

---

#### US-01 [MVP] — Chọn hợp đồng PDF đã có trong SaaS

**Story:** Là nhân viên pháp chế, tôi muốn chọn một hợp đồng PDF đã có sẵn trong danh sách hồ sơ của SaaS để đưa vào phân tích AI, để tôi không phải upload lại file đã tồn tại trong hệ thống.

**Acceptance Criteria:**

**AC-01-1: Hiển thị nút phân tích**
- **Given** tôi đang xem chi tiết một hợp đồng có file PDF đính kèm trong SaaS
- **When** tôi mở trang hồ sơ hợp đồng đó
- **Then** nút "Phân tích bằng AI" xuất hiện và ở trạng thái active

**AC-01-2: Hợp đồng không có PDF thì ẩn nút**
- **Given** hồ sơ hợp đồng không có file PDF đính kèm
- **When** tôi mở trang hồ sơ đó
- **Then** nút "Phân tích bằng AI" không hiển thị hoặc bị disabled với tooltip giải thích lý do

**AC-01-3: User không có quyền đọc hợp đồng bị chặn**
- **Given** tôi không có quyền đọc hợp đồng này trong SaaS (ví dụ: truy cập trực tiếp qua URL)
- **When** tôi cố mở trang hồ sơ hợp đồng đó
- **Then** hệ thống trả về lỗi truy cập (403/404); không hiển thị bất kỳ nội dung hợp đồng hay kết quả AI nào

---

#### US-02 [MVP] — Upload hợp đồng PDF mới

**Story:** Là nhân viên pháp chế, tôi muốn upload một hợp đồng PDF mới lên SaaS bằng chức năng upload sẵn có, để tôi có thể phân tích hợp đồng vừa nhận mà chưa có trong hệ thống.

**Acceptance Criteria:**

**AC-02-1: Upload thành công rồi mới hiện nút phân tích**
- **Given** tôi chưa có hợp đồng trong SaaS
- **When** tôi upload file PDF hợp lệ qua chức năng upload của SaaS và upload thành công
- **Then** hồ sơ hợp đồng mới được tạo, file PDF đính kèm, nút "Phân tích bằng AI" xuất hiện

**AC-02-2: Từ chối file không phải PDF**
- **Given** tôi cố upload file không phải PDF (ví dụ `.docx`, `.jpg`)
- **When** tôi chọn file và xác nhận upload
- **Then** hệ thống hiện thông báo lỗi định dạng, không tạo hồ sơ mới

**AC-02-3: User không có quyền upload/tạo hợp đồng mới bị chặn**
- **Given** tôi không có quyền tạo hợp đồng mới trong SaaS (role view-only)
- **When** tôi cố thực hiện upload file PDF
- **Then** hệ thống từ chối với lỗi phân quyền (403); không tạo hồ sơ hợp đồng mới; UI không hiển thị nút upload với role này

---

#### US-03 [MVP] — Kích hoạt phân tích AI

**Story:** Là nhân viên pháp chế, tôi muốn bấm "Phân tích bằng AI" và nhận kết quả trong thời gian hợp lý, để tôi không phải chờ đợi lâu giữa các hợp đồng cần xử lý.

**Acceptance Criteria:**

**AC-03-1: Phản hồi trong SLA**
- **Given** tôi đang xem hồ sơ hợp đồng có file PDF hợp lệ (~20 trang, text-layer)
- **When** tôi bấm "Phân tích bằng AI"
- **Then** hệ thống bắt đầu xử lý, hiện progress indicator, và trả về kết quả trong vòng 30 giây (p95)

**AC-03-2: Progress indicator trong quá trình xử lý**
- **Given** tôi đã bấm "Phân tích bằng AI"
- **When** hệ thống đang xử lý
- **Then** UI hiển thị trạng thái đang xử lý, nút "Phân tích bằng AI" bị disabled để tránh double-submit

**AC-03-3: Xử lý lỗi khi phân tích thất bại**
- **Given** hệ thống gặp lỗi trong quá trình phân tích (timeout, lỗi pipeline)
- **When** quá trình phân tích kết thúc với lỗi
- **Then** UI hiển thị thông báo lỗi rõ ràng, cho phép thử lại, không lưu kết quả nháp nào

**AC-03-4: User chỉ có quyền đọc không được kích hoạt phân tích AI**
- **Given** tôi là user chỉ có quyền đọc (read-only) trên hợp đồng này
- **When** tôi cố bấm "Phân tích bằng AI" (hoặc gọi API trigger trực tiếp)
- **Then** hệ thống từ chối với lỗi phân quyền (403); không tạo job phân tích mới; không tốn LLM token; nút "Phân tích bằng AI" không hiển thị hoặc bị disabled với role này

---

#### US-04 [MVP] — Xem tóm tắt hợp đồng

**Story:** Là nhân viên pháp chế, tôi muốn xem bản tóm tắt ngắn (~200 từ) do AI tạo ra, để tôi nắm được nội dung tổng thể của hợp đồng mà không cần đọc toàn văn.

**Acceptance Criteria:**

**AC-04-1: Tóm tắt luôn có và đạt ngưỡng chất lượng tối thiểu**
- **Given** AI đã hoàn thành phân tích hợp đồng
- **When** kết quả hiển thị trên UI
- **Then** phần tóm tắt luôn có nội dung, đủ để người đọc hiểu được chủ thể, mục đích và các bên của hợp đồng mà không cần đọc nguyên văn (DoD-7)

**AC-04-2: Độ dài tóm tắt**
- **Given** AI đã tạo tóm tắt
- **When** tóm tắt được hiển thị
- **Then** tóm tắt không vượt quá 200 từ

**AC-04-3: Trạng thái khi phân tích thất bại trước khi tạo được tóm tắt**
- **Given** pipeline AI gặp lỗi và kết thúc mà không tạo ra kết quả (timeout, lỗi LLM, file không đọc được)
- **When** người dùng mở trang kết quả AI của hợp đồng đó
- **Then** UI hiển thị trạng thái lỗi rõ ràng với thông báo "Phân tích thất bại — vui lòng thử lại"; không hiển thị tóm tắt trống, không hiển thị bảng trường rỗng; có nút cho phép chạy lại

**AC-04-4: Tóm tắt neo được về nguồn** *(DoD-7 vế b)*
- **Given** AI đã trả tóm tắt ở trạng thái `grounded`
- **When** người dùng mở trang kết quả
- **Then** mọi câu chứa dữ kiện trong tóm tắt đều có con trỏ nguồn đối chiếu được; **0 câu dữ kiện không neo** trên mẫu nghiệm thu 5 hợp đồng thực tế (§3.0, D6-b)

> Cách hiển thị con trỏ nguồn (hover · click · số chú thích cuối câu) là **quyết định UX ở bước [3]**, cố ý không chốt trong SPEC.

**AC-04-5: Tóm tắt không đủ nguồn**
- **Given** pipeline trả trường ⑥ ở trạng thái `insufficient_grounding` (AC-15-1b)
- **When** trang kết quả render
- **Then** UI hiển thị nhãn trạng thái rõ ràng **thay cho** tóm tắt; không hiển thị tóm tắt một phần; không hiển thị ô trống; người dùng biết ngay cần tự đọc hợp đồng

---

#### US-05 [MVP] — Xem bảng 6 trường trích xuất

**Story:** Là nhân viên pháp chế, tôi muốn xem bảng 6 trường quan trọng được AI trích xuất từ hợp đồng, để tôi tra cứu nhanh thông tin cốt lõi mà không cần tìm từng trang.

**Acceptance Criteria:**

**AC-05-1: Đủ 6 trường, mỗi trường có giá trị hoặc trạng thái**
- **Given** AI đã hoàn thành phân tích
- **When** bảng kết quả hiển thị
- **Then** bảng có đúng 6 trường: Các bên · Ngày hiệu lực · Ngày hết hạn · Giá trị hợp đồng · Điều khoản phạt · Tóm tắt; mỗi trường có giá trị hoặc nhãn trạng thái rõ ràng — không có trường trống không giải thích

**AC-05-2: Trạng thái `not_found`, `uncertain` và `insufficient_grounding` hiển thị rõ**
- **Given** AI không tìm thấy, không chắc về giá trị một trường, hoặc không neo đủ nguồn cho tóm tắt
- **When** kết quả hiển thị
- **Then** trường đó hiển thị nhãn `not_found` / `uncertain` / `insufficient_grounding` bằng màu/icon khác biệt — không hiển thị giá trị giả mạo; trường ở các trạng thái này **không** hiển thị nhãn độ tin cậy (§3.0)

**AC-05-3: UI luôn render đủ 6 hàng dù backend trả về thiếu field**
- **Given** API response chỉ chứa 5 field (ví dụ: một field bị drop do lỗi pipeline hoặc malformed response)
- **When** bảng kết quả render trên UI
- **Then** UI vẫn hiển thị đủ 6 hàng tương ứng 6 trường cố định; field thiếu trong response được render tự động là "Không tìm thấy"; không có hàng nào bị ẩn hoặc bỏ qua silently

**AC-05-4: Trường đa giá trị / đa đoạn hiển thị đủ**
- **Given** hợp đồng có nhiều hơn một bên (trường ①) hoặc nhiều điều khoản phạt (trường ⑤)
- **When** bảng kết quả hiển thị
- **Then** UI hiển thị **đủ mọi giá trị**, mỗi giá trị có span riêng để đối chiếu; không cắt còn 1 giá trị; không gộp thành 1 chuỗi làm mất khả năng đối chiếu từng span (§3.0)

---

#### US-06 [MVP] — Xem nguồn trích dẫn cho mỗi trường

**Story:** Là nhân viên pháp chế, tôi muốn xem đoạn trích gốc và số trang trong hợp đồng tương ứng với mỗi trường được trích xuất, để tôi có thể đối chiếu trực tiếp với hợp đồng gốc và xác nhận tính chính xác.

**Acceptance Criteria:**

**AC-06-1: Mỗi trường có nguồn hoặc nhãn**
- **Given** AI đã trích xuất một trường với giá trị
- **When** trường đó hiển thị trên UI
- **Then** bên cạnh giá trị có: số trang và đoạn trích ngắn từ hợp đồng gốc (≤ 3 dòng) (DoD-2)

**AC-06-2: Hiển thị nhãn độ tin cậy và cảnh báo heuristic trên mọi trường**
- **Given** AI đã trả kết quả cho một trường (dù có giá trị hay uncertain)
- **When** trường đó hiển thị trên UI
- **Then** UI hiển thị nhãn ước tính độ tin cậy **Cao / Trung bình / Thấp** tương ứng với mức confidence từ pipeline; trường `uncertain` hiển thị nhãn bằng màu/icon cảnh báo nổi bật; tất cả nhãn confidence đi kèm chú thích ngắn *"Đây là ước tính hỗ trợ, không phải xác suất chính xác"* để người dùng không bỏ bước đối chiếu nguồn (A6, DoD-6)

**AC-06-3: Trường không có nguồn grounding hiển thị nhãn rõ ràng thay vì trống**
- **Given** AI đã xử lý nhưng không tìm được đoạn nguồn cho một trường (grounding failure ở pipeline — AC-15-1)
- **When** bảng kết quả render trên UI
- **Then** trường đó hiển thị nhãn `not_found` hoặc `uncertain` bằng màu/icon cảnh báo nổi bật; không hiển thị ô trống; không hiển thị giá trị giả; user biết ngay trường này cần tự điền thủ công

---

#### US-07 [MVP] — Chỉnh sửa giá trị trường trước khi lưu

**Story:** Là nhân viên pháp chế, tôi muốn chỉnh sửa trực tiếp giá trị của từng trường mà AI đề xuất, để tôi có thể sửa thông tin không chính xác trước khi xác nhận lưu chính thức.

**Acceptance Criteria:**

**AC-07-1: Inline editing trên từng trường**
- **Given** kết quả AI đang hiển thị ở trạng thái `draft_ai`
- **When** tôi click vào giá trị của một trường
- **Then** trường chuyển sang chế độ edit, tôi có thể nhập giá trị mới

**AC-07-2: UI phân biệt giá trị AI vs giá trị đã chỉnh sửa**
- **Given** tôi đã chỉnh sửa một trường
- **When** xem lại bảng kết quả
- **Then** trường đã chỉnh sửa được đánh dấu khác biệt so với trường giữ nguyên giá trị AI (ví dụ: icon bút, màu khác)

**AC-07-3: Không mất dữ liệu khi reload nhưng chưa save**
- **Given** tôi đã chỉnh sửa một hoặc nhiều trường nhưng chưa bấm "Xác nhận & Lưu"
- **When** tôi vô tình reload trang
- **Then** UI hiển thị cảnh báo có thay đổi chưa lưu trước khi rời trang

**AC-07-4: User chỉ có quyền đọc không được chỉnh sửa**
- **Given** tôi là user chỉ có quyền đọc (read-only) trên hợp đồng này trong SaaS
- **When** tôi xem trang kết quả AI và click vào giá trị một trường
- **Then** trường không chuyển sang chế độ edit; UI hiển thị icon khóa hoặc tooltip "Bạn không có quyền chỉnh sửa hợp đồng này"; nút "Xác nhận & Lưu" bị ẩn hoặc disabled

---

#### US-08 [MVP] — Xác nhận và lưu kết quả đã duyệt

**Story:** Là nhân viên pháp chế, tôi muốn bấm "Xác nhận & Lưu" sau khi kiểm tra xong để kết quả được lưu chính thức gắn vào hồ sơ hợp đồng, để downstream và báo cáo có thể đọc dữ liệu đã được xác nhận.

**Acceptance Criteria:**

**AC-08-1: Chỉ lưu khi người dùng bấm xác nhận**
- **Given** AI đã trả kết quả ở trạng thái `draft_ai`
- **When** tôi chưa bấm "Xác nhận & Lưu"
- **Then** không có bản ghi `approved` nào được tạo — hệ thống không tự động approve (DoD-3)

**AC-08-2: Lưu thành công chuyển trạng thái**
- **Given** tôi đã xem qua và bấm "Xác nhận & Lưu"
- **When** hệ thống xử lý xong
- **Then** kết quả chuyển sang trạng thái `approved`, gắn vào hồ sơ hợp đồng, UI xác nhận lưu thành công

**AC-08-3: Downstream chỉ đọc bản approved**
- **Given** có bản `approved` đã lưu
- **When** API hoặc báo cáo đọc kết quả hợp đồng
- **Then** chỉ trả về bản `approved` mới nhất; bản `draft_ai` không lộ ra ngoài

**AC-08-4: User không có quyền approve bị chặn**
- **Given** tôi là user chỉ có quyền đọc (read-only) trên hợp đồng này
- **When** tôi cố bấm "Xác nhận & Lưu" (hoặc gọi API approve trực tiếp)
- **Then** hệ thống trả về lỗi phân quyền (403); không có bản `approved` nào được tạo; hành động được ghi vào audit log như một "unauthorized approve attempt"

---

#### US-09 [MVP] — Chạy lại AI mà không mất bản đã duyệt

**Story:** Là nhân viên pháp chế, tôi muốn chạy lại phân tích AI trên hợp đồng đã có kết quả `approved`, để tôi có thể so sánh hoặc cập nhật mà không mất lịch sử đã duyệt.

**Acceptance Criteria:**

**AC-09-1: Chạy lại tạo version mới, không ghi đè**
- **Given** hợp đồng đã có bản kết quả `approved`
- **When** tôi bấm "Phân tích lại bằng AI"
- **Then** một version `draft_ai` mới được tạo; bản `approved` cũ giữ nguyên và vẫn truy cập được (D7)

**AC-09-2: UI hiển thị rõ version đang xem**
- **Given** hợp đồng có nhiều version kết quả
- **When** tôi mở trang kết quả AI
- **Then** UI hiển thị rõ đang xem version nào (draft/approved, timestamp) và cho phép chuyển đổi giữa các version

**AC-09-3: User chỉ có quyền đọc không được chạy lại AI**
- **Given** tôi là user chỉ có quyền đọc (read-only) trên hợp đồng này
- **When** tôi cố bấm "Phân tích lại bằng AI"
- **Then** hệ thống từ chối với lỗi phân quyền (403); không tạo version `draft_ai` mới; nút "Phân tích lại" không hiển thị hoặc disabled với role này

**AC-09-4: Từ chối job mới khi đang có phân tích đang chạy**
- **Given** hợp đồng đang có một job phân tích AI chưa hoàn thành (đang processing)
- **When** tôi bấm "Phân tích lại bằng AI" lần thứ hai
- **Then** hệ thống từ chối tạo job mới; hiển thị thông báo "Phân tích đang được thực hiện — vui lòng chờ"; không spawn job song song; không tốn thêm LLM token

---

#### US-10 — Xem lịch sử các phiên phân tích *(Post-MVP)*

**Story:** Là nhân viên pháp chế, tôi muốn xem danh sách tất cả các phiên phân tích AI đã chạy trên một hợp đồng cùng trạng thái của từng phiên, để tôi theo dõi được lịch sử thay đổi.

> **Post-MVP** — Phụ thuộc vào versioning UI đủ trưởng thành sau MVP.

---

### 3.2 Role: Quản trị sản phẩm (PM/Admin)

---

#### US-11 [MVP] — Xem nhật ký kiểm toán

**Story:** Là Quản trị sản phẩm, tôi muốn xem nhật ký ghi lại đầy đủ ai chạy AI, ai sửa trường nào, ai duyệt và vào lúc nào, để tôi có thể kiểm tra tính hợp lệ của quy trình và truy vết khi có sự cố.

**Acceptance Criteria:**

**AC-11-1: Log đầy đủ mọi hành động**
- **Given** người dùng thực hiện bất kỳ hành động nào (chạy AI / sửa trường / duyệt)
- **When** hành động hoàn thành
- **Then** audit log ghi lại: `user_id`, `action_type`, `timestamp`, `contract_id`, và với hành động sửa trường: `before_value` + `after_value` (DoD-5)

**AC-11-2: Log không thể xóa**
- **Given** bản ghi audit log đã được tạo
- **When** bất kỳ user nào (kể cả admin) cố xóa log
- **Then** hệ thống từ chối; log là append-only

**AC-11-3: Không lưu nội dung hợp đồng trong log**
- **Given** người dùng chạy AI hoặc sửa trường
- **When** log được ghi
- **Then** log không chứa nội dung văn bản hợp đồng — chỉ chứa metadata (`field_name`, before/after value, page reference)

**AC-11-4: Có thể query log theo hợp đồng**
- **Given** PM muốn kiểm tra một hợp đồng cụ thể
- **When** PM truy vấn audit log theo `contract_id`
- **Then** hệ thống trả về toàn bộ lịch sử hành động trên hợp đồng đó theo thứ tự thời gian

**AC-11-5: Nhân viên pháp chế / kinh doanh không được xem audit log**
- **Given** tôi là nhân viên pháp chế (không phải PM/Admin)
- **When** tôi cố truy cập trang audit log (qua URL trực tiếp hoặc API)
- **Then** hệ thống từ chối với lỗi phân quyền (403); nội dung audit log không lộ ra; trang UI không hiển thị link hoặc menu dẫn đến audit log với role này

---

#### US-12 — Cấu hình ngưỡng confidence *(Post-MVP)*

**Story:** Là Quản trị sản phẩm, tôi muốn điều chỉnh ngưỡng hiển thị nhãn độ tin cậy **Cao / Trung bình / Thấp**, để tôi có thể tinh chỉnh theo từng loại hợp đồng.

> **Post-MVP** — Cần dữ liệu thực tế để calibrate ngưỡng. Không hardcode trong MVP.

---

### 3.3 Role: Hệ thống AI (Internal / System)

---

#### US-13 [MVP] — Trích xuất text từ PDF có text layer

**Story:** Là AI Service, tôi muốn tự động trích xuất text từ PDF có text layer kèm metadata trang và vị trí ký tự, để pipeline downstream có thể link kết quả về đúng đoạn nguồn trong hợp đồng.

**Acceptance Criteria:**

**AC-13-1: Trích xuất đủ text và metadata**
- **Given** file PDF có text layer hợp lệ
- **When** AI service nhận PDF và bắt đầu xử lý
- **Then** service trả về text đã trích kèm `page_number` và `char_offset` cho mỗi đoạn; không persist text thô vào DB sau khi pipeline hoàn thành (D4)

**AC-13-2: Xử lý trong SLA**
- **Given** PDF ~20 trang, text-layer
- **When** pipeline chạy end-to-end
- **Then** hoàn thành trong < 30s (p95) (DoD-1)

**AC-13-3: PDF được bảo vệ bằng mật khẩu hoặc bị corrupt**
- **Given** file PDF yêu cầu mật khẩu để mở, hoặc file bị corrupt/truncated không parse được
- **When** AI service nhận file và cố trích xuất text
- **Then** service trả về lỗi có cấu trúc (ví dụ: `error: "pdf_unreadable"`) về SaaS backend; không crash pipeline; UI hiển thị thông báo rõ ràng "Không thể đọc file PDF — vui lòng kiểm tra lại file"; không lưu bất kỳ kết quả nháp nào

---

#### US-14 [MVP] — Xử lý PDF scan bằng OCR

**Story:** Là AI Service, tôi muốn tự động nhận diện PDF scan và áp dụng OCR để trích xuất text, để pipeline có thể xử lý hợp đồng scan mà không báo lỗi.

**Acceptance Criteria:**

**AC-14-1: Tự động detect và áp dụng OCR**
- **Given** file PDF không có text layer (PDF scan)
- **When** AI service nhận file
- **Then** service tự động phát hiện là scan và áp dụng OCR; không yêu cầu người dùng thao tác thêm

**AC-14-2: OCR best-effort — không có SLA với file kém chất lượng**
- **Given** PDF scan bị mờ, hỏng nặng, hoặc thiếu trang
- **When** OCR hoàn thành
- **Then** service vẫn trả về kết quả tốt nhất có thể; các trường không trích được đánh dấu `not_found` / `uncertain`; không crash pipeline

---

#### US-15 [MVP] — Trích xuất 6 trường với grounding

**Story:** Là AI Service, tôi muốn gọi LLM để trích xuất 6 trường quan trọng từ text hợp đồng, mỗi trường kèm metadata nguồn (trang + đoạn gốc), để kết quả luôn truy được về đoạn gốc và không có trường nào được bịa.

**Acceptance Criteria:**

**AC-15-1a: Trường trích xuất ①→⑤ — không có đường thứ ba** *(D6-a)*
- **Given** LLM đã xử lý text hợp đồng
- **When** service chuẩn bị response
- **Then** mỗi trường ①→⑤ phải có (a) giá trị + `page_number` + `source_excerpt` khớp **verbatim** với text nguồn, **HOẶC** (b) nhãn `uncertain` / `not_found`. Với trường đa giá trị ① và đa đoạn ⑤: **mỗi giá trị / mỗi đoạn có span riêng** (§3.0). Không trường nào thiếu cả hai. (DoD-2)

**AC-15-1b: Trường tổng hợp ⑥ — neo theo câu** *(D6-b)*
- **Given** LLM đã sinh bản tóm tắt
- **When** service kiểm tra grounding của tóm tắt
- **Then** mỗi câu chứa **dữ kiện** (tên bên · ngày · số tiền · nghĩa vụ · chế tài · thời hạn) phải có ≥1 con trỏ nguồn khớp verbatim; câu không neo được **bị cắt khỏi tóm tắt**, không viết mềm đi; nếu sau khi cắt phần còn lại không đủ nghĩa → trả trạng thái `insufficient_grounding` cho trường ⑥, **không trả tóm tắt trôi nổi**. (DoD-2, D6-b)

> ⚠️ **Chi phí đã biết:** lượt đối chiếu câu-về-nguồn ăn vào ngân sách 30s của DoD-1 / NFR-P1. Phải đo ở **lát cắt dọc đầu tiên** (bước [8]). Nếu vượt, đòn bẩy đã chốt là **rút tóm tắt từ ~200 xuống ~120 từ** — không nới D6-b.

**AC-15-2: Egress guard — không gửi text hợp đồng ra ngoài whitelist**
- **Given** pipeline đang chuẩn bị gọi LLM
- **When** egress guard kiểm tra request
- **Then** nếu endpoint đích không nằm trong whitelist đã được Legal/Security phê duyệt, request bị chặn và ghi log lỗi (DoD-4, D5)

**AC-15-3: Provider-agnostic — đổi model không đổi business logic**
- **Given** cần chuyển từ LLM provider A sang provider B
- **When** thay đổi config provider
- **Then** logic trích xuất, grounding, và format output không cần thay đổi

**AC-15-4: LLM timeout hoặc trả về kết quả không hợp lệ**
- **Given** LLM call vượt quá thời gian chờ tối đa, hoặc LLM trả về JSON không parse được / thiếu trường bắt buộc
- **When** pipeline nhận response từ LLM
- **Then** pipeline không crash; ghi log lỗi kèm `request_id`, `timestamp`, và loại lỗi; trả về lỗi có cấu trúc về SaaS backend để UI hiển thị thông báo "Phân tích thất bại — vui lòng thử lại"; không ghi bất kỳ bản `draft_ai` nào với dữ liệu không đầy đủ

---

#### US-16 [MVP] — Xử lý hợp đồng tiếng Việt và tiếng Anh

**Story:** Là AI Service, tôi muốn xử lý chính xác hợp đồng bằng tiếng Việt và tiếng Anh (bao gồm hợp đồng hỗn hợp hai ngôn ngữ), để pipeline không bị giới hạn bởi ngôn ngữ đầu vào trong phạm vi MVP.

**Acceptance Criteria:**

**AC-16-1: Trích xuất đúng với hợp đồng tiếng Việt**
- **Given** file PDF là hợp đồng viết bằng tiếng Việt
- **When** pipeline xử lý và trích xuất 6 trường
- **Then** kết quả trả về đúng giá trị các trường bằng tiếng Việt, source excerpt trích nguyên văn tiếng Việt từ hợp đồng

**AC-16-2: Trích xuất đúng với hợp đồng tiếng Anh**
- **Given** file PDF là hợp đồng viết bằng tiếng Anh
- **When** pipeline xử lý và trích xuất 6 trường
- **Then** kết quả trả về đúng giá trị các trường bằng tiếng Anh, source excerpt trích nguyên văn tiếng Anh từ hợp đồng

**AC-16-3: Không crash với hợp đồng hỗn hợp VI/EN**
- **Given** file PDF chứa nội dung hỗn hợp tiếng Việt và tiếng Anh (ví dụ: hợp đồng song ngữ)
- **When** pipeline xử lý
- **Then** hệ thống xử lý không bị lỗi; các trường tìm được trả về kết quả, trường không tìm được đánh nhãn `not_found` / `uncertain`

**AC-16-4: Ngôn ngữ ngoài VI/EN không làm crash pipeline**
- **Given** file PDF viết bằng ngôn ngữ không được hỗ trợ (ví dụ: tiếng Nhật, tiếng Trung, tiếng Pháp)
- **When** pipeline xử lý
- **Then** pipeline không crash (không trả HTTP 500); toàn bộ 6 trường được đánh nhãn `not_found` hoặc `uncertain`; UI hiển thị cảnh báo "Hợp đồng có thể không thuộc phạm vi ngôn ngữ được hỗ trợ (VI/EN) — kết quả có thể không chính xác" để người dùng biết và tự xử lý

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Hiệu năng

| ID | Yêu cầu | Ngưỡng | Điều kiện |
|---|---|---|---|
| **NFR-P1** | Thời gian phân tích end-to-end | < 30s (p95) | PDF text-layer ~20 trang |
| **NFR-P2** | Thời gian phân tích PDF scan | < 60s (p95) *(team target — không phải DoD gate; SCOPE không cam kết SLA cho OCR scan)* | PDF scan — hiển thị progress + cảnh báo chờ lâu hơn |
| **NFR-P3** | UI phản hồi sau khi bấm "Phân tích bằng AI" | < 2s | Bắt đầu hiện progress indicator |
| **NFR-P4** | Không block UI trong quá trình xử lý | N/A | Processing chạy async; user vẫn có thể điều hướng |

### 4.2 Bảo mật & Dữ liệu

| ID | Yêu cầu | Mức độ |
|---|---|---|
| **NFR-S1** | Không gửi nội dung hợp đồng ra ngoài whitelist endpoint | Bắt buộc — kiểm bằng egress test (DoD-4) |
| **NFR-S2** | External LLM API chỉ được bật sau khi có DPA + phê duyệt Legal/Security | Bắt buộc — cờ config bị khóa mặc định (D5, OI-02) |
| **NFR-S3** | Text thô hợp đồng không được persist vào DB sau khi pipeline hoàn thành | Bắt buộc — kiểm bằng DB schema audit (D4) |
| **NFR-S4** | API key và secret không được hardcode trong source code | Bắt buộc — dùng secret manager |
| **NFR-S5** | Audit log là append-only, không thể xóa | Bắt buộc |
| **NFR-S6** | Audit log không chứa nội dung văn bản hợp đồng | Bắt buộc |
| **NFR-S7** | Truyền thông giữa SaaS backend và AI service qua internal network (không public internet) | Bắt buộc (A5) |

### 4.3 Phân quyền

| ID | Yêu cầu | Ghi chú |
|---|---|---|
| **NFR-A1** | Chỉ user đã xác thực qua auth hiện tại của SaaS mới truy cập được tính năng AI | Reuse JWT/session của SaaS (D1) |
| **NFR-A2** | User chỉ phân tích được hợp đồng mà họ có quyền đọc trong SaaS | Kế thừa phân quyền hợp đồng hiện tại của SaaS |
| **NFR-A3** | Bản `draft_ai` không lộ ra ngoài qua API hoặc export | Chỉ bản `approved` được đọc bởi downstream (D3) |
| **NFR-A4** | Khả năng mở rộng phân quyền cho external parties | Chờ OI-01 — không build trong MVP |

### 4.4 Khả dụng & Độ tin cậy

| ID | Yêu cầu | Ngưỡng |
|---|---|---|
| **NFR-AV1** | AI service lỗi không làm sập SaaS hiện tại | AI service là microservice riêng — lỗi chỉ ảnh hưởng tính năng AI |
| **NFR-AV2** | Khi AI service không phản hồi | UI hiển thị thông báo lỗi rõ ràng, cho phép thử lại |
| **NFR-AV3** | Không mất dữ liệu bản approved đã lưu | Lưu trên PostgreSQL hiện tại với backup sẵn có của SaaS |
| **NFR-AV4** | Grounding 100% — không xuất trường thiếu nguồn | Fail-closed ở pipeline level (**D6-a** cho trường ①→⑤, **D6-b** cho trường ⑥ tính theo **câu dữ kiện**); DoD-2 |

### 4.5 Ngôn ngữ

| ID | Yêu cầu | Ngưỡng |
|---|---|---|
| **NFR-L1** | Pipeline hỗ trợ tiếng Việt và tiếng Anh là ngôn ngữ đầu vào | Bắt buộc — kiểm tra bằng test set gồm cả hai ngôn ngữ |
| **NFR-L2** | Độ chính xác trích xuất không được suy giảm đáng kể giữa VI và EN | QA kiểm tra trên mẫu hợp đồng song ngữ trước khi ship |
| **NFR-L3** | Ngôn ngữ ngoài VI/EN không được làm crash pipeline | Nếu detect ngôn ngữ khác → pipeline xử lý best-effort, không trả lỗi 500 |

---

## 5. Use Cases theo Role

### 5.0 Ma trận Role × Use Case

Bảng này xác định rõ role nào **được phép** và **không được phép** thực hiện từng use case. Cột "❌" không phải "không liên quan" — là **ràng buộc phân quyền phải enforce**.

| Use Case | Nhân viên pháp chế/Kinh doanh | Quản trị sản phẩm (PM) | Hệ thống AI (Internal) |
|---|:---:|:---:|:---:|
| **UC-01:** Phân tích HĐ từ danh sách | ✅ Thực hiện | ❌ Không có UI access | ❌ |
| **UC-02:** Upload và phân tích HĐ mới | ✅ Thực hiện | ❌ Không có UI access | ❌ |
| **UC-03:** Review, sửa và duyệt kết quả | ✅ Thực hiện (nếu có quyền write) | ❌ Xem được, không sửa/duyệt | ❌ |
| **UC-04:** Chạy lại AI | ✅ Thực hiện (nếu có quyền write; không trùng job) | ❌ | ❌ |
| **UC-05:** Kiểm tra audit trail | ❌ Bị chặn (403) | ✅ Thực hiện | ❌ |
| **UC-06:** Xử lý PDF nội bộ & gọi LLM | ❌ | ❌ | ✅ Tự động (không có UI) |

> **Ghi chú phân quyền:** "Quyền write" kế thừa từ phân quyền hợp đồng sẵn có của SaaS (NFR-A2). User chỉ có read-only trên hợp đồng → thấy kết quả AI nhưng không sửa, không duyệt được (AC-07-4, AC-08-4).

---

### UC-01: Phân tích hợp đồng mới (chọn từ danh sách)

**Role:** Nhân viên pháp chế · **Story liên quan:** US-01 [MVP], US-03 [MVP], US-04 [MVP], US-05 [MVP], US-06 [MVP]

1. User mở hồ sơ hợp đồng có PDF đính kèm.
2. User bấm "Phân tích bằng AI".
3. Hệ thống xử lý (progress indicator), trả về kết quả trong < 30s.
4. User xem tóm tắt và bảng 6 trường kèm nguồn trích dẫn.

**Luồng thay thế:**
- PDF không có text layer → OCR tự động, kết quả trả về trong < 60s kèm cảnh báo.
- Pipeline lỗi → hiển thị thông báo lỗi, cho phép thử lại.

---

### UC-02: Upload và phân tích hợp đồng mới

**Role:** Nhân viên pháp chế · **Story liên quan:** US-02 [MVP], US-03 [MVP], US-04 [MVP], US-05 [MVP], US-06 [MVP]

1. User upload PDF mới qua chức năng upload của SaaS.
2. Hồ sơ hợp đồng mới được tạo, PDF đính kèm.
3. User bấm "Phân tích bằng AI" → tiếp tục như UC-01 từ bước 3.

**Luồng thay thế:**
- File không phải PDF → báo lỗi định dạng, không tạo hồ sơ.

---

### UC-03: Review, chỉnh sửa và duyệt kết quả AI

**Role:** Nhân viên pháp chế · **Story liên quan:** US-07 [MVP], US-08 [MVP]

1. User xem bảng kết quả `draft_ai`.
2. User đối chiếu từng trường với source excerpt.
3. User chỉnh sửa các trường cần sửa (UI đánh dấu trường đã sửa).
4. User bấm "Xác nhận & Lưu".
5. Kết quả chuyển sang `approved`, lưu vào hồ sơ.
6. Audit log ghi nhận: user, timestamp, các trường đã sửa (before/after).

**Luồng thay thế:**
- User rời trang chưa lưu → cảnh báo mất thay đổi.
- User không sửa gì và bấm lưu → toàn bộ giá trị AI được approved nguyên vẹn.
- User chỉ có quyền đọc cố click vào trường để sửa → trường không vào edit mode; UI hiển thị icon khóa; nút "Xác nhận & Lưu" không hiển thị (AC-07-4).

---

### UC-04: Chạy lại AI trên hợp đồng đã có kết quả

**Role:** Nhân viên pháp chế · **Story liên quan:** US-09 [MVP]

1. User mở hồ sơ hợp đồng đã có bản `approved`.
2. User bấm "Phân tích lại bằng AI".
3. Hệ thống tạo version `draft_ai` mới, bản `approved` cũ giữ nguyên.
4. UI hiển thị version mới ở trạng thái draft, cho phép so sánh với bản cũ.

---

### UC-05: Kiểm tra audit trail

**Role:** Quản trị sản phẩm · **Story liên quan:** US-11 [MVP]

1. PM truy vấn audit log theo `contract_id` hoặc `user_id`.
2. Hệ thống trả về danh sách hành động: loại action, user, timestamp, thay đổi.
3. PM có thể xác nhận quy trình review đã được thực hiện đúng.

---

### UC-06: Xử lý nội bộ PDF và gọi LLM (System)

**Role:** AI Service (Internal) · **Story liên quan:** US-13 [MVP], US-14 [MVP], US-15 [MVP]

1. Nhận PDF từ SaaS backend qua internal REST.
2. Detect PDF type (text-layer hoặc scan).
3. Trích text (pdfplumber) hoặc OCR (Tesseract) kèm page/offset metadata.
4. Chunk text và tạo embedding để grounding.
5. Gọi LLM qua provider-agnostic layer (egress guard kiểm tra endpoint).
6. LLM trả về 6 trường; service link từng trường về source chunk.
7. Validate: mọi trường phải có source hoặc nhãn — không có đường thứ ba.
8. Trả `draft_ai` response về SaaS backend.
9. Xóa text thô khỏi memory sau khi hoàn thành.

---

## 6. Mapping Story → DoD

| Story | Nội dung | DoD liên quan | MVP? |
|---|---|---|:---:|
| **US-01** | Chọn hợp đồng đã có trong SaaS | — (precondition) | ✅ |
| **US-02** | Upload hợp đồng PDF mới | DoD-4 (data không rời vùng cho phép) | ✅ |
| **US-03** | Kích hoạt phân tích AI | DoD-1 (< 30s end-to-end) | ✅ |
| **US-04** | Xem tóm tắt hợp đồng | DoD-7 **(a)** đủ hiểu chủ thể + **(b)** mọi câu dữ kiện neo được (AC-04-4); `insufficient_grounding` (AC-04-5) | ✅ |
| **US-05** | Xem bảng 6 trường trích xuất | DoD-2 (100% trường có nguồn hoặc nhãn) + cardinality §3.0 (AC-05-4) | ✅ |
| **US-06** | Xem nguồn trích dẫn cho mỗi trường | DoD-2, DoD-6 (grounding + UX uncertain) | ✅ |
| **US-07** | Chỉnh sửa giá trị trường trước khi lưu | DoD-3 (human gate), DoD-5 (audit log) | ✅ |
| **US-08** | Xác nhận và lưu kết quả đã duyệt | DoD-3 (0 auto-approved), DoD-5 (audit log) | ✅ |
| **US-09** | Chạy lại AI không ghi đè bản approved | DoD-3, DoD-5 | ✅ |
| **US-10** | Xem lịch sử các phiên phân tích | — | ❌ Post-MVP |
| **US-11** | Xem nhật ký kiểm toán | DoD-5 (100% hành động có log) | ✅ |
| **US-12** | Cấu hình ngưỡng confidence | — | ❌ Post-MVP |
| **US-13** | Trích xuất text từ PDF text-layer | DoD-1 (< 30s), DoD-4 (không persist text thô) | ✅ |
| **US-14** | Xử lý PDF scan bằng OCR | DoD-1 (best-effort), DoD-2 (fallback nhãn not_found) | ✅ |
| **US-15** | Trích 6 trường với grounding + egress guard | DoD-2 (**D6-a** AC-15-1a + **D6-b** AC-15-1b), DoD-4 (egress guard) | ✅ |
| **US-16** | Xử lý ngôn ngữ VI/EN | DoD-2 (grounding trên cả hai ngôn ngữ) | ✅ |

---

## 7. Out-of-Scope Confirmation

Các mục dưới đây **không thuộc SPEC này**. Ghi rõ để dev không vô tình implement thêm. Nguồn: `SCOPE-PB06` §5.

| Tính năng | Lý do không build trong MVP |
|---|---|
| Admin tự thêm/bỏ trường trích xuất | Schema động làm phức tạp prompt + validation (D2) |
| Gửi hợp đồng ra LLM API bên ngoài khi chưa có DPA | Chờ Legal/Security — egress guard đóng mặc định (D5, OI-02) |
| Tự động approve khi confidence cao | Human gate bắt buộc — không có ngoại lệ (D3, DoD-3) |
| Tự động nhắc gia hạn / workflow downstream | Cần approved data đủ chính xác trước |
| Tự động ký hợp đồng | Hành động pháp lý — cần trust vào data trước |
| Phân tích pháp lý / đánh giá rủi ro điều khoản | Sản phẩm khác, đòi hỏi liability framework riêng |
| Đa ngôn ngữ ngoài VI/EN | Chưa có baseline để đánh giá accuracy (NFR-L3 chỉ yêu cầu không crash) |
| Full-text search nội dung hợp đồng từ kết quả AI | Text thô không persist (D4) |
| SLA xử lý PDF scan bị mờ, hỏng nặng, hoặc thiếu trang | OCR là capability bắt buộc; chất lượng với file cực kém là giới hạn kỹ thuật, không phải DoD |
| Xem lịch sử phiên phân tích (US-10) | Post-MVP |
| Cấu hình ngưỡng confidence (US-12) | Post-MVP |

---

*SPEC-PB06 v1.1 · Nguồn scope: `SCOPE-PB06.md` v3.2 · Sign-off: BA + Tech Lead. Bất kỳ thay đổi nào chạm A1–A7 hoặc D1–D7 đều phải mở lại review scope trước khi triển khai.*
