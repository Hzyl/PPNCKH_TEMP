# Bộ bài PPNCKH của nhóm 4 lớp DCT123C4

Cập nhật ngày 06/11/2026 theo phần hướng dẫn mới của giảng viên do người dùng cung cấp.

## Bài hiện hành

- Giữa kỳ: `BaiGiuaKy/GiuaKy_Nhom4_DCT123C4.docx` và `.pdf`. Giữ nguyên; làm việc với một bài báo nền tảng, hai hình vẽ lại và một hình mới.
- Cuối kỳ: `BaiCuoiKy/PPNCKH_3123411114_3123411120_3123411144_3123411151_3123411064.docx` và `.pdf`. Bản mới 18 trang kể cả bìa, tổng quan 5 bài và đề cương theo 5 phần: Giới thiệu, Tổng quan, Phương pháp đề xuất, Kế hoạch, Kết quả dự kiến.
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
