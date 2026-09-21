# DELEGATION-MAP-PB06 — Bản đồ uỷ quyền AI (MVP)
### AI Tóm Tắt & Trích Xuất Hợp Đồng

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-06
> **Input:** `WBS-PB06.md` **v1.1** · `RISK-PB06.md` **v1.0** · `ARCH-PB06.md` **v1.4** · `CLAUDE.md` §3–§5 (thang L0–L5 Operating Model · Leash A/A+ · 3 luật cứng)
> **Trạng thái:** ✅ **Có hiệu lực** — đã qua cổng hiểu bước [6] ngày 2026-09-06 (hồ sơ: `DEVBOOK` DB-16)
> Artefact bước **[6b] Delegation Map** · Capstone Playbook · drill EX-06

**Cấu trúc hai tầng — không trộn:** §2 tầng **BUILD** (ai/AI được làm gì khi *xây* hệ thống — PM là người gỡ chốt) · §4 tầng **RUNTIME** (bản thân *sản phẩm* được để AI làm gì — khách hàng là người gỡ chốt). Câu kiểm nhanh cho mọi dòng: *"dòng này ai gỡ chốt — mình hay khách hàng của mình?"*

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.1** | 2026-09-06 | Sửa theo cổng hiểu [6] (`DEVBOOK` DB-16): **dòng #8 bị PM bắt thiếu đặc tả kênh bằng chứng** — thêm ràng buộc *artifact-của-runner là nguồn sự thật* + cấm AI sửa test/lint cùng lượt chạy, **giữ L4** (đổi kênh bằng chứng thay vì hạ mức — hạ L3 sẽ giết CI và đẻ rubber-stamping ở tầng review). Dòng #9 bổ sung lõi lý do A+: bất-khả-đảo-ngược + cổng máy không kiểm được ngữ nghĩa schema (tiền lệ DB-02). |
| **1.0** | 2026-09-06 | Bản đầu: tầng BUILD 18 task × (nhóm 5-loại · mức L · Leash · ai duyệt · lý do); §3 hai việc **cố tình giữ thấp** (EX-06 bước 3); tầng RUNTIME 7 hành vi kèm dòng L5-không-cấp. |

---

## 1. Quy ước

Thang **L0–L5** theo Operating Model (`CLAUDE.md` §3): L0 Observe · L1 Draft · L2 Recommend · L3 Execute-bounded · L4 Operate-workflow · L5 Restricted (**không cấp**). **Leash:** A = mặc định (≈L3, tự đóng khi cổng verify xanh) · A+ = chạm hazard (≈L4, BUILT-flagged chờ người). **Nhóm 5-loại:** `AI-do` · `Human-do` · `AI-review` · `Human-review` · `AI-KHÔNG-nên`. Ba luật cứng áp mọi dòng: không tự push/merge/release · không đụng secret/dữ liệu thật · không tự Done khi đang chờ duyệt.

---

## 2. TẦNG BUILD — 18 task (PM gỡ chốt)

