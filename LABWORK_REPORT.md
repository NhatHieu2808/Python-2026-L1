# Báo cáo bài tập Python 2026-2027

Sinh viên: Trương Quý Nhật Hiếu, 2410287. Kiểm thử tự động ngày 10/10/2026.
Kiểm chứng curses thật ngày 08/10/2026.
Đối chiếu phản hồi giảng viên và kiểm chứng bản nộp PW2 ngày 11/10/2026.
Kiểm chứng riêng Labwork 6a và 6b ngày 14/10/2026.

## Nguồn yêu cầu

[Thư mục môn học](https://drive.google.com/drive/folders/17cWgUNkzYeh7GmEq2Fj_QQamldU24zbs)
có 6 PDF Labworks, 5 PDF Slides và 2 CSV tại lần kiểm kê ngày 08/10/2026.

| Đề | Bài và file trong repository |
| --- | --- |
| `labwork1.pdf` | 12 bài Python cơ bản, `labwork1.py` |
| `labwork1b-student-management.pdf` | Practical Work 1, `labwork1b.py` |
| `labwork2.pdf` | PW2: fork L2, README, commit và nộp Labwork 1/1b; xem `LABWORK2.md` |
| `labwork3-modules-package.pdf` | PW3: `3.student.mark.oop.math.py`; PW4: `pw4/` |
| `labwork4-files.pdf` | PW5: `pw5/` |
| `labwork5.pdf` | 14 yêu cầu Pandas: `labwork5_pandas/main.py` |
| `labwork6a-matplotlib.txt` | Hàm số và PDF: `labwork6_matplotlib/main.py` |
| `labwork6b-pandas-plot.txt` | Scatter, histogram và boxplot: `labwork6_pandas_plot/main.py` |

Đã đọc đầy đủ 2 trang đề PW5 và 38 trang bài giảng
`4. Files and Directories.pdf` trước khi triển khai phần lưu dữ liệu.

## Các sửa lỗi

- `labwork1b.py` từ chối ID rỗng hoặc trùng và cho nhập lại. Điểm hai sinh viên có ID riêng được lưu riêng.
- PW3 có menu nhập sinh viên, môn, điểm và xem các bảng kết quả, thay cho chương trình chỉ chạy dữ liệu mẫu trên GitHub cũ.
- PW4 giữ đầy đủ các chức năng của PW3 khi tách module.
- PW3, PW4 và PW5 phân trang theo chiều cao màn hình, cuộn ngang bằng Left/Right để xem GPA ở terminal 40 cột.
- Các hàm nhập cho nhập lại ID trùng. Lớp quản lý từ chối ID rỗng, tín chỉ không phải số nguyên dương và điểm không hữu hạn.
- `requirements.txt` ở gốc gồm NumPy, Pandas, Matplotlib và `windows-curses` cho Windows.
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

## Labwork 5a: pickle, CSV và query

Nguồn: [TXT bổ sung của giảng viên](https://drive.google.com/file/d/1_XvMWLd4JLAx1SNUjE7s49P7fmHtlfOf/view).
`pw5/extras.py` dùng dữ liệu PW5 để thực hiện bốn phần còn thiếu: pickle
round-trip, xuất ba CSV, đọc cả ba thành DataFrame và truy vấn sinh viên
bằng một điều kiện bằng. Hiểu `Po` là Pandas theo ngữ cảnh bài giảng.
Pickle là snapshot riêng, không thay TXT hoặc ZIP và chỉ đọc file vừa
được chính chương trình tạo trong luồng thực hành.

Sáu test mới PASS: giữ Unicode, dấu phẩy/nháy, ID `001`, tên `NA`, số tín
chỉ và điểm; CSV rỗng có header; pickle giữ bản ghi và không đụng archive
cũ khi lỗi ghi; từ chối cột hoặc liên kết sai; truy vấn trả tất cả người
trùng tên và xử lý input không hợp lệ. Test tiến trình thật nhập và lưu
bằng `pw5/main.py`, sau đó chạy `extras.py` từ thư mục khác để xuất, đọc
DataFrame và nhập điều kiện. Lệnh và cú pháp ở [hướng dẫn PW5](pw5/README.md).

Bản `pw5_completed.zip` có 11 file, CRC và mã Python khớp nguồn. Đã giải
nén vào thư mục tạm và chạy hai tiến trình độc lập với dữ liệu thử: 3 sinh
viên, 1 môn, 2 điểm. Truy vấn trả đúng `Nguyễn, "An"`; archive PW5 không
đổi sau khi chạy phần mở rộng. ZIP không chứa cache hoặc dữ liệu phát sinh.

## Labwork 6a và 6b

Nguồn: [đề 6a](https://drive.google.com/file/d/1ZLfUQmONuNF2Wd_LDoyhGprvg8bYjWPU/view),
[đề 6b](https://drive.google.com/file/d/1_-Q29uunJXDu2mYZmnpuEZ0slM66PaQK/view)
và [slide Data Visualization](https://drive.google.com/file/d/13EE5qIipM4NKzeaxOzEETM9ylqKP3jNN/view).
Đối chiếu các trang liên quan về plot, nhãn, savefig, scatter, histogram,
boxplot và Pandas plotting; không dùng thêm Seaborn.

6a vẽ `y = 2*x + sin(x)**2 + 3` tại 1001 điểm gồm hai đầu [-5, 5],
bật grid, đặt tiêu đề `hello, po!`, nhãn x/y và xuất `po.pdf`.
6b đọc CSV gốc, dùng `plot.scatter`, `plot.hist` và `plot.box` của Pandas
để xuất `scattered.png`, `histo.png` và `box.png`. Trục X scatter là thứ tự
sinh viên trong CSV, một lựa chọn triển khai vì đề không quy định trục.
Histogram có ba subplot; boxplot có một axes và ba box.

Ngày 14/10/2026: Python 3.12.14, NumPy 2.5.3, Pandas 3.0.6,
Matplotlib 3.11.2. Ba test tập trung PASS:

```text
python -B -m unittest discover -s tests -p test_labwork6.py -v
```

Kiểm tra đường cong với công thức độc lập bằng `math.sin`, `y(0)=3`,
nhãn và grid; đối chiếu từng điểm scatter với `csv.DictReader`, tần suất
histogram và trung vị/tứ phân vị boxplot với dữ liệu gốc. Hai CLI chạy
từ thư mục khác, thoát mã 0 và tạo đúng bốn output. Số điểm hợp lệ là
Python 30, Math 28, Database 29; ô thiếu được bỏ qua riêng từng môn.
SHA-256 CSV không đổi và khớp bản nguồn:
`7f335eb4aa7d5a0d5ab3dd62c3a6fd072945013ff8745cb33677402355ebe8d3`.

Đã mở xem ba PNG, kiểm tra PDF một trang bằng `pdfinfo`, render và xem
hình PDF: có dữ liệu, nhãn rõ, không cắt hoặc chồng chữ. `pip check` PASS.
Không chạy lại bộ test bài cũ trong đợt này; kết quả 26 test ngày 10/10/2026
ở phần dưới là lịch sử, không phải kết quả kiểm thử mới.

## Bằng chứng kiểm thử

Chạy từ thư mục gốc bằng Python 3.12:

```text
python -B -m unittest discover -s tests -v
```

Bộ test ngày 10/10/2026 có 26 test và đã chạy qua: 14 test bài cũ, 3 test Pandas,
3 test hồi quy Unicode và 6 test Labwork 5a. Các nhóm kiểm tra bao gồm 12 bài Lab1,
ID rỗng/trùng, điểm 0 và 10, điểm ngoài khoảng và NaN, tín chỉ không hợp lệ,
GPA theo tín chỉ, thứ tự GPA, menu curses mô phỏng, phân trang, cuộn ngang,
lưu file, nén, khôi phục và bảo toàn dữ liệu khi có lỗi. Test Unicode kiểm tra
cả ba phiên bản với ASCII, tên tiếng Việt dài, dấu tổ hợp và ký tự rộng;
kiểm tra Backspace, nhập rỗng, phím đặc biệt, resize và khôi phục tên PW5.

Ngày 11/10/2026 đã kiểm chứng riêng bản nộp tại thư mục L2: 12 bài Labwork
1 và bốn kiểm tra màu PASS; chạy CLI với Red và Green đều thoát mã 0.
Labwork 1b chạy CLI bằng dữ liệu thử hai sinh viên, một môn, điểm 8.5 và
7.0; nhập, liệt kê và xem điểm PASS, giữ tên tiếng Việt và ID có số 0 đầu.
Kiểm tra nhập lại ID rỗng/trùng và điểm không hợp lệ PASS. Nội dung hai file
đọc lại từ GitHub khớp SHA-256 với bản L1 và bản local L2. Không chạy lại
toàn bộ 26 test; kết quả bộ test đó vẫn thuộc ngày 10/10/2026.

## Trạng thái và xác nhận của giảng viên

| Bài | Trạng thái chức năng local |
| --- | --- |
| Labwork 1 | PASS: giảng viên cho phép tự chọn danh sách màu |
| Labwork 1b | PASS |
| Labwork 2 (PW2) | PASS: đúng fork L2, commit `First student commit` và hai bài đã xác nhận trên remote |
| PW3 | PASS: kế thừa chức năng Labwork 1b, bổ sung làm tròn, GPA, NumPy và curses |
| PW4 | PASS: tách PW3 thành module và package theo đề |
| PW5 | PASS: lưu, nén và khôi phục theo đề |
| Labwork 5a | PASS: pickle, ba CSV, ba DataFrame và query; 6 test riêng đã qua |
| Labwork 5 Pandas | PASS: 14/14 yêu cầu, 3 test riêng đã qua |
| Labwork 6a | PASS: công thức, khoảng, nhãn, grid và PDF đã kiểm chứng ngày 14/10/2026 |
| Labwork 6b | PASS: ba dạng biểu đồ và dữ liệu gốc đã kiểm chứng ngày 14/10/2026 |

### Phản hồi giảng viên được cung cấp ngày 11/10/2026

Sinh viên cung cấp phản hồi trực tiếp của giảng viên, xác nhận:

- PW2 là thực hành GitHub và nộp Labwork 1/1b lên fork của
  [`phuongnghiem/Python-2026-L2`](https://github.com/phuongnghiem/Python-2026-L2).
  Đã hoàn thành tại [fork L2 của sinh viên](https://github.com/NhatHieu2808/Python-2026-L2),
  [commit `0243787`](https://github.com/NhatHieu2808/Python-2026-L2/commit/02437873359706e18a9d55cb6bb76dd8667a0f4a).
  Metadata GitHub xác nhận `parent` và `source` đúng repo L2; SHA nhánh
  `main`, hai bài và README đã được đọc lại từ remote.
- PW2 được nhắc trong PW3 chính là Labwork 1b. Đối chiếu `labwork1b.py`
  với `3.student.mark.oop.math.py` xác nhận các trường sinh viên và môn,
  nhập điểm theo môn, liệt kê sinh viên/môn và xem điểm được kế thừa.
  Trang 2 đề PW3 yêu cầu thêm `math.floor`, GPA theo tín chỉ bằng NumPy,
  sắp xếp GPA giảm dần và curses; các phần này đã có trong PW3 và có
  bằng chứng kiểm thử trước đó. Giới hạn nguồn PW2 trước đây đã được giải đáp.
- Python Language kết thúc ở slide `63/66` là đúng theo giảng viên.
- Labwork 1 câu 5 được tự chọn danh sách màu. Giữ
  `["Blue", "Yellow", "White", "Red"]`: Red trả về 3, Green trả về -1,
  Blue trả về 0 và danh sách rỗng trả về -1; bốn trường hợp đã chạy PASS.

Đợt nộp L2 này gồm Labwork 1/1b theo phản hồi của giảng viên. PW3, PW4,
PW5 và các bài Pandas hiện vẫn nằm trong repo L1. Hai điểm thiếu căn cứ
trước đây về PW2 và danh sách màu đã được giải đáp bằng phản hồi trên.

Đã kiểm tra curses thật với `windows-curses` 2.4.2: menu PW3, PW4, PW5
nhập sinh viên, môn, điểm và xem kết quả. PW5 khôi phục tên tiếng Việt và
GPA `8.70` sau khi đóng rồi mở lại. Màn hình thật 10x40 với 30 sinh viên
đã chuyển trang và cuộn ngang để xem GPA trong cả PW3, PW4 và PW5.

Trạng thái push được xác nhận riêng bằng commit và nội dung đọc lại từ GitHub.
