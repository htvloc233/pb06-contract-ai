# SCOPE-PB06 — AI Tóm Tắt & Trích Xuất Hợp Đồng (MVP)

> **Phiên bản:** 3.2 · **Ngày:** 2026-09-06 · **Trạng thái:** ✅ **Locked — đã sign-off D6 + A6** (PM + Tech Lead, 2026-09-06 · ghi nhận theo xác nhận của PM trong phiên)
> **Nguyên tắc chủ đạo:** Con người chốt (human-in-the-loop) · Mọi trường truy được về đoạn gốc (grounding) · Mặc định không gửi hợp đồng ra ngoài (fail-closed).
>
> Artefact bước **[0] Làm rõ scope** · Capstone Playbook · đề `PB-06`

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **3.2** | 2026-09-06 | **Ghi thành văn nguyên tắc nhãn-vs-trạng thái.** Mở rộng **A6**: nhãn độ tin cậy là *thuộc tính hiển thị*, không phải cổng — **không quyết định trạng thái trường**, chỉ hiển thị trên trường `grounded`. Trước v3.2 nguyên tắc này chỉ được **hàm ý** qua D6 (cổng là grounding cơ học) + A6 (confidence là heuristic), chưa được viết ⇒ `SPEC-PB06` US-12 đã diễn giải ngược (ngưỡng confidence quyết định `uncertain`). **Chạm A6 ⇒ cần sign-off.** Không đổi scope, không đổi D1–D7, không thêm trường. |
| **3.1** | 2026-09-06 | Vá lỗ hổng grounding của trường tổng hợp. **Chạm D6 ⇒ cần sign-off theo quy định cuối tài liệu.** ① §4: bảng 6 trường thêm cột `Loại` + `Nguồn bắt buộc`, chốt cardinality (đơn trị / đa giá trị / đa đoạn / tổng hợp); ô trạng thái của trường ⑥ trả về đúng loại dữ liệu (`insufficient_grounding`, trước đây bị dán nhầm tiêu chí chất lượng từ DoD-7). ② **D6 tách thành D6-a (trường trích xuất) và D6-b (trường tổng hợp)** — tóm tắt neo nguồn theo *câu chứa dữ kiện*, không được miễn trừ. ③ DoD-2 + DoD-7 bổ sung vế kiểm neo nguồn cho tóm tắt. ④ §5 ghi thành văn hướng bị loại "tóm tắt tự do không neo nguồn". |
| **3.0** | 2026-07-29 | Bản chốt cho SRS: Problem Statement · A1–A7 · D1–D7 · In-Scope · Out-of-Scope · DoD 7 tiêu chí · OI-01/OI-02. |

---

## 1. Problem Statement

Người dùng hệ thống SaaS quản lý hợp đồng hiện phải đọc thủ công từng hợp đồng PDF để tìm các thông tin cốt lõi — các bên, giá trị, ngày hiệu lực, ngày hết hạn, điều khoản phạt. Quá trình này tốn thời gian, dễ bỏ sót, và không scale được khi khối lượng hợp đồng tăng. MVP đặt cược vào một giả thuyết có thể chứng minh hoặc bác bỏ: *nếu* AI trích đúng 6 trường đó kèm trích dẫn nguồn (trang + đoạn gốc) và người dùng chỉ cần đối chiếu–duyệt thay vì đọc từ đầu, *thì* tốc độ xử lý hợp đồng tăng lên đáng kể mà không đánh đổi độ tin cậy. Về mặt kinh doanh, tính năng này biến sản phẩm từ kho lưu trữ hợp đồng thụ động thành trợ lý đọc hợp đồng chủ động — tạo lợi thế cạnh tranh rõ rệt so với các SaaS quản lý hợp đồng chỉ có search cơ bản, và mở cơ hội upsell cho phân khúc khách hàng có khối lượng hợp đồng lớn. Rủi ro lớn nhất — và là điều định hình toàn bộ thiết kế — là AI "bịa" dữ liệu nhạy cảm mà người dùng không phát hiện, hoặc nội dung hợp đồng bị đẩy ra ngoài vùng cho phép. Vì vậy mọi output AI đều là bản nháp phải có người duyệt, mọi trường phải truy ngược được về đoạn gốc, và pipeline mặc định đóng cổng gửi hợp đồng ra bất kỳ API bên ngoài nào.