| # | Task (nguồn WBS) | Nhóm 5-loại | Mức L | Leash | Ai duyệt | Lý do gán mức |
|---|---|---|:-:|:-:|---|---|
| 1 | Đọc & tóm tắt tài liệu SaaS hiện có, brief, ARCH | AI-do | **L0** | A | — | Chỉ-đọc, không đổi gì — vùng tự do nhất |
| 2 | Sinh code FE bảng kết quả S3 (W1-17, F-03) | AI-do + Human-review | **L3** | A | FE dev | Rủi ro thấp, test + review bắt được; sai thì sửa rẻ |
| 3 | Sinh skeleton controller Gateway (W1-03) | AI-do + Human-review | **L3** | A | BE | Khung theo spec đã có; LOCK contract vẫn chờ N6 (G8) |
| 4 | Sinh OpenAPI spec từ ARCH §4 | AI-do + Human-review | **L3** | BE | BE | Máy sinh từ nguồn đã duyệt — kiểm diff với ARCH |
| 5 | **Prompt + JSON schema trích xuất** (W1-12, W1-19, F-01) | AI-draft + Human-review | **L2** ⬇ | A | PM + AI eng | **Cố tình giữ thấp — xem §3.** Prompt là logic nghiệp vụ |
| 6 | Code validator D6-a/D6-b (W1-13, W1-20) | AI-do + Human-review | **L3** | A | AI eng; PM đọc test case | AI viết cổng thì **test của cổng phải do người duyệt nội dung** — cổng tự viết tự chấm là cổng giấy |
| 7 | Sinh unit/integration test | AI-do + Human-review | **L3** | A | Dev tương ứng | Bẫy "test giả" (assert true) — người kiểm test có *ý nghĩa*, không chỉ có *màu xanh* |
| 8 | Chạy bộ test + lint + egress test, báo kết quả | AI-do | **L4** | A | Spot-check + **artifact bắt buộc** | ⚠️ *Sửa theo PM bắt tại cổng [6]:* nguồn sự thật = **exit code + report do test runner sinh**, KHÔNG BAO GIỜ là lời tường thuật của AI — chặn "passed ảo"; **cấm AI sửa test/lint config trong cùng lượt chạy** (việc đó thuộc #7, người duyệt nội dung); spot-check đối chiếu report ↔ log định kỳ. Giữ L4 vì luồng lặp lại và hàng rào giờ nằm ở kênh bằng chứng, không nằm ở lời AI |
| 9 | Migration DB — 8 bảng + constraints (W1-04) | AI-draft + Human-review | **L1** | **A+** | Tech Lead + BE | Đổi schema = hazard theo luật cứng; BUILT-flagged chờ duyệt từng migration. *Lõi của A+ (chốt tại cổng [6]):* migration **gần như không đảo ngược rẻ** khi dữ liệu đã đổ vào, và **cổng máy không kiểm được ngữ nghĩa schema** — CHECK constraint xanh vẫn mô hình hoá sai được (tiền lệ DB-02) |
| 10 | Egress guard + whitelist config (W1-11) | AI-draft + Human-review | **L1** | **A+** | Security/Tech Lead | Ranh giới dữ liệu — B1 điểm 20; cấu hình sai một dòng là sự cố pháp lý |
| 11 | Cấu hình secret / API key / credential | **Human-do · AI-KHÔNG-nên** | **L0** | — | BE | Luật cứng #2 — AI không đụng, kể cả "chỉ đọc để debug" |
| 12 | Commit / push / merge / release | **Human-do · AI-KHÔNG-nên** | — | — | Dev | Luật cứng #1 — AI dừng ở bản nháp/PR dry-run |
| 13 | Soạn 5 hợp đồng synthetic (W1-06) | AI-draft + Human-review | **L2** | A | PM | AI nháp mẫu; PM kiểm **không chứa mảnh dữ liệu thật nào** — synthetic bẩn là B1 cửa sau |
| 14 | Gán nhãn gold set | **Human-do · AI-KHÔNG-nên** | **L0** | — | Pháp chế | Nguồn sự thật để chấm AI **không được do AI tạo** — thẩm định vòng tròn |
| 15 | Soạn hồ sơ ĐGTĐ chuyển dữ liệu (F-08) | AI-draft | **L1** | **A+** | Legal duy nhất | Văn bản pháp lý nộp cơ quan quản lý — người ký chịu trách nhiệm cá nhân |
| 16 | Weekly report + tổng hợp telemetry | AI-draft | **L2** | A | PM | Mọi số phải truy được nguồn; số không nguồn → `[THIẾU DỮ LIỆU]`, cấm lấp |
| 17 | Chẩn đoán lỗi tích hợp (W1-18, E-01) | AI-review (đề xuất chẩn đoán + fix) | **L2** | A | Dev liên quan | AI đề phương án, người chọn — lỗi tích hợp hay có nguyên nhân ngoài code |
| 18 | **Viết Dev Book** | **Human-do · AI-KHÔNG-nên** *(AI chỉ nhắc + giữ khung)* | **L0** | — | PM | Bằng chứng *người* hiểu — AI viết hộ là phá cơ chế đánh giá (CLAUDE.md §1). **Cố tình giữ thấp — xem §3** |

---

## 3. Hai việc CỐ TÌNH giữ thấp dù AI "làm được" *(EX-06 bước 3 — bài kiểm judgment)*

**① Prompt trích xuất giữ L2, không nâng L3/L4.** AI hoàn toàn *có thể* tự sinh prompt, tự chạy, tự chấm output tốt rồi tự tinh chỉnh — vòng lặp đó chạy được về kỹ thuật. Không cho, vì: prompt là nơi **định nghĩa nghiệp vụ** ("thế nào là một bên", "câu nào là dữ kiện") — để AI tự tối ưu là để AI tự định nghĩa đề bài rồi tự chấm mình theo định nghĩa đó; drift sẽ xảy ra êm ái, không có diff nào đỏ. Mỗi thay đổi prompt phải qua mắt người như thay đổi business rule.

**② Dev Book giữ L0 tuyệt đối.** AI viết Dev Book nhanh hơn, đủ hơn, đúng format hơn — và chính vì thế mà cấm: giá trị của Dev Book nằm ở chỗ nó *đắt* với người viết. Một Dev Book AI soạn là nhật ký hiểu bài do người-không-cần-hiểu viết hộ — đúng định nghĩa rubber-stamping, đóng gói đẹp.

---

## 4. TẦNG RUNTIME — hành vi của SẢN PHẨM (khách hàng gỡ chốt)

| # | Hành vi runtime | Mức L | Cổng đi kèm | Vì sao |
|---|---|:-:|---|---|
| R1 | Đọc PDF, trích text + metadata | **L3** | Không persist text thô (D4) | Trong ranh giới, không đổi dữ liệu nghiệp vụ |
| R2 | Sinh bản tóm tắt + trích 6 trường → `draft_ai` | **L1–L2** | D6-a/D6-b fail-closed; trạng thái do máy kiểm, không do model tự khai | Nháp có nguồn, người chốt |
| R3 | Gửi nội dung hợp đồng ra LLM endpoint | **L4** | Egress whitelist **mặc định đóng**; chỉ mở sau OI-02 + (nếu external) hồ sơ ĐGTĐ | Hazard dữ liệu — B1 |
| R4 | Ghi kết quả **đã người bấm "Xác nhận & Lưu"** vào hồ sơ | **L3** | Chỉ chạy sau human gate (D3); audit atomic | Máy thực thi *quyết định của người* |
| R5 | Vận hành cả luồng phân tích async (job → validate → lưu draft → thông báo) | **L4** | Hàng rào: validator + egress + audit; người duyệt ngoại lệ | Operate-workflow đúng nghĩa — trong lồng cổng |
| R6 | Tự gắn nhãn trạng thái trường (`grounded`/`uncertain`/`not_found`/`insufficient_grounding`) | **L3** | Quyết định bằng **kiểm tra cơ học** (span/parse), không phải phán đoán model (A6) | Nhãn là output của thuật toán kiểm, không phải của LLM |
| **R7** | **AI tự chốt một trường pháp lý thành `approved` không qua người** — kể cả confidence "Cao" | **L5 — KHÔNG CẤP** | — | Đây chính là lý do L5 tồn tại mà không bao giờ mở: một lần sai không ai kiểm là đủ mất trust (D3); và ngưỡng confidence không bao giờ là cổng (A6 v3.2) |

> Ranh giới nghề nghiệp của bảng này: mở R7 hay nâng R3 là **quyết định của khách hàng + Legal của họ**, không phải của team build — team chỉ được thiết kế sao cho *muốn mở cũng phải đi qua thủ tục*, không mở được bằng một cờ config lặng lẽ.

---

*DELEGATION-MAP-PB06 v1.0 · `draft_ai` — hiệu lực sau cổng hiểu bước [6]. Mọi đề nghị nâng mức L của bất kỳ dòng nào → ghi Dev Book + người có thẩm quyền tương ứng duyệt, không nâng bằng thoả thuận miệng.*
