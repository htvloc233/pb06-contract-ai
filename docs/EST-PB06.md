# EST-PB06 — Estimation 3-Point & Kết luận khả thi (MVP)
### AI Tóm Tắt & Trích Xuất Hợp Đồng

> **Phiên bản:** 1.1 · **Ngày:** 2026-09-06
> **Input:** `WBS-PB06.md` **v1.1** (có hiệu lực) · `SCOPE-PB06.md` **v3.2** · `SPEC-PB06.md` **v1.1** · `MODULEMAP-PB06.md` **v1.2** · `ARCH-PB06.md` **v1.4**
> **Trạng thái:** ✅ **Có hiệu lực** — đã qua cổng hiểu bước [5] ngày 2026-09-06, qua sạch cả hai vế (hồ sơ: `DEVBOOK` DB-15)
> **Nguồn hiệu chuẩn phụ:** fragment EST tham khảo của một team khác cùng đề (cây WBS khác — **không bê số theo task**; chỉ dùng 2 bài học meta, gắn nhãn `[hiệu chuẩn từ EST tham khảo — fragment]`)
> Artefact bước **[5] Estimation** · Capstone Playbook · drill EX-03

---

## 0. Changelog

| Version | Ngày | Nội dung |
|---|---|---|
| **1.1** | 2026-09-06 | Sửa theo phán quyết của PM tại cổng hiểu [5] (`DEVBOOK` DB-15): **W1-03 bị bác đúng** — giả định "đã đặc tả sẵn ở ARCH" xích vào N6 (Architecture Review chưa xong) mà không định giá rủi ro. Nới đuôi P 2.5→3.5 (PERT 1.58→**1.75**), giả định viết lại nối N6, thêm **G8**. Tổng: PERT 78.7→78.9 · tổng cần 94.5→**94.7 MD** — kết luận khả thi-có-điều-kiện **không đổi**. |
| **1.0** | 2026-09-06 | Bản đầu: 3-point toàn bộ W1-01→23 · F-01→09 · E-01→04; reserve tích hợp 20% theo wave; kiểm tải theo người; kết luận **khả thi có điều kiện** + 2 trigger cắt định trước; giải bài 26-vs-62 MD. Ước lượng độc lập — chưa nhìn số theo-task của bản tham khảo. |

---

## 1. Phương pháp & giả định nền

**Công thức:** PERT = (O + 4M + P) / 6, đơn vị **MD** (man-day, ngày công một người).

**Giả định nền — sai cái nào thì tính lại từ đầu:**

| # | Giả định | Nếu sai |
|---|---|---|
| G1 | Hệ số hiệu dụng **80%**: mỗi người 4 MD hiệu dụng/tuần (trừ họp, review, điều phối) | Tổng capacity đổi tuyến tính |
| G2 | Capacity: Wave 1 = 3 tuần × 4 người × 4 = **48 MD** · Wave 2 = **48 MD** · Wave 3 = **32 MD** · tổng **128 MD** | — |
| G3 | Không ai bị rút giữa chừng (A7 của SCOPE) | Mở lại scope theo A7 |
| G4 | BE viết được Python ở mức nhận W1-11 (egress guard là hạ tầng config/network, AI review) | AI quay lại 114% Wave 1 → trượt lịch |
| G5 | Staging sẵn sàng từ Sprint 1; không tính công dựng hạ tầng mới (dùng hạ tầng SaaS — D1) | Thêm 3–5 MD BE |
| G6 | Gold set đợt 1 (10 HĐ) về đúng tuần 2 (N4) | F-02 benchmark + F-06 trượt theo, ngoài kiểm soát team |
| G7 | Số ở đây là **draft_ai** — PM phải thách thức tại cổng hiểu [5] trước khi dùng cho cam kết — ✅ đã xảy ra (DB-15) |
| G8 | ARCH v1.4 qua Architecture Review (N6) trong Sprint 0–1 **không đổi shape API**; contract chỉ LOCK sau review | Review đổi shape sau khi FE đã build trên contract → rework FE + kích hoạt đuôi P của W1-18 |

**Hai hiệu chuẩn từ bên ngoài** — nguồn: fragment EST của team khác cùng đề:

