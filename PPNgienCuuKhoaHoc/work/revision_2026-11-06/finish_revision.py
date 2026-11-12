from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from docx import Document
from pypdf import PdfReader
import hashlib, json, re, shutil
import pandas as pd
ROOT=Path(r'C:\Users\ASUS\OneDrive\Máy tính\c\PPNgienCuuKhoaHoc')
WORK=ROOT/'work/revision_2026-11-06'
SRC=ROOT/'TaiLieuNguon/TongQuan_2026-11-06'
STEM='PPNCKH_3123411114_3123411120_3123411144_3123411151_3123411064'
DOC=ROOT/'BaiCuoiKy'/(STEM+'.docx');PDF=DOC.with_suffix('.pdf')
TEMPLATE=Path(r'C:\Users\ASUS\OneDrive\Documents\Custom Office Templates\style_word_dang_bao_cao.dotx')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
before=json.loads((WORK/'midterm-before.json').read_text(encoding='utf-8'))
checks['midterm_unchanged']=all(sha(ROOT/k)==v for k,v in before.items())
manifest=json.loads((SRC/'manifest_5_bai.json').read_text(encoding='utf-8'))
checks['five_distinct_full_papers']=len(manifest)==5 and len({x['doi'] for x in manifest})==5
checks['source_hashes_and_pages']=all(sha(SRC/x['file'])==x['sha256'] and len(PdfReader(SRC/x['file']).pages)==x['pages'] for x in manifest)
df=pd.read_csv(ROOT/'TaiLieuNguon/data.csv',sep=';')
checks['dataset_shape']=df.shape==(4424,37)
checks['dataset_labels']=df.Target.value_counts().to_dict()=={'Graduate':2209,'Dropout':1421,'Enrolled':794}
checks['no_empty_or_exact_duplicate']=int(df.isna().sum().sum())==0 and int(df.duplicated().sum())==0
checks['p2_confusion_matrix']=sum([773,60,92,829])==1754 and round((773+829)/1754,4)==0.9133
d=Document(DOC); paragraphs=[p.text for p in d.paragraphs]
checks['five_chapters']=all(h in paragraphs for h in ['1 Giới thiệu','2 Tổng quan nghiên cứu','3 Phương pháp đề xuất','4 Kế hoạch thực hiện','5 Kết quả dự kiến'])
checks['five_papers_compared']=any(len(t.rows)==6 and len(t.columns)==6 and all(t.cell(i,0).text.startswith('P'+str(i)) for i in range(1,6)) for t in d.tables)
checks['eight_vertical_criteria']=all(x in paragraphs for x in ['Dữ liệu và khả năng tái lập','Nhãn đích và đối tượng dự báo','Thời điểm thông tin','Tiền xử lý và mất cân bằng lớp','Lựa chọn mô hình','Giao thức và chỉ số đánh giá','Kết quả và mức độ tin cậy của phép so sánh','Ưu điểm và hạn chế có thể kế thừa'])
checks['five_members']=all(x in '\n'.join(paragraphs) for x in ['3123411114','3123411120','3123411144','3123411151','3123411064'])
checks['planned_not_fabricated']='Nhóm chưa huấn luyện các mô hình' in '\n'.join(paragraphs)
reader=PdfReader(PDF); texts=[p.extract_text() or '' for p in reader.pages]
checks['pdf_18_pages']=len(texts)==18
checks['one_landscape_page']=sum(float(p.mediabox.width)>float(p.mediabox.height) for p in reader.pages)==1
checks['no_field_errors']=not any(t in '\n'.join(texts) for t in ['Error!','Bookmark not defined','Error: Reference','[[COMPARISON]]'])
checks['toc_updated']=all(re.search(label+r'\s*\.*\s*'+str(n),texts[1]) is not None for label,n in [('1 Giới thiệu',3),('2 Tổng quan nghiên cứu',4),('3 Phương pháp đề xuất',10),('4 Kế hoạch thực hiện',13),('5 Kết quả dự kiến',15)])
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(TEMPLATE) as z: ts=E.fromstring(z.read('word/styles.xml'))
with ZipFile(DOC) as z:
 ds=E.fromstring(z.read('word/styles.xml')); xml=E.fromstring(z.read('word/document.xml'))
