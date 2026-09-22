# DEVBOOK-PB06 — Nhật ký quyết định

> **Đề:** `PB-06` — AI Tóm Tắt & Trích Xuất Hợp Đồng
> **Giai đoạn:** bước [0] Làm rõ scope → [1] SW Spec (SRS) · *chưa vào [8] BUILD*
> **Artefact liên quan:** `SCOPE-PB06.md` v3.2 · `SPEC-PB06.md` v1.1 · `MODULEMAP-PB06.md` v1.2 · `ARCH-PB06.md` v1.4 · `WBS-PB06.md` v1.1 · `EST-PB06.md` v1.1 · `RISK-PB06.md` v1.1 · `DELEGATION-MAP-PB06.md` v1.1 · `DOR-PB06.md` v1.0 · `CLAUDE.md`

**Dev Book này ghi gì:** mỗi lần AI làm sai / thiếu / suy diễn quá tay → PM sửa gì, vì sao, gán mức L nào, cổng nào chặn, có hard-stop không. Đây là bằng chứng PM **hiểu** artefact mình nộp, không phải đóng dấu bừa output AI. Chấm nặng hơn cả bản kế hoạch.

> ⚠️ **Các ô `[PM tự điền]` phải do PM điền, không để AI viết hộ.** Telemetry giờ-thật và số lần override là số của người, AI không biết và không được suy đoán — chính là nguyên tắc *"không bịa"* mà đề PB-06 đang dạy.

---

## Bảng tra nhanh

| ID | Chỗ sai | Ai phát hiện | Mức L | Cổng chặn | Hard-stop |
|---|---|:---:|:---:|:---:|:---:|
| DB-01 | Hai thang L0–L5 mâu thuẫn trong giáo trình | AI | L2 | — | — |
| DB-02 | SCOPE §4: ô trạng thái trường ⑥ dán nhầm tiêu chí DoD-7 | AI | L2 | Cổng hiểu [0] | — |
| DB-03 | SCOPE D6 không phủ trường tổng hợp | AI | **L2** | Cổng hiểu [0] | ✅ |
| DB-04 | DoD-2 / DoD-7 không bắt được vi phạm D6-b | AI | L2 | Cổng hiểu [0] | — |
| DB-05 | Bản copy SPEC hỏng — 13 chỗ mất chữ | AI | **L1** | Fail-closed | ✅✅✅ |
| DB-06 | Phục hồi token trạng thái theo bằng chứng nội tại | AI | L2 | Đối chiếu sau | — |
| DB-07 | UC-06 bước 8: `dratf_ai` — lỗi gõ của PM | AI | L3 | — | — |
| DB-08 | SPEC v1.0 tụt sau SCOPE v3.1 — 4 điểm lệch | AI | L2 | Cổng hiểu [1] | — |
| DB-09 | Mơ hồ nhãn-vs-trạng thái phát sinh sau khi ghép | AI | **L2** | Cổng hiểu [1] | ✅ |
| DB-10 | Nguyên tắc A6 mới chỉ được hàm ý, chưa thành văn | AI | L2 | Quy định sign-off | — |
| DB-11 | Module Map tụt phiên bản + 4 điểm chặn cổng [2] | AI | L2 | Cổng hiểu [2] | — |
| DB-12 | ARCH v1.3 (reference) lệch nền — schema không chứa được D6-b | AI | L2 | Cổng hiểu [3] | — |
| DB-13 | WBS: cổng [4] hai chiều — PM bắt 2 lỗi AI · AI giữ cổng W1-13 | PM + AI | L2 | Cổng hiểu [4] | — |
| DB-14 | EST tham khảo tới dạng fragment 3 lần rỗng/1 lần đuôi — từ chối review mù; EST v1.0 độc lập | AI | L2 | Fail-closed | ✅ |
| DB-15 | Cổng [5] qua sạch — PM bác trúng W1-03 (giả định xích N6 chưa định giá) → EST v1.1 | PM | L2 | Cổng hiểu [5] | — |
| DB-16 | Cổng [6] qua sạch — PM bắt dòng #8 thiếu kênh bằng chứng ("passed ảo") → DELEG v1.1 + RISK A7 | PM | L2 | Cổng hiểu [6] | — |
| DB-17 | Cổng [7] qua sạch lần 3 liên tiếp — kèm chỉnh khái niệm "tối đa bao nhiêu tầng" | PM + AI | L2 | Cổng hiểu [7] | — |
| DB-18 | D7 repo/CI lật PASS bằng hành vi — PM tự dựng, vượt 4 lỗi thật; AI chặn "tưởng xong" | PM + AI | L3 | Fail-closed + xác minh độc lập | — |
| DB-19 | D11 lật PASS — DECISION-D11 (5 role + Q1–Q3) duyệt nguyên trạng; lớp 🔴 = 0 | PM | L2 | Luật tiền-đề DOR | — |
| DB-20 | N6 đạt — câu stack xuất sắc vòng 1; câu độ nhạy 2 vòng, PM bắt nhãn hai mặt `error_detail_ref` → ARCH v1.5 + LOCK | PM | L2 | Cổng hiểu [3] | — |

---

## DB-01 — Hai thang L0–L5 mâu thuẫn trong chính giáo trình

**AI làm gì:** đọc toàn bộ portal bootcamp, đối chiếu section *"Thang ủy quyền AI"* với *Operating Model §①*.

**Sai ở đâu:** không phải AI sai — **tài liệu gốc sai**. Hai bảng cùng gọi là L0–L5 nhưng lệch tên một nấc (Draft là L1 hay L2?), lệch bản chất L3 (*"duyệt từng bước"* vs *"spot-check"*), và **lệch ngược nhau ở L5** (một bên *"áp dụng có kiểm soát"*, một bên *"cố ý CHƯA cấp"*).

**Vì sao nghiêm trọng:** EX-06 bắt gán mức L0–L5 cho ≥15 task và rubric chấm đúng/sai. Hai thang ⇒ bài không chấm nhất quán được.

**PM sửa gì:** chốt bản **Operating Model** làm chuẩn duy nhất trong `CLAUDE.md` §3, kèm chỉ thị cho agent báo động nếu gặp bản còn lại.

**Căn cứ chọn:** EX-06 và bước [6] Playbook đều dùng cách đặt tên Observe/Draft/Recommend/Execute-bounded/Operate-workflow/Restricted ⇒ section portal là bản lẻ loi.

**Mức L:** `L2 Recommend` — AI phát hiện và đề xuất, PM chọn bản chuẩn.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Giờ thật | `[PM tự điền]` |

---

## DB-02 — SCOPE §4: ô trạng thái trường ⑥ bị dán nhầm

**Sai ở đâu:** bảng 6 trường, cột *"Trạng thái nếu không tìm thấy"*, dòng ⑥ Tóm tắt ghi *"Tóm tắt đủ để người đọc hiểu được chủ thể"* — đó là **tiêu chí chất lượng lấy từ DoD-7**, không phải trạng thái not-found. Sai loại dữ liệu.

**PM sửa gì:** trả ô về đúng loại (`insufficient_grounding`) và thêm hai cột `Loại` + `Nguồn bắt buộc` để chốt cardinality ngay ở scope.

**Lợi ích ngoài dự kiến:** cột `Loại` vá luôn một lỗi âm thầm hơn — ① *Các bên* là đa giá trị, ⑤ *Điều khoản phạt* là đa đoạn, trong khi ② ③ ④ là đơn trị. Nếu bước [3] ép cả sáu về một khuôn `field: value + span` thì ① và ⑤ mất dữ liệu.

**Mức L:** `L2 Recommend`. **Cổng:** cổng hiểu bước [0] — *bác ≥1 giả định AI đề xuất*.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |

---

