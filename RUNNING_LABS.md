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

Các test tạo dữ liệu giả trong thư mục tạm và tự dọn sau khi chạy.
