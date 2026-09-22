# MANIFEST-SYNTH-PB06 — Bộ 5 hợp đồng synthetic + Answer Key
### Nhiên liệu hợp pháp cho pipeline khi OI-02 chưa chốt · lật DoR **D10** (task W1-06)

> **Phiên bản:** 1.0 · **Ngày:** 2026-09-21 · **Trạng thái:** `draft_ai` — **chờ PM review** (Delegation #13: AI-draft L2, PM kiểm từng bản)
> **Sinh bởi:** `gen_synth.py` (kèm trong gói) — chạy lại script = tái tạo đúng bộ này ⇒ **chứng minh được là dữ liệu giả 100%**
> **Đã máy-kiểm:** text-layer thật (pdfplumber đọc được word-level offset) · mọi giá trị answer key khớp **verbatim** trong PDF · HD-04 đạt 19 trang (dải chuẩn đo ~20 của DoD-1)

---

## 1. Thiết kế bộ — mỗi hợp đồng kiểm MỘT thứ

| File | Trang | Kiểm cái gì | Neo |
|---|:-:|---|---|
| `HD-01-bao-tri-phan-mem.pdf` | 2 | **Happy-path chuẩn** — 2 bên, đủ 6 trường rõ ràng. Nhiên liệu Slice 1 | AC-15-1a |
| `HD-02-lien-danh-trien-khai.pdf` | 2 | **Đa giá trị + đa đoạn** — 4 bên liên danh; phạt nằm ở 3 điều khác nhau (Đ4 · Đ6 · Đ7) | AC-05-4, items |
| `HD-03-bay-notfound-uncertain.pdf` | 2 | **Bẫy trạng thái** — không có ngày hết hạn (→`not_found`); 3 con số tiền cạnh tranh (→`uncertain`) | §3.0 SPEC |
| `HD-04-dai-20-trang-chuan-do.pdf` | 19 | **Chuẩn đo p95** Slice 1b (DoR-1b B2) — bảng 120 hạng mục + 3 phụ lục | DoD-1, W1-22 |
| `HD-05-song-ngu-vi-en.pdf` | 2 | **Song ngữ VI/EN xen kẽ + ngoại tệ USD** — nhiên liệu sớm cho F-01/US-16 | AC-16-3 |

## 2. Answer Key — kỳ vọng của validator (mini gold set)

### HD-01 · Số 01/2026/HĐDV-MV-AB
| Trường | Kỳ vọng | Trạng thái |
|---|---|---|
| ① Các bên | CÔNG TY TNHH GIẢI PHÁP PHẦN MỀM MẪU VIỆT · CÔNG TY CỔ PHẦN THƯƠNG MẠI THỬ NGHIỆM AN BÌNH (2 items) | grounded |
| ② Hiệu lực | 01/03/2026 | grounded |
| ③ Hết hạn | 28/02/2027 | grounded |
| ④ Giá trị | 480.000.000 đồng | grounded |
| ⑤ Phạt | 1 đoạn (Điều 4): 0,05%/ngày chậm, trần 8% | grounded |
| ⑥ Tóm tắt | Dữ kiện phải neo được: dịch vụ bảo trì · 2 bên · 480tr · 01/03/2026→28/02/2027 | grounded |

### HD-02 · Số 07/2026/HĐHT-LD
| Trường | Kỳ vọng | Trạng thái |
|---|---|---|
| ① Các bên | **4 items** (A · B1 · B2 · B3) — cắt còn 1 chuỗi gộp = FAIL AC-05-4 | grounded |
| ②/③ | 15/04/2026 · 15/10/2027 | grounded |
| ④ Giá trị | 2.750.000.000 đồng | grounded |
| ⑤ Phạt | **3 items**: Đ4 chậm tiến độ (0,1%/tuần, trần 10%) · Đ6 bảo mật (200.000.000 đ/lần) · Đ7 chấm dứt trước hạn (5% phần chưa thực hiện) — thiếu bất kỳ item nào = FAIL | grounded |

### HD-03 · Số 12/2026/HĐTC-HP-DB — hợp đồng BẪY
| Trường | Kỳ vọng | Trạng thái |
|---|---|---|
| ② Hiệu lực | 05/05/2026 (ngày ký, ghi rõ) | grounded |
| ③ Hết hạn | **KHÔNG TỒN TẠI** — văn bản chỉ nói *"chấm dứt khi hai bên hoàn thành toàn bộ nghĩa vụ"* | **`not_found`** — trả bất kỳ ngày nào = model bịa |
| ④ Giá trị | **3 ứng viên cạnh tranh**: tạm tính 1.200.000.000 · tạm ứng 360.000.000 · bảo lãnh 60.000.000 | **`uncertain`** (nhiều ứng viên — đúng định nghĩa §3.0); chọn thẳng 1 số không cảnh báo = FAIL |
| ⑤ Phạt | 1 đoạn (Đ4): 0,08%/ngày trên giá trị *tạm tính*, trần 8% | grounded |

### HD-04 · Số 25/2026/HĐCC-KM — chuẩn đo
④ 5.640.000.000 đồng · ② 01/06/2026 · ③ 31/05/2028 · ⑤ **2 items** (Đ4 tiến độ 0,05%/ngày trần 10% · Đ5 SLA 1%/điểm thiếu hụt) · dùng cho **W1-22 đo p95**, không dùng làm bài dễ cho accuracy.

### HD-05 · Số 31/2026/HĐTV-SN — song ngữ
④ **25.000 USD** (kiểm đơn vị ngoại tệ — trả "25.000 đồng" = FAIL parse) · ② 10/07/2026 · ③ 09/07/2027 · ⑤ 1 item (Đ4: 10.000 USD/lần vi phạm bảo mật) · đoạn EN in nghiêng xen kẽ — pipeline không được crash (AC-16-3).

## 3. Noise CỐ Ý — đừng "sửa" chúng

- **Tên công ty bị xuống dòng** giữa chữ (vd "AN / BÌNH") — thực tế của mọi PDF; pipeline phải ghép được, đây là feature của bộ test.
- **Footer marker lặp mỗi trang** ("TÀI LIỆU TỔNG HỢP (SYNTHETIC)…") — vừa là tem an toàn chống nhầm với tài liệu thật, vừa là bài kiểm: câu này **không được lọt vào tóm tắt** hay bất kỳ trường nào.
- Mọi MST dạng `09090000xx`, địa chỉ "Đường Kiểm Thử / Phường Dữ Liệu Mẫu / Quận Ví Dụ / Thành phố Giả Định", tên người mang từ khoá test (Mẫu, Thử Nghiệm, Demo, Sandbox, Fixture, Placeholder, Sampleton) — **cố ý lộ liễu** để không ai nhầm là thật.

## 4. Checklist PM review — tick đủ 5 thì D10 lật PASS

| ✔ | Kiểm | Cách |
|---|---|---|
| ☐ | Không mảnh dữ liệu thật nào (tên, MST, địa chỉ, số tiền quen) | Mở lướt 5 PDF; đối chiếu mục 3 |
| ☐ | Answer key khớp file | Chọn xác suất 2 hợp đồng, dò 6 trường với §2 *(máy đã kiểm verbatim toàn bộ — đây là kiểm chéo của người)* |
| ☐ | HD-04 đủ dài cho phép đo (19 trang, có bảng + phụ lục) | Mở file, kéo tới Phụ lục C |
| ☐ | Marker synthetic hiện diện mọi trang | Nhìn footer |
| ☐ | Bộ phủ đúng 4 lớp kiểm: happy · đa giá trị/đa đoạn · trạng thái bẫy · dài + song ngữ | Bảng §1 |

## 5. Sau khi duyệt

Commit vào repo: thư mục **`data/synthetic/`** (5 PDF + manifest này + `gen_synth.py`) qua một vòng PR — message gợi ý: `data: bo 5 hop dong synthetic + answer key, lat D10 (DB-21)`. Báo phán quyết để lật D10 trong DOR và ghi Dev Book.

---

*MANIFEST-SYNTH-PB06 v1.0 · answer key này đồng thời là bộ test đầu vào cho validator W1-13/W1-20 — hợp đồng nào validator trả khác kỳ vọng ở đây là có chuyện để điều tra, ở validator hoặc ở chính answer key.*
