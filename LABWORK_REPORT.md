# Báo cáo bài tập Python 2026-2027

Sinh viên: Trương Quý Nhật Hiếu, 2410287. Kiểm chứng ngày 08/10/2026.

## Nguồn yêu cầu

[Thư mục môn học](https://drive.google.com/drive/folders/17cWgUNkzYeh7GmEq2Fj_QQamldU24zbs)
có 5 PDF Labworks và 4 PDF Slides tại lần kiểm kê gần nhất.

| Đề | Bài và file trong repository |
| --- | --- |
| `labwork1.pdf` | 12 bài Python cơ bản, `labwork1.py` |
| `labwork1b-student-management.pdf` | Practical Work 1, `labwork1b.py` |
| `labwork2.pdf` | Fork, README, commit và push; xem `LABWORK2.md` |
| `labwork3-modules-package.pdf` | PW3: `3.student.mark.oop.math.py`; PW4: `pw4/` |
| `labwork4-files.pdf` | PW5: `pw5/` |

Đã đọc đầy đủ 2 trang đề PW5 và 38 trang bài giảng
`4. Files and Directories.pdf` trước khi triển khai phần lưu dữ liệu.

## Các sửa lỗi

- `labwork1b.py` từ chối ID rỗng hoặc trùng và cho nhập lại. Điểm hai sinh viên có ID riêng được lưu riêng.
- PW3 có menu nhập sinh viên, môn, điểm và xem các bảng kết quả, thay cho chương trình chỉ chạy dữ liệu mẫu trên GitHub cũ.
- PW4 giữ đầy đủ các chức năng của PW3 khi tách module.
- PW3, PW4 và PW5 phân trang theo chiều cao màn hình, cuộn ngang bằng Left/Right để xem GPA ở terminal 40 cột.
- Các hàm nhập cho nhập lại ID trùng. Lớp quản lý từ chối ID rỗng, tín chỉ không phải số nguyên dương và điểm không hữu hạn.
- `requirements.txt` ở gốc gồm NumPy và `windows-curses` cho Windows.
- Báo cáo dùng đúng tên file trong repository; xem `RUNNING_LABS.md` để chạy và kiểm thử.

## Practical Work 5

PW5 sao chép PW4 và thêm `persistence.py`. Sau thao tác nhập thành công,
chương trình ghi `students.txt`, `courses.txt`, `marks.txt` bằng JSON UTF-8.
Khi thoát, ZIP DEFLATE nén ba file thành `students.dat`. Khi mở lại, chương
trình kiểm tra và khôi phục dữ liệu từ archive. Các kỹ thuật JSON, file tạm,
`with open`, ngoại lệ và `zipfile` đều có trong bài giảng.

Test hai tiến trình xác nhận tên tiếng Việt, điểm đã làm tròn và GPA còn đúng
sau khi thoát và chạy lại. Các test archive rỗng/hỏng, JSON hỏng, ID trùng,
tham chiếu sai và lỗi thay archive xác nhận dữ liệu cũ được giữ lại.

## Bằng chứng kiểm thử

Chạy từ thư mục gốc bằng Python 3.12:

```text
python -B -m unittest discover -s tests -v
```

Bộ test gồm 14 test, đã chạy qua. Các nhóm kiểm tra bao gồm 12 bài Lab1,
ID rỗng/trùng, điểm 0 và 10, điểm ngoài khoảng và NaN, tín chỉ không hợp lệ,
GPA theo tín chỉ, thứ tự GPA, menu curses mô phỏng, phân trang, cuộn ngang,
lưu file, nén, khôi phục và bảo toàn dữ liệu khi có lỗi.

## Trạng thái và giới hạn

| Bài | Trạng thái chức năng local |
| --- | --- |
| Labwork 1 | PASS, với lưu ý danh sách màu bên dưới |
| Labwork 1b | PASS |
| Labwork 2 | PASS: đúng fork và có commit `First student commit` |
| PW3 | PARTIAL: chức năng qua test, chưa đối chiếu được nguồn PW2 |
| PW4 | PARTIAL: chức năng qua test, kế thừa giới hạn nguồn PW2 |
| PW5 | PASS các yêu cầu lưu, nén, khôi phục đã đọc; kế thừa giới hạn nguồn PW2 |

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
