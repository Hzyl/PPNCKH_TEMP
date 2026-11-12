from pathlib import Path
import sys, json, shutil, hashlib
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree
from docx.shared import Cm, Pt
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(r'C:\Users\ASUS\OneDrive\Máy tính\c\PPNgienCuuKhoaHoc')
WORK=ROOT/'work'/'revision_2026-11-06'
sys.path.insert(0,str(ROOT/'work'))
import build_reports as b
TITLE='Đánh giá giá trị bổ sung của thông tin học kỳ thứ nhất trong dự báo nguy cơ bỏ học của sinh viên trên dữ liệu UCI 697'
doc=b.base_document('CUỐI KỲ',TITLE)
TEMPLATE=Path(r'C:\Users\ASUS\OneDrive\Documents\Custom Office Templates\style_word_dang_bao_cao.dotx')
with ZipFile(TEMPLATE) as z: source_styles=etree.fromstring(z.read('word/styles.xml'))
selected=['Normal','Heading1','Heading2','Heading3','Heading4','Heading1Char','Heading2Char','Heading3Char','Heading4Char','Caption']+[f'TOC{i}' for i in range(1,10)]
target_styles=doc.styles.element
for old in list(target_styles):
 if old.tag==qn('w:docDefaults') or old.get(qn('w:styleId')) in selected:target_styles.remove(old)
target_styles.insert(0,deepcopy(source_styles.find(qn('w:docDefaults'))))
for el in source_styles:
 if el.get(qn('w:styleId')) in selected:target_styles.append(deepcopy(el))
# The cover remains the previously accepted design, independent of the new body defaults.
for p in doc.paragraphs:
 p.paragraph_format.first_line_indent=Cm(0)
 p.paragraph_format.left_indent=Cm(0)
 if 'THÁNG 10 NĂM 2026' in p.text:
  for r in p.runs:r.text=r.text.replace('THÁNG 10 NĂM 2026','THÁNG 11 NĂM 2026')
(WORK/'style-evidence.json').write_text(json.dumps({'template':str(TEMPLATE),'sha256':hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),'imported_styles':selected,'body':'Times New Roman 13; line 1.3; before/after 6 pt; first line 1.27 cm','exceptions':'Accepted cover retained; tables have zero first-line indent and compact readable spacing; front-matter Title retained; existing A4 page geometry retained.'},ensure_ascii=False,indent=2),encoding='utf-8')

def p(text,style=None):return b.paragraph(doc,text,style)
def tab(headers,rows,widths,caption,size=11.5):
 t=b.table(doc,headers,rows,caption)
 for j,w in enumerate(widths):t.columns[j].width=Cm(w)
 for i,row in enumerate(t.rows):
  for j,c in enumerate(row.cells):
   c.width=Cm(widths[j]); pr=c._tc.get_or_add_tcPr()
   for el in list(pr.findall(qn('w:shd'))):pr.remove(el)
   for para in c.paragraphs:
    para.paragraph_format.first_line_indent=Cm(0)
    para.paragraph_format.left_indent=Cm(0)
    para.paragraph_format.keep_with_next=(i<len(t.rows)-1) if caption and (caption.startswith('Bảng 4 ') or caption.startswith('Bảng 6 ')) else i==0
    for run in para.runs:b.set_font(run,size,i==0)
 return t
def orient(landscape):
 s=doc.add_section(WD_SECTION_START.NEW_PAGE)
 s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
 s.page_width=Cm(29.7 if landscape else 21);s.page_height=Cm(21 if landscape else 29.7)
 s.left_margin=Cm(1.5 if landscape else 3);s.right_margin=Cm(1.5)
 s.top_margin=Cm(1.5);s.bottom_margin=Cm(1.6)
 for e in list(s._sectPr.findall(qn('w:pgNumType'))):s._sectPr.remove(e)
 s.footer.is_linked_to_previous=True;s.header.is_linked_to_previous=True

