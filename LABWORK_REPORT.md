# Báo cáo bài tập Python 2026-2027

Sinh viên: Trương Quý Nhật Hiếu, 2410287. Kiểm chứng ngày 08/10/2026.

## Nguồn yêu cầu

[Thư mục môn học](https://drive.google.com/drive/folders/17cWgUNkzYeh7GmEq2Fj_QQamldU24zbs)
có 6 PDF Labworks, 5 PDF Slides và 2 CSV tại lần kiểm kê ngày 08/10/2026.

| Đề | Bài và file trong repository |
| --- | --- |
| `labwork1.pdf` | 12 bài Python cơ bản, `labwork1.py` |
| `labwork1b-student-management.pdf` | Practical Work 1, `labwork1b.py` |
| `labwork2.pdf` | Fork, README, commit và push; xem `LABWORK2.md` |
| `labwork3-modules-package.pdf` | PW3: `3.student.mark.oop.math.py`; PW4: `pw4/` |
| `labwork4-files.pdf` | PW5: `pw5/` |
| `labwork5.pdf` | 14 yêu cầu Pandas: `labwork5_pandas/main.py` |

Đã đọc đầy đủ 2 trang đề PW5 và 38 trang bài giảng
`4. Files and Directories.pdf` trước khi triển khai phần lưu dữ liệu.

## Các sửa lỗi

- `labwork1b.py` từ chối ID rỗng hoặc trùng và cho nhập lại. Điểm hai sinh viên có ID riêng được lưu riêng.
- PW3 có menu nhập sinh viên, môn, điểm và xem các bảng kết quả, thay cho chương trình chỉ chạy dữ liệu mẫu trên GitHub cũ.
- PW4 giữ đầy đủ các chức năng của PW3 khi tách module.
- PW3, PW4 và PW5 phân trang theo chiều cao màn hình, cuộn ngang bằng Left/Right để xem GPA ở terminal 40 cột.
- Các hàm nhập cho nhập lại ID trùng. Lớp quản lý từ chối ID rỗng, tín chỉ không phải số nguyên dương và điểm không hữu hạn.
- `requirements.txt` ở gốc gồm NumPy, Pandas và `windows-curses` cho Windows.
- Báo cáo dùng đúng tên file trong repository; xem `RUNNING_LABS.md` để chạy và kiểm thử.

## Sửa lỗi P2 nhập Unicode trong curses

PW3, PW4 và PW5 dùng `get_wch()` với bộ đệm ký tự Unicode, thay cho giới hạn
byte của `getstr()`. Chuỗi dài cuộn vùng hiển thị theo độ rộng ký tự, không
cắt dữ liệu. Enter, Backspace, nhập rỗng và resize đã được kiểm tra. Phím
điều hướng và các phím đặc biệt không được thêm vào chuỗi.

Đã kiểm chứng curses thật trên Windows, `windows-curses` 2.4.2: cả ba phiên
bản giữ nguyên `Nguyễn Trương Thị Phương Thảo` (29 ký tự, 39 byte UTF-8)
và chuỗi lặp hai tên (59 ký tự) ở màn hình 10x40. Nhập ASCII, Backspace,
nhập rỗng và thu nhỏ rồi phóng lại màn hình hoạt động. PW5 lưu tên nhập
qua curses và một tiến trình mới khôi phục đúng tên từ `students.dat`.

## Practical Work 5

PW5 sao chép PW4 và thêm `persistence.py`. Sau thao tác nhập thành công,
chương trình ghi `students.txt`, `courses.txt`, `marks.txt` bằng JSON UTF-8.
Khi thoát, ZIP DEFLATE nén ba file thành `students.dat`. Khi mở lại, chương
trình kiểm tra và khôi phục dữ liệu từ archive. Các kỹ thuật JSON, file tạm,
`with open`, ngoại lệ và `zipfile` đều có trong bài giảng.

Test hai tiến trình xác nhận tên tiếng Việt, điểm đã làm tròn và GPA còn đúng
sau khi thoát và chạy lại. Các test archive rỗng/hỏng, JSON hỏng, ID trùng,
tham chiếu sai và lỗi thay archive xác nhận dữ liệu cũ được giữ lại.

## Labwork 5 Pandas

`labwork5_pandas/main.py` thực hiện đủ 14 yêu cầu của `labwork5.pdf`,
dùng hai CSV của giáo viên. Phần 1 phân tích dữ liệu gốc; phần 2 điền ô
số thiếu bằng trung bình cột trên bản sao, ghép theo `student_id`, tính
trung bình ba môn, top 5 và điểm trung bình theo ngành. Các giá trị điền
được ghi rõ là ước tính. Xem [hướng dẫn bài](labwork5_pandas/README.md).

Đã chạy bằng Python 3.12.14, Pandas 3.0.6 và NumPy 2.5.3:

```text
python labwork5_pandas/main.py
python -B -m unittest discover -s tests -p test_labwork5_pandas.py -v
```

Script thoát với mã 0. Ba test riêng đã qua, kiểm tra phân tích dữ liệu gốc,
làm sạch và ghép bảng, trung bình từng sinh viên và ngành, thứ tự top 5,
đủ 14 mục output, chạy từ thư mục khác và bảo toàn CSV. Kết quả được đối
chiếu bằng `csv` và `statistics.mean` độc lập với các phép tính Pandas.

Dữ liệu có 30 sinh viên; ban đầu thiếu 1 `age`, 2 `GPA`, 2 `math` và
1 `database`. Sau xử lý còn 0 ô thiếu. Top 5 theo điểm trung bình là
Tina (96.333333), Kate (95), David (93.333333), Grace (93), Zack (92.333333).
SHA-256 của hai CSV trong bài khớp bản tải từ Drive và không đổi sau khi chạy.
`pip check` không phát hiện dependency hỏng.

## Bằng chứng kiểm thử

Chạy từ thư mục gốc bằng Python 3.12:

```text
python -B -m unittest discover -s tests -v
```

Bộ test hiện có 20 test và đã chạy qua: 14 test bài cũ, 3 test Pandas,
3 test hồi quy Unicode. Các nhóm kiểm tra bao gồm 12 bài Lab1,
ID rỗng/trùng, điểm 0 và 10, điểm ngoài khoảng và NaN, tín chỉ không hợp lệ,
GPA theo tín chỉ, thứ tự GPA, menu curses mô phỏng, phân trang, cuộn ngang,
lưu file, nén, khôi phục và bảo toàn dữ liệu khi có lỗi. Test Unicode kiểm tra
cả ba phiên bản với ASCII, tên tiếng Việt dài, dấu tổ hợp và ký tự rộng;
kiểm tra Backspace, nhập rỗng, phím đặc biệt, resize và khôi phục tên PW5.

## Trạng thái và giới hạn

| Bài | Trạng thái chức năng local |
| --- | --- |
| Labwork 1 | PASS, với lưu ý danh sách màu bên dưới |
| Labwork 1b | PASS |
| Labwork 2 | PASS: đúng fork và có commit `First student commit` |
| PW3 | PARTIAL: chức năng qua test, chưa đối chiếu được nguồn PW2 |
| PW4 | PARTIAL: chức năng qua test, kế thừa giới hạn nguồn PW2 |
| PW5 | PASS các yêu cầu lưu, nén, khôi phục đã đọc; kế thừa giới hạn nguồn PW2 |
| Labwork 5 Pandas | PASS: 14/14 yêu cầu, 3 test riêng đã qua |

Đề Lab1 không cung cấp danh sách màu gốc. Chương trình dùng danh sách mẫu
có Red ở index 3 và hàm `find_color` nhận danh sách truyền vào.

Chưa tìm thấy đề hoặc starter Practical Work 2 trong inventory và phần
Practice đã kiểm tra. Đây không phải Labwork 2 về Git. Báo cáo không khẳng
định đã tái tạo chính xác starter PW2 hoặc đã đọc mọi slide của các chương cũ.

Đã kiểm tra curses thật với `windows-curses` 2.4.2: menu PW3, PW4, PW5
nhập sinh viên, môn, điểm và xem kết quả. PW5 khôi phục tên tiếng Việt và
GPA `8.70` sau khi đóng rồi mở lại. Màn hình thật 10x40 với 30 sinh viên
đã chuyển trang và cuộn ngang để xem GPA trong cả PW3, PW4 và PW5.

Trạng thái push được xác nhận riêng bằng commit và nội dung đọc lại từ GitHub.