**Go/no-go metrics:** AI phân tích 1 hợp đồng < 30s (DoD-1) — ước tính giảm 50–70% thời gian xử lý so với đọc thủ công · trích đúng 6 trường ở mức người duyệt chấp nhận được · 0 sự cố rò rỉ dữ liệu · 0 bản ghi `approved` không qua người duyệt.

---

## 2. Assumptions Locked

Các giả định đã được chốt. **Nếu bất kỳ giả định nào sai → mở lại scope.**

| # | Giả định | → Mở lại scope nếu sai |
|---|---|---|
| **A1** | Người dùng MVP là nhân viên pháp chế/kinh doanh nội bộ — người trực tiếp dùng tính năng AI. Quản trị sản phẩm là người duyệt nghiệm thu. | Nếu external parties (đối tác, khách hàng ký kết) cũng cần truy cập → mở lại scope: phải xác định auth model, phân quyền theo hợp đồng, threat model mới — xem OI-01 |
| **A2** | PDF đầu vào đến từ hai path: (1) chọn từ danh sách hợp đồng đã có trong SaaS, hoặc (2) upload PDF mới bằng chức năng upload sẵn có của SaaS — không cần build upload flow mới | Nếu SaaS chưa có chức năng upload PDF → phải build upload flow riêng trước khi ship |
| **A3** | Đại đa số hợp đồng đầu vào là PDF có text layer (không phải scan ảnh) | Phải re-estimate effort OCR; nếu volume scan lớn → OCR accuracy trở thành tiêu chí nghiệm thu riêng |
| **A4** | 6 trường cố định (xem D2) đủ để chứng minh giá trị MVP | Phải mở rộng schema trường trước khi ra mắt |
| **A5** | SaaS hiện tại có internal network zone đủ để chạy AI service riêng | Phải thiết kế lại hạ tầng |
| **A6** | "Độ tin cậy" hiển thị là chỉ báo heuristic hỗ trợ người duyệt, **KHÔNG** phải xác suất đúng đã hiệu chỉnh → UX không hứa tuyệt đối. **Hệ quả bắt buộc (v3.2):** nhãn độ tin cậy là **thuộc tính hiển thị, không phải cổng** — nó **không bao giờ quyết định trạng thái trường**. Trạng thái (`grounded` · `uncertain` · `not_found` · `insufficient_grounding`) chỉ do **kiểm tra grounding cơ học** quyết định (D6-a / D6-b), không do model tự khai. Nhãn độ tin cậy **chỉ hiển thị trên trường `grounded`**; trường ở ba trạng thái còn lại hiển thị **nhãn trạng thái**, không hiển thị nhãn độ tin cậy. | Nếu bị hiểu là "đảm bảo đúng", người dùng bỏ bước đối chiếu → phải sửa truyền thông/UX. **Nếu có yêu cầu để ngưỡng confidence tự gán trạng thái** (vd auto-`uncertain` khi điểm thấp) → **mở lại scope**: đó là lấy số heuristic làm cổng gác, trái D6 + A6 |
| **A7** | Team 4 người được phân bổ đủ năng lực và thời gian trong toàn bộ 8 tuần MVP — không bị rút người giữa chừng cho dự án khác | Phải re-estimate timeline và thu hẹp scope nếu capacity thay đổi |

---

## 3. Foundational Decisions

Mỗi quyết định là một ngã rẽ — đã chọn một hướng và **bỏ hướng kia có chủ đích**.

**D1 — Tích hợp vào SaaS hiện tại, không build standalone.**
*Bỏ hướng:* app AI riêng biệt. *Lý do:* user đã có hợp đồng trong SaaS; standalone tạo thêm bước export/import và làm khó audit trail. *Hệ quả:* AI feature dùng chung auth, DB, frontend hiện tại.

**D2 — 6 trường cố định cho MVP, không có admin field editor.**
*Bỏ hướng:* schema động, admin tự cấu hình trường. *Lý do:* schema động cần thêm 3–4 tuần build và làm phức tạp prompt engineering. Chứng minh accuracy trên 6 trường quan trọng nhất đủ để go/no-go. *Trường chốt:* ① Các bên · ② Ngày hiệu lực · ③ Ngày hết hạn · ④ Giá trị hợp đồng · ⑤ Điều khoản phạt · ⑥ Tóm tắt (~200 từ).

