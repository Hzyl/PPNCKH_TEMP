"""Ghép nội dung đã kiểm chứng vào bìa và cấu trúc mẫu chính thức."""
from pathlib import Path
from copy import deepcopy
import json
import re

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from midterm_content import TITLE, content, REFERENCES

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
MEMBERS = [("Lý Đức Huy", "3123411114"), ("Nguyễn Quốc Huy", "3123411120"),
           ("Trần Nam Khang", "3123411144"), ("Võ Quốc Khánh", "3123411151"), ("Lâm Trác Đạt", "3123411064")]
FINAL_STEM = "PPNCKH_" + "_".join(student_id for _, student_id in MEMBERS)
MID_STEM = "GiuaKy_Nhom4_DCT123C4"

def set_font(run, size=13, bold=None):
    run.font.name = "Times New Roman"
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.font.all_caps = False
    if bold is not None:
        run.bold = bold

def style_document(doc):
    for name, size, bold in [("Normal", 13, False), ("Title", 16, True), ("Heading 1", 14, True),
                             ("Heading 2", 13, True), ("Heading 3", 13, True), ("Caption", 11, False)]:
        style = doc.styles[name] if name in doc.styles else doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.all_caps = False
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Times New Roman")
        pf = style.paragraph_format
        pf.line_spacing = 1.08
        pf.space_after = Pt(5)
        if name.startswith("Heading"):
            pf.space_before = Pt(10)
            pf.keep_with_next = True
            pf.keep_together = True
            outline = OxmlElement("w:outlineLvl")
            outline.set(qn("w:val"), str(int(name[-1]) - 1))
            style.element.get_or_add_pPr().append(outline)
    doc.styles["Normal"].paragraph_format.widow_control = True
    doc.styles["Normal"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def clear_text(p, text, size, bold=False):
    p.clear()
    p.style = "Normal"
    outline = OxmlElement("w:outlineLvl")
    outline.set(qn("w:val"), "9")
    p._p.get_or_add_pPr().append(outline)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing = 1.1
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.keep_with_next = False
    pf.keep_together = True
    set_font(p.add_run(text), size, bold)

def base_document(term, title):
    doc = Document(WORK / "mau-bia.docx")
    style_document(doc)
    paragraphs = list(doc.paragraphs)
    # Giữ nguyên đoạn chứa khung VML của bìa; chỉ chỉnh các vùng chữ.
    values = {
        2: ("ỦY BAN NHÂN DÂN TP. HỒ CHÍ MINH", 15, False),
        3: ("TRƯỜNG ĐẠI HỌC SÀI GÒN", 16, True),
        6: ("BÁO CÁO " + term, 17, True),
        7: ("PHƯƠNG PHÁP NGHIÊN CỨU KHOA HỌC\nTRONG CÔNG NGHỆ THÔNG TIN", 16, True),
        10: (title.upper(), 16, True),
        15: ("NHÓM 4 – LỚP DCT123C4\n" + "\n".join(name + " – " + number for name, number in MEMBERS), 13, False),
        19: ("NGÀNH: CÔNG NGHỆ THÔNG TIN", 14, True),
        20: ("TRÌNH ĐỘ ĐÀO TẠO: ĐẠI HỌC", 14, True),
        29: ("TP. HỒ CHÍ MINH, THÁNG 10 NĂM 2026", 13, False)
    }
    # Không xóa phần tử hình/shape gốc của mẫu.
    spacers = {1: 26, 4: 16, 5: 28, 8: 18, 9: 18, 11: 25, 12: 18, 16: 28, 21: 32, 22: 32}
    for i, p in enumerate(paragraphs):
        if i in values:
            clear_text(p, *values[i])
        elif i == 0:
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(2)
        elif i in spacers:
            p.clear()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(spacers[i])
            set_font(p.add_run(""), 1)
        else:
            p._element.getparent().remove(p._element)
    doc.paragraphs[-1].paragraph_format.space_before = Pt(42)
    doc.core_properties.author = "Nhóm 4 – DCT123C4"
    doc.core_properties.title = title
    doc.core_properties.subject = "Phương pháp nghiên cứu khoa học trong Công nghệ thông tin"
    doc.core_properties.comments = ""
    doc.core_properties.last_modified_by = "Nhóm 4 – DCT123C4"
    for section in doc.sections:
        for footer in [section.footer, section.first_page_footer, section.even_page_footer]:
            for p in footer.paragraphs:
                p.clear()
    section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.6)
    section.left_margin = Cm(3)
    section.right_margin = Cm(1.5)
    section.header_distance = Cm(0.6)
    section.footer_distance = Cm(0.7)
    section.different_first_page_header_footer = False
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    for item in section._sectPr.findall(qn("w:pgBorders")):
        section._sectPr.remove(item)
    pg = section._sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        section._sectPr.append(pg)
    pg.set(qn("w:start"), "1")
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    p._p.append(field)
    return doc