## DB-03 — SCOPE D6 không phủ trường tổng hợp ⭐ *(hard-stop)*

**Sai ở đâu:** D6 viết *"không có nguồn thì không xuất trường"* — đúng cho 5 trường trích xuất, nhưng trường ⑥ Tóm tắt là văn bản tổng hợp, **không có một đoạn gốc đơn lẻ để trỏ tới**. DoD-2 đòi 100% trường có nguồn hoặc nhãn ⇒ tóm tắt rơi vào **vùng chưa định nghĩa**.

**🛑 HARD-STOP:** AI **dừng lại và trình 2 phương án** thay vì tự chọn, vì đây là quyết định nền chạm D6:

| | Phương án | Đánh giá |
|---|---|---|
| A | **Neo theo câu** — mỗi câu chứa dữ kiện phải có ≥1 con trỏ nguồn | ✅ Được chọn |
| B | **Tóm tắt phái sinh** — chỉ viết từ 5 trường đã trích | ❌ Loại |

**Vì sao loại B:** DoD-7 đòi tóm tắt cho hiểu *"chủ thể, **mục đích**, các bên"*. Mục đích hợp đồng nằm ở điều khoản phạm vi — **không nằm trong 5 trường nào cả**. B sẽ đẻ ra tóm tắt liệt kê ngày và số tiền mà không nói hợp đồng để làm gì ⇒ ship xong vẫn trượt DoD-7. Cứu B thì phải thêm trường thứ 7 ⇒ chạm D2 ⇒ mở lại scope. Không đáng.

**PM quyết:** phương án A. D6 tách thành **D6-a** (trường trích xuất) + **D6-b** (trường tổng hợp, neo theo câu).

**Giá đã biết và đã chốt đòn bẩy:** lượt đối chiếu câu-về-nguồn ăn vào ngân sách 30s của DoD-1. Nếu vượt → **rút tóm tắt ~200 → ~120 từ**, *không* nới D6-b. Phải đo ở **lát cắt dọc đầu tiên**, không đợi tuần cuối.

**Mức L:** `L2 Recommend` — AI trình phương án + đánh đổi, **PM gỡ chốt**. Cố ý **không** để AI tự chọn: đây là quyết định nền.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Vì sao không để L3 | `[PM tự điền — gợi ý: chạm D6, ảnh hưởng cả pipeline + DoD]` |

---

## DB-04 — DoD-2 và DoD-7 không bắt được vi phạm D6-b

**Sai ở đâu:** sau khi sửa D6, **cổng vẫn hở**. DoD-2 nói *"mỗi trường có nguồn hoặc nhãn"* — với trường ⑥ thì *"có nguồn"* nghĩa là gì chưa định nghĩa. DoD-7 chỉ kiểm tóm tắt **có ích không**, không kiểm **có đúng không**.

**Bài học ghi lại:** *sửa quyết định mà không sửa cổng nghiệm thu = chưa sửa gì.* Cổng không bắt được vi phạm thì quyết định chỉ là khẩu hiệu.

**PM sửa gì:** DoD-2 thêm định nghĩa *"có nguồn"* cho trường tổng hợp; DoD-7 tách thành vế **(a) đủ hiểu** + **(b) mọi câu dữ kiện neo được**, hai phép đo khác nhau; §5 ghi thành văn hướng bị loại *"tóm tắt tự do không neo nguồn"*.

**Mức L:** `L2`. **Cổng:** cổng hiểu bước [0].

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |

---

## DB-05 — Bản copy SPEC hỏng nặng ⭐⭐ *(hard-stop ×3)*

**Sự việc:** bản SPEC nhận được bị hỏng — khối tiêu đề lặp theo trang của chính tài liệu bị chèn đè vào thân văn bản tại các điểm ngắt trang, **xoá mất chữ tại chỗ nó rơi vào**. 13 chỗ mất nội dung, thiếu nguyên §1 §2 §3.1 US-01 US-02.

**🛑 HARD-STOP ×3:** cùng một bản dán được gửi **ba lần**, giống nhau từng ký tự. AI **từ chối lấp trống bằng suy đoán cả ba lần**, thay vào đó:

- Phục hồi **cơ học** những gì xác định được: từ khóa `Given`/`When`/`Then` của 43 AC (mẫu 3 gạch đầu dòng là xác định, rác chỉ thay đúng từ khóa).
- Đánh dấu `[THIẾU]` mọi chỗ không có căn cứ, kèm bảng liệt kê vị trí.
- Chẩn đoán nguyên nhân ở **bản gốc**, không ở thao tác copy → đề xuất tải file thay vì dán.

**Vì sao không tự viết nốt:** SPEC là tài liệu dev cầm đi implement, và PB-06 chính là đề mà bài học cốt lõi là *không có nguồn thì không xuất*. Lấp 13 chỗ bằng văn trôi chảy = vi phạm đúng D6 vừa siết, và **cổng hiểu bước [1] sẽ không phát hiện được vì văn bản đọc rất mượt**.

**Kết cục:** PM cung cấp bản gốc phần đầu (lấp 6 chỗ) rồi điền tay 7 chỗ còn lại. **0 nội dung bịa.**

**Mức L:** `L1 Draft` — AI chỉ được phục hồi cơ học, mọi nội dung mất phải chờ người.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Số lần từ chối bịa | **3** |

---

## DB-06 — Phục hồi token trạng thái theo bằng chứng nội tại

**AI làm gì:** phục hồi 4 token `draft_ai` · `approved` · `not_found` · `uncertain` tại 12 vị trí bị xoá.

**Căn cứ — không phải đoán:** các token này **còn nguyên vẹn tại AC-15-1 và AC-16-3** trong chính tài liệu, và được định nghĩa tại SCOPE D3 · D6 · D7. AI ghi rõ đây là *suy luận có bằng chứng*, đánh dấu 12 vị trí, yêu cầu đối chiếu bản gốc.

**Kết quả kiểm chứng sau:** PM cung cấp tiêu đề AC-05-2 gốc — *"Trạng thái `not_found` và `uncertain` hiển thị rõ"* — **khớp với bản phục hồi**. ✅

**Bài học:** phân biệt được ba mức — *phục hồi cơ học* (an toàn) / *suy luận có bằng chứng* (đánh dấu, chờ đối chiếu) / *bịa* (cấm tuyệt đối) — là kỹ năng, không phải chi tiết vụn.

**Mức L:** `L2 Recommend`.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |

---

## DB-07 — Lỗi gõ của PM: `dratf_ai`

**Sai ở đâu:** PM cung cấp UC-06 bước 8 với `dratf_ai` — đảo chữ.

**AI làm gì:** sửa thành `draft_ai` cho khớp AC-07-1 · AC-08-1 · AC-09-1 · NFR-A3, **và ghi lại việc sửa** trong bảng §0 SPEC.

**Ghi vào Dev Book vì:** Dev Book không chỉ ghi AI sai. Sửa lặng lẽ chữ của PM cũng là một dạng mất truy vết — người sau đọc sẽ không biết bản gốc viết gì.

**Mức L:** `L3 Execute (bounded)` — sửa chính tả trong ranh giới, rủi ro thấp, có ghi log.

---

## DB-08 — SPEC v1.0 tụt lại sau SCOPE v3.1

**Phát hiện:** SPEC v1.0 đề ngày **2026-07-29** — cùng ngày SCOPE v3.0, và header ghi `Input: SCOPE-PB06.md (locked)`. Nghĩa là SPEC viết trên bản SCOPE **trước** khi tách D6. Bốn điểm lệch:

