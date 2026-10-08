# Chạy Labwork 5 Pandas

Từ thư mục gốc repository, cài thư viện và chạy bài:

```text
python -m pip install -r requirements.txt
python labwork5_pandas/main.py
```

Script đọc hai CSV đi kèm theo đường dẫn của `main.py`, nên có thể chạy
bằng đường dẫn tuyệt đối từ thư mục khác. Output đánh số `1.1` đến `1.7`
và `2.1` đến `2.7` theo 14 yêu cầu của đề.

Phần 1 dùng `students.csv` gốc. Các GPA thiếu nằm cuối bảng sắp xếp và
không tham gia tính GPA trung bình theo ngành.

Phần 2 sao chép dữ liệu trong bộ nhớ. Các ô thiếu ở `age`, `GPA`, `math`
và `database` nhận trung bình các giá trị đã có trong cột tương ứng.
Đây là giá trị ước tính để thực hành làm sạch dữ liệu, không phải điểm
hoặc thông tin gốc của sinh viên. Script hiển thị số ô thiếu và các
trung bình dùng để điền. Hai CSV trên đĩa được giữ nguyên.

Hai bảng ghép theo `student_id`, với mỗi ID xuất hiện một lần ở mỗi bảng.
`average_score` là trung bình cộng của `python`, `math`, `database` sau
khi điền ô thiếu. Top 5 sắp xếp giảm dần theo `average_score`. Điểm trung
bình theo ngành tính từ các trung bình sinh viên. Các phép tính giữ nguyên
độ chính xác; Pandas chỉ rút gọn số khi hiển thị.

Chạy kiểm thử riêng bài này từ thư mục gốc:

```text
python -B -m unittest discover -s tests -p test_labwork5_pandas.py -v
```

Nguồn: [đề Labwork 5](https://drive.google.com/file/d/1Tf9JcZRWb07zxNudI6HbmMQQOJnPajAh/view),
[slide Data Manipulation in Python](https://drive.google.com/file/d/1Ez04DmwbSB3cl8pa5goKoU8Nw85oKdYm/view),
[students.csv](https://drive.google.com/file/d/1proEEYo6hI4hF5hpds5xM6NYcT26bH2r/view),
[scores.csv](https://drive.google.com/file/d/1adWK5J5XBRCyjSHAAiw_jQkRScN_7P7I/view).
