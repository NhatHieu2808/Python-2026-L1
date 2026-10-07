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
```

Trên Windows, requirements cài `windows-curses`. PW3, PW4 và PW5 dùng curses
khi chạy trong terminal tương tác. Khi chuyển hướng input/output hoặc thiếu
curses, chương trình dùng menu console.

Trong bảng curses, dùng Up/Down hoặc PageUp/PageDown để chuyển trang.
Dùng Left/Right để xem các cột bị khuất và q hoặc Enter để quay lại.

PW5 mặc định lưu dữ liệu trong `pw5/`. Để chạy với một thư mục dữ liệu riêng:

```text
python pw5/main.py --data-dir demo-data
```

Đọc [hướng dẫn PW5](pw5/README.md) trước khi sửa các file dữ liệu.

Chạy bộ kiểm thử từ thư mục gốc:

```text
python -B -m unittest discover -s tests -v
```

Các test tạo dữ liệu giả trong thư mục tạm và tự dọn sau khi chạy.
