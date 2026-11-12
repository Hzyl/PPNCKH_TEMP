# Biên bản kiểm tra bộ bài làm

Ngày kiểm tra: 22/10/2026. Kết quả: hoàn tất hai báo cáo, mỗi PDF 13 trang kể cả bìa, kèm bản Word chỉnh sửa được.

## Đối chiếu yêu cầu

| Yêu cầu | Vị trí và kết quả |
|---|---|
| Giữa kỳ: thông tin bài, DOI, chỉ mục, chỉ số, lĩnh vực | Mục 1, trang PDF 3–4; minh chứng SCImago ở trang 13. CiteScore 2019 được ghi rõ là chỉ số lịch sử. |
| Bối cảnh, khoảng trống, mục tiêu, dữ liệu, phương pháp, chỉ số và kết quả | Mục 2–4, trang PDF 4–6. Phân biệt nội dung tác giả với diễn giải của nhóm. |
| Hai hình vẽ lại có nguồn, cách tái tạo, diễn giải và so sánh | Mục 5–6, trang PDF 7–8. Sơ đồ quy trình và phân bố nhãn được dựng bằng Python/ReportLab. |
| Một hình mới, nguồn số liệu, cách tính và giá trị bổ sung | Mục 7, trang PDF 9–10. Tỷ lệ Dropout theo số học phần đạt và khoảng Wilson 95%; có phân tích nhạy cảm khi loại Enrolled. |
| Phản biện, tái lập và trích dẫn | Mục 8–9, trang PDF 10–11; bảy tài liệu tham khảo ở trang 12; mã và CSV lưu riêng. |
| Cuối kỳ: bìa và mẫu NCKHSV | Bìa theo mẫu môn học; 16 mục theo thứ tự của mẫu thuyết minh, trang PDF 2–11; phần xác nhận ở trang 12. |
| Đề tài phù hợp và khả thi | So sánh T0/T1 bằng Logistic Regression và Random Forest; giao thức chia tập, ngưỡng, chỉ số, bootstrap và giới hạn thời gian được nêu rõ. |
| Tiến độ, nhân sự, sản phẩm, kinh phí | Năm thành viên đúng ảnh cung cấp; kế hoạch 12 tuần; dự toán 150.000 đồng tự đóng góp. Vai trò là dự kiến. |
| Trích dẫn và tên PDF cuối kỳ | Ba nguồn đánh số theo IEEE, gồm bài quốc tế, UCI và nghiên cứu trong nước có DOI. Tên PDF chứa đủ năm MSSV theo ngoại lệ nhóm đã được người dùng xác nhận. |
| Chuẩn bị trình bày | Hướng dẫn đọc, gợi ý trình bày tám phút và câu hỏi bảo vệ trong `HUONG_DAN_DOC_VA_NOP_BAI.md`. Đề không yêu cầu nộp slide. |

## Kiểm tra số liệu và cấu trúc

`work/verify_deliverables.py` đã chạy thành công: **60/60 kiểm tra đạt**. Chi tiết, kích thước và SHA-256 của bốn tệp chính được lưu trong `work/verification.json`.

- Đọc CSV độc lập bằng pandas: 4.424 dòng, 37 cột, không ô thiếu, không dòng trùng hoàn toàn.
- Nhãn: 1.421 Dropout, 794 Enrolled, 2.209 Graduate; khớp Figure 2 của bài báo.
- Đếm lại bốn nhóm học phần bằng `pd.cut` và bảng chéo; đối chiếu tử số, mẫu số, tỷ lệ, phân tích nhạy cảm và CSV xuất.
- Kiểm tra hai cận Wilson bằng phương trình kiểm định score, không gọi lại hàm Wilson của mã tạo hình.
- Kiểm tra họ tên, MSSV, lớp, số trang, mục lục, 16 mục cuối kỳ, DOI, hình nhúng và lỗi trường tham chiếu.
- Đề cương ghi rõ các mô hình và điểm số kiểm tra là công việc dự kiến; chưa có kết quả huấn luyện được tạo ra trong đề cương.

## Kiểm tra bản trình bày

Hai DOCX được mở bằng Microsoft Word, cập nhật trường và mục lục, lưu rồi xuất PDF. PDF được kết xuất bằng Poppler thành ảnh để đọc trực quan toàn bộ trang 1–13 của mỗi báo cáo. Đã sửa lỗi chữ bìa sát khung, ngắt trang bảng, tiêu đề cột STT và đoạn công thức Wilson. Sau lần sửa cuối, đã xem lại các trang thay đổi: giữa kỳ 9, 10, 11, 13; cuối kỳ 3, 9, 10, 11. Các trang còn lại có ảnh kết xuất cùng SHA-256 với bản đã xem trước đó.

Kết quả đọc: không thấy chữ bị cắt, hình hoặc bảng tràn lề; tên thành viên và mục lục đọc được; chú thích và nguồn hình hiện đầy đủ. Ảnh kiểm tra hiện hành là `work/qa-mid/page-01.png` đến `page-13.png` và tương tự trong `work/qa-final`. Các ảnh có số lớn hơn 13, nếu còn, thuộc lần dàn trang trước và không phải bản PDF giao.

## Minh chứng nguồn và giới hạn hành chính

Ảnh SCImago người dùng gửi đã được lưu nguyên bản, đọc và đưa vào phụ lục giữa kỳ. Ảnh thể hiện Computer Science (Computer Science Applications, Information Systems) và Decision Sciences (Information Systems and Management). Ảnh cắt không chứa tên tạp chí; việc gắn với Data dựa trên ngữ cảnh trả lời đúng URL hồ sơ đã gửi. Không suy ra điểm SJR hoặc hạng Q từ ảnh này.

Bản PDF nghiên cứu trong nước tải về có lỗi bao tệp: hai dấu BOM trước đầu PDF và thiếu dấu kết thúc. Tệp nguồn được giữ nguyên; bản phục vụ đọc ở `work/domestic-tnu-readable.pdf` chỉ bỏ sáu byte đầu và thêm dấu kết thúc PDF, không sửa nội dung bài. Đã đọc đủ sáu trang để đối chiếu phương pháp và số liệu.

Tên giảng viên, thông tin liên hệ và chữ ký chưa được người dùng cung cấp nên không tự điền. Những ô duyệt chính thức còn để trống. Chưa nộp bài lên hệ thống, chưa gửi giảng viên và chưa in; các bước đó do nhóm thực hiện theo lịch môn học.
