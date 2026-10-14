# Chạy Labwork 6b

Từ thư mục gốc repository:

```text
python labwork6_pandas_plot/main.py
```

Script đọc `labwork5_pandas/scores.csv` bằng Pandas và lưu ba hình trong
thư mục này. Cột `database` tương ứng với `db` trong đề.

- `scattered.png`: ba nhóm điểm Math, Python và Database. Trục X là thứ tự
  sinh viên trong CSV (1–30), trục Y là điểm. Đây là lựa chọn triển khai vì
  đề không chỉ định trục; thứ tự này không biểu diễn thời gian.
- `histo.png`: ba subplot histogram, mỗi môn dùng 10 khoảng điểm.
- `box.png`: một axes chứa ba box, so sánh trung vị và phân bố điểm từng môn.

CSV được giữ nguyên. Mỗi biểu đồ bỏ qua ô thiếu riêng cho từng môn;
không điền điểm và không loại điểm hợp lệ của môn khác. Với CSV hiện tại,
Python có 30 điểm, Math có 28 điểm và Database có 29 điểm.

Nguồn: [đề Labwork 6b](https://drive.google.com/file/d/1_-Q29uunJXDu2mYZmnpuEZ0slM66PaQK/view)
và [slide Data Visualization](https://drive.google.com/file/d/13EE5qIipM4NKzeaxOzEETM9ylqKP3jNN/view).