p('MỤC LỤC','Title')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z')
doc.add_paragraph()._p.append(field)
doc.add_page_break()
p('CÁCH ĐỌC BÁO CÁO','Title')
p('Báo cáo gồm phần tổng quan năm bài báo và đề cương thực nghiệm. P1–P5 tương ứng tài liệu [1]–[5]. Những kết quả có trích dẫn là số liệu của tác giả; các cấu hình T0–T1, kế hoạch và sản phẩm thực nghiệm là đề xuất của nhóm, chưa phải kết quả đã chạy.')
tab(['Ký hiệu','Ý nghĩa'],[
 ['T0 / T1','Thông tin đầu vào / thông tin đầu vào cộng thông tin học kỳ một.'],
 ['LR / RF / BRF','Logistic Regression / Random Forest / Balanced Random Forest.'],
 ['NN / DNN / SVM','Mạng nơ-ron / mạng nơ-ron sâu / máy véc-tơ hỗ trợ.'],
 ['LMS','Hệ thống quản lý học tập, nguồn nhật ký hoạt động học.'],
 ['SMOTE','Kỹ thuật tạo mẫu tổng hợp cho lớp thiểu số.'],
 ['AUC','Diện tích dưới đường cong ROC trong bài P4; khác accuracy.'],
 ['Macro-F1','Trung bình F1 không trọng số giữa các lớp.'],
 ['Fold / seed','Phần dữ liệu trong kiểm định chéo / hạt giống sinh số ngẫu nhiên.']],[3.3,13.2],'Bảng 1 Giải thích ký hiệu')

def keywords():
 tab(['Nhóm','Từ khóa hoặc chuỗi truy vấn'],[
 ['Vấn đề','student dropout prediction; academic success; higher education; dự đoán sinh viên bỏ học'],
 ['Thời điểm','early prediction; phased prediction; first semester; pre-enrollment data'],
 ['Kỹ thuật','machine learning; Random Forest; logistic regression; class imbalance; data leakage'],
 ['Truy vấn kết hợp','"student dropout" AND "higher education" AND "first semester"; "Multi-Class Phased Prediction"; "dropout prediction" AND "oversampling"'],
 ['Truy vấn tiếng Việt','"dự đoán" "bỏ học" "sinh viên" "học máy"']],[3.3,13.2],None)
def compare():
 orient(True)
 rows=[
 ['P1\n[1]','4.424 hồ sơ Portalegre. Ba lớp. Biến nhập học và hai học kỳ; 34 biến đầu vào trong bài mô tả.','Ghép nguồn; làm sạch, loại trùng, ẩn danh; phân tích mất cân bằng và tương quan.','RF, XGBoost, LightGBM, CatBoost để khảo sát permutation importance theo F1. Không có giao thức benchmark đủ chi tiết.','Graduate 2.209; Dropout 1.421; Enrolled 794. Biến học phần đạt và học phí nổi bật. Không lấy accuracy làm mốc.','Ưu: mô tả và công bố dữ liệu. Hạn chế: không có ngày bỏ học; không suy diễn sẵn hiệu năng cảnh báo sớm. Tr. 3–4, 7, 10–11.'],
 ['P2\n[2]','UCI 4.424 hồ sơ, 36 biến. Gộp Graduate và Enrolled. Có thông tin cả học kỳ hai.','Mã hóa nhãn, chuẩn hóa; mô tả nhân đôi Dropout trước chia tập; xem xét đặc trưng quan trọng.','NN, RF, SVM. Chia 80/20 trên dữ liệu đã cân bằng; thử một số cấu hình. Chỉ số chính accuracy.','RF accuracy 0,9133. Bài ghi 1.169 mẫu kiểm tra; ma trận RF cộng thành 1.754. Không dùng làm mốc trực tiếp.','Ưu: đối chiếu thuật toán, có tham số và ma trận. Hạn chế: nguy cơ bản sao giữa các tập; số mẫu thiếu nhất quán; nhãn nhị phân. Tr. 3–5.'],
 ['P3\n[3]','4.433 hồ sơ gốc. Ba lớp; S0, S1, S2. Loại hồ sơ đã bỏ học khỏi các giai đoạn sau, làm thay đổi thành phần mẫu.','SMOTE hoặc SVMSMOTE với RF; hoặc cân bằng trong thuật toán. SMOTE được mô tả áp dụng trên tập huấn luyện.','SMOTE+RF, SVMSMOTE+RF, BRF, EE, RB. Chia 90/10 phân tầng; CV 10 phần; lặp 10 seed.','S1: SVMSMOTE+RF Test F1 0,745 ± 0,014; BRF F1 Dropout 0,728 ± 0,026. Giữ tên global F1 của bài.','Ưu: so sánh theo giai đoạn, có độ phân tán và điểm từng lớp. Hạn chế: tập mẫu thay đổi; không đồng nhất với CSV UCI hiện dùng. Tr. 4–9.'],
 ['P4\n[4]','8.267 sinh viên, 2019–2022; nhiều ngành. Bỏ học: không đăng ký môn 2 năm liên tiếp, chưa hoàn thành chương trình. Nhiều mốc từ 4 tuần.','Điền thiếu; chuẩn hóa theo môn; gom môn bằng k-means; đặc trưng studentship từ LMS. XGBoost dùng SMOTE; NN dùng trọng số loss.','XGBoost và NN; chia ngẫu nhiên 80/20; GridSearch cho XGBoost. AUC, recall Dropout và importance theo nhóm biến.','Riêng ngành CS, XGBoost không LMS: AUC Pre-Entry 0,63; Exam B 0,86. Lợi ích LMS phụ thuộc mô hình và thời điểm.','Ưu: xem xét thời gian, ngành, nhóm thông tin. Hạn chế: dữ liệu nội bộ; đặc trưng phức tạp; cần làm rõ phạm vi fit các bước tổng hợp khi tái lập. Tr. 3–7, 10.'],
 ['P5\n[5]','20.050 sinh viên; khoảng 168.000 bản ghi học kỳ. Nhị phân, nhiều biến của học kỳ cuối; tổng hợp theo sinh viên.','Làm trơn điểm, chọn biến tương quan, StandardScaler trước chia tập trong đoạn mã; thử SMOTE, ADASYN, Borderline-SMOTE.','LR, DT, RF, SVM, DNN, LightGBM. Chia 80/20; bảng kết quả là trung bình 5 lần. Accuracy, precision, recall, F1.','LightGBM: accuracy 0,955; F1 Dropout 0,840. RF F1 0,827 → 0,830 khi SMOTE. Không có kết quả LightGBM+SMOTE.','Ưu: khảo sát chỉ số lớp dương và tác động oversampling. Hạn chế: chuẩn hóa trước chia; biến học kỳ cuối không chứng minh dự báo sớm. Tr. 5–8, 10–15.']]
 tab(['Bài','Dữ liệu và thời điểm','Tiền xử lý','Mô hình và đánh giá','Kết quả tác giả báo cáo','Ưu điểm và hạn chế'],rows,[1.15,4.65,4.5,5.0,5.15,6.25],'Bảng 2 So sánh năm bài báo theo các tiêu chí kỹ thuật',10.5)
 orient(False)
