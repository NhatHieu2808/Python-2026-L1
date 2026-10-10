# Practical Work 5: lưu và khôi phục dữ liệu

PW5 sao chép cấu trúc PW4 và bổ sung `persistence.py`. Các chức năng nhập
sinh viên, môn học, điểm và các bảng kết quả giữ nguyên.

## Chạy chương trình

Từ thư mục gốc repository:

```text
python -m pip install -r requirements.txt
python pw5/main.py
```

Nhập dữ liệu bằng menu. Chọn `0` để nén dữ liệu và thoát.
Chạy lại chương trình để khôi phục dữ liệu đã lưu.

## File dữ liệu

Sau mỗi thao tác nhập thành công, chương trình ghi ba file JSON UTF-8:

- `students.txt`: danh sách ID, họ tên và ngày sinh.
- `courses.txt`: danh sách ID, tên môn và số tín chỉ.
- `marks.txt`: danh sách ID sinh viên, ID môn và điểm đã làm tròn xuống.

JSON là định dạng văn bản được so sánh với pickle trong bài giảng.
`ensure_ascii=False` giữ tên tiếng Việt đọc được trong các file.

Khi thoát, `zipfile.ZIP_DEFLATED` nén đúng ba file thành `students.dat`.
`zipfile` có trong phần Compression của bài giảng và hỗ trợ nhiều file trong
một archive. Phần mở rộng `.dat` tuân theo đề bài, nội dung bên trong là ZIP.

Mặc định, dữ liệu nằm cạnh `main.py`, không phụ thuộc thư mục gọi chương trình.
Tham số `--data-dir` chọn thư mục dữ liệu riêng để kiểm thử hoặc giữ các bộ dữ liệu khác nhau.

## Khôi phục và xử lý lỗi

Nếu có `students.dat`, chương trình đọc archive, kiểm tra đủ ba file, kiểm tra
JSON, ID, tín chỉ, điểm và tham chiếu trước khi khôi phục các file `.txt`.
Nếu không có archive nhưng đủ ba file `.txt`, chương trình đọc dữ liệu từ chúng.
Lần chạy đầu chưa có file sẽ bắt đầu với danh sách rỗng.

Danh sách rỗng hợp lệ được lưu bằng `[]`. File rỗng, JSON hỏng, ID trùng,
tham chiếu không tồn tại hoặc archive hỏng làm chương trình dừng khi khởi động.
Chương trình không tiếp tục bằng dữ liệu rỗng rồi ghi đè archive lỗi.
Khôi phục một bản sao hợp lệ trước khi chạy lại.

Archive mới được ghi vào file tạm rồi thay thế `students.dat`.
Nếu lưu thất bại khi chọn thoát, menu giữ dữ liệu trong bộ nhớ và cho thử lại.

Khi đồng thời tồn tại archive và các file `.txt`, archive là nguồn khôi phục
theo đề bài. Nếu sửa `.txt` thủ công, chuyển archive cũ sang nơi sao lưu trước
khi mở chương trình để nạp ba file `.txt`.

## Labwork 5a: pickle, CSV và truy vấn

[Đề bổ sung](https://drive.google.com/file/d/1_XvMWLd4JLAx1SNUjE7s49P7fmHtlfOf/view)
yêu cầu pickle và xuất dữ liệu quản lý sang CSV để truy vấn bằng DataFrame.
Chữ `Po` trong TXT được hiểu là Pandas theo ngữ cảnh bài giảng.

Nhập và lưu dữ liệu bằng `main.py`, sau đó chạy từ gốc repository:

```text
python pw5/main.py --data-dir demo-data
python pw5/extras.py --data-dir demo-data
```

Nếu chạy bản PW5 độc lập sau khi giải nén ZIP, dùng:

```text
python -m pip install -r requirements.txt
python main.py --data-dir demo-data
python extras.py --data-dir demo-data
```

`extras.py` dùng cùng quy tắc nạp dữ liệu của PW5. Các file mới nằm trong
`demo-data/exports/`, tách khỏi CSV phân tích trong `labwork5_pandas/`:

| File | Cột hoặc nội dung |
| --- | --- |
| `students.csv` | `id`, `name`, `dob` |
| `courses.csv` | `id`, `name`, `credits` |
| `marks.csv` | `student_id`, `course_id`, `score` |
| `snapshot.pkl` | Các bản ghi sinh viên, môn và điểm |

CSV dùng UTF-8 và có header khi dữ liệu rỗng. Pandas đọc đủ ba file, giữ
ID và trường văn bản là chuỗi, gồm cả tên `NA`. Bộ nạp kiểm tra cột,
ID, tín chỉ, điểm và liên kết sinh viên với môn trước khi truy vấn.

Dòng đề về pickle không quy định thay thế cơ chế lưu cũ. Phần thực hành
dùng `pickle.dump` và `pickle.load` trên cùng file tạm vừa tạo, đối chiếu
bản ghi rồi lưu thành `snapshot.pkl`. Chương trình không nạp snapshot
có sẵn hoặc file pickle từ bên ngoài. TXT và `students.dat` vẫn là dữ liệu
của chương trình chính.

Nhập một điều kiện bằng với giá trị trong dấu nháy kép:

```text
name = "Mr. Volunteers"
id == "001"
```

Các cột được hỗ trợ là `id`, `name`, `dob`. Giá trị dùng escape JSON,
ví dụ `name = "Nguyễn, \"An\""`. Chương trình lọc bằng boolean mask,
không thực thi chuỗi nhập. Người trùng tên đều xuất hiện. Điều kiện sai
trả thông báo và mã thoát 2. Không có kết quả được thông báo rõ; Enter
không nhập điều kiện bỏ qua truy vấn. Chạy lại lệnh để nhập điều kiện khác.

Kiểm thử riêng phần này từ gốc repository:

```text
python -B -m unittest discover -s tests -p test_pw5_extras.py -v
```
