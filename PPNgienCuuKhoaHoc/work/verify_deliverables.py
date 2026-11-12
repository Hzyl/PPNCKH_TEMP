"""Kiểm tra độc lập số liệu và cấu trúc tệp giao; không thay thế đọc ảnh từng trang."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import re

import pandas as pd
from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
checks = []


def check(name, condition):
    checks.append({"check": name, "passed": bool(condition)})
    if not condition:
        raise AssertionError(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((ROOT / "HinhVaSoLieu/kiem_tra_so_lieu.json").read_text(encoding="utf-8"))
data_path = ROOT / "TaiLieuNguon/data.csv"
df = pd.read_csv(data_path, sep=";")
df.columns = df.columns.str.strip()
check("CSV SHA-256 matches saved analysis", sha(data_path) == audit["input_sha256"])
check("4424 rows and 37 columns", df.shape == (4424, 37))
check("No missing cells or exact duplicate rows", not df.isna().any().any() and not df.duplicated().any())
check("Class counts agree with source Figure 2", df["Target"].value_counts().to_dict() == {"Graduate": 2209, "Dropout": 1421, "Enrolled": 794})
check("Majority accuracy", math.isclose(df["Target"].eq("Graduate").mean(), audit["majority_accuracy"]))
units = df["Curricular units 1st sem (approved)"]
check("Approved units are nonnegative integers", units.ge(0).all() and units.mod(1).eq(0).all())
groups = pd.cut(units, [-1, 0, 2, 5, float("inf")], labels=["0", "1–2", "3–5", "≥6"])
counts = pd.crosstab(groups, df["Target"])
csv_rows = pd.read_csv(ROOT / "HinhVaSoLieu/hinh_moi_so_lieu.csv").to_dict("records")
z = 1.959963984540054
for expected, csv_row in zip(audit["bins"], csv_rows):
    label = expected["passed_units"]
    observed = counts.loc[label]
    n = int(observed.sum())
    k = int(observed["Dropout"])
    p = k / n
    check(f"Group {label}: independently counted n and all three labels", all([
        n == expected["n"],
        k == expected["dropout"],
        int(observed["Enrolled"]) == expected["enrolled"],
        int(observed["Graduate"]) == expected["graduate"]
    ]))
    check(f"Group {label}: proportions including and excluding Enrolled", math.isclose(p, expected["proportion"]) and math.isclose(k / (n - observed["Enrolled"]), expected["dropout_excluding_enrolled"]))
    for bound_name in ["ci_low", "ci_high"]:
        bound = expected[bound_name]
        score_statistic = n * (bound - p) ** 2 / (bound * (1 - bound))
        check(f"Group {label}: {bound_name} solves score equation", math.isclose(score_statistic, z * z, rel_tol=1e-10))
    check(f"Group {label}: bounds bracket point estimate", 0 < expected["ci_low"] < p < expected["ci_high"] < 1)
    check(f"Group {label}: exported CSV agrees", all(csv_row[key] == value if isinstance(value, str) else math.isclose(csv_row[key], value) for key, value in expected.items()))

label_csv = pd.read_csv(ROOT / "HinhVaSoLieu/phan_bo_nhan.csv").set_index("label")
for label, count in df["Target"].value_counts().items():
    check(f"Distribution CSV {label}", label_csv.loc[label, "n"] == count and math.isclose(label_csv.loc[label, "percent"], count / len(df) * 100))

names = ["Lý Đức Huy", "Nguyễn Quốc Huy", "Trần Nam Khang", "Võ Quốc Khánh", "Lâm Trác Đạt"]
ids = ["3123411114", "3123411120", "3123411144", "3123411151", "3123411064"]
stems = json.loads((WORK / "report-stems.json").read_text(encoding="utf-8"))
outputs = []
for index, stem in enumerate(stems):
    stem = Path(stem)
    docx = stem.with_suffix(".docx")
    pdf = stem.with_suffix(".pdf")
    document = Document(docx)
    reader = PdfReader(pdf)
    pages = [page.extract_text() for page in reader.pages]
    text = " ".join(" ".join(pages).split())
    check(f"{stem.name}: 13 PDF pages", len(pages) == 13)
    check(f"{stem.name}: all names, IDs and class on cover", all(value in " ".join(pages[0].split()) for value in names + ids + ["DCT123C4"]))
    check(f"{stem.name}: no placeholder or field errors", all(value.lower() not in text.lower() for value in ["TODO", "TBD", "lorem ipsum", "Error! Reference", "Error! Bookmark", "\ufffd"]))
    check(f"{stem.name}: paper and dataset DOI present", "10.3390/data7110146" in text and "10.24432/C5MC89" in text)
    headings = [p.text for p in document.paragraphs if p.style.name == "Heading 1"]
    if index == 0:
        check("Midterm: 9 numbered main sections", [int(re.match(r"^(\d+) ", h).group(1)) for h in headings if re.match(r"^(\d+) ", h)] == list(range(1, 10)))
        check("Midterm: 3 charts and SCImago screenshot embedded", len(document.inline_shapes) == 4)
        check("Midterm: cached TOC excludes cover member names", "Tóm tắt" in pages[1] and not any(name in pages[1] for name in names))
        check("Midterm: SCImago categories and dated metric", all(value in text for value in ["Computer Science Applications", "Information Systems and Management", "Decision Sciences", "CiteScore năm 2019"]))
        for row in audit["bins"]:
            percent = f"{row['proportion'] * 100:.2f}%".replace(".", ",")
            check(f"Midterm: group {row['passed_units']} percentage present", percent in text)
    else:
        check("Final: 16 ordered official sections", [int(re.match(r"^(\d+)\.", h).group(1)) for h in headings if re.match(r"^(\d+)\.", h)] == list(range(1, 17)))
        check("Final: all five IDs in submission filename", all(value in stem.name for value in ids))
        check("Final: domestic primary source cited", "10.34238/tnu-jst.12201" in text)
        check("Final: planned work is explicitly distinguished from results", "chưa có kết quả huấn luyện" in text)
        check("Final: 12-week plan and funding", "12 tuần" in text and "150.000" in text)
    for path in [docx, pdf]:
        outputs.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path), "pdf_pages": len(pages) if path.suffix == ".pdf" else None})

check("Original article has 17 pages", len(PdfReader(ROOT / "TaiLieuNguon/paper.pdf").pages) == 17)
indexing = json.loads((WORK / "indexing-evidence.json").read_text(encoding="utf-8"))
check("SCImago evidence gap resolved with supplied image", indexing["scimago_field"]["status"] == "resolved_from_user_supplied_screenshot" and indexing["open_requirement"] is None)
check("Source screenshot retained", (ROOT / indexing["scimago_field"]["local_evidence"]).is_file())
for name in ["hinh_1_quy_trinh", "hinh_2_phan_bo", "hinh_3_moi"]:
    check(f"{name}: vector PDF and report PNG retained", (ROOT / f"HinhVaSoLieu/{name}.pdf").is_file() and (ROOT / f"HinhVaSoLieu/{name}.png").is_file())
report = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "result": "PASS",
    "method": "Independent pandas grouping; Wilson bounds checked by score equation, not by reusing production function; DOCX/PDF structural checks.",
    "visual_qa": "See KIEM_TRA_BAI_LAM.md; script alone does not establish visual quality.",
    "checks": checks,
    "outputs": outputs
}
(WORK / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"result": report["result"], "checks_passed": len(checks), "outputs": outputs}, ensure_ascii=False, indent=2))