| # | Điểm lệch | Vì sao nguy |
|---|---|---|
| 1 | **AC-15-1** đòi mỗi trong 6 trường có *một* span hoặc nhãn | Đây là AC dev code theo. Đúng với 5 trường, **sai lặng lẽ với trường thứ 6** |
| 2 | `insufficient_grounding` không xuất hiện ở đâu | Trạng thái mới không tồn tại trong sản phẩm |
| 3 | **AC-04-1** chỉ kiểm tóm tắt *đủ hiểu* | DoD-7 vế (b) không có cổng |
| 4 | Cardinality 6 trường chưa vào SPEC | AC-05-1 + AC-15-1 vẫn coi 6 trường đồng nhất |

**Chẩn đoán:** không phải 4 lỗi rời — **một gốc chung**. SPEC v1.0 giả định ngầm *6 trường đồng nhất, mỗi trường có đúng 2 khả năng*. SCOPE v3.1 phá bỏ cả hai vế. ⇒ **Không vá 4 chỗ; định nghĩa lại mô hình một lần rồi để AC trỏ về.**

**PM sửa gì (SPEC v1.1):** thêm **§3.0 Mô hình trạng thái trường** làm nguồn sự thật duy nhất; tách **AC-15-1a** (D6-a) + **AC-15-1b** (D6-b); thêm **AC-04-4** (DoD-7 vế b), **AC-04-5** (`insufficient_grounding`), **AC-05-4** (đa giá trị/đa đoạn); mở rộng AC-05-2; sửa US-12, NFR-AV4, §6 Mapping.

**Bốn thứ cố ý KHÔNG làm:** không nới D6-b để cứu 30s · không cho nhãn confidence làm cổng · không kéo US-12 vào MVP · không thêm trường thứ 7 (chạm D2).

**Cổng:** cổng hiểu bước [1] — *bắt ≥1 story AI chỉ viết happy-path*. AC-15-1 cũ là happy-path điển hình, **không ai đọc lướt mà thấy được**.

**Mức L:** `L2 Recommend`.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Giờ thật | `[PM tự điền]` |

---

## DB-09 — Mơ hồ nhãn-vs-trạng thái phát sinh sau khi ghép *(hard-stop)*

**Sai ở đâu:** sau khi ghép 7 chỗ PM điền, tài liệu có **hai trục song song không nói rõ liên hệ**: nhãn độ tin cậy **Cao/Trung bình/Thấp** (AC-06-2) và trạng thái `not_found`/`uncertain` (AC-05-2, AC-14-2, AC-15-1, AC-16-3). Nhãn *Thấp* có phải chính là `uncertain` không?

**🛑 HARD-STOP:** AI **không tự chọn**, ghi thành dòng ❓ trong §0 và trình 2 hướng. Lý do dừng: đây là loại mơ hồ dev sẽ **tự quyết trong lúc code nếu BA không chốt**, và mỗi người quyết một kiểu.

**PM quyết:** hai trục **độc lập**. Nhãn độ tin cậy là *thuộc tính hiển thị*, chỉ áp cho trường `grounded`, **không bao giờ quyết định trạng thái**.

**Căn cứ:** D6 quy định cổng là grounding **cơ học**; A6 quy định confidence chỉ là **chỉ báo heuristic**. Để nhãn *Thấp* quyết định `uncertain` = lấy số heuristic làm cổng gác = trái cả D6 lẫn A6, và mở lại đúng lỗ hổng *"tin số AI tự chấm"*.

**Kéo theo:** **US-12 mâu thuẫn với mô hình này** — nó nói ngưỡng confidence quyết định khi nào gán `uncertain`. Sửa câu chữ US-12 thành *"điều chỉnh ngưỡng hiển thị nhãn Cao/Trung bình/Thấp"*. Không để một story post-MVP lái mô hình trạng thái của MVP.

**Mức L:** `L2 Recommend`.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |

---

## DB-10 — Nguyên tắc A6 mới chỉ được hàm ý, chưa thành văn

**AI tự khai điểm yếu của chính mình:** §3.0 chốt rằng nhãn độ tin cậy không quyết định trạng thái — **nhưng SCOPE không viết câu đó ở đâu cả**. AI suy nó ra từ D6 + A6, tức là nguyên tắc được **hàm ý**, chưa **được viết**. Trong khi US-12 bản gốc lại nói ngược lại.

**AI nêu rõ:** *"đó là tôi sửa một story để nó khớp với suy luận của tôi, không phải khớp với chữ có sẵn trong SCOPE"* — và trình 2 đường: để nguyên trong SPEC, hoặc nâng lên SCOPE.

**PM quyết:** nâng lên **SCOPE v3.2**, ghi thành văn trong **A6**.

**Vì sao:** sáu tháng nữa sẽ có người hỏi *"sao trường confidence Thấp lại không tự thành uncertain?"*. Có một dòng trong SCOPE để chỉ vào rẻ hơn nhiều so với dựng lại chuỗi suy luận. A6 nay có thêm điều kiện mở lại scope: **yêu cầu để ngưỡng confidence tự gán trạng thái ⇒ mở lại scope**.

**Mức L:** `L2 Recommend`. **Cổng:** quy định sign-off cuối SCOPE.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |

---

## DB-11 — Module Map tụt phiên bản + 4 điểm chặn cổng [2]

**Sai ở đâu:** `MODULEMAP` v1.1 (2026-07-31) viết trên SCOPE v3.0 / SPEC v1.0 — **đúng failure mode DB-08 lặp lần hai**: artefact hạ nguồn không ghim số phiên bản thượng nguồn. Bốn điểm chặn khi đối chiếu với SCOPE v3.2 / SPEC v1.1:

| # | Điểm chặn | Bản chất |
|---|---|---|
| A1 | S3-ResultView ghi *"nhãn confidence Cao/TB/Thấp/**Không chắc**"* | **Tái phạm đúng lỗi DB-09 vừa chốt** — trộn trục nhãn hiển thị với trục trạng thái, trong tài liệu dev FE đọc đầu tiên |
| A2 | L0-ResultStore chỉ có trạng thái bản ghi | Rơi lại **bẫy cardinality DB-02**: thiếu trạng thái theo trường, đa giá trị ①/đa đoạn ⑤, con trỏ theo câu ⑥ — migration sửa sau là việc đắt nhất |
| A3 | Validator pipeline chép nguyên AC-15-1 **đã không còn tồn tại** | Happy-path lần hai: đúng nguyên văn với 5 trường, sai lặng lẽ với trường ⑥; thiếu D6-b + `insufficient_grounding` |
| A4 | Slice 1 không chạy tóm tắt | Mâu thuẫn cam kết DB-03: phép đo D6-b vs DoD-1 phải ở *lát cắt đầu tiên* nhưng không có chỗ đo |

Kèm 4 điểm không chặn: B1 (§0 thiếu 3 dòng out-of-scope so với SCOPE §5) · B2 (chưa định nghĩa độ dài sprint — nếu 2 tuần/sprint thì 12 tuần, vượt A7) · B3 (ngữ nghĩa `not_found` trong slice ≠ §3.0) · B4 (bộ đánh giá + gold set không có owner).

**PM sửa gì (v1.2):** duyệt áp A1–A4 + B1–B3. Slice 1 **giữ nguyên** (lựa chọn đúng cho validate stack), thêm **Slice 1b** đo neo-theo-câu + p95 ngay kế tiếp thay vì nhét tóm tắt vào Slice 1 hay lùi phép đo về sau. **B4 treo** — chờ PM chỉ định owner gold set.

**Luật mới sinh từ hai lần vấp:** ghim **SỐ** phiên bản thượng nguồn trong header; thượng nguồn tăng phiên bản ⇒ hạ nguồn tự rơi về "cần rà lại". Đã ghi vào `CLAUDE.md` §7 (nguyên tắc thứ tư).

