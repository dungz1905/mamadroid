import os
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.metrics import classification_report, confusion_matrix


# =========================================================
# DEMO MAMADROID SIMPLIFIED
# Phát hiện mã độc Android bằng Markov Chain + Machine Learning
# =========================================================


# =========================================================
# 1. Danh sách trạng thái API family
# Mỗi trạng thái tương ứng với một nhóm API.
#
# Vì có 8 trạng thái nên ma trận Markov sẽ có kích thước:
# 8 x 8 = 64 đặc trưng
# =========================================================

STATES = [
    "android",
    "google",
    "java",
    "javax",
    "xml",
    "apache",
    "self-defined",
    "obfuscated"
]


# =========================================================
# 2. Hàm chuyển API sequence thành vector Markov
# =========================================================

def sequence_to_markov_vector(sequence, states):
    """
    Chuyển một chuỗi API family thành vector đặc trưng Markov.

    Ví dụ sequence:
        android java android google

    Các transition được tạo:
        android -> java
        java    -> android
        android -> google

    Sau đó chương trình tính xác suất chuyển trạng thái:
        P(android -> java)
        P(java -> android)
        P(android -> google)

    Cuối cùng, ma trận Markov được flatten thành vector đặc trưng.
    """

    calls = str(sequence).strip().split()

    n = len(states)
    state_to_idx = {state: idx for idx, state in enumerate(states)}

    # Ma trận đếm số lần chuyển trạng thái
    transition_counts = np.zeros((n, n), dtype=float)

    for i in range(len(calls) - 1):
        src = calls[i]
        dst = calls[i + 1]

        if src in state_to_idx and dst in state_to_idx:
            src_idx = state_to_idx[src]
            dst_idx = state_to_idx[dst]
            transition_counts[src_idx, dst_idx] += 1

    # Ma trận xác suất chuyển trạng thái
    transition_probs = np.zeros((n, n), dtype=float)

    for i in range(n):
        row_sum = transition_counts[i].sum()

        if row_sum > 0:
            transition_probs[i] = transition_counts[i] / row_sum

    # Chuyển ma trận 8 x 8 thành vector 64 chiều
    feature_vector = transition_probs.flatten()

    return feature_vector


# =========================================================
# 3. Load dataset và tạo feature vector
# =========================================================

def load_dataset(csv_path):
    """
    Đọc dataset CSV.

    Dataset cần có ít nhất 3 cột:
        app_id   : mã ứng dụng
        sequence : chuỗi API family
        label    : 0 = benign, 1 = malware

    Sau khi đọc, mỗi sequence sẽ được chuyển thành vector Markov.
    """

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Không tìm thấy file dataset: {csv_path}\n"
            "Hãy đặt file dataset_harder.csv cùng thư mục với code."
        )

    df = pd.read_csv(csv_path)

    required_columns = ["sequence", "label"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"File CSV thiếu cột bắt buộc: {col}")

    X = np.array([
        sequence_to_markov_vector(seq, STATES)
        for seq in df["sequence"]
    ])

    y = df["label"].values

    return X, y, df


# =========================================================
# 4. Đánh giá bằng 10-fold cross validation
# =========================================================

def evaluate_models(X, y):
    """
    Đánh giá các mô hình bằng 10-fold cross validation.

    10-fold cross validation:
        - Chia dataset thành 10 phần.
        - Mỗi lần dùng 9 phần để train, 1 phần để test.
        - Lặp 10 lần.
        - Lấy kết quả trung bình.

    Các mô hình sử dụng:
        - Random Forest
        - 1-NN
        - 3-NN
        - SVM
    """

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=51,
            max_depth=8,
            random_state=42
        ),
        "1-NN": KNeighborsClassifier(n_neighbors=1),
        "3-NN": KNeighborsClassifier(n_neighbors=3),
        "SVM": SVC(
            kernel="rbf",
            random_state=42
        )
    }

    scoring = {
        "precision": "precision",
        "recall": "recall",
        "f1": "f1"
    }

    cv = StratifiedKFold(
        n_splits=10,
        shuffle=True,
        random_state=42
    )

    results = []

    for name, model in models.items():
        print(f"[*] Đang đánh giá mô hình: {name}")

        scores = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            error_score="raise"
        )

        results.append({
            "Model": name,
            "Precision": scores["test_precision"].mean(),
            "Recall": scores["test_recall"].mean(),
            "F1-score": scores["test_f1"].mean()
        })

    return pd.DataFrame(results)