- `[hiệu chuẩn từ EST tham khảo — fragment]` **Reserve tích hợp/ổn định = 20% task effort, gắn theo TỪNG wave** — không dồn một cục cuối. Bản tham khảo tự thú *"buffer tích hợp không có trong WBS — khoảng sót lớn nhất"*; WBS v1.1 của ta thủng đúng chỗ đó (chỉ có W1-18 một ngày + E-05 cục cuối).
- `[hiệu chuẩn từ EST tham khảo — fragment]` **Đuôi bi quan P/O = 3.5–4×** cho lớp task *grounding validator* và *hội tụ tích hợp* — team đi trước ghi nhận P/O 3.7–4× thực tế ở đúng hai lớp này. Áp cho **W1-13 · W1-20 · W1-18** (và E-01).

---

## 2. Wave 1 — 3-point theo task (Sprint 0–2)

> Mỗi con số có giả định. **Estimate không giả định = estimate bị bác** (EX-03).

### Sprint 0

| ID | O | M | P | **PERT** | Owner | Giả định sau con số |
|---|---:|---:|---:|---:|---|---|
| W1-01 | 0.25 | 0.5 | 1.0 | **0.54** | PM+BE | 1 buổi làm việc đủ để team SaaS chốt tên role; P = họ đòi họp lần 2 |
| W1-02 | 1.5 | 2 | 3.5 | **2.17** | BE | Permission model SaaS là role-based đơn giản; P = có ACL theo từng hợp đồng phải map thêm |
| W1-03 | 1.0 | 1.5 | **3.5** | **1.75** | BE | ⚠️ *Sửa theo PM bác tại cổng [5]:* đặc tả 12 endpoint nằm ở ARCH v1.4 **chưa qua review (N6)** — P = review đổi shape (`items[]`/`sentences[]` là phần mới, dễ bị mổ) → một phần thành thiết kế lại. Skeleton làm ngay; **LOCK contract chỉ sau N6** (G8) |
| W1-04 | 1.5 | 2 | 3.5 | **2.17** | BE | 8 bảng đã có ERD; P = review A+ trả về sửa constraint ≥1 vòng |
| W1-05 | 0.75 | 1 | 2 | **1.13** | BE | Postgres trigger append-only là mẫu chuẩn; P = SaaS có RLS riêng phải hoà giải |
| W1-06 | 0.25 | 0.5 | 1 | **0.54** | PM | 5 HĐ synthetic soạn bằng template, không cần đa dạng ngay |
| W1-07 | 0.25 | 0.5 | 0.75 | **0.50** | PM | Chỉ tính công soạn + bám đuổi tuần đầu; chờ đợi không tính vào MD |
| W1-08 | 0.25 | 0.5 | 1 | **0.54** | PM | Pháp chế đồng ý cấp người trong 1 tuần (nếu không → G6 vỡ) |
| W1-09 | 0.25 | 0.5 | 1.5 | **0.63** | FE | Upload flow SaaS có tài liệu; P = phải mò bằng tay + hỏi team SaaS |
| **Cộng S0** | | | | **9.97** | | |

### Sprint 1

| ID | O | M | P | **PERT** | Owner | Giả định sau con số |
|---|---:|---:|---:|---:|---|---|
| W1-10 | 1.5 | 2 | 3.5 | **2.17** | AI | pdfplumber giữ được word-level bbox trên HĐ tiếng Việt chuẩn; P = font nhúng lỗi offset |
| W1-11 | 1.0 | 1.5 | 3.0 | **1.67** | **BE** *(san từ AI — G4)* | Whitelist ở config + proxy layer; P = hạ tầng SaaS không cho egress control ở app-level |
| W1-12 | 0.75 | 1 | 2.5 | **1.21** | AI | 3–5 vòng chỉnh prompt là đủ ổn cho trường ①; P = LLM variance trên tên tổ chức VN |
| W1-13 ⭐ | 1.5 | 2.5 | **5.5** | **2.83** | AI | `[hiệu chuẩn — fragment]` P/O 3.7×: verbatim match vướng normalize unicode/khoảng trắng tiếng Việt; transaction atomicity test mất nhiều vòng hơn dự kiến |
| W1-14 | 0.75 | 1 | 2 | **1.13** | BE | Tech Lead chốt option A (Celery); P = option B phải học job framework SaaS |
| W1-15 | 0.5 | 1 | 1.5 | **1.00** | FE | Component quyền đã có pattern trong SaaS |
| W1-16 | 1.0 | 1.5 | 2.5 | **1.58** | FE | Polling 2 nhánh timeout; P = state machine job phức tạp hơn khi thêm ca lỗi |
| W1-17 | 1.5 | 2 | 3 | **2.08** | FE | Ranh giới bản mỏng đã chốt (WBS v1.1) nên không mạ vàng; P = schema response đổi sau khi ARCH review |
| **Cộng S1** | | | | **13.67** | | |