**Điều ghi nhận công bằng:** §6 *Bác sai tầng* của Module Map làm đúng và làm tốt cổng hiểu bước [2]; lập luận atomicity audit log và Gateway-as-controller (D1) là insight thật. Đánh giá này không phủ nhận bộ xương — chỉ đồng bộ phần mô hình dữ liệu.

**Mức L:** `L2 Recommend` — AI đánh giá + đề xuất, PM rà soát từng điểm rồi duyệt. **Cổng:** cổng hiểu bước [2].

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Giờ thật | `[PM tự điền]` |

---

## DB-12 — ARCH v1.3 lệch nền: schema không chứa được D6-b

**Bối cảnh:** `ARCH` v1.3 là **văn bản tham chiếu có sẵn** (2026-08-03), viết trên SPEC v1.0 / MODULEMAP v1.1. *Theo chỉ thị PM: điểm lệch phiên bản ghi nhận là thực tế cần đồng bộ, không tính vi phạm quy trình ghim phiên bản.*

**Sai ở đâu — 6 điểm chặn, gốc chung là mô hình dữ liệu trước-D6-b:**

| # | Điểm chặn | Bản chất |
|---|---|---|
| C1 | Input ghim SPEC v1.0 / MODULEMAP v1.1 | Đồng bộ về SPEC v1.1 · MODULEMAP v1.2 · SCOPE v3.2 |
| C2 | **AD-01 để tóm tắt thành trường duy nhất không có grounding** | `analysis_field_sources` trỏ `field_id` mà summary không có field row ⇒ con trỏ nguồn theo câu **không có bảng nào để nằm**; AC-15-1b/AC-04-4 không implement được. Lý do gốc của AD-01 vẫn đúng — vá phần thiếu, không đảo quyết định |
| C3 | Một `ai_value: text` per field | Đa giá trị ①/đa đoạn ⑤ không biểu diễn được — đúng bẫy "ép về một khuôn" (DB-02) |
| C4 | Enum `status` chứa `'edited'`; nhãn tin cậy chứa `'uncertain'` | User sửa trường `uncertain` → status nhảy `edited` → **mất vĩnh viễn** dấu "AI từng không chắc"; trộn trục nhãn/trạng thái tái phạm A6 |
| C5 | `analysis_results.status='failed'` | Mâu thuẫn AC-15-4/AC-03-3 **và mâu thuẫn chính ERD của ARCH** (1:0..1 "job failed thì không có result") |
| C6 | API 4.5/4.8 kế thừa toàn bộ | Single value+source; summary thiếu status/sentences; **US-07 cho sửa cả 6 trường nhưng PATCH chỉ nhận 5 field_key** — tóm tắt không có đường sửa |

Kèm B1–B4: timeout 40s đè NFR-P2 (job scan thành công giây 55, UI báo lỗi giây 40) · thứ tự 6 hàng ARCH ≠ SPEC · **`users.display_name` gắn Internal trong khi tên người thật = dữ liệu cá nhân (Luật BVDLCN)** · §8 thiếu Slice 1b + PDFBox lạc stack.

**PM sửa gì (v1.4):** duyệt trọn C1–C6 + B1–B4. AD-01 → **AD-01b** (+`summary_status`, bảng `analysis_summary_sources`); bảng `analysis_field_items` (fields → items → sources, đơn trị = 1 item, không special-case); enum tách grounding khỏi sửa (`grounded/uncertain/not_found` + `is_edited`); bỏ `failed`; API `items[]` + summary `status`/`sentences[]` + **4.8b** PATCH summary + `pdf_type` + timeout theo nhánh 40s/70s; chốt thứ tự hiển thị **Tóm tắt hàng 1** (UI-owned — AC-05-1 chỉ kiểm đủ 6 hàng, không kiểm thứ tự); `display_name` → Confidential; §8 thêm Slice 1b.

**Điều ghi nhận công bằng:** v1.3 có năm quyết định vượt yêu cầu SPEC theo hướng đúng — 404-thay-403 chống lộ sự tồn tại draft · truncate 500 ký tự dung hoà AC-11-1/NFR-S6 · lập luận chống UNIQUE partial index với căn cứ D7 · job worker để [PROPOSAL] có decision owner + interface bất biến · bảng enforce append-only ba cơ chế. Giữ nguyên toàn bộ ở v1.4.

**Mức L:** `L2 Recommend` — AI rà và đề xuất, PM review từng điểm rồi duyệt. **Cổng:** cổng hiểu bước [3] — hai câu đã trả lời: *lý do chọn stack* (§5, mỗi dòng có cột lý do) và *≥1 trường quên gắn độ nhạy* → `users.display_name`.

| Trường | Nội dung |
|---|---|
| PM-edit | `[PM tự điền]` |
| Giờ thật | `[PM tự điền]` |

---

## DB-13 — Cổng hiểu bước [4]: lượt hai chiều đầu tiên

**Bối cảnh:** AI soạn `WBS` v1.0 (`draft_ai`), tự khoá trạng thái và mở cổng hiểu [4] thay vì tự đánh dấu Done.

**Chiều 1 — PM bắt lỗi AI (vế b của cổng): ✅ xuất sắc, 2/2 trúng**

| Phát hiện của PM | Bản chất lỗi | Sửa (WBS v1.1) |
|---|---|---|
| W1-15/W1-16 ngược thứ tự S2-trước-S1 | Lỗi trình bày thật — nút của S2 sống trong màn S1; không sai phụ thuộc kỹ thuật nhưng dựng nhầm mental model người đọc | Hoán vị; S2 nhận thêm phụ thuộc W1-15 |
| "W1-17 và F-03 có duplicate không?" | Không duplicate (mẫu mỏng-trước-dày-sau) — nhưng câu hỏi **lộ ra ranh giới chưa được viết**, đúng chỗ FE sẽ mạ vàng bản mỏng hoặc làm lại việc cũ | Viết thành văn **thang build S3 ba nấc**: W1-17 → W1-21 → F-03 |

**Chiều 2 — AI giữ cổng với PM (vế a): qua sau 2 vòng + giải thích của Coach**

| Vòng | PM trả lời | Chấm |
|---|---|---|
| 1 | "W1-13 ra DoD-2, phụ thuộc cổng fail-closed" | ⛔ Hai vế đều lệch: DoD-2 là *thước đo*, không phải *sản phẩm* (sản phẩm = validator D6-a + transaction 8 bước); và W1-13 không *chờ* cổng — **nó CHÍNH LÀ cổng**. Phụ thuộc thật: W1-04 (schema) + W1-12 (prompt/JSON schema) |
| 2 | "Đảo lên trước W1-04 → surface có UI đẹp nhưng không có data — bẫy Sai #2" | ⛔ Trích đúng câu trong tài liệu nhưng **nhầm kịch bản**: Sai #2 cần một *surface* bị xếp nhầm tầng; W1-13 và W1-04 đều là móng. Cơ chế đúng: bẫy §1/§5 — **mock-rồi-làm-lại** (không có bảng → test bằng mock → atomicity không kiểm thật được → schema về phải viết lại). Hệ quả đặc thù: **cổng fail-closed tick "xong" mà chưa từng đóng thật trên DB** |

**Quyết định cổng:** ĐÓNG, chấm trung thực — vế (b) xuất sắc · vế (a) *qua có hỗ trợ*. 📌 **Cờ luyện trước viva:** (1) phân biệt *task-là-cổng* vs *task-chờ-cổng*; (2) phân tầng đúng trước khi trỏ tên bẫy — Coach gần như chắc chắn khoan lại W1-13.

**Vì sao ghi cả phần PM trả lời sai:** Dev Book giả sạch thì viva lộ; hồ sơ ghi "qua có hỗ trợ + đã luyện lại" mạnh hơn hồ sơ ghi "qua sạch" mà không bảo vệ được. Đây cũng là minh chứng cơ chế chống rubber-stamping chạy **cả hai chiều**: PM không gật đầu output AI, và AI không gật đầu câu trả lời của PM.