def features():
 tab(['Nhóm biến','Các biến và nguyên tắc sử dụng'],[
 ['T0\n8 biến','Application mode; Application order; Course; Daytime/evening attendance; Previous qualification; Previous qualification (grade); Admission grade; Age at enrollment.'],
 ['T1\n14 biến','Toàn bộ T0 cộng sáu cột Curricular units 1st sem: (credited), (enrolled), (evaluations), (approved), (grade), (without evaluations).'],
 ['Không dùng trong phân tích chính','Mọi cột học kỳ hai; Target trong đầu vào; Debtor, Tuition fees up to date, Scholarship holder do thời điểm cập nhật cần làm rõ; các biến còn lại ngoài danh sách để giữ phạm vi đối chứng thống nhất.']],[3.3,13.2],'Bảng 3 Danh sách biến cho hai cấu hình',11.5)
def models():
 tab(['Cấu hình','Không gian tham số dự kiến','Vai trò'],[
 ['Mô hình nền','Luôn dự báo lớp phổ biến nhất từ tập huấn luyện.','Mốc kiểm tra tối thiểu; không sử dụng nhãn kiểm tra để chọn lớp.'],
 ['Logistic Regression','C: 0,1; 1; 10. class_weight: không dùng hoặc balanced. max_iter khởi đầu 2.000.','Đối chứng tuyến tính, chuẩn hóa biến định lượng trong pipeline.'],
 ['Random Forest','200 cây. max_depth: 6 hoặc không giới hạn. min_samples_leaf: 2 hoặc 5. class_weight: không dùng hoặc balanced.','Đối chứng phi tuyến; cùng lưới và seed cho T0–T1.']],[3.2,7,6.3],'Bảng 4 Mô hình và cấu hình tìm kiếm')
def schedule():
 tab(['Tuần','Công việc','Sản phẩm và điều kiện kiểm tra'],[
 ['1–2','Đối chiếu toàn văn, hoàn thiện bảng và nhận xét theo tiêu chí.','Năm PDF, sổ trích xuất, mỗi số liệu có trang/bảng nguồn.'],
 ['3','Khóa câu hỏi, nhãn, danh sách biến và protocol.','Từ điển T0–T1; cách chia tập và chỉ số được chốt trước thực nghiệm.'],
 ['4','Kiểm tra dữ liệu, tạo chỉ số dòng, chia tập và pipeline.','Schema, checksum; các tập không giao nhau; fit tiền xử lý đúng phạm vi.'],
 ['5–7','Huấn luyện mô hình nền và bốn cấu hình; chọn tham số bằng CV.','Nhật ký từng cấu hình, tham số và kết quả xác thực.'],
 ['8–9','Đánh giá kiểm tra sau khi chốt; so sánh ghép cặp, phân tích lỗi.','Bảng chỉ số từng lớp, ma trận, khoảng chênh lệch; không chọn lại bằng test.'],
 ['10','Khảo sát độ ổn định hoặc nhị phân nếu còn thời gian.','Kết quả bổ sung tách biệt, có ghi phạm vi và hạn chế.'],
 ['11–12','Viết kết quả, rà nguồn và mã, chuẩn bị trình bày.','Báo cáo hoàn chỉnh, hướng dẫn chạy lại, kiểm tra chéo nội dung.']],[1.7,6.3,8.5],'Bảng 5 Tiến độ dự kiến')
