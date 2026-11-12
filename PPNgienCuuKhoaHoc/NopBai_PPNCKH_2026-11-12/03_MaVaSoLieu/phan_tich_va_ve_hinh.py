"""Tái lập toàn bộ số liệu và ba hình của báo cáo giữa kỳ.

Chạy từ thư mục bất kỳ: python phan_tich_va_ve_hinh.py
Yêu cầu Python >= 3.10 và reportlab. Không huấn luyện mô hình.
Dữ liệu nguồn: ../TaiLieuNguon/data.csv, UCI 697, DOI 10.24432/C5MC89.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import platform
from collections import Counter

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "HinhVaSoLieu"
OUT.mkdir(exist_ok=True)
DATA = ROOT / "TaiLieuNguon/data.csv"
FONT = Path("C:/Windows/Fonts/arial.ttf")
BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
if not FONT.exists():
    FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("Chart", str(FONT)))
pdfmetrics.registerFont(TTFont("ChartBold", str(BOLD)))

with DATA.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    rows = [{k.strip(): v for k, v in row.items()} for row in reader]
    columns = [k.strip() for k in reader.fieldnames]

counts = Counter(row["Target"] for row in rows)
assert len(rows) == 4424
assert len(columns) == 37
assert counts == {"Graduate": 2209, "Dropout": 1421, "Enrolled": 794}
missing = sum(value.strip() == "" for row in rows for value in row.values())
duplicates = len(rows) - len({tuple(row.values()) for row in rows})
assert missing == 0
assert duplicates == 0

def wilson(k, n):
    """Khoảng Wilson hai phía 95%, z=1.959963984540054."""
    z = 1.959963984540054
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return center - half, center + half

def bin_label(value):
    if value == 0:
        return "0"
    if value <= 2:
        return "1–2"
    if value <= 5:
        return "3–5"
    return "≥6"

bins = []
for label in ["0", "1–2", "3–5", "≥6"]:
    selected = [row for row in rows if bin_label(int(row["Curricular units 1st sem (approved)"])) == label]
    c = Counter(row["Target"] for row in selected)
    k = c["Dropout"]
    n = len(selected)
    low, high = wilson(k, n)
    bins.append({"passed_units": label, "n": n, "dropout": k, "enrolled": c["Enrolled"],
                 "graduate": c["Graduate"], "proportion": k / n, "ci_low": low, "ci_high": high,
                 "dropout_excluding_enrolled": k / (n - c["Enrolled"])})
assert sum(x["n"] for x in bins) == len(rows)
assert sum(x["dropout"] for x in bins) == counts["Dropout"]
for name, records in [("phan_bo_nhan.csv", [{"label": key, "n": counts[key], "percent": counts[key] / len(rows) * 100} for key in ["Dropout", "Enrolled", "Graduate"]]), ("hinh_moi_so_lieu.csv", bins)]:
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

NAVY = HexColor("#173b58")
TEAL = HexColor("#167785")
ORANGE = HexColor("#b85c32")
GRAY = HexColor("#536272")
LIGHT = HexColor("#edf3f6")

def text(c, x, y, value, size=12, bold=False, color=NAVY, align="left"):
    c.setFillColor(color)
    c.setFont("ChartBold" if bold else "Chart", size)
    if align == "center":
        c.drawCentredString(x, y, value)
    elif align == "right":
        c.drawRightString(x, y, value)
    else:
        c.drawString(x, y, value)

def base(name, title, subtitle, height=470):
    c = canvas.Canvas(str(OUT / name), pagesize=(720, height))
    c.setTitle(title)
    c.setAuthor("Nhóm 4 – DCT123C4")
    c.setFillColor(white)
    c.rect(0, 0, 720, height, fill=1, stroke=0)
    text(c, 30, height - 35, title, 18, True)
    text(c, 30, height - 57, subtitle, 11, color=GRAY)
    return c

def box(c, x, y, w, h, title, lines):
    c.setFillColor(LIGHT)
    c.setStrokeColor(TEAL)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    text(c, x + 12, y + h - 23, title, 13, True)
    for i, line in enumerate(lines):
        text(c, x + 12, y + h - 46 - i * 18, line, 11)

def arrow(c, x1, y1, x2, y2):
    c.setStrokeColor(TEAL)
    c.setFillColor(TEAL)
    c.setLineWidth(1.5)
    c.line(x1, y1, x2, y2)
    angle = math.atan2(y2 - y1, x2 - x1)
    path = c.beginPath()
    path.moveTo(x2, y2)
    path.lineTo(x2 - 8 * math.cos(angle - 0.4), y2 - 8 * math.sin(angle - 0.4))
    path.lineTo(x2 - 8 * math.cos(angle + 0.4), y2 - 8 * math.sin(angle + 0.4))
    path.close()
    c.drawPath(path, fill=1, stroke=0)

c = base("hinh_1_quy_trinh.pdf", "Quy trình xây dựng bộ dữ liệu", "Vẽ lại Figure 1, trang 4 của Realinho và cộng sự (2022)", 560)
box(c, 30, 365, 315, 105, "1  Chuẩn bị dữ liệu tuyển sinh", ["CNAES: các tệp Access theo năm", "Trích xuất bằng VBA", "Đầu ra: competition.csv"])
box(c, 375, 365, 315, 105, "2  Chuẩn bị hồ sơ sinh viên", ["AMS: 13.992 dòng, 398 cột ban đầu", "Lọc hồ sơ, chọn và đổi tên thuộc tính", "Xử lý bằng Python"])
box(c, 375, 225, 315, 105, "3  Chuẩn bị kết quả học tập", ["Dữ liệu đánh giá từ AMS", "Tổng hợp các thuộc tính học kỳ 1 và 2", "Xử lý bằng Python"])
box(c, 30, 225, 315, 105, "Dữ liệu kinh tế vĩ mô", ["Nguồn PORDATA", "Thất nghiệp, lạm phát và GDP", "Thông tin bổ sung tại bước hợp nhất"])
box(c, 115, 70, 490, 115, "4  Hợp nhất và tiền xử lý", ["Ghép nguồn theo hồ sơ, xử lý bất thường và dữ liệu thiếu", "Ẩn danh và xác định nhãn tại cuối thời lượng khóa học", "Kết quả bài báo: 4.424 hồ sơ, 34 biến đầu vào và Target"])
arrow(c, 532, 365, 532, 330)
arrow(c, 345, 417, 375, 417)
arrow(c, 187, 225, 220, 185)
arrow(c, 532, 225, 500, 185)
text(c, 30, 32, "Sơ đồ khái quát do nhóm tái dựng; mũi tên thể hiện luồng dữ liệu, không phải thời gian xử lý.", 10, color=GRAY)
c.save()

c = base("hinh_2_phan_bo.pdf", "Phân bố ba trạng thái học tập", "Tính từ UCI 697; đối chiếu Figure 2, trang 7 của bài báo; N = 4.424")
for tick in range(0, 2501, 500):
    x = 175 + tick / 2500 * 465
    c.setStrokeColor(HexColor("#dce4e9"))
    c.line(x, 105, x, 370)
    text(c, x, 85, str(tick), 11, align="center", color=GRAY)
for i, (label, translation, color) in enumerate([("Dropout", "Bỏ học", ORANGE), ("Enrolled", "Còn theo học", GRAY), ("Graduate", "Tốt nghiệp", TEAL)]):
    y = 320 - i * 95
    text(c, 158, y + 15, label, 13, True, align="right")
    text(c, 158, y - 3, translation, 10, align="right", color=GRAY)
    c.setFillColor(color)
    c.rect(175, y, counts[label] / 2500 * 465, 35, fill=1, stroke=0)
    value = f"{counts[label]:,}  ({counts[label] / len(rows) * 100:.2f}%)".replace(",", ".").replace("49.93", "49,93").replace("32.12", "32,12").replace("17.95", "17,95")
    text(c, 185, y + 11, value, 12, True, white)
text(c, 410, 53, "Số hồ sơ sinh viên", 12, align="center")
text(c, 30, 20, "Nguồn: Realinho et al., Data 7(11), 146 (2022); UCI DOI 10.24432/C5MC89.", 10, color=GRAY)
c.save()

c = base("hinh_3_moi.pdf", "Tỷ lệ nhãn Dropout theo số học phần đạt", "Hình mới: kết quả học kỳ 1, tỷ lệ trong từng nhóm và khoảng Wilson 95%", 510)
for tick in range(0, 101, 20):
    y = 125 + tick / 100 * 285
    c.setStrokeColor(HexColor("#dce4e9"))
    c.line(85, y, 680, y)
    text(c, 70, y - 4, f"{tick}%", 11, align="right", color=GRAY)
for i, item in enumerate(bins):
    x = 150 + i * 155
    low_y = 125 + item["ci_low"] * 285
    high_y = 125 + item["ci_high"] * 285
    y = 125 + item["proportion"] * 285
    c.setStrokeColor(TEAL)
    c.setLineWidth(2)
    c.line(x, low_y, x, high_y)
    c.line(x - 9, low_y, x + 9, low_y)
    c.line(x - 9, high_y, x + 9, high_y)
    c.setFillColor(TEAL)
    c.circle(x, y, 5, fill=1, stroke=0)
    text(c, x, high_y + 13, f"{item['proportion'] * 100:.1f}%".replace(".", ","), 13, True, align="center")
    text(c, x, 101, item["passed_units"], 13, True, align="center")
    text(c, x, 80, f"{item['dropout']}/{item['n']} hồ sơ", 10, align="center", color=GRAY)
text(c, 380, 55, "Số học phần đạt trong học kỳ 1", 12, align="center")
text(c, 30, 30, "Tử số: Dropout; mẫu số: cả 3 nhãn trong nhóm. Đây là liên hệ mô tả, không phải nhân quả.", 10, color=GRAY)
text(c, 30, 13, "Nguồn: UCI 697. Khoảng Wilson không biểu diễn sai số đo, sai lệch chọn mẫu hay khả năng chuyển trường.", 9, color=GRAY)
c.save()

report = {"input_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(), "rows": len(rows), "columns": columns,
          "missing_cells": missing, "duplicate_rows": duplicates, "class_counts": dict(counts), "bins": bins,
          "majority_accuracy": counts["Graduate"] / len(rows), "python": platform.python_version(),
          "reportlab": reportlab.Version, "figure_sources": {"1": "paper Figure 1 p4", "2": "paper Figure 2 p7 and CSV", "3": "new CSV analysis"}}
(OUT / "kiem_tra_so_lieu.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: report[k] for k in ["rows", "missing_cells", "duplicate_rows", "class_counts", "bins", "majority_accuracy"]}, ensure_ascii=False, indent=2))