**D3 — AI output luôn là `draft_ai`; phải bấm "Xác nhận & Lưu" mới thành `approved`.**
*Bỏ hướng:* auto-approve khi confidence cao. *Lý do:* hợp đồng là dữ liệu pháp lý — một lần AI sai không ai kiểm tra là đủ mất trust, và trust mất rồi rất khó lấy lại. *Hệ quả:* mọi downstream (API, báo cáo, export) chỉ đọc bản approved. Mỗi lần chạy/duyệt/sửa đều ghi audit log.

**D4 — Không lưu text thô hợp đồng sau khi xử lý xong.**
*Bỏ hướng:* lưu lại text đã trích để dùng sau (search, re-analyze). *Lý do:* thu hẹp phạm vi compliance và đơn giản hóa incident response — văn bản hợp đồng là dữ liệu nhạy cảm, không lưu thêm bản sao nào ngoài file PDF gốc. *Hệ quả:* chỉ lưu kết quả đã duyệt + metadata chunk (trang, offset) để trace nguồn + audit log. Không thể full-text search nội dung hợp đồng từ kết quả AI — muốn có phải mở lại D4.

**D5 — Đóng cổng external LLM; chờ quyết định được phép dùng external hay không.**
*Bỏ hướng:* giả định external OK và build theo provider cụ thể ngay. *Lý do:* chưa có thông tin về DPA, chính sách bảo mật, và phê duyệt pháp lý — đây là quyết định của Legal/Security, không phải team build tự chốt. *Hệ quả:* pipeline được thiết kế provider-agnostic (đổi provider không đổi business logic); cổng gọi ra ngoài bị khóa bằng egress guard cho đến khi có quyết định chính thức. Khi Legal/Security chốt (external được phép hoặc phải self-host), team chỉ mở/cấu hình đúng một điểm — không cần refactor.

**D6 — Fail-closed grounding: không có nguồn thì không xuất.**
*Bỏ hướng:* cho AI "đoán" giá trị khi không tìm thấy đoạn gốc; và cho tóm tắt được miễn trừ khỏi ràng buộc nguồn vì "tóm tắt vốn là văn bản tổng hợp". *Lý do:* "kết quả AI luôn truy được về đoạn gốc" là cổng fail-closed không thể bỏ. Miễn trừ tóm tắt sẽ mở đúng lỗ hổng nguy hiểm nhất — một câu sai về nghĩa vụ hoặc điều khoản phạt khó bị phát hiện hơn một ô ngày tháng sai. *Hệ quả:* ràng buộc áp **theo loại trường** (xem cột "Loại" ở §4), tách thành D6-a và D6-b.

**D6-a — Trường trích xuất (① → ⑤).** Mỗi giá trị bắt buộc kèm (a) trích dẫn nguồn (trang + đoạn) khớp nguyên văn với văn bản, hoặc (b) nhãn `not_found` / `uncertain`. **Không có đường thứ ba** — trường không nguồn, không nhãn thì không được ghi ra.

**D6-b — Trường tổng hợp (⑥ Tóm tắt).** Tóm tắt không có span đơn, nên ràng buộc chuyển từ *trường* xuống *câu*:

- Mỗi câu chứa **dữ kiện** (tên bên · ngày · số tiền · nghĩa vụ · chế tài · thời hạn) phải kèm ≥1 con trỏ nguồn (trang + đoạn).
- Câu không neo được **không được đưa vào tóm tắt** — cắt bỏ, không viết mềm đi.
- Nếu sau khi cắt, phần neo được không đủ để tóm tắt có nghĩa → trả trạng thái `insufficient_grounding` cho cả trường ⑥ và hiển thị nhãn cho người duyệt, thay vì trả một bản tóm tắt trôi nổi.

Trường gắn nhãn `uncertain`, `not_found` hoặc `insufficient_grounding` được làm nổi bật để người duyệt xử lý trước.

> ⚠️ *Chi phí đã biết:* neo theo câu cần thêm một lượt đối chiếu sau khi sinh tóm tắt, ăn vào ngân sách 30s của DoD-1. Phải đo ở lát cắt dọc đầu tiên. Nếu vượt, đòn bẩy là **rút tóm tắt từ ~200 xuống ~120 từ**, không phải nới D6-b.

