HƯỚNG DẪN CHẠY DEMO MAMADROID 

1. Yêu cầu:
   - Máy tính đã cài Python 3.
   - Có kết nối Internet lần đầu để cài thư viện.

2. Cách chạy:
   - Mở thư mục mamadroid_demo.
   - Double click file run.bat.
   - Chương trình sẽ tự cài thư viện cần thiết và chạy thực nghiệm.

3. Kết quả hiển thị:
   - Số lượng mẫu.
   - Số chiều feature Markov.
   - Số benign/malware.
   - Kết quả 10-fold cross validation.
   - Classification report.
   - Confusion matrix.

4. Ghi chú:
   Đây là phiên bản thực nghiệm rút gọn của MAMADROID.
   Chương trình sử dụng chuỗi API family mô phỏng để xây dựng Markov Chain,
   sau đó dùng các mô hình học máy như Random Forest, KNN và SVM để phân loại
   benign/malware.

5. Dataset:
   File dataset.csv gồm 500 mẫu mô phỏng, trong đó mỗi mẫu có:
   - app_id
   - sequence: chuỗi API family
   - label: 0 là benign, 1 là malware
