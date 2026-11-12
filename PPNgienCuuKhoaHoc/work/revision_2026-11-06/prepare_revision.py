from pathlib import Path
import shutil, json, hashlib
from pypdf import PdfReader
ROOT=Path(r'C:\Users\ASUS\OneDrive\Máy tính\c\PPNgienCuuKhoaHoc')
WORK=ROOT/'work'/'revision_2026-11-06'; WORK.mkdir(exist_ok=True)
BACK=ROOT/'LuuTru'/'Truoc_cap_nhat_2026-11-06'; BACK.mkdir(parents=True,exist_ok=True)
files=list((ROOT/'BaiCuoiKy').glob('*'))+[ROOT/'HUONG_DAN_DOC_VA_NOP_BAI.md',ROOT/'KIEM_TRA_BAI_LAM.md']
for f in files:
 if f.is_file() and not (BACK/f.name).exists(): shutil.copy2(f,BACK/f.name)
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'BaiGiuaKy').glob('*') if p.is_file()}
(WORK/'midterm-before.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
SRC=ROOT/'TaiLieuNguon'/'TongQuan_2026-11-06'
mapping=[('P1_Realinho_2022',ROOT/'TaiLieuNguon/paper.pdf','https://doi.org/10.3390/data7110146'),('P2_NongThiHoa_2025',ROOT/'work/domestic-tnu-readable.pdf','https://doi.org/10.34238/tnu-jst.12201'),('P3_Martins_2023',SRC/'P3_Phashed_2023.pdf','https://doi.org/10.3390/app13084702'),('P4_Goren_2024',SRC/'P5_EDM_2024.pdf','https://doi.org/10.5281/zenodo.12729834'),('P5_Cho_2023',SRC/'P6_Sahmyook_2023.pdf','https://doi.org/10.3390/app132112004')]
manifest=[]
for name,src,doi in mapping:
 dst=SRC/(name+'.pdf')
 if not dst.exists():shutil.copy2(src,dst)
 pages=[p.extract_text() or '' for p in PdfReader(dst).pages]
 (SRC/(name+'.txt')).write_text('\n\n'.join(f'=== TRANG PDF {i+1} ===\n{v}' for i,v in enumerate(pages)),encoding='utf-8')
 manifest.append(dict(id=name[:2],file=dst.name,doi=doi,pages=len(pages),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),note='Bản đọc sửa cấu trúc PDF; bản tải gốc giữ tại TaiLieuNguon/domestic-tnu.pdf' if name.startswith('P2') else 'Toàn văn'))
(SRC/'manifest_5_bai.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(WORK/'artifact.md').write_text('''# Bản cuối kỳ theo hướng dẫn mới ngày 06-11-2026
Giữ mẫu bìa đã được người dùng chấp nhận tại work/mau-bia.docx, không thay đổi tệp mẫu.
Thay phần nội dung 16 mục cũ bằng 5 phần người dùng yêu cầu. Ngày trên bìa đổi sang tháng 11/2026.
A4 dọc, TNR 13, lề trái 3 cm phải 1,5 cm; mục lục và số trang cập nhật bằng Word.
Bảng so sánh nhiều tiêu chí dùng section A4 ngang, chữ 10,5–11, viền mảnh, nền trắng.
Nguồn đầy đủ tải trước phân tích; 5 bài báo không bao gồm kho dữ liệu UCI.
Bài giữa kỳ giữ nguyên bằng SHA256; bản cuối kỳ cũ lưu trong LuuTru/Truoc_cap_nhat_2026-11-06.
Kết quả mô hình thuộc các bài báo phải có nguồn; phần phương pháp của nhóm là đề xuất chưa chạy.
''',encoding='utf-8')
print(json.dumps({'backup':str(BACK),'sources':manifest,'midterm_files':len(hashes)},ensure_ascii=False,indent=2))
