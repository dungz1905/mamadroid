# MAMADROID Demo

## Giới thiệu

Đây là phiên bản thực nghiệm rút gọn mô phỏng ý tưởng chính của MAMADROID: phát hiện mã độc Android bằng cách mô hình hóa chuỗi lời gọi API dưới dạng Markov Chain và sử dụng các mô hình học máy để phân loại ứng dụng thành benign hoặc malware.

Repo này được xây dựng phục vụ mục đích học tập và minh họa cho bài tiểu luận về phương pháp MAMADROID. Đây không phải là bản tái hiện đầy đủ hệ thống MAMADROID gốc, vì hệ thống gốc yêu cầu phân tích tĩnh trên số lượng lớn tệp APK bằng các công cụ như Soot và FlowDroid. Thay vào đó, repo tập trung vào pipeline cốt lõi:

```text
API family sequence → Markov Chain → Feature vector → Machine Learning classifier
```
## Cấu trúc thư mục 
Repo được tổ chức như sau:

mamadroid/
├── README.md
├── mamadroid_experiment.py
├── dataset_harder.csv
├── requirements.txt
└── run.bat

Trong đó:
+ README.md: mô tả mục đích, quy trình thực nghiệm, cách chạy chương trình và kết quả chính.
+ mamadroid_experiment.py: mã nguồn chính của chương trình thực nghiệm.
+ dataset.csv: bộ dữ liệu mô phỏng chuỗi API family.
+ requirements.txt: danh sách thư viện cần cài đặt.
+ run.bat: file hỗ trợ chạy nhanh chương trình trên Windows.

## Dataset
Bộ dữ liệu sử dụng trong demo là dataset.csv, gồm 500 mẫu mô phỏng:
+ 244 mẫu benign
+ 256 mẫu malware
+ Mỗi mẫu là một chuỗi API family
+ Số trạng thái API family: 8
+ Số chiều vector Markov: 8 × 8 = 64

## Quy trình thực nghiệm
Bước 1. Đọc dataset chứa chuỗi API family.
Bước 2. Tách mỗi chuỗi thành các trạng thái API family.
Bước 3. Xác định các cặp chuyển trạng thái liên tiếp.
Bước 4. Tính xác suất chuyển trạng thái giữa các API family.
Bước 5. Xây dựng ma trận Markov cho từng mẫu.
Bước 6. Chuyển ma trận Markov thành vector đặc trưng.
Bước 7. Huấn luyện và đánh giá các mô hình học máy.

## Mô hình sử dụng
Các mô hình học máy được sử dụng trong thực nghiệm gồm:

+ Random Forest
+ 1-Nearest Neighbor
+ 3-Nearest Neighbor
+ Support Vector Machine

Các mô hình được đánh giá bằng các chỉ số:

+ Precision
+ Recall
+ F1-score

## Cách chạy chương trình

### Cách 1. Chạy bằng Python

Trước tiên, cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install -r requirements.txt
```

Sau khi cài đặt xong, chạy chương trình bằng lệnh:

```bash
python mamadroid_experiment.py
```

Chương trình sẽ tự động đọc dữ liệu từ file `dataset_harder.csv`, xây dựng vector đặc trưng Markov và đánh giá các mô hình học máy.

### Cách 2. Chạy nhanh trên Windows

Trên hệ điều hành Windows, có thể chạy trực tiếp file:

```text
run.bat
```

File `run.bat` sẽ tự động cài đặt các thư viện cần thiết trong `requirements.txt`, sau đó chạy chương trình thực nghiệm.

Sau khi chạy xong, kết quả sẽ được hiển thị trên màn hình dòng lệnh, bao gồm thông tin dataset, kết quả đánh giá mô hình và confusion matrix.
## Kết quả thực nghiệm

Sau khi chuyển chuỗi API family thành vector đặc trưng Markov 64 chiều, chương trình tiến hành đánh giá các mô hình học máy bằng phương pháp 10-fold cross validation. Các chỉ số được sử dụng để đánh giá gồm Precision, Recall và F1-score.

Kết quả thu được như sau:

| Model | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Random Forest | 0.792382 | 0.769077 | 0.776358 |
| 1-NN | 0.612432 | 0.703077 | 0.652533 |
| 3-NN | 0.629346 | 0.764769 | 0.689283 |
| SVM | 0.794857 | 0.768923 | 0.777901 |

Kết quả cho thấy hai mô hình có hiệu quả tốt nhất là SVM và Random Forest. Trong đó, SVM đạt F1-score khoảng 0.778, còn Random Forest đạt F1-score khoảng 0.776. Điều này cho thấy vector đặc trưng được xây dựng từ Markov Chain có khả năng biểu diễn hành vi ứng dụng ở mức nhất định, từ đó hỗ trợ quá trình phân loại ứng dụng thành benign hoặc malware.

## Confusion Matrix

Confusion Matrix của mô hình Random Forest trên tập kiểm thử 20%:

```text
[[38 11]
 [18 33]]
```

Ý nghĩa của ma trận trên:

- 38 mẫu benign được dự đoán đúng là benign.
- 11 mẫu benign bị nhầm thành malware.
- 18 mẫu malware bị bỏ sót thành benign.
- 33 mẫu malware được dự đoán đúng là malware.

Kết quả này cho thấy mô hình vẫn tồn tại cả false positive và false negative. Đặc biệt, có 18 mẫu malware bị phân loại nhầm thành benign, đây là trường hợp cần lưu ý trong bài toán phát hiện mã độc vì có thể dẫn đến việc bỏ sót ứng dụng độc hại.

## Nhận xét kết quả

Thực nghiệm cho thấy pipeline rút gọn của MAMADROID có thể được mô phỏng bằng cách chuyển chuỗi API family thành ma trận Markov, sau đó sử dụng các xác suất chuyển trạng thái làm vector đặc trưng cho mô hình học máy.

Tuy nhiên, do bộ dữ liệu sử dụng trong demo là dữ liệu mô phỏng và có sự chồng lấn giữa hai lớp benign/malware, kết quả không đạt mức tuyệt đối. Điều này phản ánh thực tế rằng trong bài toán phát hiện mã độc Android, hành vi của ứng dụng lành tính và ứng dụng độc hại có thể có điểm tương đồng, khiến việc phân loại trở nên khó khăn hơn.

Do đó, kết quả thực nghiệm trong repo chủ yếu có ý nghĩa minh họa phương pháp, giúp làm rõ cách MAMADROID kết hợp Markov Chain và học máy trong phát hiện mã độc Android.