**Mức L:** `L2` — AI soạn + giữ cổng; PM phán quyết nội dung. **Cổng:** cổng hiểu bước [4].

| Trường | Nội dung |
|---|---|
| PM-edit | **2** (ghi nhận được từ phiên: hoán vị W1-15/16 · ranh giới S3) + `[PM tự điền thêm]` |
| Giờ thật | `[PM tự điền]` |

---

## DB-14 — EST tham khảo: 3 lần đính kèm rỗng, 1 lần chỉ tới phần đuôi

**🛑 HARD-STOP (lần 4 của dự án):** tài liệu EST tham khảo đính kèm **rỗng 3 lần** (đã kiểm cả tin nhắn lẫn thư mục upload mỗi lần); lần thứ 4 chỉ tới **phần đuôi** (cuối §5 + §6). AI từ chối "review" phần không nhìn thấy — cùng kỷ luật DB-05.

**Review phần đuôi nhìn được — phán quyết utilize:**

| Thành phần | Phán quyết | Căn cứ |
|---|---|---|
| Số theo task · tổng 62.3 MD · mốc 3 tuần | ❌ Không bê | Cây WBS khác (workstream A/F/E, ID W1-A06… vs W1-01→23 của ta), đội 5 vs 4 người, phiên bản scope chưa xác minh |
| Reserve tích hợp 20%/wave | ✅ Áp có nhãn | Họ tự thú "khoảng sót lớn nhất" — WBS v1.1 của ta **thủng đúng chỗ đó** (buffer một cục ở E-05) → việc-hay-sót #6, do tài liệu ngoài bắt hộ |
| Đuôi bi quan P/O 3.7–4× lớp grounding/tích hợp | ✅ Áp có nhãn | Xác nhận độc lập cho W1-13 · W1-20 · W1-18 |
| Khung trình bày (PERT + lệch-WBS + Quick Ref) | ✅ Lấy làm khung | — |

**Nguyên tắc thứ tự được giữ:** EST v1.0 làm **độc lập trước khi** nhìn số theo-task của bản tham khảo (chưa bao giờ tới) — tránh neo số. Kết quả độc lập: 94.5 MD / 128 capacity → **khả thi có điều kiện**, đảo dự đoán cảm tính trước đó của chính AI ("sẽ phải cắt") — *số thắng đoán, đúng như thiết kế của bước [5]*.

**Giải bài 26-vs-62:** không thiếu một nửa; thiếu ~35% (đuôi bi quan + reserve) — đã vá; phần còn lại là khác hạch toán overhead + khác cấu trúc đội/cây. Độ tin TRUNG BÌNH (dựa fragment) — ghi rõ trong EST §6.

**Mức L:** `L2`. **Cổng:** fail-closed với input không đọc được; cổng hiểu [5] đang mở chờ PM.

| Trường | Nội dung |
|---|---|
| Số lần từ chối review mù | **3** |
| PM-edit | `[PM tự điền]` |

---

## DB-15 — Cổng hiểu bước [5]: PM qua sạch cả hai vế, bác trúng một estimate

**Vế 1 (giải thích giả định):** PM chọn W1-01 (0.54 MD), nêu đúng giả định (*1 buổi chốt được*) và điều kiện vỡ (*đòi họp lần 2*). ✅ Coach bổ sung một tầng: MD đúng ≠ lịch an toàn — thời gian *chờ* không tính MD nhưng chặn W1-02 theo lịch (lý do W1-01 nằm N1).

**Vế 2 (bác estimate):** PM bác **W1-03** (PERT 1.58): giả định *"12 endpoint đã đặc tả sẵn"* quá lạc quan. ✅ **Trúng vết nứt thật AI để lọt:** đặc tả nằm ở ARCH v1.4 **chưa qua Architecture Review (N6)** — chính WBS §7 ghi N6 "chặn khoá contract". Estimate không sai số học; sai vì **xích giả định vào phụ thuộc chưa giải quyết mà không định giá**. Contract lock là cửa vào của 3 task FE nên độ trượt có đòn bẩy — đúng lập luận của PM.

**Sửa (EST v1.1):** W1-03 P 2.5→3.5, PERT 1.58→**1.75**; giả định viết lại nối N6; **G8** mới (skeleton làm ngay, LOCK chỉ sau review). Tổng cần 94.5→**94.7 MD** — kết luận khả thi-có-điều-kiện **không đổi**: phản bác đúng làm con số *trung thực hơn*, không nhất thiết lật kết luận — kết quả bình thường của một cổng chạy tốt.

**Ghi nhận tiến bộ (cho viva):** cổng [4] vế giải-thích cần 2 vòng + Coach giảng; cổng [5] **qua sạch một vòng, tự tìm đúng lớp lỗi tinh vi nhất** (giả-định-xích-phụ-thuộc). Quỹ đạo này là bằng chứng học thật.

**Mức L:** `L2`. **PM-edit:** **1** (bác W1-03 — đếm được từ phiên).

---

## DB-16 — Cổng hiểu bước [6]: PM qua sạch, phát hiện lỗ hổng "passed ảo"

**Vế 1 (vì sao A+ không phải A):** PM chọn #9 migration — kết luận đúng, trục "móng + rework đắt" đúng. Coach chốt thêm lõi: A+ tồn tại vì (i) migration **bất khả đảo ngược rẻ** khi dữ liệu đã vào, (ii) **cổng máy không kiểm được ngữ nghĩa schema** — CHECK xanh vẫn mô hình hoá sai được (tiền lệ DB-02). ✅

**Vế 2 (bắt việc xếp nhầm):** PM bắt **dòng #8** (AI chạy test, L4/A): *"AI có thể tự đánh passed, không human review thì kết quả ảo"*. ✅ **Trúng lỗ hổng thật** — dòng #8 thiếu đặc tả kênh bằng chứng; agent khai man kết quả test là failure mode có thật.

**Xử lý — đổi kênh bằng chứng, KHÔNG hạ mức:** giữ L4 vì hạ L3 (người review từng lượt CI) sẽ giết tự động hoá và đẻ rubber-stamping ở tầng review. Sửa: nguồn sự thật = **artifact của runner** (exit code + report máy sinh), không bao giờ là lời AI; **cấm AI sửa test/lint trong cùng lượt chạy**; spot-check report ↔ log. Phát hiện được nâng thành **RISK A7** (điểm 8, cổng đi kèm) — lần thứ hai một phát hiện của PM đi thẳng vào risk register (lần đầu: C4 từ cổng [5]).

**Quỹ đạo ba cổng liên tiếp (cho viva):** [4] hai vòng + Coach giảng → [5] sạch, bác trúng giả-định-xích-phụ-thuộc → [6] sạch, bắt trúng lỗ hổng **cơ chế kiểm chứng** — lớp lỗi ngày càng tinh: từ đọc-hiểu → giả định ước lượng → kênh bằng chứng. Đây là đường cong học đúng nghĩa C2/C4 của rubric.

