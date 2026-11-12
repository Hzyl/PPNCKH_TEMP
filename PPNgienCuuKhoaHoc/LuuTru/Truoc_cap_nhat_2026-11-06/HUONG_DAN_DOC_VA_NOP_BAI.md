# Bộ bài làm Phương pháp nghiên cứu khoa học trong Công nghệ thông tin

Nhóm 4, lớp DCT123C4: Lý Đức Huy, Nguyễn Quốc Huy, Trần Nam Khang, Võ Quốc Khánh và Lâm Trác Đạt. Nhóm 5 người được giảng viên cho phép theo xác nhận của bạn.

## Hai bài chính

- **Giữa kỳ:** [Bản PDF](BaiGiuaKy/GiuaKy_Nhom4_DCT123C4.pdf) và [bản Word chỉnh sửa](BaiGiuaKy/GiuaKy_Nhom4_DCT123C4.docx). Phân tích bài báo của Realinho và cộng sự; có hai hình vẽ lại, một hình mới, số liệu đối chiếu, phản biện và tài liệu tham khảo.
- **Cuối kỳ:** [Bản PDF](BaiCuoiKy/PPNCKH_3123411114_3123411120_3123411144_3123411151_3123411064.pdf) và [bản Word chỉnh sửa](BaiCuoiKy/PPNCKH_3123411114_3123411120_3123411144_3123411151_3123411064.docx). Đề cương nghiên cứu theo 16 mục mẫu NCKHSV, nghiên cứu giá trị bổ sung của kết quả học kỳ 1 khi dự báo trạng thái học tập.

Cuối kỳ yêu cầu nộp một PDF, trình bày và nộp bản in theo thông báo của giảng viên. Tên PDF đã dùng đủ 5 MSSV theo ngoại lệ quy mô nhóm. Không có thao tác nộp bài lên hệ thống hoặc gửi cho giảng viên trong quá trình chuẩn bị này.

## Những điểm nhóm cần nắm trước khi trình bày

1. **Hai bài có nhiệm vụ khác nhau.** Giữa kỳ là phân tích công trình có sẵn và tự dựng hình. Cuối kỳ là đề cương nghiên cứu sẽ thực hiện; không có kết quả huấn luyện giả trong đề cương.
2. **Bài báo gốc là Data Descriptor.** Nó công bố dữ liệu và phân tích khám phá. Không nói tác giả đã chứng minh Random Forest hay XGBoost tốt nhất bằng một bảng accuracy mà bài không có.
3. **Định nghĩa nhãn:** Dropout là trạng thái theo góc nhìn cơ sở/chương trình; Enrolled vẫn theo học ở mốc quan sát; Graduate tốt nghiệp. Enrolled không có nghĩa chắc chắn sẽ tốt nghiệp.
4. **Phiên bản:** bài báo mô tả 35 cột gồm Target; CSV UCI dùng trong bài có 37 cột. Hai biến thêm là Previous qualification (grade) và Admission grade. Ba số đếm nhãn khớp bài báo, nhưng điều đó không chứng minh mọi mã và mọi dòng của các phiên bản giống hệt nhau.
5. **Hình mới:** mỗi nhóm chia theo số học phần đạt ở học kỳ 1. Tỷ lệ = số Dropout / toàn bộ hồ sơ thuộc nhóm, gồm cả Enrolled. Khoảng Wilson mô tả bất định nhị thức theo giả định, không bao hàm sai lệch chọn mẫu hay hiệu quả trên trường khác.
6. **T0/T1:** T0 dùng 8 biến tuyển sinh đã định trước; T1 thêm 6 biến học kỳ 1. Không dùng học kỳ 2; không dùng trạng thái học phí khi chưa chứng minh được thời điểm ghi nhận. Dữ liệu thiếu thời điểm bỏ học nên nghiên cứu chỉ so sánh hồi cứu, chưa kiểm chứng hệ thống cảnh báo đang vận hành.

## Gợi ý trình bày khoảng 8 phút

- **Phút 0–1 — Lý Đức Huy:** giới thiệu bài báo, chỉ mục, nguồn dữ liệu và bài toán.
- **Phút 1–2 — Nguyễn Quốc Huy:** giải thích hai hình tái tạo và mất cân bằng lớp. Bộ phân loại luôn chọn Graduate vẫn có accuracy 49,93% nhưng recall Dropout bằng 0.
- **Phút 2–3 — Trần Nam Khang:** giải thích hình mới, tử số/mẫu số và giới hạn nhân quả; nhắc khác biệt phiên bản dữ liệu.
- **Phút 3–5 — Võ Quốc Khánh:** trình bày câu hỏi cuối kỳ, T0/T1, Logistic Regression/Random Forest, cách chia tập và tránh rò rỉ.
- **Phút 5–7 — Lâm Trác Đạt:** chỉ số, bootstrap ghép cặp, tiến độ 12 tuần và sản phẩm dự kiến.
- **Phút 7–8 — Nguyễn Quốc Huy:** đóng góp có giới hạn, kết quả chưa thực hiện và hướng kiểm chứng tại cơ sở Việt Nam trong tương lai.