def paragraph(doc, text, style=None):
    p = doc.add_paragraph(text, style=style)
    if style == "Caption":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_together = True
    return p

def table(doc, headers, rows, caption=None, template=None):
    if caption:
        p = paragraph(doc, caption, "Caption")
        p.paragraph_format.keep_with_next = True
    if template is None:
        t = doc.add_table(rows=1, cols=len(headers))
    else:
        el = deepcopy(template._element)
        doc._body._body.insert(len(doc._body._body) - 1, el)
        t = Table(el, doc._body)
        for row in list(t.rows)[1:]:
            t._tbl.remove(row._tr)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    n = len(headers)
    if n == 2:
        widths = [4.1, 12.4]
    elif n == 3:
        widths = [3.1, 5.8, 7.6]
    elif n == 5 and headers[0] == "STT":
        widths = [1.2, 3.1, 3.0, 7.9, 1.3]
    elif n == 5:
        widths = [3.1, 2.5, 2.5, 3.1, 5.3]
    elif n == 4 and "Thời gian" in headers:
        widths = [1.2, 6.8, 2.0, 6.5]
    elif n == 4 and headers[0] in ("STT", "TT"):
        widths = [1.2, 6.4, 5.6, 3.3]
    else:
        widths = [16.5 / n] * n
    for cell, value in zip(t.rows[0].cells, headers):
        cell.text = value
    for data in rows:
        cells = t.add_row().cells
        for cell, value in zip(cells, data):
            cell.text = str(value)
    for j, col in enumerate(t.columns):
        col.width = Cm(widths[j])
    props = t._tbl.tblPr
    borders = props.find(qn("w:tblBorders"))
    if borders is not None:
        props.remove(borders)
    borders = OxmlElement("w:tblBorders")
    for edge in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "A0A0A0")
        borders.append(e)
    props.append(borders)
    for i, row in enumerate(t.rows):
        trpr = row._tr.get_or_add_trPr()
        # Bỏ chiều cao cố định kế thừa của mẫu.
        for height in trpr.findall(qn("w:trHeight")):
            trpr.remove(height)
        trpr.append(OxmlElement("w:cantSplit"))
        if i == 0:
            trpr.append(OxmlElement("w:tblHeader"))
        for j, cell in enumerate(row.cells):
            cell.width = Cm(widths[j])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr = cell._tc.get_or_add_tcPr()
            margins = OxmlElement("w:tcMar")
            for edge in ["top", "bottom", "left", "right"]:
                x = OxmlElement("w:" + edge)
                x.set(qn("w:w"), "70")
                x.set(qn("w:type"), "dxa")
                margins.append(x)
            tcpr.append(margins)
            if i == 0:
                shade = OxmlElement("w:shd")
                shade.set(qn("w:fill"), "E7ECF0")
                tcpr.append(shade)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.keep_with_next = i == 0
                if j == 0 and headers[0] in ("STT", "TT"):
                    p.paragraph_format.first_line_indent = Cm(0)
                    p.paragraph_format.left_indent = Cm(0)
                    p.paragraph_format.right_indent = Cm(0)
                for r in p.runs:
                    set_font(r, 11.5, i == 0)
    paragraph(doc, "").paragraph_format.space_after = Pt(0)
    return t