### Sprint 2

| ID | O | M | P | **PERT** | Owner | Giả định sau con số |
|---|---:|---:|---:|---:|---|---|
| W1-18 ⭐ | 2 | 4 | **8** | **4.33** | cả team (AI 1.5 · BE 1.5 · FE 1.0 · PM 0.33) | `[hiệu chuẩn — fragment]` P/O 4× hội tụ tích hợp: lần đầu 6 module chạm nhau, mỗi mismatch contract = nửa ngày |
| W1-19 | 0.25 | 0.5 | 1.25 | **0.58** | AI | Prompt tóm tắt kế thừa ngữ cảnh W1-12 |
| W1-20 ⭐⭐ | 1.5 | 3 | **6** | **3.25** | AI | `[hiệu chuẩn — fragment]` P/O 4×: tách câu tiếng Việt + phát hiện "câu dữ kiện" chưa có lời giải đóng hộp; đây là **estimate kém chắc chắn nhất toàn dự án** |
| W1-21 | 0.75 | 1 | 2 | **1.13** | FE | Render sentences[] theo contract 4.5 đã chốt |
| W1-22 | 0.5 | 1 | 1.5 | **1.00** | AI+PM | Staging sẵn (G5) + HĐ ~20 trang chuẩn có trong bộ synthetic |
| **Cộng S2** | | | | **10.29** | | |

**Wave 1: PERT 33.9 MD** + reserve 20% = **6.8 MD** `[hiệu chuẩn — fragment]` → **40.7 MD** / capacity 48 MD = **85% đội**.

---

## 3. Wave 2 & Wave 3 — 3-point mức feature/epic

> Grain thô đúng rolling-wave; bẻ lại đầu Sprint 3 với số đo Slice 1b.

### Wave 2 (Sprint 3–5)

| ID | O | M | P | **PERT** | Owner chính | Giả định sau con số |
|---|---:|---:|---:|---:|---|---|
| F-01 | 4 | 6 | 10 | **6.33** | AI | Trường ②③④ dễ (đơn trị, parse kiểu); ⑤ đa đoạn + song ngữ EN chiếm nửa; P = hợp đồng song ngữ hai cột phá layout |
| F-02 | 3 | 5 | 9 | **5.33** | AI 3.5 · BE 1.8 | P/O 3× — chất lượng OCR trên gold set quyết; cần gold set đợt 1 (G6) |
| F-03 | 2 | 3 | 5 | **3.17** | FE | Thang S3 đã chốt ranh giới nên chỉ làm phần còn thiếu |
| F-04 | 3 | 4.5 | 7 | **4.67** | FE 3 · BE 1.7 | 4.8b + audit atomic; P = trạng thái edit trên đa giá trị phát sinh ca UI |
| F-05 | 2 | 3 | 4.5 | **3.08** | FE 2 · BE 1.1 | Version selector — không diff view |
| F-06 | 2 | 3 | 5 | **3.17** | AI 2 · PM 1.2 | Gold set ≥30 HĐ về trước S4 (G6); metric per-field + câu-không-neo |
| F-07 | 1.5 | 2 | 3 | **2.08** | FE | PM-only, CRUD đọc đơn giản |
| F-08 | 0.5 | 0.75 | 1.5 | **0.83** | PM (Legal làm chính) | Chỉ tính công PM; kích hoạt nếu OI-02 = external — deadline pháp lý ngoài lịch |
| F-09 | 2 | 3 | 5 | **3.17** | PM + cả team | **Thuế 0-QA**: PM soạn ca, dev chạy chéo; P = số ca negative phình khi F-01 xong |
| **Cộng W2** | | | | **31.8** | | + reserve 20% = 6.4 → **38.2 MD** / 48 = 80% đội |

### Wave 3 (Sprint 6–7)