# =========================================================
# 5. Train/test split để in báo cáo chi tiết
# =========================================================

def train_test_report(X, y):
    """
    Huấn luyện Random Forest trên 80% dữ liệu,
    kiểm thử trên 20% dữ liệu còn lại.

    Phần này dùng để in:
        - Classification report
        - Confusion matrix
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=51,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n=== CLASSIFICATION REPORT - RANDOM FOREST ===")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["Benign", "Malware"],
        zero_division=0
    ))

    cm = confusion_matrix(y_test, y_pred)

    print("\n=== CONFUSION MATRIX ===")
    print(cm)

    print("\nGiải thích Confusion Matrix:")
    print("[[True Benign,  False Positive],")
    print(" [False Negative, True Malware]]")

    print(f"\nBenign dự đoán đúng       : {cm[0][0]}")
    print(f"Benign bị nhầm Malware    : {cm[0][1]}")
    print(f"Malware bị bỏ sót         : {cm[1][0]}")
    print(f"Malware dự đoán đúng      : {cm[1][1]}")

    total = cm.sum()
    correct = cm[0][0] + cm[1][1]
    wrong = cm[0][1] + cm[1][0]

    print(f"\nTổng số mẫu test          : {total}")
    print(f"Số mẫu dự đoán đúng       : {correct}")
    print(f"Số mẫu dự đoán sai        : {wrong}")
    print(f"Accuracy trên tập test    : {correct / total:.4f}")


# =========================================================
# 6. In ví dụ minh họa Markov Chain từ một sequence
# =========================================================

def show_markov_example(df):
    """
    In ví dụ một sequence đầu tiên trong dataset để giảng viên thấy:
        sequence ban đầu là gì
        chương trình tạo vector Markov ra sao
    """

    print("\n" + "=" * 70)
    print("[MINH HỌA] MỘT MẪU API SEQUENCE")
    print("=" * 70)

    sample = df.iloc[0]

    app_id = sample["app_id"] if "app_id" in df.columns else "unknown_app"
    sequence = sample["sequence"]
    label = sample["label"]

    print("App ID:", app_id)
    print("Label:", label, "(0 = Benign, 1 = Malware)")

    calls = str(sequence).split()

    print("\nMột phần sequence:")
    print(" -> ".join(calls[:20]))

    if len(calls) > 20:
        print(f"... còn {len(calls) - 20} trạng thái phía sau")

    print("\nCác transition đầu tiên:")
    for i in range(min(10, len(calls) - 1)):
        print(f"{calls[i]} -> {calls[i + 1]}")

    vector = sequence_to_markov_vector(sequence, STATES)

    print("\nVector Markov sau khi flatten:")
    print("Số chiều vector:", len(vector))
    print("10 giá trị đầu tiên:", vector[:10])


# =========================================================
# 7. Main
# =========================================================

if __name__ == "__main__":

    # Đổi tên file ở đây nếu bạn muốn dùng dataset khác
    csv_path = "dataset.csv"

    print("=" * 70)
    print("DEMO MAMADROID SIMPLIFIED")
    print("Phát hiện mã độc Android bằng Markov Chain và Machine Learning")
    print("=" * 70)

    print("\n[GIỚI THIỆU]")
    print("Đây là phiên bản rút gọn của MAMADROID.")
    print("Mục tiêu của demo là minh họa pipeline cốt lõi:")
    print("API sequence -> Markov Chain -> Feature vector -> Machine Learning")
    print("Dataset sử dụng là chuỗi API family mô phỏng, không phải APK thật.")

    print("\n[BUOC 1] Đọc bộ dữ liệu API sequence")
    print("File dataset:", csv_path)

    X, y, df = load_dataset(csv_path)

    print("\n[THÔNG TIN DATASET]")
    print("Số lượng mẫu:", len(df))
    print("Số benign:", sum(y == 0))
    print("Số malware:", sum(y == 1))

    print("\n[BUOC 2] Trừu tượng hóa API calls về family")
    print("Các API family được sử dụng:")
    for idx, state in enumerate(STATES):
        print(f"  {idx + 1}. {state}")

    print("\n[BUOC 3] Xây dựng Markov Chain")
    print("Mỗi API family được xem là một trạng thái.")
    print("Chương trình tính xác suất chuyển trạng thái giữa các family.")
    print("Ví dụ: P(android -> java), P(java -> self-defined), ...")

    print("\n[BUOC 4] Tạo vector đặc trưng")
    print("Ma trận Markov được flatten thành vector đặc trưng.")
    print("Số trạng thái:", len(STATES))
    print("Số chiều feature:", X.shape[1])
    print(f"Giải thích: {len(STATES)} x {len(STATES)} = {X.shape[1]} đặc trưng.")

    show_markov_example(df)

    print("\n" + "=" * 70)
    print("[BUOC 5] Đánh giá mô hình bằng 10-fold Cross Validation")
    print("=" * 70)

    print("Dataset được chia thành 10 phần.")
    print("Mỗi lần dùng 9 phần để huấn luyện và 1 phần để kiểm thử.")
    print("Kết quả cuối cùng là trung bình của 10 lần đánh giá.\n")

    results = evaluate_models(X, y)

    print("\n=== KẾT QUẢ 10-FOLD CROSS VALIDATION ===")
    print(results)

    results.to_csv("mamadroid_simplified_results.csv", index=False)
    print("\nĐã lưu kết quả vào file: mamadroid_simplified_results.csv")

    print("\n[NHẬN XÉT TỰ ĐỘNG]")
    best_model = results.sort_values(by="F1-score", ascending=False).iloc[0]

    print(f"Mô hình tốt nhất theo F1-score: {best_model['Model']}")
    print(f"Precision: {best_model['Precision']:.4f}")
    print(f"Recall   : {best_model['Recall']:.4f}")
    print(f"F1-score : {best_model['F1-score']:.4f}")

    print("\nÝ nghĩa:")
    print("- Precision cao nghĩa là ít benign bị nhầm thành malware.")
    print("- Recall cao nghĩa là phát hiện được nhiều malware thật.")
    print("- F1-score cân bằng giữa Precision và Recall.")

    print("\n" + "=" * 70)
    print("[BUOC 6] Đánh giá chi tiết Random Forest trên tập test 20%")
    print("=" * 70)

    train_test_report(X, y)

    print("\n" + "=" * 70)
    print("[KẾT LUẬN DEMO]")
    print("=" * 70)

    print("Chương trình đã thực hiện đầy đủ pipeline rút gọn:")
    print("1. Đọc chuỗi API family.")
    print("2. Xây dựng ma trận Markov từ các transition.")
    print("3. Chuyển ma trận Markov thành vector đặc trưng.")
    print("4. Huấn luyện các mô hình học máy.")
    print("5. Đánh giá bằng Precision, Recall và F1-score.")

    print("\nLưu ý:")
    print("Đây là bản MAMADROID simplified dùng dataset mô phỏng.")
    print("Bản gốc của MAMADROID sử dụng APK thật, Soot/FlowDroid để trích xuất call graph.")
    print("Demo này tập trung minh họa phần lõi: Markov Chain + Machine Learning.")