def blocks(doc, items, templates=None, section=None):
    for block in items:
        kind = block["type"]
        if kind == "p":
            p = paragraph(doc, block["text"])
            if block["text"].startswith("Nhóm dùng khoảng Wilson"):
                p.paragraph_format.keep_together = True
        elif kind == "h":
            doc.add_heading(block["text"], level=block.get("level", 2))
        elif kind == "bullet":
            for item in block["items"]:
                paragraph(doc, "• " + item)
        elif kind == "table":
            source = None
            if templates and section in {"5", "13", "14"}:
                source = templates[{"5": 2, "13": 4, "14": 5}[section]]
            table(doc, block["headers"], block["rows"], block.get("caption"), source)
        elif kind == "figure":
            p = paragraph(doc, "")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.keep_together = True
            run = p.add_run()
            shape = run.add_picture(str(ROOT / "HinhVaSoLieu" / (block["name"] + ".png")), width=Cm(16.1))
            shape._inline.docPr.set("descr", block["caption"])
            paragraph(doc, block["caption"], "Caption")
        else:
            raise ValueError(kind)

def heading(doc, value, page_break=False):
    p = doc.add_heading(value, level=1)
    p.paragraph_format.page_break_before = page_break
    return p

def integrate_final(data):
    sections = data["sections"]
    # Cập nhật tổng quan bằng nguồn trong nước đã đọc đầy đủ tại root.
    sections["8"][1]["text"] = sections["8"][1]["text"].replace("công bố bộ dữ liệu và thực nghiệm phân loại kết quả học tập", "công bố bộ dữ liệu, phân tích khám phá và mức quan trọng của đặc trưng")
    sections["8"][-1] = {"type": "p", "text": "Trong nước, Nông Thị Hoa [3] so sánh mạng nơ-ron, Random Forest và SVM trên bộ UCI, báo cáo accuracy cao nhất 91,33%. Công trình gộp Enrolled với Graduate và mô tả nhân đôi lớp Dropout trước bước chia tập. Điều này gợi ra nguy cơ bản sao xuất hiện ở cả huấn luyện lẫn kiểm tra. Bài còn ghi 1.169 mẫu kiểm tra nhưng các ô ma trận của Random Forest cộng thành 1.754, nên chưa thể coi đây là mốc đối chứng trực tiếp. Đề tài kế thừa cách so sánh nhiều mô hình, đồng thời giữ ba nhãn trong phân tích chính, chỉ xử lý cân bằng trong huấn luyện và lưu chỉ số dòng để kiểm chứng. Công trình do tác giả trong nước thực hiện vẫn dùng dữ liệu nước ngoài; nó chưa chứng minh hiệu quả trên sinh viên Việt Nam."}
    sections["8"][-2]["text"] = sections["8"][-2]["text"].replace("Bài báo nền tảng và kho UCI là các nguồn đã xác định; tổng quan hiện tại chưa đủ để khẳng định mức độ phổ biến hoặc hiệu quả tại Việt Nam.", "Đối chiếu các công trình đã đọc cho thấy cần làm rõ giao thức và đối tượng đánh giá, thay vì chỉ so sánh trực tiếp các điểm accuracy khác cách chia tập hoặc định nghĩa nhãn.")
    sections["7"] = [{"type": "p", "text": "Cán bộ hướng dẫn theo phân công của học phần. Nội dung xin ý kiến gồm tính hợp lệ theo thời điểm của các biến, cách xử lý Enrolled và phương án đánh giá. Thông tin hành chính được kê khai khi đăng ký chính thức."}]
    sections["14"][-1]["text"] = "Cam kết của chủ nhiệm đề tài: kết quả thực hiện đề tài này không trùng lặp với sản phẩm, công trình khoa học khác đã công bố. Dữ liệu, thuật toán và các nghiên cứu nền tảng được trích dẫn; đóng góp dự kiến của nhóm nằm ở giao thức so sánh, thực nghiệm và phân tích. Phần ký cam kết chính thức do chủ nhiệm thực hiện sau khi thống nhất nội dung."
    sections["16"][-1]["text"] = "Dự toán sẽ được điều chỉnh theo số bản in và đơn giá thực tế khi nộp; khoản phát sinh cần được nhóm thống nhất. Các mục xác nhận dưới đây dành cho quy trình xét duyệt chính thức."
    sections["12"].insert(8, {"type": "p", "text": "Trong cấu hình chính, xử lý mất cân bằng bằng class_weight trong mô hình. Không nhân bản hoặc tổng hợp thêm hồ sơ ở tập xác thực hay kiểm tra. Nếu khảo sát lấy mẫu trong phần mở rộng, thao tác đó chỉ diễn ra trong tập huấn luyện của từng fold; số lượng và phân bố thật ở xác thực/kiểm tra được giữ nguyên."})
    data["references"][1] = "[2] V. Realinho, M. Vieira Martins, J. Machado, and L. Baptista, ‘Predict Students’ Dropout and Academic Success,’ UCI Machine Learning Repository, 2021, doi: 10.24432/C5MC89. Available: https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success. Accessed: Oct. 22, 2026."
    data["references"].append("[3] N. T. Hoa, ‘Ứng dụng các mô hình học máy vào dự đoán tình trạng bỏ học của sinh viên,’ TNU Journal of Science and Technology, vol. 230, no. 07, pp. 120–125, 2025, doi: 10.34238/tnu-jst.12201. Available: https://jst.tnu.edu.vn/jst/article/view/12201.")
    return data