| ID | O | M | P | **PERT** | Giả định |
|---|---:|---:|---:|---:|---|
| E-01 | 3 | 4 | 6 | **4.17** | `[hiệu chuẩn — fragment]` lớp tích hợp; egress + append-only test đã tự động từ Wave 1 nên chỉ chạy lại |
| E-02 | 2 | 2.5 | 4 | **2.67** | 5 user review sắp lịch được trong 1 tuần; **cần căn cứ dùng HĐ thật nội bộ** (nối OI-02) |
| E-03 | 2 | 3 | 5 | **3.17** | Đòn bẩy 120-từ đã kích hoạt từ Slice 1b nếu cần — không dồn sửa hiệu năng về đây |
| E-04 | 2 | 3 | 4.5 | **3.08** | RTM + Dev Book đã ghi dọc đường (không viết bù) — nếu viết bù thì con số này vô nghĩa |
| **Cộng W3** | | | | **13.1** | + reserve 20% = 2.6 → **15.7 MD** / 32 = 49% đội |

---

## 4. Tổng hợp & kiểm tải theo NGƯỜI — chỗ kết luận thật nằm ở đây

| | Wave 1 | Wave 2 | Wave 3 | Tổng |
|---|---:|---:|---:|---:|
| PERT | 33.9 | 31.8 | 13.1 | **78.9** |
| Reserve 20% `[hiệu chuẩn]` | 6.8 | 6.4 | 2.6 | **15.8** |
| **Tổng cần** | **40.7** | **38.2** | **15.7** | **94.7 MD** |
| Capacity (G1–G2) | 48 | 48 | 32 | **128 MD** |
| Tải đội | 85% | 80% | 49% | **74%** |

**Tổng đội nhìn ổn — nhưng tổng đội là con số đánh lừa.** Kiểm theo người:

| Người | W1 | /cap 12 | W2 | /cap 12 | Tổng /32 | Đọc số |
|---|---:|---:|---:|---:|---:|---|
| **AI engineer** | 12.0 *(sau khi san W1-11 → BE)* | **100%** | 11.8 | **98%** | **~84% + phần lớn reserve grounding** | **Critical path, zero slack hai wave liên tiếp.** Chưa san W1-11 thì W1 = 114% → trượt ngay trên giấy |
| BE | 11.3 | 94% | 4.6 | 38% | ~60% | Căng S0–S1, rảnh dần — người nhận reserve tích hợp |
| FE | 7.4 | 62% | 9.4 | 78% | ~65% | Đỉnh ở S4 (F-03+F-04) |
| PM | ~2.9 + N1–N6 | — | ~2.7 | — | — | Việc thật là điều phối phụ thuộc ngoài + thuế 0-QA (F-09) |

---

## 5. Kết luận khả thi (EX-03) — KHẢ THI CÓ ĐIỀU KIỆN, kèm trigger cắt định trước

**Kết luận:** 8 tuần **đạt được mà chưa phải cắt scope hôm nay** — 94.5/128 MD — **với 3 điều kiện cứng**:

1. **San tải AI → BE:** W1-11 chuyển BE (đã phản ánh trong bảng, ràng buộc G4); phần hạ tầng của F-02 (service OCR, queue) BE nhận. Không san thì AI 114% Wave 1 và kết luận đảo thành *không khả thi*.
2. **Bảo vệ lịch AI engineer:** hai wave liền ở ~100%, mọi lệch đuôi bi quan của W1-13/W1-20 ăn thẳng vào critical path. W1-20 không giao kèm việc khác (đã ghi WBS); pair AI–BE 1 buổi/tuần là truyền kiến thức chống SPOF, **không phải chia task để tăng throughput**.
3. **Phụ thuộc ngoài đúng hạn (G6, N1–N6):** gold set trễ 1 tuần → F-02 và F-06 trôi khỏi Wave 2 → dồn Wave 3 → vỡ.

**Hai trigger cắt — quyết trước, khỏi họp khẩn:**

| Trigger | Kích hoạt khi | Hành động đã chốt | Thủ tục |
|---|---|---|---|
| T1 | Slice 1b đo p95 > 30s (W1-22) | Rút tóm tắt ~200 → **~120 từ**; không nới D6-b | Trong thẩm quyền — đã chốt ở SCOPE v3.1/D6-b note |
| T2 | Hết Sprint 3 mà F-01 chưa xong 4 trường, hoặc AI vượt 110% hai tuần liên tiếp | Đề xuất **lùi tiếng Anh (US-16) sang phase 2** — MVP chỉ VI | ⚠️ **Chạm SCOPE §4 phạm vi ngôn ngữ ⇒ mở lại review scope** + sửa ngược SPEC US-16/NFR-L, WBS F-01. Change request soạn sẵn, chỉ chờ bắn |
| — | **Không bao giờ cắt** | Grounding (D6-a/b) · human gate (D3) · audit (DoD-5) — lõi giá trị | SCOPE E-05 |