def people():
 tab(['Thành viên','Nhiệm vụ dự kiến'],[
 ['Lý Đức Huy\n3123411114','Theo dõi tài liệu và DOI; kiểm tra nguồn của bảng tổng quan.'],
 ['Nguyễn Quốc Huy\n3123411120','Tổng hợp đề cương; quản lý phiên bản và tích hợp kết quả.'],
 ['Trần Nam Khang\n3123411144','Kiểm tra dữ liệu, từ điển biến và cách chia tập.'],
 ['Võ Quốc Khánh\n3123411151','Xây dựng pipeline, huấn luyện LR và RF theo protocol đã chốt.'],
 ['Lâm Trác Đạt\n3123411064','Tính chỉ số, kiểm tra bảng và hình, phân tích lỗi, phối hợp trình bày.']],[5.1,11.4],'Bảng 6 Phân công nhóm 4 lớp DCT123C4')
def evidence():
 tab(['Nguồn','Vị trí trong PDF','Nội dung cần đối chiếu'],[
 ['P1','Tr. 3–4, 7, 10–11','34 biến + nhãn; quy trình dữ liệu; 4.424 hồ sơ và số lượng lớp; permutation importance, không có bảng benchmark accuracy.'],
 ['P2','Tr. 3, mục 2.2; tr. 4, mục 3 và Bảng 2; tr. 5, Bảng 5','Gộp nhãn và nhân đôi Dropout; chia 80/20; 1.169 mẫu ghi trong bài; RF: 773 + 60 + 92 + 829 = 1.754; accuracy 0,9133.'],
 ['P3','Tr. 4–7, mục 4; tr. 8, Bảng 3–5; tr. 9, Bảng 7','4.433 hồ sơ gốc; khác tập mẫu theo mốc; giao thức 90/10 và CV; S1 Test F1 0,745 ± 0,014; F1 Dropout BRF 0,728 ± 0,026.'],
 ['P4','Tr. 3, mục 2–3; tr. 5, Bảng 2; tr. 10, Phụ lục A–D','8.267 sinh viên; định nghĩa nhãn; AUC 0,63 và 0,86 của XGBoost không LMS ở ngành CS; preprocessing và tham số.'],
 ['P5','Tr. 5–8, mục 3; tr. 10–11, Bảng 8; tr. 13, Bảng 10','Tổng hợp bản ghi; StandardScaler trước chia trong đoạn mã; LightGBM F1 0,840; RF 0,827 và 0,830; thiếu kết quả LightGBM+SMOTE.'],
 ['UCI [6]','TaiLieuNguon/data.csv và trang UCI 697','Tệp thực nghiệm: 4.424 dòng, 36 biến và Target. Đây là nguồn dữ liệu, không phải bài báo thứ sáu.']],[1.7,5.4,9.4],'Bảng 7 Sổ đối chiếu các dữ kiện chính')

handlers={'KEYWORDS':keywords,'COMPARISON':compare,'FEATURES':features,'MODELS':models,'SCHEDULE':schedule,'PEOPLE':people,'EVIDENCE':evidence}
source=Path(__file__).with_name('final_revision.md')
for line in source.read_text(encoding='utf-8').splitlines():
 if not line.strip():continue
 if line.startswith('[['):handlers[line[2:-2]]();continue
 if line.startswith('# '):
  h=doc.add_heading(line[2:],level=1)
  h.paragraph_format.page_break_before=line.startswith('# 1 ') or line.startswith('# Phụ lục')
 elif line.startswith('## '):
  h=doc.add_heading(line[3:],level=2)
 elif line.startswith('### '):doc.add_heading(line[4:],level=3)
 else:p(line)
settings=doc.settings.element
u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');settings.append(u)
out=ROOT/'BaiCuoiKy'/(b.FINAL_STEM+'.docx')
doc.save(out)
shutil.copy2(source,WORK/source.name)
shutil.copy2(Path(__file__),WORK/Path(__file__).name)
print(json.dumps({'docx':str(out),'paragraphs':len(doc.paragraphs),'tables':len(doc.tables),'sections':len(doc.sections)},ensure_ascii=False))
