# Kiểm chứng tạp chí Data — 22/10/2026

## Đã xác minh được

1. **Scopus**: API serial metadata chính thức của Elsevier trả về tên Data, nhà xuất bản MDPI, eISSN 2306-5729 và liên kết nguồn Scopus có ID **21100924372**. File gốc `TaiLieuNguon/evidence-scopusapi.html` thực tế chứa JSON. API: https://api.elsevier.com/content/serial/title/issn/23065729?httpAccept=application%2Fjson . Hồ sơ nguồn: https://www.scopus.com/sourceid/21100924372 . Đây là bằng chứng trực tiếp về hồ sơ tạp chí; không phải truy vấn riêng từng bài trên Scopus.

2. **Lịch sử bao phủ**: trang lịch sử chính thức của nhà xuất bản ghi nhận Scopus lập chỉ mục năm 2019, bắt đầu từ tập 1 số 1; ESCI thuộc Web of Science từ năm 2017, bắt đầu tập 2 số 1. Bài được chọn xuất bản năm 2022 tập 7 nằm sau các mốc này. Không gọi ESCI là SCIE/SCI. Nguồn: https://www.mdpi.com/journal/data/history ; bản văn đã lưu `TaiLieuNguon/evidence-jina-history.txt`.

3. **Chỉ số có năm tham chiếu rõ ràng**: trang lịch sử ghi CiteScore **2019 = 2,1**, được công bố năm 2020. Có thể sử dụng để đáp ứng yêu cầu ghi CiteScore, nhưng phải ghi đúng năm và nói rõ đây là chỉ số lịch sử, không phải chỉ số năm 2022 hay hiện hành.

4. **Chỉ số đang hiển thị khi kiểm tra**: trang thống kê MDPI hiển thị Impact Factor 2,4; 5-year IF 2,5; CiteScore 5,4. Tuy nhiên văn bản tải về không nêu rõ năm tham chiếu các chỉ số; không tự gán 2024/2025. Không cần dùng các số này khi báo cáo đã dùng chỉ số lịch sử có năm rõ ràng. Nguồn https://www.mdpi.com/journal/data/stats ; bản lưu `TaiLieuNguon/evidence-jina-stats.txt`.

## Trạng thái trước khi nhận ảnh từ người dùng (đã được bổ sung bên dưới)

**Lĩnh vực lấy trực tiếp từ SCImago chưa xác minh được.** Trang https://www.scimagojr.com/journalsearch.php?q=21100924372&tip=sid trả 403 khi truy cập trực tiếp, và bản truy xuất công khai qua Jina chỉ chứa trang kiểm tra bảo mật. Tra theo ISSN và tải dữ liệu xếp hạng cũng không cho nội dung sử dụng được. Không ghi các nhóm ngành hoặc hạng Q là “theo SCImago” khi chưa đọc được hồ sơ.

Trang MDPI thống kê liệt kê các nhóm **CiteScore**: Information Systems and Management; Information Systems; Computer Science Applications. Đây là bằng chứng chính thức của nhà xuất bản cho nhóm CiteScore, **không thay thế yêu cầu lấy lĩnh vực từ SCImago**. Có thể dùng làm đối chiếu phụ và phải gắn đúng tên nguồn.

## Câu đề xuất đưa vào báo cáo

“Bài báo được công bố trên tạp chí Data (eISSN 2306-5729). Hồ sơ nguồn Scopus của tạp chí có ID 21100924372, được đối chiếu qua API serial metadata của Elsevier. Theo lịch sử tạp chí do MDPI công bố, Data được đưa vào Scopus năm 2019, bao phủ từ tập 1 số 1, và vào ESCI thuộc Web of Science năm 2017. CiteScore năm 2019 là 2,1, công bố năm 2020; đây là chỉ số lịch sử, không đại diện cho năm xuất bản bài báo. Các chỉ số tạp chí không thay thế việc đánh giá chất lượng phương pháp của từng nghiên cứu.”

Không chép nguyên văn dài từ các nguồn. Khi trích dẫn dùng liên kết gốc MDPI/Elsevier; ghi trong nhật ký kiểm chứng rằng MDPI được đọc qua dịch vụ văn bản Jina do truy cập trực tiếp lỗi 403. Các phản hồi tìm kiếm Bing không liên quan nên không dùng làm bằng chứng. Các URL flyer phỏng đoán đều 404, không sử dụng. Không chỉnh sửa tài liệu hay số liệu của root.

## Cập nhật sau khi nhận minh chứng

Ngày 22/10/2026, người dùng đã gửi ảnh phần **Subject Area and Category** để trả lời yêu cầu đối chiếu hồ sơ Data tại URL SCImago nêu trên. Bản sao giữ nguyên tại `TaiLieuNguon/scimago-subject-user.png`:

- **Computer Science:** Computer Science Applications; Information Systems.
- **Decision Sciences:** Information Systems and Management.

Root đã đọc ảnh, cập nhật mục thông tin tạp chí và đưa ảnh vào phụ lục báo cáo giữa kỳ. Khoảng thiếu về lĩnh vực đã được giải quyết bằng minh chứng người dùng cung cấp. Ảnh cắt không chứa tiêu đề tạp chí; liên hệ ảnh với Data dựa trên ngữ cảnh người dùng trả lời đúng yêu cầu và URL, không phải một lần truy cập trực tiếp thành công của công cụ. Ảnh không chứng minh điểm SJR, hạng Q hoặc năm chỉ số; báo cáo không đưa ra các khẳng định đó.