> T2 chọn tiếng Anh chứ không chọn trường nào trong 6 trường: cắt trường chạm **D2** (6 trường cố định — nền của toàn bộ AC), còn ngôn ngữ là chiều mở rộng có đường lùi sạch (NFR-L3 vẫn giữ không-crash).

---

## 6. Giải bài 26-vs-62: WBS thô của ta 26 MD, team tham khảo 62.3 MD — ta có thiếu một nửa không?

**Không — nhưng ta đã thiếu ~35%, và bản EST này vá xong.** Truy từng lớp:

| Lớp | MD | Giải thích |
|---|---:|---|
| WBS v1.1 thô (tổng M) | ~26 | Điểm xuất phát |
| + Đuôi bi quan (3-point thay số trần) | +7.8 → 33.8 | Số M trần luôn lạc quan; PERT kéo đúng về giữa |
| + Reserve tích hợp 20% | +6.8 → 40.6 | `[hiệu chuẩn — fragment]` — đúng "khoảng sót lớn nhất" họ tự thú |
| + Overhead đã nằm trong hệ số 80% (G1), quy đổi | ~+9.6 → ~50 tương đương | Họ tính overhead vào task; ta trừ vào capacity — hai cách hạch toán, cùng bản chất |
| Chênh còn lại so với 62.3 | ~12 | Khác **cấu trúc**: đội 5 người (thêm giao tiếp), cây WBS khác (spike hạ tầng kiểu A06 mà ta không cần vì đứng trên SaaS sẵn — D1), và scope họ chưa xác minh phiên bản |

**Độ tin của lời giải: TRUNG BÌNH** — vế cuối dựa trên fragment, không thấy header + bảng task đầy đủ của họ. Nếu phần đầu bản tham khảo về được, diff theo lớp task sẽ nâng độ tin.

---

## 7. Top-3 ước lượng rủi ro nhất — nhìn kỹ trước khi tin

| # | Task | PERT | Vì sao kém chắc | Đối sách |
|---|---|---:|---|---|
| 1 | **W1-20** neo-theo-câu | 3.25 (P=6) | Tách câu tiếng Việt + định nghĩa "câu dữ kiện" chưa có lời giải chuẩn; variance LLM | Timebox 3 ngày → nếu chưa hội tụ: hạ heuristic v1 (mọi câu có số/ngày/tên = dữ kiện, over-flag chấp nhận được vì fail-closed an toàn về phía chặt) |
| 2 | **W1-18 / E-01** hội tụ tích hợp | 4.33 / 4.17 (P/O 4×) | Lần đầu 6 module chạm nhau; kinh nghiệm team tham khảo xác nhận 4× | Contract lock sớm (W1-03) + reserve nằm sẵn theo wave |
| 3 | **F-02** OCR | 5.33 (P=9) | Chất lượng scan thực tế chưa ai thấy; engine chưa benchmark | Benchmark trên gold set đợt 1 NGAY khi có (S3 đầu); best-effort đã là luật (AC-14-2) — không cam SLA |

---

## 8. Quick Reference — một trang cho stakeholder

| Metric | Giá trị |
|---|---|
| Tổng PERT | **78.9 MD** |
| Reserve tích hợp (20%/wave) `[hiệu chuẩn — fragment]` | **15.8 MD** |
| **Tổng cần** | **94.7 MD** |
| Capacity 8 tuần × 4 người × 80% | **128 MD** |
| Tải đội / tải AI engineer | 74% / **~100% hai wave đầu** |
| Kết luận | **Khả thi có điều kiện** — 3 điều kiện §5 |
| Trigger cắt | T1: p95>30s → tóm tắt 120 từ · T2: trượt S3 → lùi EN (mở scope review) |
| Không bao giờ cắt | Grounding · human gate · audit |
| Estimate kém chắc nhất | W1-20 (P/O 4×) |
| Phụ thuộc ngoài nguy nhất | Gold set (N4 — owner **vẫn chưa có tên** ❗) |

---

*EST-PB06 v1.0 · `draft_ai` — hiệu lực sau cổng hiểu bước [5]. Mọi con số có giả định đi kèm; con số nào bị phát hiện không có giả định → bác theo EX-03. Trigger T2 chạm SCOPE §4 ⇒ thủ tục mở lại scope, không tự áp.*