**D7 — Mỗi lần chạy lại AI tạo version `draft_ai` mới; bản `approved` đã có không bị ghi đè.**
*Bỏ hướng:* ghi đè trực tiếp lên kết quả cũ khi chạy lại AI. *Lý do:* hợp đồng là tài liệu pháp lý — nếu ghi đè, mất khả năng audit (ai thay đổi gì, khi nào) và không thể rollback nếu kết quả AI mới sai hơn bản đã duyệt. Đây là yêu cầu của audit trail, không phải tính năng tiện ích. *Hệ quả:* DB phải lưu nhiều version per hợp đồng; downstream luôn đọc bản approved mới nhất; UX hiển thị rõ version đang xem.

---

## 4. In-Scope for MVP

Những gì MVP cam kết deliver — không thêm, không bớt.

**Luồng chính (core flow):**
Người dùng chọn hợp đồng PDF đã có trong SaaS hoặc upload hợp đồng mới bằng chức năng upload của SaaS (A2) → bấm "Phân tích bằng AI" → hệ thống trả về bản tóm tắt ngắn + bảng 6 trường → người dùng xem, đối chiếu nguồn, sửa nếu cần → bấm "Xác nhận & Lưu" → kết quả approved gắn vào hồ sơ hợp đồng.

**6 trường trích xuất (cố định):**

| # | Trường | Loại | Nguồn bắt buộc | Trạng thái nếu không đủ nguồn |
|---|---|---|---|---|
| ① | Các bên trong hợp đồng | Trích xuất — đa giá trị | ≥1 span cho mỗi bên | `not_found` |
| ② | Ngày hiệu lực | Trích xuất — đơn trị | 1 span | `uncertain` |
| ③ | Ngày hết hạn | Trích xuất — đơn trị | 1 span | `uncertain` |
| ④ | Giá trị hợp đồng (số + đơn vị tiền tệ) | Trích xuất — đơn trị | 1 span | `uncertain` |
| ⑤ | Điều khoản phạt | Trích xuất — đa đoạn | ≥1 span cho mỗi điều khoản | `not_found` |
| ⑥ | Tóm tắt ngắn (~200 từ) | **Tổng hợp** | ≥1 span cho **mỗi câu chứa dữ kiện** (xem D6-b) | `insufficient_grounding` |

> Cột **Loại** chốt cardinality ngay ở scope: ② ③ ④ là giá trị đơn, còn ① ⑤ là tập hợp. Data model ở bước [3] không được ép cả sáu về một khuôn `field: value + span`, nếu không ① và ⑤ sẽ mất dữ liệu.

**Grounding & confidence:** Mỗi trường kèm trích dẫn nguồn (trang + đoạn gốc) hoặc nhãn `uncertain` / `not_found`. Trường không có nguồn không được xuất ra (D6).

**Human review:** Người dùng chỉnh sửa trực tiếp từng trường; UI phân biệt rõ "giá trị AI đề xuất" vs "giá trị đã chỉnh sửa". Nút "Xác nhận & Lưu" không tự kích hoạt.

**Audit log:** Ghi nhận mọi hành động — ai chạy AI, ai sửa trường nào (before/after), ai duyệt, timestamp. Không lưu nội dung hợp đồng trong log.

**OCR cho PDF scan:** OCR là capability bắt buộc theo đề bài — hệ thống phải xử lý được PDF scan (không chỉ PDF text-layer). Tuy nhiên không có SLA về accuracy với file scan bị mờ, hỏng nặng, hoặc thiếu trang — đây là giới hạn kỹ thuật, không phải scope cut.

**Phạm vi ngôn ngữ:** Tiếng Việt và tiếng Anh.

---

## 5. Out-of-Scope (MVP)

