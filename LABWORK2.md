# Labwork 2 (Practical Work 2) - GitHub và nộp bài

Theo phản hồi giảng viên được sinh viên cung cấp ngày 11/10/2026, PW2 là
thực hành GitHub và nộp Labwork 1/1b vào fork của
[`phuongnghiem/Python-2026-L2`](https://github.com/phuongnghiem/Python-2026-L2).
PDF Labwork 2 dùng tên L1; phản hồi mới xác nhận nơi nộp là L2.

## Bản nộp đã kiểm chứng ngày 11/10/2026

1. Tạo [fork L2 của sinh viên](https://github.com/NhatHieu2808/Python-2026-L2).
   Metadata GitHub xác nhận `fork=true`, `parent` và `source` đều là
   `phuongnghiem/Python-2026-L2`.
2. Giữ tiêu đề README gốc, ghi Trương Quý Nhật Hiếu và mã 2410287,
   tạo commit `First student commit` đúng yêu cầu PDF.
3. Nộp `labwork1.py` và `labwork1b.py` giữ nguyên nội dung từ bản L1.
   Hai bài chạy bằng Python 3 và thư viện chuẩn.
4. Push [commit nộp bài](https://github.com/NhatHieu2808/Python-2026-L2/commit/02437873359706e18a9d55cb6bb76dd8667a0f4a).
   Đã đọc lại SHA nhánh `main`, README và hai file từ GitHub; SHA-256 của
   hai file khớp bản local L2 và bản nguồn L1.

Kiểm tra tại thư mục L2: 12 bài Labwork 1 và bốn trường hợp tìm màu PASS;
hai lượt chạy CLI với Red và Green thoát mã 0. Luồng Labwork 1b dùng dữ liệu
thử gồm hai sinh viên, một môn, điểm 8.5 và 7.0; nhập, xem danh sách và xem
điểm đều PASS. ID có số 0 đầu và tên tiếng Việt được giữ nguyên. Kiểm tra
nhập lại ID rỗng/trùng và điểm không hợp lệ cũng PASS.

## Chương trình nền cho PW3

Giảng viên xác nhận PW2 được nhắc trong đề PW3 chính là chương trình
Labwork 1b. PW3 giữ các chức năng nhập sinh viên, môn, điểm, liệt kê sinh
viên/môn và xem điểm từng môn; bổ sung lớp, tín chỉ, làm tròn, GPA và curses
theo đề PW3. Các bài tiếp theo và báo cáo hiện nằm trong
[repo L1](https://github.com/NhatHieu2808/Python-2026-L1).