def sig(el):
 if el is None:return None
 return (E.QName(el).localname,tuple(sorted((E.QName(k).localname,v) for k,v in el.attrib.items() if 'rsid' not in k)),tuple(sig(c) for c in el))
style_checks={}
for sid in ['Normal','Heading1','Heading2','Heading3','Caption','TOC1','TOC2']:
 a=ts.xpath('w:style[@w:styleId="'+sid+'"]',namespaces=ns)[0]
 b=ds.xpath('w:style[@w:styleId="'+sid+'"]',namespaces=ns)[0]
 style_checks[sid]=all(sig(a.find('w:'+x,ns))==sig(b.find('w:'+x,ns)) for x in ['pPr','rPr'])
checks['template_style_properties']=all(style_checks.values())
checks['template_doc_defaults']=sig(ts.find('w:docDefaults',ns))==sig(ds.find('w:docDefaults',ns))
checks['template_file_unchanged']=sha(TEMPLATE)==json.loads((WORK/'style-evidence.json').read_text(encoding='utf-8'))['sha256']
checks['no_decorative_table_fills']=not xml.xpath('//w:tcPr/w:shd[@w:fill!="FFFFFF" and @w:fill!="auto"]',namespaces=ns)
checks['png_review_complete']=all((WORK/'qa_styled_v3'/f'page-{i:02}.png').exists() for i in range(1,19))
checks['old_final_backed_up']=(ROOT/'LuuTru/Truoc_cap_nhat_2026-11-06'/DOC.name).exists()
result={'checks':checks,'style_checks':style_checks,'pages':len(texts),'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [DOC,PDF]},'dataset_sha256':sha(ROOT/'TaiLieuNguon/data.csv'),'visual_review':'All 18 final page images inspected by assistant; no clipping or overlap observed. Page before landscape table retains whitespace for orientation change.','renderer':'Word COM and Poppler; packaged renderer attempted and unavailable because soffice.exe is absent.','experiments':'Not run; report is literature review and proposed protocol.'}
(WORK/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert all(checks.values()),[k for k,v in checks.items() if not v]

# Keep exactly the five selected papers visible; retain redundant download files in work.
downloads=WORK/'download_history';downloads.mkdir(exist_ok=True)
for pat in ['P3_Phashed_2023.*','P5_EDM_2024.*','P6_Sahmyook_2023.*','downloads.json']:
 for f in SRC.glob(pat):
  dest=downloads/f.name
  assert f.resolve().is_relative_to(ROOT.resolve()) and dest.resolve().is_relative_to(ROOT.resolve())
  if not dest.exists():shutil.move(str(f),str(dest))
readme='''# Năm bài báo dùng trong tổng quan cuối kỳ

P1 — Realinho và cộng sự (2022), Data, DOI 10.3390/data7110146, 17 trang.
P2 — Nông Thị Hoa (2025), TNU Journal of Science and Technology, DOI 10.34238/tnu-jst.12201, 6 trang.
P3 — Martins và cộng sự (2023), Applied Sciences, DOI 10.3390/app13084702, 15 trang.
P4 — Goren, Cohen và Rubinstein (2024), EDM, DOI 10.5281/zenodo.12729834, 11 trang.
P5 — Cho, Yu và Kim (2023), Applied Sciences, DOI 10.3390/app132112004, 16 trang.

Mỗi PDF đã được lưu trước khi phân tích nội dung. Các tệp TXT hỗ trợ tìm kiếm; kiểm tra số liệu bằng PDF và tên bảng/trang nêu trong báo cáo.
P2 là bản đọc đã sửa phần bao tệp PDF bị lỗi; bản tải gốc được giữ tại TaiLieuNguon/domestic-tnu.pdf. Không sửa nội dung bài.
manifest_5_bai.json ghi DOI, số trang và SHA-256. Bộ tổng quan có 5 bài; UCI 697 là nguồn dữ liệu bổ trợ, không tính là bài thứ sáu.
Các PDF giữ nguyên thông tin tác giả và giấy phép trong bài. Gói này phục vụ việc đọc, đối chiếu học phần; chưa được gửi hoặc nộp ra bên ngoài.
'''
(SRC/'README.md').write_text(readme,encoding='utf-8')
pack=ROOT/'TaiLieuNguon'/'5_BaiBao_PPNCKH_2026-11-06.zip'
with ZipFile(pack,'w',ZIP_DEFLATED) as z:
 for x in manifest:z.write(SRC/x['file'],x['file'])
 for name in ['README.md','manifest_5_bai.json']:z.write(SRC/name,name)

guide=f'''# Bộ bài PPNCKH của nhóm 4 lớp DCT123C4

Cập nhật ngày 06/11/2026 theo phần hướng dẫn mới của giảng viên do người dùng cung cấp.

## Bài hiện hành

- Giữa kỳ: `BaiGiuaKy/GiuaKy_Nhom4_DCT123C4.docx` và `.pdf`. Giữ nguyên; làm việc với một bài báo nền tảng, hai hình vẽ lại và một hình mới.
- Cuối kỳ: `BaiCuoiKy/{STEM}.docx` và `.pdf`. Bản mới 18 trang kể cả bìa, tổng quan 5 bài và đề cương theo 5 phần: Giới thiệu, Tổng quan, Phương pháp đề xuất, Kế hoạch, Kết quả dự kiến.
- Nguồn: `TaiLieuNguon/TongQuan_2026-11-06/` hoặc gói `TaiLieuNguon/5_BaiBao_PPNCKH_2026-11-06.zip` gồm đủ 5 PDF, DOI và checksum.
- Bản cuối kỳ trước đây và hướng dẫn cũ được lưu ở `LuuTru/Truoc_cap_nhat_2026-11-06/`. Cấu trúc 16 mục cũ không còn là cấu trúc của báo cáo hiện hành.

## Những điểm cần đọc khi trình bày bài cuối kỳ

1. Mục 2.1: ý tưởng, từ khóa, cách chọn và tải toàn văn. P1 là bài mô tả dữ liệu; P2–P5 là các nghiên cứu thực nghiệm. UCI không được tính là một bài báo.
2. Bảng so sánh nằm ở trang PDF 8. Mục 2.4 từ trang PDF 9 so sánh theo chiều dọc 8 tiêu chí, mỗi tiêu chí một đoạn.
3. Mục 2.5: hướng dự báo theo giai đoạn đã có trong P3. Đề tài của nhóm là kiểm chứng và làm rõ quy trình, không nhận ý tưởng hoàn toàn mới.
4. Mục 3: T0 có 8 biến; T1 thêm 6 biến học kỳ một. LR và RF, chia 60/20/20, CV 5 phần trong train, tránh fit preprocessing trên validation/test.
5. Mục 5: chưa có mô hình thực nghiệm của nhóm, không cam kết accuracy 90%. Kế hoạch 12 tuần là dự kiến tương đối, không phải hạn nộp.
6. Phụ lục: kiểm tra trang/bảng của từng số liệu. Accuracy, global F1, macro-F1 và AUC không phải cùng chỉ số; không xếp hạng trực tiếp giữa các bài khác dữ liệu/nhãn.

## Style và bìa

Đã nhập Normal, Heading 1–3, Caption và các style mục lục từ `style_word_dang_bao_cao.dotx` người dùng gửi. Nội dung thường: Times New Roman 13, giãn dòng 1,3, trước/sau đoạn 6 pt, thụt đầu dòng 1,27 cm. Giữ bìa môn học đã được chấp nhận, bảng nền trắng và một trang ngang cho bảng so sánh. Không chép nội dung Học sâu hay tên giảng viên từ tệp mẫu sang báo cáo này.

## Tệp nộp và trạng thái

Đề cuối kỳ đã lưu trước đây yêu cầu PDF, trình bày và bản in; phần hướng dẫn mới chưa thay đổi rõ định dạng nộp. DOCX dùng để chỉnh sửa, PDF là bản cố định để đọc/in/nộp khi đúng thông báo. Gói bài báo nguồn dành để đối chiếu, không khẳng định giảng viên bắt buộc nộp ZIP. Chưa có thao tác nộp bài hoặc gửi cho giảng viên.

Năm thành viên và MSSV giữ đúng ảnh người dùng cung cấp; người dùng xác nhận giảng viên cho phép cả năm làm chung. Phân công trong đề cương là đề xuất, không phải xác nhận đóng góp đã hoàn thành. Không tự điền tên giảng viên, chữ ký hoặc thông tin liên hệ.

## Tái lập và kiểm tra

Mã `MaNguon/phan_tich_va_ve_hinh.py` vẫn tái lập số liệu/hình giữa kỳ; không phải mã huấn luyện mô hình cuối kỳ. Nội dung và bộ dựng bản mới ở `work/revision_2026-11-06/`. Không chạy bộ dựng cũ `work/build_reports.py` để cập nhật cuối kỳ vì nó dùng cấu trúc 16 mục trước đây.

Kết quả kiểm tra hiện hành ghi tại `work/revision_2026-11-06/verification.json`; ảnh QA mới ở `qa_styled_v3`. Hồ sơ kiểm tra cũ không thay thế kiểm tra bản mới. Nếu sửa Word, cập nhật mục lục rồi xuất lại PDF và xem các trang thay đổi.
'''
(ROOT/'HUONG_DAN_DOC_VA_NOP_BAI.md').write_text(guide,encoding='utf-8')
qa=f'''# Kiểm tra bản cuối kỳ PPNCKH ngày 06/11/2026

Bản hiện hành gồm DOCX và PDF 18 trang kể cả bìa. Đã xem ảnh kết xuất của đủ 18 trang, không phát hiện chữ cắt, chồng lấn hoặc bảng tràn lề. Trước bảng ngang có khoảng trắng do chuyển hướng trang. Mục lục cập nhật bằng Word.

Đã kiểm tra {len(checks)}/{len(checks)} điều kiện trong `work/revision_2026-11-06/verification.json`: năm PDF toàn văn/DOI riêng, checksum và số trang nguồn; dữ liệu 4.424 × 37, số lượng ba nhãn; phép cộng ma trận P2; năm chương; năm hàng so sánh; tám đoạn so sánh theo tiêu chí; năm MSSV; phân biệt đề xuất với kết quả; mục lục, hướng trang và lỗi trường; style của mẫu; bản sao lưu và tính nguyên vẹn giữa kỳ.

Style Normal, Heading 1–3, Caption, TOC 1–2 và docDefaults trong DOCX sau lưu Word có thuộc tính trùng mẫu `.dotx`. Tệp mẫu không bị thay đổi. Bìa và bố cục bảng có định dạng riêng để giữ mẫu bìa đã chấp nhận và khả năng đọc; không chép nội dung mẫu.

Năm bài đã được đọc từ toàn văn đã lưu; các dữ kiện quan trọng được đối chiếu bằng trang/bảng ghi ở phụ lục. Có cả bài công bố dữ liệu và bốn bài thực nghiệm. Không gọi kho UCI là bài báo thứ sáu. Các điểm số trong tổng quan thuộc tác giả, chưa được nhóm tái lập. Không huấn luyện mô hình hoặc tạo kết quả giả cho đề cương.

Môi trường xuất: Microsoft Word COM và Poppler. Bộ render đóng gói đã thử nhưng không chạy vì thiếu soffice.exe; không dùng việc kiểm tra XML thay cho kiểm tra ảnh.

SHA-256 bản cuối kỳ hiện hành:
- DOCX: `{sha(DOC)}`
- PDF: `{sha(PDF)}`

Bài giữa kỳ giữ nguyên cả ba tệp, đã đối chiếu SHA-256 với trước sửa. Chi tiết kiểm tra cũ ngày 22/10/2026 nằm trong bản lưu ở `LuuTru/Truoc_cap_nhat_2026-11-06/`; kết quả 60 kiểm tra cũ không được dùng để khẳng định bản cuối kỳ mới đạt.

Chưa nộp bài, gửi tài liệu hoặc công bố ra bên ngoài. Hạn nộp và yêu cầu bổ sung sau này cần theo thông báo trực tiếp của giảng viên.
'''
(ROOT/'KIEM_TRA_BAI_LAM.md').write_text(qa,encoding='utf-8')
for name in ['prepare_revision.py','fetch_review.py','finish_revision.py']:
 src=Path(__file__).with_name(name)
 if src.exists():shutil.copy2(src,WORK/name)
with (WORK/'artifact.md').open('a',encoding='utf-8') as f:
 f.write('\n## Style theo yêu cầu bổ sung\nĐã dùng style từ '+str(TEMPLATE)+'; SHA-256 '+sha(TEMPLATE)+'. Thuộc tính nhập và ngoại lệ xem style-evidence.json. Bản cuối sau style 18 trang; QA tại qa_styled_v3.\n')
print('PACKAGE',str(pack),pack.stat().st_size)