| Bị loại | Lý do có thể bỏ ở MVP |
|---|---|
| Đảm bảo SLA xử lý PDF scan bị mờ, hỏng nặng, hoặc thiếu trang | OCR là capability bắt buộc (có trong In-Scope), nhưng không cam kết kết quả với file đầu vào cực kỳ kém chất lượng — đây là giới hạn kỹ thuật của OCR engine, không phải quyết định scope |
| Admin tự thêm/bỏ trường trích xuất | D2: schema động làm phức tạp prompt + validation, trì hoãn việc chứng minh accuracy trên 6 trường cốt lõi |
| Gửi hợp đồng ra API LLM bên ngoài khi chưa có DPA | D5: chạm luật cứng về dữ liệu nhạy cảm. Chỉ bật sau DPA + duyệt Legal |
| Tự động approve khi confidence cao | D3: đánh đổi trust lấy tốc độ. Chưa đo được "confidence thực" (A6) cho hợp đồng pháp lý ở giai đoạn này |
| Tự động nhắc gia hạn / workflow downstream | Cần dữ liệu approved đủ chính xác trước. Accuracy chưa cao → automation tạo noise thay vì giá trị |
| Tự động ký hợp đồng | Ký là hành động pháp lý không thể sai — cần trust vào approved data ổn định trước |
| Phân tích pháp lý / đánh giá rủi ro điều khoản | Sản phẩm khác — đòi hỏi legal domain knowledge, fine-tuning và khung trách nhiệm riêng |
| Đa ngôn ngữ ngoài VI/EN | Chưa có data đánh giá accuracy. Mở rộng ngôn ngữ sau khi có baseline VI/EN |
| Full-text search nội dung hợp đồng từ kết quả AI | D4: text thô không persist. Muốn có → phải mở lại D4 |
| Tóm tắt tự do không neo nguồn | D6-b: tóm tắt được miễn trừ khỏi grounding là lỗ hổng lớn nhất của tính năng — câu sai về nghĩa vụ khó phát hiện hơn ô dữ liệu sai |

---

## 6. Definition of Done (Gate nghiệm thu)

MVP chỉ được ship khi **tất cả 7 tiêu chí** đạt:

| # | Tiêu chí | Ngưỡng đạt |
|---|---|---|
| **DoD-1 · Hiệu năng** | Phân tích 1 hợp đồng ~20 trang | < 30s (p95) |
| **DoD-2 · Grounding** | Mỗi trường xuất ra có nguồn *hoặc* nhãn "không tìm thấy/không chắc". Với trường ⑥, "có nguồn" nghĩa là **mọi câu chứa dữ kiện đều có ≥1 con trỏ nguồn** (D6-b) | 100% — 0 trường thiếu cả hai; 0 câu dữ kiện không neo |
| **DoD-3 · Human gate** | Bản ghi approved tạo ra mà không qua "Xác nhận & Lưu" của người dùng | 0 trường hợp |
| **DoD-4 · Ranh giới dữ liệu** | Request mang nội dung hợp đồng rời khỏi vùng cho phép | 0 (kiểm bằng egress test) |
| **DoD-5 · Audit log** | Mỗi lần *chạy AI / duyệt / sửa* có log: ai, khi nào, thay đổi gì | 100% hành động có log |
| **DoD-6 · UX duyệt** | Trường "không chắc" được đánh dấu rõ + hiển thị đoạn trích để đối chiếu | Có, trên toàn bộ 6 trường |
| **DoD-7 · Tóm tắt** | **(a)** Tóm tắt đủ để người đọc hiểu được chủ thể, mục đích và các bên của hợp đồng mà không cần đọc nguyên văn; **(b)** mọi câu chứa dữ kiện đều neo được về đoạn gốc | **(a)** user review trên mẫu tối thiểu 5 hợp đồng thực tế; **(b)** 0 câu dữ kiện không neo trên cùng mẫu |

---

## 7. Open Items (Chặn scope nếu chưa có câu trả lời)

| ID | Câu hỏi | Owner | Hạn chốt |
|---|---|---|---|
| **OI-01** | Đối tác/khách hàng bên ngoài (bên ký kết hợp đồng) có cần truy cập tính năng AI này không? Nếu có → phải xác định auth model, phân quyền theo hợp đồng, và threat model trước khi WBS | Product Owner / Stakeholder | Trước Sprint 0 |
| **OI-02** | Có được phép gửi nội dung hợp đồng ra LLM API bên ngoài không? Nếu có → DPA với provider nào, điều kiện gì? Nếu không → chốt self-host model nào? | Legal / Security Lead | Trước Sprint 0 |

---

*Bất kỳ thay đổi nào chạm A1–A7 hoặc D1–D7 đều phải mở lại review scope trước khi triển khai. Sign-off: PM + Tech Lead.*
