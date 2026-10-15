# Chạy bài tập và kiểm thử

Từ thư mục gốc repository, cài các thư viện trong `requirements.txt`:

```text
python -m pip install -r requirements.txt
```

Chạy từng bài:

```text
python labwork1.py
python labwork1b.py
python 3.student.mark.oop.math.py
python pw4/main.py
python pw5/main.py
python pw5/extras.py
python labwork5_pandas/main.py
python labwork6_matplotlib/main.py
python labwork6_pandas_plot/main.py
python 2.student.mark.oop.py
```

Trên Windows, requirements cài `windows-curses`. PW3, PW4 và PW5 dùng curses
khi chạy trong terminal tương tác. Khi chuyển hướng input/output hoặc thiếu
curses, chương trình dùng menu console.

Trong ô nhập curses, gõ tên tiếng Việt rồi nhấn Enter. Backspace xóa ký tự
cuối; chuỗi dài tự cuộn ngang và vẫn được giữ đầy đủ. Nếu terminal có dưới
4 dòng hoặc dưới 12 cột, phóng to để nhập tiếp; nội dung đã gõ được giữ lại.

Trong bảng curses, dùng Up/Down hoặc PageUp/PageDown để chuyển trang.
Dùng Left/Right để xem các cột bị khuất và q hoặc Enter để quay lại.

PW5 mặc định lưu dữ liệu trong `pw5/`. Để chạy với một thư mục dữ liệu riêng:

```text
python pw5/main.py --data-dir demo-data
```

Đọc [hướng dẫn PW5](pw5/README.md) trước khi sửa các file dữ liệu.

Labwork 5a dùng dữ liệu PW5 đã lưu. Chạy `python pw5/extras.py --data-dir
demo-data` sau khi nhập và lưu bằng `pw5/main.py` với cùng `--data-dir`.
Script tạo ba CSV và snapshot pickle trong `demo-data/exports/`, đọc lại
CSV thành DataFrame và nhận điều kiện như `name = "Mr. Volunteers"`.
Xem [cú pháp và cách chạy bản ZIP](pw5/README.md#labwork-5a-pickle-csv-và-truy-vấn).

Labwork 5 Pandas đọc `students.csv` và `scores.csv` trong `labwork5_pandas/`.
Xem [hướng dẫn và cách xử lý dữ liệu thiếu](labwork5_pandas/README.md).
Để kiểm thử riêng bài mới:

```text
python -B -m unittest discover -s tests -p test_labwork5_pandas.py -v
```

Chạy bộ kiểm thử từ thư mục gốc:

```text
python -B -m unittest discover -s tests -v
```

Các test bài quản lý sinh viên tạo dữ liệu giả trong thư mục tạm và tự dọn
sau khi chạy. Test bài Pandas và Labwork 6 còn đối chiếu với CSV của giáo viên.

## Chạy Labwork 6a và 6b

Hai script dùng backend `Agg`, lưu hình mà không mở cửa sổ. Đường dẫn
dữ liệu và output được tính từ vị trí script, nên có thể chạy từ thư mục khác.
Labwork 6a ghi `labwork6_matplotlib/po.pdf`. Labwork 6b đọc CSV gốc tại
`labwork5_pandas/scores.csv`, ghi `scattered.png`, `histo.png` và `box.png`
trong `labwork6_pandas_plot/`. Chạy lại sẽ cập nhật các hình này.

Chạy kiểm thử riêng phần mới:

```text
python -B -m unittest discover -s tests -p test_labwork6.py -v
```

Test Labwork 6 chạy hai script từ thư mục tạm và tạo lại bốn output trong
thư mục bài. Xem [cách đọc các biểu đồ](labwork6_pandas_plot/README.md).

## Chạy Labwork 7 OOP

```text
python 2.student.mark.oop.py
python -B -m unittest discover -s tests -p test_labwork7.py -v
```

Bài dùng thư viện chuẩn. Nhập số sinh viên, ID/tên/ngày sinh, số môn và
ID/tên môn; nhập 0 nếu danh sách rỗng. Menu 1/2 liệt kê sinh viên/môn,
3 nhập điểm một môn, 4 xem điểm môn đó, 0 thoát. ID rỗng/trùng và điểm
không hợp lệ được yêu cầu nhập lại. Điểm từ 0 đến 10, không làm tròn;
`Not entered` nghĩa là chưa nhập điểm. Dữ liệu chỉ giữ trong bộ nhớ.
