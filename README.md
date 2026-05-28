# MAMADROID Demo

## Giới thiệu

Đây là phiên bản thực nghiệm rút gọn mô phỏng ý tưởng chính của MAMADROID: phát hiện mã độc Android bằng cách mô hình hóa chuỗi lời gọi API dưới dạng Markov Chain và sử dụng các mô hình học máy để phân loại ứng dụng thành benign hoặc malware.

Repo này được xây dựng phục vụ mục đích học tập và minh họa cho bài tiểu luận về phương pháp MAMADROID. Đây không phải là bản tái hiện đầy đủ hệ thống MAMADROID gốc, vì hệ thống gốc yêu cầu phân tích tĩnh trên số lượng lớn tệp APK bằng các công cụ như Soot và FlowDroid. Thay vào đó, repo tập trung vào pipeline cốt lõi:

```text
API family sequence → Markov Chain → Feature vector → Machine Learning classifier

## Cấu trúc thư mục