def build_midterm():
    audit = json.loads((ROOT / "HinhVaSoLieu/kiem_tra_so_lieu.json").read_text(encoding="utf-8"))
    doc = base_document("GIỮA KỲ", TITLE)
    paragraph(doc, "Nội dung báo cáo", "Title")
    paragraph(doc, "Báo cáo gồm thông tin bài báo, phân tích nghiên cứu, hai hình tái tạo, một hình mới, phản biện và mã nguồn tái lập.")
    p = paragraph(doc, "")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), 'TOC \\o "1-1" \\h \\z \\u')
    p._p.append(field)
    for i, (name, items) in enumerate(content(audit)):
        heading(doc, name, i == 0 or name.startswith(("5 ", "6 ", "7 ")))
        blocks(doc, items)
    heading(doc, "Tài liệu tham khảo", True)
    for ref in REFERENCES:
        p = paragraph(doc, ref)
        p.paragraph_format.keep_together = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    heading(doc, "Phụ lục đối chiếu nguồn và số liệu", True)
    paragraph(doc, "Ảnh phần Subject Area and Category do nhóm cung cấp từ hồ sơ Data trên SCImago [6] được lưu tại TaiLieuNguon/scimago-subject-user.png. Ảnh này chỉ làm bằng chứng phân loại tạp chí; ba hình phân tích trong báo cáo đều được vẽ bằng mã nguồn.")
    p = paragraph(doc, "")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    shape = p.add_run().add_picture(str(ROOT / "TaiLieuNguon/scimago-subject-user.png"), width=Cm(8.0))
    shape._inline.docPr.set("descr", "Bằng chứng Subject Area and Category từ SCImago của Data")
    paragraph(doc, "SHA-256 của data.csv: " + audit["input_sha256"]).alignment = WD_ALIGN_PARAGRAPH.LEFT
    out = ROOT / "BaiGiuaKy"
    out.mkdir(exist_ok=True)
    doc.save(out / (MID_STEM + ".docx"))
    return out / MID_STEM

