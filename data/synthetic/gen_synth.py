# -*- coding: utf-8 -*-
"""Sinh 5 hợp đồng synthetic PB-06 (PDF text-layer, tiếng Việt) + MANIFEST answer key.
Tái lập được: chạy lại script = ra lại đúng bộ này. Mọi thực thể đều hư cấu có chủ đích."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))

OUT = "/home/claude/synthetic"
os.makedirs(OUT, exist_ok=True)

S  = ParagraphStyle("n", fontName="DV",  fontSize=10.5, leading=15, spaceAfter=6)
SB = ParagraphStyle("b", parent=S, fontName="DVB")
H1 = ParagraphStyle("h1", parent=SB, fontSize=14, alignment=1, spaceAfter=2)
H2 = ParagraphStyle("h2", parent=SB, fontSize=11.5, spaceBefore=10, spaceAfter=4)
CT = ParagraphStyle("ct", parent=S, alignment=1)

MARKER = ("TÀI LIỆU TỔNG HỢP (SYNTHETIC) — CHỈ DÙNG KIỂM THỬ PB-06 — "
          "KHÔNG CÓ GIÁ TRỊ PHÁP LÝ")

def footer(canv, doc):
    canv.saveState()
    canv.setFont("DV", 7.2)
    canv.setFillColor(colors.grey)
    canv.drawCentredString(A4[0] / 2, 10 * mm, MARKER)
    canv.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Trang {canv.getPageNumber()}")
    canv.restoreState()

def party_block(parties):
    out = []
    for i, p in enumerate(parties):
        out.append(Paragraph(f"<b>{p['vai']}: {p['ten']}</b>", SB))
        rows = [f"Mã số thuế: {p['mst']}", f"Địa chỉ: {p['dc']}",
                f"Đại diện: {p['dd']} — Chức vụ: {p['cv']}"]
        for r in rows:
            out.append(Paragraph(r, S))
        out.append(Spacer(1, 4))
    return out

def sign_table(parties):
    names = [Paragraph(f"<b>ĐẠI DIỆN {p['vai'].upper()}</b><br/><br/><br/><br/>{p['dd']}", CT)
             for p in parties]
    t = Table([names], colWidths=[(A4[0] - 40 * mm) / len(names)] * len(names))
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t

def build(fname, title, so, ngay_ky, parties, dieu_list, extra=None):
    doc = SimpleDocTemplate(os.path.join(OUT, fname), pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=20 * mm,
                            title=title, author="PB-06 Synthetic Generator")
    st = [Paragraph("CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM", CT),
          Paragraph("Độc lập - Tự do - Hạnh phúc", CT), Spacer(1, 8),
          Paragraph(title, H1), Paragraph(f"Số: {so}", CT), Spacer(1, 6),
          Paragraph(f"Hôm nay, ngày {ngay_ky}, tại Thành phố Giả Định, chúng tôi gồm:", S)]
    st += party_block(parties)
    st.append(Paragraph("Các bên thống nhất ký kết hợp đồng với các điều khoản sau:", S))
    for tt, paras in dieu_list:
        st.append(Paragraph(tt, H2))
        for p in paras:
            st.append(p if not isinstance(p, str) else Paragraph(p, S))
    if extra:
        st += extra
    st.append(Spacer(1, 16))
    st.append(sign_table(parties))
    doc.build(st, onFirstPage=footer, onLaterPages=footer)

DC = "Số {n}, Đường Kiểm Thử, Phường Dữ Liệu Mẫu, Quận Ví Dụ, Thành phố Giả Định"

# ================= HD-01 — happy path chuẩn =================
p1 = [dict(vai="Bên A (Bên thuê dịch vụ)", ten="CÔNG TY TNHH GIẢI PHÁP PHẦN MỀM MẪU VIỆT",
           mst="0909000001", dc=DC.format(n=1), dd="Nguyễn Văn Mẫu", cv="Giám đốc"),
      dict(vai="Bên B (Bên cung cấp dịch vụ)", ten="CÔNG TY CỔ PHẦN THƯƠNG MẠI THỬ NGHIỆM AN BÌNH",
           mst="0909000002", dc=DC.format(n=2), dd="Trần Thị Thử Nghiệm", cv="Tổng Giám đốc")]
build("HD-01-bao-tri-phan-mem.pdf", "HỢP ĐỒNG DỊCH VỤ BẢO TRÌ PHẦN MỀM",
      "01/2026/HĐDV-MV-AB", "20/02/2026", p1, [
    ("Điều 1. Đối tượng hợp đồng",
     ["Bên B cung cấp dịch vụ bảo trì, hỗ trợ vận hành hệ thống phần mềm quản lý bán hàng cho Bên A, bao gồm khắc phục lỗi, cập nhật bản vá bảo mật và hỗ trợ người dùng trong giờ hành chính."]),
    ("Điều 2. Giá trị hợp đồng và thanh toán",
     ["Tổng giá trị hợp đồng là <b>480.000.000 đồng</b> (Bằng chữ: bốn trăm tám mươi triệu đồng), đã bao gồm thuế giá trị gia tăng.",
      "Bên A thanh toán cho Bên B theo quý, mỗi quý 120.000.000 đồng, trong vòng 10 ngày làm việc kể từ ngày nhận hoá đơn hợp lệ."]),
    ("Điều 3. Thời hạn hợp đồng",
     ["Hợp đồng có hiệu lực từ ngày <b>01/03/2026</b> và hết hạn vào ngày <b>28/02/2027</b>.",
      "Trước khi hết hạn 30 ngày, hai bên có thể thoả thuận gia hạn bằng phụ lục."]),
    ("Điều 4. Phạt vi phạm",
     ["Trường hợp Bên B chậm khắc phục sự cố nghiêm trọng quá thời hạn cam kết, Bên B chịu phạt <b>0,05% giá trị hợp đồng cho mỗi ngày chậm</b>, tổng mức phạt không vượt quá <b>8% giá trị hợp đồng</b>."]),
    ("Điều 5. Bảo mật thông tin",
     ["Hai bên cam kết bảo mật toàn bộ thông tin, tài liệu trao đổi trong quá trình thực hiện hợp đồng và trong 24 tháng sau khi hợp đồng chấm dứt."]),
    ("Điều 6. Điều khoản chung",
     ["Mọi tranh chấp được giải quyết trước hết bằng thương lượng; nếu không thành, đưa ra Toà án có thẩm quyền tại nơi Bên A đặt trụ sở.",
      "Hợp đồng được lập thành 04 bản, mỗi bên giữ 02 bản có giá trị pháp lý như nhau."])])

# ================= HD-02 — đa giá trị (4 bên) + đa đoạn phạt (3 chỗ) =================
p2 = [dict(vai="Bên A (Bên giao thầu)", ten="CÔNG TY CỔ PHẦN ĐẦU TƯ HẠ TẦNG SỐ VÍ DỤ",
           mst="0909000003", dc=DC.format(n=3), dd="Lê Văn Ví Dụ", cv="Chủ tịch HĐQT"),
      dict(vai="Bên B1 (Thành viên đứng đầu liên danh)", ten="CÔNG TY TNHH CÔNG NGHỆ MẪU SỐ MỘT",
           mst="0909000004", dc=DC.format(n=4), dd="Phạm Thị Kiểm", cv="Giám đốc"),
      dict(vai="Bên B2 (Thành viên liên danh)", ten="CÔNG TY TNHH TÍCH HỢP HỆ THỐNG GIẢ LẬP",
           mst="0909000005", dc=DC.format(n=5), dd="Hoàng Văn Demo", cv="Giám đốc"),
      dict(vai="Bên B3 (Thành viên liên danh)", ten="CÔNG TY CỔ PHẦN DỊCH VỤ SỐ THỬ NGHIỆM MIỀN NAM",
           mst="0909000006", dc=DC.format(n=6), dd="Vũ Thị Sandbox", cv="Phó Giám đốc")]
build("HD-02-lien-danh-trien-khai.pdf", "HỢP ĐỒNG HỢP TÁC TRIỂN KHAI HỆ THỐNG QUẢN LÝ VẬN HÀNH",
      "07/2026/HĐHT-LD", "10/04/2026", p2, [
    ("Điều 1. Đối tượng và phạm vi",
     ["Liên danh Bên B1 - B2 - B3 (gọi chung là Bên B) thực hiện khảo sát, xây dựng và triển khai hệ thống quản lý vận hành cho Bên A tại 12 chi nhánh, theo phạm vi kỹ thuật tại Phụ lục 01."]),
    ("Điều 2. Giá trị hợp đồng",
     ["Tổng giá trị hợp đồng là <b>2.750.000.000 đồng</b> (Bằng chữ: hai tỷ bảy trăm năm mươi triệu đồng), đã gồm thuế và chi phí triển khai tại chỗ.",
      "Phân bổ nội bộ liên danh do các thành viên Bên B tự thoả thuận và không làm thay đổi trách nhiệm liên đới trước Bên A."]),
    ("Điều 3. Hiệu lực và thời hạn",
     ["Hợp đồng có hiệu lực từ ngày <b>15/04/2026</b> đến hết ngày <b>15/10/2027</b>."]),
    ("Điều 4. Tiến độ và phạt chậm tiến độ",
     ["Tiến độ chia 4 giai đoạn theo Phụ lục 02. Nếu Bên B chậm mốc nghiệm thu giai đoạn, Bên B chịu phạt <b>0,1% giá trị hợp đồng cho mỗi tuần chậm</b>, tổng không vượt quá <b>10% giá trị hợp đồng</b>."]),
    ("Điều 5. Trách nhiệm phối hợp",
     ["Bên A cung cấp mặt bằng, hạ tầng mạng và đầu mối nghiệp vụ tại từng chi nhánh trong 05 ngày làm việc kể từ khi nhận yêu cầu bằng văn bản."]),
    ("Điều 6. Bảo mật và phạt vi phạm bảo mật",
     ["Mỗi hành vi tiết lộ trái phép dữ liệu vận hành của Bên A cho bên thứ ba, bên vi phạm trong liên danh chịu phạt <b>200.000.000 đồng cho mỗi lần vi phạm</b> và bồi thường thiệt hại thực tế phát sinh."]),
    ("Điều 7. Chấm dứt trước hạn",
     ["Bên đơn phương chấm dứt hợp đồng không do lỗi của bên kia phải chịu phạt bằng <b>5% giá trị phần nghĩa vụ chưa thực hiện</b> tại thời điểm chấm dứt."]),
    ("Điều 8. Điều khoản chung",
     ["Hợp đồng lập thành 08 bản, mỗi bên giữ 02 bản. Tranh chấp giải quyết tại Trung tâm trọng tài thương mại (giả định) theo quy tắc tố tụng hiện hành của trung tâm."])])

# ============ HD-03 — bẫy: expiry not_found + contract_value uncertain ============
p3 = [dict(vai="Bên A (Chủ đầu tư)", ten="CÔNG TY TNHH SẢN XUẤT THIẾT BỊ MẪU HOÀ PHÁT GIẢ ĐỊNH",
           mst="0909000007", dc=DC.format(n=7), dd="Đỗ Văn Placeholder", cv="Giám đốc"),
      dict(vai="Bên B (Nhà thầu)", ten="CÔNG TY CỔ PHẦN XÂY LẮP DEMO ĐÔNG BẮC",
           mst="0909000008", dc=DC.format(n=8), dd="Bùi Thị Fixture", cv="Giám đốc")]
build("HD-03-bay-notfound-uncertain.pdf", "HỢP ĐỒNG THI CÔNG CẢI TẠO NHÀ XƯỞNG",
      "12/2026/HĐTC-HP-DB", "05/05/2026", p3, [
    ("Điều 1. Đối tượng hợp đồng",
     ["Bên B thi công cải tạo nhà xưởng số 2 của Bên A theo hồ sơ thiết kế đã được phê duyệt, bao gồm phần kết cấu, hoàn thiện và hệ thống điện chiếu sáng."]),
    ("Điều 2. Giá hợp đồng và tạm ứng",
     ["Giá trị hợp đồng <b>tạm tính là 1.200.000.000 đồng</b>; giá trị quyết toán cuối cùng xác định theo khối lượng thi công thực tế được nghiệm thu và đơn giá tại Phụ lục kèm theo.",
      "Bên A tạm ứng cho Bên B <b>360.000.000 đồng</b> trong 07 ngày kể từ ngày hợp đồng có hiệu lực.",
      "Bên B nộp bảo lãnh thực hiện hợp đồng giá trị <b>60.000.000 đồng</b> trước khi nhận tạm ứng."]),
    ("Điều 3. Hiệu lực và chấm dứt",
     ["Hợp đồng có hiệu lực kể từ ngày ký, <b>ngày 05/05/2026</b>.",
      "Hợp đồng <b>chấm dứt khi hai bên hoàn thành toàn bộ nghĩa vụ</b> và hoàn tất quyết toán, thanh lý; các bên không ấn định một ngày hết hạn cụ thể."]),
    ("Điều 4. Phạt vi phạm",
     ["Bên B chậm bàn giao so với tiến độ cam kết chịu phạt <b>0,08% giá trị tạm tính cho mỗi ngày chậm</b>, tổng mức phạt không vượt quá <b>8%</b>."]),
    ("Điều 5. An toàn lao động",
     ["Bên B chịu trách nhiệm toàn bộ về an toàn lao động, phòng chống cháy nổ trong phạm vi công trường và mua bảo hiểm theo quy định."]),
    ("Điều 6. Điều khoản chung",
     ["Hợp đồng lập thành 04 bản. Nội dung nào chưa quy định thì áp dụng quy định pháp luật hiện hành về xây dựng và dân sự."])])

# ================= HD-04 — dài ~20 trang (chuẩn đo p95) =================
p4 = [dict(vai="Bên A (Bên mua)", ten="TỔNG CÔNG TY VẬN HÀNH KHO MẪU GIẢ ĐỊNH",
           mst="0909000009", dc=DC.format(n=9), dd="Ngô Văn Chuẩn Đo", cv="Tổng Giám đốc"),
      dict(vai="Bên B (Bên cung cấp)", ten="CÔNG TY CỔ PHẦN GIẢI PHÁP KHO VẬN THỬ NGHIỆM TOÀN QUỐC",
           mst="0909000010", dc=DC.format(n=10), dd="Đinh Thị Hai Mươi Trang", cv="Giám đốc Dự án")]
dieu4 = [
    ("Điều 1. Đối tượng hợp đồng",
     ["Bên B cung cấp, lắp đặt và triển khai Hệ thống quản lý kho thông minh (gọi tắt là Hệ thống) cho Bên A tại Trung tâm phân phối Giả Định, gồm phần mềm lõi, 60 hạng mục thiết bị tại Phụ lục A và dịch vụ đào tạo chuyển giao."]),
    ("Điều 2. Giá trị hợp đồng",
     ["Tổng giá trị hợp đồng là <b>5.640.000.000 đồng</b> (Bằng chữ: năm tỷ sáu trăm bốn mươi triệu đồng), trọn gói, đã bao gồm thuế, phí vận chuyển và lắp đặt."]),
    ("Điều 3. Hiệu lực và thời hạn",
     ["Hợp đồng có hiệu lực từ ngày <b>01/06/2026</b> đến hết ngày <b>31/05/2028</b>, bao gồm 06 tháng triển khai và 18 tháng bảo hành - vận hành hỗ trợ."]),
    ("Điều 4. Phạt vi phạm tiến độ",
     ["Bên B chậm mốc nghiệm thu tổng thể chịu phạt <b>0,05% giá trị hợp đồng cho mỗi ngày chậm</b>, tổng mức phạt tối đa <b>10% giá trị hợp đồng</b>."]),
    ("Điều 5. Phạt vi phạm mức dịch vụ (SLA)",
     ["Trong giai đoạn vận hành hỗ trợ, nếu Hệ thống không đạt mức cam kết tại Phụ lục B trong một tháng bất kỳ, Bên B chịu phạt <b>1% giá trị dịch vụ tháng đó cho mỗi điểm phần trăm thiếu hụt</b>, khấu trừ trực tiếp vào kỳ thanh toán kế tiếp."]),
]
for i in range(6, 14):
    k=i-5
    dieu4.append((f"Điều {i}. Quy trình phối hợp phân hệ {k}",
        [f"Hai bên thành lập nhóm công tác số {k} phụ trách phân hệ tương ứng, gồm tối thiểu một trưởng nhóm, một cán bộ nghiệp vụ và một cán bộ kỹ thuật của mỗi bên; nhóm họp giao ban định kỳ vào thứ Ba hằng tuần tại văn phòng dự án hoặc trực tuyến, lập biên bản có xác nhận của trưởng nhóm hai bên và lưu trong hồ sơ dự án theo quy ước đặt tên thống nhất.",
         f"Mọi thay đổi phạm vi thuộc phân hệ {k} phải lập Phiếu yêu cầu thay đổi theo mẫu thống nhất, mô tả rõ hiện trạng, nội dung đề nghị, tác động tới tiến độ và chi phí; phiếu chỉ được thực hiện sau khi Giám đốc dự án hai bên phê duyệt, thời gian phản hồi không quá 05 ngày làm việc kể từ ngày tiếp nhận hợp lệ.",
         f"Tài liệu kỹ thuật của phân hệ {k} được bàn giao dưới dạng bản điện tử có kiểm soát phiên bản; mỗi lần cập nhật phải ghi rõ số phiên bản, ngày phát hành, người soạn và tóm tắt nội dung thay đổi; phiên bản mới thay thế toàn bộ phiên bản cũ sau khi bên nhận xác nhận tiếp nhận bằng văn bản hoặc thư điện tử có xác thực.",
         f"Sự cố phát sinh trong quá trình triển khai phân hệ {k} được phân loại theo ba mức nghiêm trọng, thông thường và ghi nhận; mỗi sự cố phải có mã theo dõi, người phụ trách, thời hạn xử lý và được rà soát trong cuộc họp giao ban gần nhất cho tới khi đóng.",
         f"Kết thúc mỗi giai đoạn, nhóm công tác số {k} lập báo cáo tổng kết nêu khối lượng đã hoàn thành, tồn đọng, rủi ro chuyển tiếp và kiến nghị; báo cáo là căn cứ để hai bên ký biên bản nghiệm thu giai đoạn của phân hệ tương ứng."]))
dieu4.append(("Điều 14. Điều khoản chung",
    ["Hợp đồng lập thành 06 bản, mỗi bên giữ 03 bản. Các Phụ lục A, B là bộ phận không tách rời của hợp đồng."]))
extra4 = [PageBreak(), Paragraph("PHỤ LỤC A — DANH MỤC HẠNG MỤC CUNG CẤP", H1), Spacer(1, 6)]
rows = [["STT", "Hạng mục", "Đơn vị", "SL", "Ghi chú kỹ thuật"]]
for i in range(1, 121):
    rows.append([str(i), f"Thiết bị mô phỏng loại {i:03d} phục vụ phân khu {((i-1)%12)+1}",
                 "bộ", str((i % 4) + 1),
                 f"Chuẩn kết nối nội bộ KV-{i:03d}, nguồn 220V/50Hz, kèm phụ kiện lắp đặt tiêu chuẩn, tài liệu hướng dẫn vận hành tiếng Việt và tem kiểm định xuất xưởng của nhà sản xuất giả định"])
tA = Table(rows, colWidths=[12*mm, 62*mm, 16*mm, 12*mm, 68*mm], repeatRows=1)
tA.setStyle(TableStyle([("FONTNAME", (0,0), (-1,-1), "DV"), ("FONTNAME", (0,0), (-1,0), "DVB"),
                        ("FONTSIZE", (0,0), (-1,-1), 8.6), ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
                        ("VALIGN", (0,0), (-1,-1), "TOP")]))
extra4.append(tA)
extra4 += [PageBreak(), Paragraph("PHỤ LỤC B — CAM KẾT MỨC DỊCH VỤ VẬN HÀNH", H1), Spacer(1, 6)]
for i in range(1, 13):
    extra4.append(Paragraph(f"B.{i}. Phân khu {i}", H2))
    extra4.append(Paragraph(
        f"Tỷ lệ sẵn sàng của phân hệ tại phân khu {i} không thấp hơn 99,0% tính theo tháng; "
        f"thời gian tiếp nhận sự cố không quá 30 phút trong giờ vận hành; thời gian khắc phục sự cố "
        f"mức nghiêm trọng không quá 08 giờ, mức thông thường không quá 24 giờ làm việc.", S))
    extra4.append(Paragraph(
        f"Báo cáo mức dịch vụ của phân khu {i} được Bên B gửi trước ngày 05 của tháng kế tiếp, kèm "
        f"nhật ký sự cố, thống kê thời gian phản hồi và biện pháp phòng ngừa tái diễn cho từng sự cố "
        f"đã ghi nhận trong kỳ; số liệu lấy từ hệ thống giám sát do hai bên thống nhất làm nguồn duy nhất.", S))
    extra4.append(Paragraph(
        f"Bảo trì định kỳ tại phân khu {i} thực hiện mỗi quý một lần ngoài giờ vận hành cao điểm, có "
        f"kế hoạch gửi trước tối thiểu 07 ngày; thời gian dừng hệ thống cho bảo trì định kỳ không tính "
        f"vào tỷ lệ sẵn sàng nếu không vượt quá 04 giờ cho mỗi kỳ bảo trì.", S))
    extra4.append(Paragraph(
        f"Trường hợp phân khu {i} phát sinh ba sự cố mức nghiêm trọng trở lên trong cùng một tháng, hai "
        f"bên tổ chức phiên rà soát chuyên đề trong 05 ngày làm việc để xác định nguyên nhân gốc, thống "
        f"nhất kế hoạch cải thiện và cập nhật ngưỡng cảnh báo sớm trên hệ thống giám sát; kết quả phiên "
        f"rà soát được ghi thành phụ lục nhật ký vận hành của phân khu và theo dõi tới khi hoàn tất.", S))
extra4 += [PageBreak(), Paragraph("PHỤ LỤC C — QUY TRÌNH NGHIỆM THU THEO PHÂN KHU", H1), Spacer(1, 6)]
for i in range(1, 13):
    extra4.append(Paragraph(f"C.{i}. Nghiệm thu phân khu {i}", H2))
    extra4.append(Paragraph(
        f"Việc nghiệm thu tại phân khu {i} tiến hành theo ba bước: kiểm tra tĩnh đối chiếu danh mục thiết "
        f"bị đã lắp đặt với Phụ lục A; chạy thử có tải trong tối thiểu 48 giờ liên tục với bộ kịch bản do "
        f"hai bên thống nhất trước; và đánh giá kết quả theo biểu mẫu nghiệm thu kèm số liệu ghi tự động "
        f"từ Hệ thống. Biên bản nghiệm thu phân khu {i} chỉ được ký khi toàn bộ hạng mục thuộc phân khu "
        f"đạt yêu cầu hoặc các tồn tại còn lại được hai bên thống nhất ghi thành danh mục khắc phục có "
        f"thời hạn; danh mục này phải được đóng trước thời điểm nghiệm thu tổng thể. Hồ sơ nghiệm thu của "
        f"phân khu {i} gồm biên bản, nhật ký chạy thử, ảnh chụp hiện trạng lắp đặt và xác nhận đào tạo "
        f"cho nhân sự vận hành tại chỗ của Bên A.", S))
    extra4.append(Paragraph(
        f"Trong 30 ngày sau nghiệm thu, phân khu {i} vận hành ở chế độ theo dõi tăng cường: Bên B bố trí "
        f"nhân sự hỗ trợ tại chỗ tối thiểu hai ngày mỗi tuần, tổng hợp các điều chỉnh cấu hình phát sinh "
        f"và bàn giao bộ tham số vận hành cuối cùng kèm hướng dẫn cập nhật cho Bên A trước khi kết thúc "
        f"giai đoạn theo dõi; các điều chỉnh trong giai đoạn này không tính là thay đổi phạm vi.", S))
build("HD-04-dai-20-trang-chuan-do.pdf", "HỢP ĐỒNG CUNG CẤP VÀ TRIỂN KHAI HỆ THỐNG QUẢN LÝ KHO THÔNG MINH",
      "25/2026/HĐCC-KM", "25/05/2026", p4, dieu4, extra=extra4)

# ================= HD-05 — song ngữ VI/EN xen kẽ =================
p5 = [dict(vai="Bên A / Party A (Khách hàng / Client)", ten="CÔNG TY TNHH TƯ VẤN CHUYỂN ĐỔI SỐ MẪU VIỆT NAM",
           mst="0909000011", dc=DC.format(n=11), dd="Lý Văn Song Ngữ", cv="Giám đốc"),
      dict(vai="Bên B / Party B (Nhà tư vấn / Consultant)", ten="SAMPLE GLOBAL ADVISORY PTE. LTD. (SINGAPORE - GIẢ ĐỊNH)",
           mst="REG-SG-000012-X (mã đăng ký giả định)", dc="01 Test Avenue, #00-00, Fictional Tower, Singapore 000000",
           dd="John Sampleton", cv="Director")]
build("HD-05-song-ngu-vi-en.pdf", "HỢP ĐỒNG DỊCH VỤ TƯ VẤN / CONSULTING SERVICES AGREEMENT",
      "31/2026/HĐTV-SN", "05/07/2026", p5, [
    ("Điều 1. Phạm vi dịch vụ / Article 1. Scope of Services",
     ["Bên B cung cấp dịch vụ tư vấn lộ trình chuyển đổi số cho Bên A trong 12 tháng, gồm đánh giá hiện trạng, xây dựng lộ trình và rà soát quý.",
      "<i>Party B shall provide digital transformation advisory services to Party A for twelve (12) months, including current-state assessment, roadmap development and quarterly reviews.</i>"]),
    ("Điều 2. Phí dịch vụ / Article 2. Fees",
     ["Tổng phí dịch vụ là <b>25.000 USD</b> (hai mươi lăm nghìn đô la Mỹ), chưa gồm thuế nhà thầu theo quy định của pháp luật Việt Nam, thanh toán thành 04 kỳ bằng nhau.",
      "<i>The total service fee is <b>USD 25,000</b>, exclusive of applicable withholding taxes under Vietnamese law, payable in four (4) equal instalments.</i>"]),
    ("Điều 3. Thời hạn / Article 3. Term",
     ["Hợp đồng có hiệu lực từ ngày <b>10/07/2026</b> và hết hạn vào ngày <b>09/07/2027</b>.",
      "<i>This Agreement takes effect on <b>10 July 2026</b> and expires on <b>09 July 2027</b>.</i>"]),
    ("Điều 4. Bảo mật và chế tài / Article 4. Confidentiality and Remedies",
     ["Mỗi hành vi vi phạm nghĩa vụ bảo mật, bên vi phạm phải trả khoản tiền phạt ấn định <b>10.000 USD cho mỗi lần vi phạm</b>, không loại trừ quyền yêu cầu bồi thường thiệt hại thực tế.",
      "<i>For each breach of confidentiality, the breaching party shall pay liquidated damages of <b>USD 10,000 per breach</b>, without prejudice to claims for actual damages.</i>"]),
    ("Điều 5. Luật áp dụng / Article 5. Governing Law",
     ["Hợp đồng được điều chỉnh bởi pháp luật Việt Nam; bản tiếng Việt được ưu tiên áp dụng khi có khác biệt.",
      "<i>This Agreement is governed by the laws of Vietnam; the Vietnamese version prevails in case of discrepancy.</i>"])])

print("Generated:", sorted(os.listdir(OUT)))