Đây là phân công gợi ý để luyện tập, không phải xác nhận người nào đã thực hiện từng phần.

## Câu hỏi thường gặp khi bảo vệ

**Vì sao không chỉ dùng accuracy?** Các lớp không cân bằng. Cần biết bỏ sót Dropout bao nhiêu và chất lượng dự đoán từng lớp; macro-F1 cho mỗi lớp trọng số bằng nhau.

**Tỷ lệ 79,39% có phải xác suất một sinh viên bất kỳ sẽ bỏ học?** Không. Đó là 570/718 hồ sơ mang nhãn Dropout trong một nhóm của bộ dữ liệu quan sát. Chưa có mô hình cá nhân hóa hoặc kiểm định ngoài mẫu.

**Vì sao không bỏ Enrolled để kết quả đẹp hơn?** Thay đổi mẫu số làm đổi câu hỏi. Khi bỏ Enrolled, hai nhóm đầu của hình mới đổi thứ tự tỷ lệ. Báo cáo giữ ba nhãn và công khai phân tích nhạy cảm.

**Vì sao không dùng điểm học kỳ 2?** Vì nghiên cứu muốn so sánh thông tin nhập học với cuối học kỳ 1. Dùng kết quả học kỳ 2 sẽ đưa thông tin tương lai vào một thời điểm chưa có nó.

**Thấy accuracy 91,33% ở nghiên cứu trong nước thì nhóm phải đạt cao hơn không?** Không. Định nghĩa nhãn và giao thức khác nhau; tài liệu còn có điểm cần kiểm tra về nhân bản trước chia tập và số mẫu ma trận. Đề tài cần phép so sánh cùng dữ liệu kiểm tra và báo cáo trung thực, không chạy theo một điểm số không tương đương.

**Cuối kỳ đã có mô hình chưa?** Chưa. Theo đề môn học, sản phẩm đang nộp là thuyết minh. Thời gian 12 tuần, ngưỡng minh họa precision 0,60, các chỉ số và sản phẩm mô hình đều là kế hoạch.

## Chạy lại số liệu và hình

Thư mục `MaNguon` có `phan_tich_va_ve_hinh.py`. Với Python 3.10 trở lên và ReportLab, chạy:

```text
python MaNguon/phan_tich_va_ve_hinh.py
```

Chương trình dùng `TaiLieuNguon/data.csv`, tự kiểm tra 4.424 dòng, 37 cột, ba số đếm nhãn, ô rỗng và dòng trùng; sau đó ghi ba PDF hình, hai bảng CSV và `HinhVaSoLieu/kiem_tra_so_lieu.json`. Không cần tải lại dữ liệu, không gọi AI và không huấn luyện mô hình. Nếu phiên bản dữ liệu thay đổi, kiểm tra SHA-256 trước khi so sánh.

`TaiLieuNguon` chứa đề môn, mẫu bìa, mẫu thuyết minh, bài báo gốc, dữ liệu, chứng cứ chỉ mục và ảnh SCImago bạn gửi. `work` giữ tệp dựng tài liệu và ảnh kiểm tra nội bộ; không cần nộp thư mục này nếu giảng viên chỉ yêu cầu báo cáo.

## Trước khi nộp

- Cả nhóm đọc và thống nhất nội dung, đặc biệt phần dự kiến nghiên cứu và cách tính hình.
- Nguyễn Quốc Huy được ghi là điều phối/chủ nhiệm **dự kiến**; phân công có thể điều chỉnh theo thống nhất của nhóm.
- Tên giảng viên, điện thoại, email và chữ ký chưa được tự điền. Các ô duyệt chỉ dùng nếu thực hiện thủ tục đăng ký chính thức; không ký thay hoặc coi là đã được trường phê duyệt.
- Xác nhận hạn nộp và kênh nộp trực tiếp từ thông báo môn học; không suy ra hạn nộp từ lịch tháng 3–4 không ghi năm trong đề.
- Nếu sửa Word, xuất lại PDF và kiểm tra số trang, mục lục, bảng và hình trước khi nộp.