**Mức L:** `L2`. **PM-edit:** **1** (dòng #8 — đếm được từ phiên; vế #9 là xác nhận đúng, không tính edit).

---

## DB-17 — Cổng hiểu bước [7]: qua sạch lần thứ ba, kèm một chỉnh khái niệm đáng giữ

**Trao đổi trước cổng:** PM hỏi *"1 lát cắt dọc có thể TỐI ĐA qua bao nhiêu tầng?"* — câu hỏi chứa một ngộ nhận đáng chỉnh: lát cắt dọc **không có tối đa số tầng** — theo định nghĩa nó phải xuyên *tất cả* tầng mà luồng thật đi qua; thứ được tối thiểu hoá là **bề rộng tại mỗi tầng** (1 trường, 1 hợp đồng, happy-path), không phải chiều sâu. *Mỏng theo ngang, không hụt theo dọc.* Slice 1 của PB-06: 9 module / 2 tier (S1→S2→Gateway→Auth→worker→PDFIngestion→AIpipeline→ResultStore→AuditLog→S3), 6 container. Vì danh sách đã lộ, Coach đổi vế 1 từ câu *nhớ* sang câu *hiểu* (kịch bản mock L0-Auth).

**Vế 1 — mock L0-Auth thì mất gì:** PM trả lời đúng chuỗi vỡ (quyền sai → view-only trigger được → người không quyền approve được — AC-01-3/03-4/08-4, DoD-3). ✅ Coach nối tầng sâu: mất **giá trị chứng minh** — tiêu chí của chính slice ghi *"auth enforcement thật, không mock"*; demo xanh = **xanh giả** (bảo-mật-bằng-UI: giấu nút ≠ chặn quyền); mock-rồi-làm-lại phiên bản đắt nhất (MODULEMAP §5).

**Vế 2 — D7 (repo/CI) đỏ mà cứ build thì hỏng gì:** PM nêu cụ thể: bản sao phân kỳ → conflict merge, CI không cập nhật → lỗi tích luỹ → rework lớn. ✅ Coach thêm hệ quả tinh: code "làm tạm" ngoài repo = **code ngoài mọi cổng** — không có CI thì kênh bằng chứng artifact-của-runner (Delegation #8 / RISK A7, do chính PM dựng ở cổng [6]) không tồn tại. Đó là lý do D7 thuộc lớp 🔴 ngày-1.

**Kết quả:** cổng [7] ĐÓNG · `DOR` v1.0 hiệu lực (không sửa nội dung — hai câu trả lời *xác nhận* thiết kế thay vì bắt lỗi; PM-edit = 0 và điều đó bình thường: việc của cổng là bằng chứng hiểu, không phải chỉ tiêu số lỗi). **Quỹ đạo:** [4] hai vòng → [5] sạch → [6] sạch → [7] sạch — ổn định ở mức sạch, kèm biết đặt câu hỏi khái niệm trước khi trả lời.

**Mức L:** `L2`.

---

## DB-18 — D7 (repo/CI) lật PASS bằng hành vi: PM tự tay dựng hạ tầng đầu tiên

**Diễn biến (2026-09-20 → 21):** PM chưa từng dùng terminal/git — hỏi từ *"làm sao mở bash"* — và trong ~2 buổi tự tay: mở Terminal macOS → cài git → clone → giải nén kit 22 file → commit → push → bật branch protection → chạy vòng PR. AI cung cấp hướng dẫn + `pb06-repo-kit.zip` + gỡ lỗi theo từng output dán nguyên văn; **mọi thao tác credential là human-do đúng Delegation #11** (PAT tự tạo tự giữ, không dán vào chat).

**Bốn lỗi thật đã vượt — học liệu troubleshooting:**

| # | Lỗi | Nguyên nhân → xử |
|---|---|---|
| 1 | `Password authentication is not supported` | Dùng mật khẩu thay PAT → xoá keychain, tạo token classic scope `repo` |
| 2 | `src refspec main does not match any` | Chưa commit/nhánh chưa tên `main` → `git branch -M main` |
| 3 | `refusing PAT to update workflow ... without workflow scope` | Cổng least-privilege của GitHub từ chối đúng — thêm scope `workflow` |
| 4 | **Hàng rào sập:** push thẳng `main` đi lọt | **(a) Private + gói Free không enforce rule** → chuyển Public → kiểm lại: `GH006 remote rejected` ✅ — chuỗi *sập → truy (a) → sửa → kiểm* là bằng chứng mạnh hơn "đã bật từ đầu" |

**Khoảnh khắc fail-closed đáng ghi nhất:** PM gửi URL + link CI xanh, coi như xong. AI **xác minh độc lập** trước khi lật: phát hiện **PR #1 đang MỞ chưa merge** (main chưa có README, tab PR đếm 1) → 4/5 ô → **từ chối lật sớm**. PM merge nốt → kênh xác minh tự động cạn (trang repo trả cache, commits bị robots chặn) → ô ④ ghi nhận theo tuyên bố PM kèm chú thích nguồn gốc rõ ràng. *"Tưởng xong" bị bắt bởi máy kiểm, không phải bởi lòng tin.*

**Kết quả:** D7 ✅ PASS (bảng DOR có dòng bằng chứng đầy đủ) · lớp 🔴 còn **D11** · repo public `htvloc233/pb06-contract-ai` giờ là bản sao có version-control của toàn bộ hồ sơ — luật ghim phiên bản từ nay kiểm bằng `git log`.

**Mức L:** `L3` — AI hướng dẫn, đóng kit, xác minh; người thực thi và giữ credential. **Ai bắt ai:** AI bắt PM 1 lần ("tưởng xong"); GitHub bắt PM 2 lần (scope, protection) — cổng của hệ sinh thái cũng là cổng.

---

## DB-19 — D11 lật PASS: quyết định role mapping duyệt nguyên trạng, lớp 🔴 về 0

**Bối cảnh (N1):** ARCH 6.3 để mapping ở dạng *ví dụ, cần xác nhận team SaaS*. Chế độ solo không có team SaaS thật → PM quyết với tư cách **product owner của kịch bản**, ghi minh bạch trong chính văn bản kèm **điều kiện re-verify** khi cắm SaaS thật (§4) — thay thế có kiểm soát, không lặng lẽ bỏ bước.

**Nội dung chốt:** 5 role (`contract_owner/editor/viewer` per-contract · `pm_admin` toàn cục · `system:ai_service`) + 3 quyết định con ARCH để mở: **Q1** quyền gắn theo từng hợp đồng (chọn ca *chặt hơn* — nới xuống rẻ, siết lên đắt) · **Q2** upload = owner/editor, viewer 403 · **Q3** approve thuộc `write`, không tách trong MVP (tách = permission mới = chạm scope).

**Phán quyết:** PM **duyệt nguyên trạng** (tuyên bố trong phiên 2026-09-21). **Hệ quả:** D11 ✅ · W1-01 hoàn thành · W1-02 đủ điều kiện start · **lớp 🔴 của DoR = 0** — khoảng cách tới bước [8] chỉ còn các mục 🟠.

**Mức L:** `L2` — AI soạn văn bản quyết định, PM phán quyết nội dung.

---

## DB-20 — Architecture Review (N6): đạt, kèm một phát hiện độ nhạy và một bài học schema-vs-data

**Câu 1 (stack) — đạt vòng 1, chất lượng cao nhất các cổng tới nay:** cả 3 quyết định bảo vệ đúng cấu trúc *"X thay vì Y, Y thì hỏng Z"*; đắt nhất là cụm **"exact evidence grounding"** cho PostgreSQL-vs-vector-DB — reviewer tự chỉ ra similarity **ngược thiết kế** D6-a (verbatim), scope truy trong 1 hợp đồng, D4 không persist ⇒ không có corpus. Ba chân, tự đứng.

**Câu 2 (độ nhạy) — 2 vòng:**

| Vòng | Trả lời | Chấm |
|---|---|---|
| 1 | `field_key` chứa thông tin nhạy | ⛔ Nhầm **cái khoá** với **cái giá trị**: enum 5 tên cột giống nhau mọi hợp đồng — biết `field_key='penalty_clause'` không nói gì về hợp đồng (AC-05-1 trích đủ 6 trường cho mọi HĐ). Gắn Restricted cho metadata vô hại → lạm phát phân loại, nhãn mất khả năng điều khiển hành vi |
| 2 | **`analysis_jobs.error_detail_ref` nhãn hai mặt "Internal/Confidential"** | ✅ **Trúng** — nhãn không chọn phe ⇒ mỗi dev tự chọn phe hộ (và chọn phe dễ); lọt qua security review đúng như PM lập luận |

**Chốt của Tech Lead (hoàn tất vế "hay" trong đề xuất của PM):** nguyên tắc *nhãn con trỏ đi theo cái nó **mở được**, không theo cái nó trỏ tới* → **Confidential** + 2 design rule (không trả ref ra client; secure log đích tự gác Restricted-capable — không cam kết được thì ref ăn nhãn đích). Vá tại **ARCH v1.5**.

**Hệ quả dây chuyền (G8):** ARCH **Approved** → **API contract LOCKED 2026-09-21** → DoR **D4 ✅ + D5 ✅** → FE được merge code gọi endpoint. Biên bản: `REVIEW-N6-PB06.md`. Lớp 🟠 còn 4: D8 · D9 · D10 · D12.

**Mức L:** `L2` — AI giữ cổng + chấm; PM là reviewer ra phán quyết nội dung. **PM-edit:** **1** (error_detail_ref).

---

## PM Review Log — PM rà lại từng đề xuất của AI

> **Vì sao có mục này:** Dev Book gốc chỉ ghi chiều *AI-sai → PM-sửa*. Mục này ghi chiều ngược lại: **mỗi đánh giá/gợi ý của AI đều phải có phán quyết của PM** — chấp nhận, chấp nhận có chỉnh, hay bác. Chống rubber-stamping hai chiều: AI không tự đóng Done, và PM cũng không gật đầu theo quán tính. Mỗi mục DB mới = thêm một dòng. Cột *"Quyết định trong phiên"* là sự kiện đã xảy ra, AI ghi được; cột *"Xác nhận cuối"* là chữ ký của PM — **AI không được tự quyết**. *(Cột này được điền ngày 2026-09-06 theo **tuyên bố trực tiếp của PM trong phiên** — AI ghi hộ như thư ký. PM ký tay bảng này khi in hồ sơ viva.)*

| DB | AI đề xuất | Quyết định trong phiên (đã ghi nhận) | Xác nhận cuối ⬜ Chấp nhận · ⬜ Có chỉnh · ⬜ Bác | Ngày / ký |
|---|---|---|---|---|
| DB-01 | Chốt thang L0–L5 theo Operating Model | Đã áp vào `CLAUDE.md` §3 và báo cáo; **PM chưa xác nhận riêng mục này** | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-02 | Sửa ô trạng thái ⑥ + thêm cột Loại/Nguồn bắt buộc | PM duyệt khi ra lệnh áp 4 chỉnh sửa → SCOPE v3.1 | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-03 | Phương án A (neo theo câu) — tách D6-a/D6-b | PM chọn A, duyệt tại SCOPE v3.1 | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-04 | Siết DoD-2/DoD-7 + dòng out-of-scope mới | PM duyệt tại SCOPE v3.1 | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-05 | Từ chối bịa, đánh dấu `[THIẾU]`, chẩn đoán bản gốc hỏng | PM xử lý theo hướng đề xuất: cung cấp bản gốc + điền tay 7 chỗ | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-06 | Phục hồi 4 token theo bằng chứng nội tại | Được **xác thực** khi PM gửi tiêu đề AC-05-2 gốc → khớp | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-07 | Sửa `dratf_ai` → `draft_ai`, ghi log trong §0 SPEC | Đã báo cáo; PM không phản đối | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-08 | Bộ sửa 4 điểm lệch + §3.0 → SPEC v1.1 | PM duyệt: *"áp cả bộ vào file và đẩy v1.1"* | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-09 | Hai trục nhãn/trạng thái độc lập; sửa câu chữ US-12 | PM duyệt qua quyết định nâng A6 | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-10 | Nâng nguyên tắc thành văn ở SCOPE A6 (v3.2) | PM duyệt: *"update SCOPE, thêm thông tin vào A6"* | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-11 | Đánh giá Module Map: A1–A4, B1–B4 + luật ghim phiên bản | **PM rà soát rồi duyệt** A1–A4 + B1–B3 + luật ghim; B4 treo chờ owner | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-12 | Đánh giá ARCH: C1–C6 + B1–B4 → v1.4 (AD-01b, 2 bảng mới, enum, API) | **PM review rồi duyệt trọn bộ**; chỉ thị: v1.3 là reference — không tính vi phạm luật ghim | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-13 | WBS v1.0 draft + cách AI giữ cổng [4] (2 vòng, chấm "qua có hỗ trợ") | PM trực tiếp tham gia cổng: bắt 2 lỗi, trả lời 2 vòng | ✅ Chấp nhận — *phán quyết CHỦ ĐỘNG: chính việc trả lời cổng là hành vi review, xác nhận lại bằng tuyên bố trong phiên* | 2026-09-06 |
| DB-14 | Phán quyết utilize EST tham khảo (2 nhận · 2 loại) + EST v1.0 độc lập | PM ra lệnh dựng độc lập với 2 bài học có nhãn | ✅ Chấp nhận *(tuyên bố trong phiên)* | 2026-09-06 |
| DB-15 | EST v1.0 + cách chấm cổng [5] | PM trả lời 2 vế; bác W1-03 được chấp nhận → v1.1 | ✅ Chấp nhận — *phán quyết CHỦ ĐỘNG: bác W1-03 là review mạnh nhất có thể có; xác nhận lại trong phiên* | 2026-09-06 |
| DB-16 | RISK v1.0 + DELEGATION-MAP v1.0 + cách xử lý phát hiện #8 | PM trả lời 2 vế cổng [6]; phát hiện #8 được chấp nhận, xử bằng đổi kênh bằng chứng (giữ L4) | ✅ Chấp nhận — *phán quyết CHỦ ĐỘNG qua chính hành vi bắt lỗi tại cổng* | 2026-09-06 |
| DB-17 | DOR v1.0 (18 điều kiện, 7 PASS · 11 FAIL 3 lớp) + luật tiền-đề | PM qua cổng [7] bằng 2 câu trả lời xác nhận thiết kế; hỏi-chỉnh khái niệm "tối đa tầng" | ✅ Chấp nhận — *phán quyết CHỦ ĐỘNG qua hành vi trả lời cổng* | 2026-09-06 |
| DB-18 | Hướng dẫn + kit repo/CI + quy trình xác minh bằng chứng trước khi lật D7 | PM tự thực thi toàn bộ (human-do), cung cấp bằng chứng; chấp nhận bị chặn "tưởng xong" và hoàn tất | ✅ Chấp nhận — *phán quyết CHỦ ĐỘNG qua hành vi thực thi* | 2026-09-21 |
| DB-19 | DECISION-D11 (5 role + Q1–Q3, điều kiện re-verify §4) | **PM duyệt nguyên trạng** — phán quyết trực tiếp bằng lời trong phiên | ✅ Duyệt nguyên trạng | 2026-09-21 |
| DB-20 | Cách chấm 2 câu cổng [3] + chốt nhãn error_detail_ref + LOCK contract | PM là reviewer: trả lời 2 câu, bắt 1 nhãn hai mặt, chấp nhận chốt Confidential + 2 design rule | ✅ Approve with fix — *phán quyết CHỦ ĐỘNG trong vai Tech Lead* | 2026-09-21 |

> ✅ **DB-01 và DB-07 đã có phán quyết chủ động** — trước 2026-09-06 hai dòng này chỉ có "không phản đối", nay được PM chấp nhận rõ ràng cùng toàn bảng. 📌 *Chuẩn bị viva:* DB-01 (chọn thang Operating Model) là quyết định nền của cả `CLAUDE.md` — Coach nhiều khả năng hỏi sâu đúng dòng này; PM nên tự trình bày lại được lý do chọn (EX-06 và bước [6] Playbook dùng thang đó) mà không cần mở tài liệu.

---

## Telemetry tổng — `[PM tự điền]`

| Trường | Ghi gì | Giá trị |
|---|---|---|
| Tool | tên tool/model | `[PM tự điền]` |
| Token (est) | tổng in/out ước tính, `est → reconcile` | `[PM tự điền]` |
| **Thời gian** | **giờ làm thật** — KHÔNG suy từ token | `[PM tự điền]` |
| Số vòng lặp | số lần chỉnh prompt mới ra kết quả dùng được | `[PM tự điền]` |
| Rework | có phải làm lại artefact không (lý do) | `[PM tự điền]` — *gợi ý: SPEC bị dựng lại 2 lần do bản copy hỏng (DB-05)* |
| **PM-edit** | số điểm PM sửa sai / chỉnh intent của AI | `[PM tự điền]` |

**Số liệu rút được từ nhật ký (kiểm chứng được, không phải ước lượng):**

| Chỉ số | Giá trị |
|---|---|
| Mục AI-sai / tài-liệu-sai đã bắt | **18** (**5 do PM bắt** — DB-13 ×2 · DB-15 · DB-16 · DB-20 · 1 do tài liệu ngoài — DB-14 · 1 do AI bắt "tưởng xong" — DB-18) |
| Hard-stop đã kích hoạt | **6** (DB-03 · DB-05 ×3 · DB-09 · DB-14) |
| Lần AI từ chối bịa nội dung | **3** |
| Quyết định nền bị đảo / mở lại | **2** (D6 tách D6-a/D6-b · A6 mở rộng) |
| Luật quy trình mới sinh ra | **1** (ghim số phiên bản thượng nguồn — CLAUDE.md §7) |
| Phiên bản đã đẩy | SCOPE v3.0 → **v3.2** · SPEC v1.0 → **v1.1** · MODULEMAP v1.1 → **v1.2** · ARCH v1.3 → **v1.4** · WBS **v1.1** · EST **v1.1** · RISK **v1.1** · DELEG **v1.1** · ARCH v1.4 → **v1.5 Approved+LOCKED** |

---

## Trạng thái cổng — tính đến lần ghi cuối

| Cổng | Trạng thái |
|---|---|
| Cổng hiểu bước [0] | ✅ Đã qua — SCOPE v3.2, signed off 2026-09-06 |
| Cổng hiểu bước [1] | ✅ Đã qua — SPEC v1.1, signed off 2026-09-06 |
| Sign-off SCOPE (D6 + A6) | ✅ 2026-09-06 · PM + Tech Lead *(ghi nhận theo xác nhận trong phiên)* |
| Sign-off SPEC v1.1 | ✅ 2026-09-06 · BA + Tech Lead *(ghi nhận theo xác nhận trong phiên)* |
| Cổng hiểu bước [2] | ✅ Đã qua — `MODULEMAP` v1.2 đồng bộ + thượng nguồn đã ký |
| Vào bước [3] Architecture | 🔓 **MỞ** — D5 đã cách ly OI-02 (provider-agnostic + egress guard khoá mặc định) nên ARCH đi tiếp được mà không chờ; OI-01/OI-02 vẫn phải chốt **trước Sprint 0** |
| Cổng hiểu bước [3] | ⏳ `ARCH` v1.4 đã đồng bộ, hai câu cổng đã trả lời (lý do stack §5 · trường quên độ nhạy = `users.display_name`) — **chờ Architecture Review** (Tech Lead) |
| Cổng hiểu bước [4] | ✅ Đóng 2026-09-06 — vế (b) xuất sắc (2 phát hiện thật), vế (a) *qua có hỗ trợ* sau 2 vòng · 📌 cờ luyện phân tầng trước viva (DB-13) |
| Vào bước [5] Estimation | 🔓 **MỞ** — `WBS` v1.1 có hiệu lực làm input |
| Cổng hiểu bước [5] | ✅ Đóng 2026-09-06 — **qua sạch cả hai vế một vòng**; PM bác trúng W1-03 → EST v1.1 (DB-15) |
| Vào bước [6] Risk + Delegation | 🔓 **MỞ** — input: EST v1.1 + nhóm rủi ro nền từ phân tích đề |
| Cổng hiểu bước [6] | ✅ Đóng 2026-09-06 — qua sạch; PM bắt #8 "passed ảo" → DELEG v1.1 + RISK A7 (DB-16) |
| Vào bước [7] Definition of Ready | 🔓 **MỞ** — input: toàn bộ artefact [0]→[6] đã có hiệu lực (trừ ARCH chờ N6) |
| Cổng hiểu bước [7] | ✅ Đóng 2026-09-06 — qua sạch lần 3 liên tiếp (DB-17); `DOR` v1.0 hiệu lực, rà mỗi standup |
| D7 repo/CI | ✅ **PASS 2026-09-21** — bằng hành vi + xác minh độc lập (DB-18); repo: `github.com/htvloc233/pb06-contract-ai` |
| D11 role mapping | ✅ **PASS 2026-09-21** — `DECISION-D11-PB06.md` duyệt nguyên trạng (DB-19) |
| N6 Architecture Review + contract LOCK | ✅ **PASS 2026-09-21** — PM kiêm Tech Lead qua cổng [3] có chấm (DB-20); ARCH **v1.5 Approved**, §4 **LOCKED**, D4+D5 lật theo G8 |
| Vào bước [8] BUILD | 🔒 Khoá theo luật tiền-đề DOR — **🔴 sạch · 🟠 còn 4:** D8 staging *(solo: docker-compose local, ghi quyết định như D11)* · D9 egress spike *(0.5 buổi → job `egress-test`)* · D10 synthetic *(AI nháp được — Delegation #13)* · D12 worker *(chốt A/B/C, 15 phút)*. Mỗi mục lật = một PR |

---

## Việc treo

1. ~~Sign-off SCOPE v3.2 + SPEC v1.1~~ — ✅ **xong 2026-09-06**, cổng [2] và lối vào bước [3] đã mở.
2. ~~PM Review Log~~ — ✅ **11/11 dòng có phán quyết** (tuyên bố trong phiên 2026-09-06); còn ký tay khi in hồ sơ viva.
3. **`OI-01`** — external parties có cần truy cập không. Owner: Product Owner. Hạn: trước Sprint 0.
4. **`OI-02`** — được gửi hợp đồng ra LLM API ngoài không. Owner: Legal/Security. Hạn: trước Sprint 0. ⚠️ Kéo theo hồ sơ đánh giá tác động chuyển dữ liệu ra nước ngoài — **có deadline pháp lý riêng, không đợi lịch dự án**. *(ARCH không bị chặn nhờ D5, nhưng Sprint 0 thì có.)*
5. **B4 — owner cho bộ đánh giá + gold set** (DB-11). ❗ **Vẫn chưa có tên.** PM chỉ định; móc vào WBS ở bước [4]. Chưa có owner thì go/no-go *"trích đúng ở mức người duyệt chấp nhận"* không đo được.
6. **Đo chi phí neo-theo-câu ở Slice 1b** (bước [8]). DoD-1 (<30s p95) và D6-b cạnh tranh cùng ngân sách. Đòn bẩy đã chốt: rút tóm tắt ~200 → ~120 từ. *(ARCH không bị chặn nhờ D5, nhưng Sprint 0 thì cần OI-02.)*

---

*DEVBOOK-PB06 · cập nhật cùng nhịp với việc làm, không viết bù sau. Ô `[PM tự điền]` do PM điền — AI không suy đoán giờ thật hay số lần override.*