def build_final():
    data = integrate_final(json.loads((WORK / "final_sections.json").read_text(encoding="utf-8")))
    (WORK / "final_integrated.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    doc = base_document("CUỐI KỲ", data["title"])
    template = Document(ROOT / "TaiLieuNguon/mau-thuyet-minh.docx")
    header_el = deepcopy(template.tables[0]._element)
    doc._body._body.insert(len(doc._body._body) - 1, header_el)
    header = Table(header_el, doc._body)
    for row in header.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    set_font(r, 11)
                if "ngày" in p.text:
                    p.text = "Thành phố Hồ Chí Minh, tháng 10 năm 2026"
                    for r in p.runs:
                        set_font(r, 11)
    for value in ["THUYẾT MINH ĐỀ TÀI NGHIÊN CỨU KHOA HỌC", "CẤP TRƯỜNG CỦA SINH VIÊN"]:
        p = paragraph(doc, value, "Title")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
    paragraph(doc, "Đề cương nghiên cứu phục vụ học phần Phương pháp nghiên cứu khoa học trong Công nghệ thông tin.").alignment = WD_ALIGN_PARAGRAPH.CENTER
    labels = ["Tên đề tài", "Lĩnh vực nghiên cứu", "Thời gian thực hiện", "Chủ nhiệm đề tài", "Các thành viên tham gia thực hiện đề tài", "Mô tả năng lực nghiên cứu chủ nhiệm và các thành viên", "Cán bộ hướng dẫn sinh viên thực hiện đề tài", "Tình hình nghiên cứu liên quan đến đề tài", "Tính cấp thiết của đề tài", "Mục tiêu đề tài", "Đối tượng và phạm vi nghiên cứu", "Phương pháp nghiên cứu", "Nội dung nghiên cứu và tiến độ thực hiện", "Sản phẩm khoa học và công nghệ của đề tài", "Khả năng ứng dụng và phát triển của đề tài", "Kinh phí thực hiện đề tài NCKH của sinh viên"]
    for i, label in enumerate(labels, 1):
        heading(doc, str(i) + ". " + label, i in [5, 12])
        if i == 2:
            paragraph(doc, "☒ Khoa học Kỹ thuật và Công nghệ\n☐ Khoa học Tự nhiên    ☐ Khoa học Y, dược    ☐ Khoa học Nông nghiệp\n☐ Khoa học Xã hội    ☐ Khoa học Nhân văn").alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph(doc, "Loại đề tài: ☐ A1     ☐ B1     ☐ B2     ☐ C")
        blocks(doc, data["sections"][str(i)], template.tables, str(i))
        if i == 7:
            table(doc, ["Họ và tên", "Số ĐTDĐ", "Khoa", "Chữ ký"], [["Theo phân công", "", "Công nghệ thông tin", ""]], template=template.tables[3])
    heading(doc, "Các mục xác nhận theo mẫu", True)
    paragraph(doc, "Ngày …… tháng …… năm ……")
    signatures = deepcopy(template.tables[7]._element)
    doc._body._body.insert(len(doc._body._body) - 1, signatures)
    t = Table(signatures, doc._body)
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    set_font(r, 11)
    for _ in range(5):
        paragraph(doc, "")
    for value in ["XÁC NHẬN CỦA TRƯỜNG ĐẠI HỌC SÀI GÒN", "TL. HIỆU TRƯỞNG", "TRƯỞNG PHÒNG QUẢN LÝ KHOA HỌC", "(Ký và ghi rõ họ tên)"]:
        p = paragraph(doc, value)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading(doc, "Tài liệu tham khảo", True)
    for ref in data["references"]:
        p = paragraph(doc, ref)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_together = True
    heading(doc, "Phụ lục bảng quyết định về nhóm đặc trưng")
    table(doc, ["Cấu hình", "Biến được phép", "Vai trò"], [
        ["T0", "Application mode; Application order; Course; Daytime/evening attendance; Previous qualification; Previous qualification (grade); Admission grade; Age at enrollment", "8 biến tuyển sinh; cấu hình bảo thủ khóa trước thực nghiệm"],
        ["T1", "T0 và 6 biến Curricular units 1st sem: credited; enrolled; evaluations; approved; grade; without evaluations", "14 biến; so sánh thông tin hồi cứu bổ sung từ học kỳ 1"],
        ["Không dùng trong mô hình chính", "6 biến học kỳ 2; Debtor; Tuition fees up to date; Scholarship holder; các biến nhân khẩu/gia đình còn lại và kinh tế vĩ mô", "Tránh thông tin tương lai hoặc giả định thời gian chưa được kiểm chứng; giới hạn phạm vi"],
        ["Target", "Dropout; Enrolled; Graduate", "Chỉ làm nhãn; không đưa vào đầu vào"]
    ])
    paragraph(doc, "Đầu ra của đề cương là kế hoạch có thể kiểm chứng. Các mô hình, điểm số kiểm tra, bootstrap và sản phẩm nghiên cứu 12 tuần ở trên là công việc dự kiến; chưa có kết quả huấn luyện trong tài liệu này.")
    out = ROOT / "BaiCuoiKy"
    out.mkdir(exist_ok=True)
    doc.save(out / (FINAL_STEM + ".docx"))
    return out / FINAL_STEM

if __name__ == "__main__":
    stems = [build_midterm(), build_final()]
    (WORK / "report-stems.json").write_text(json.dumps([str(p) for p in stems], ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(str(p) + ".docx" for p in stems))
