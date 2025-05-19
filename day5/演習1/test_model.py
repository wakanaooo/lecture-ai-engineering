import os
import pickle
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# モデルと同じデータ前処理
def prepare_test_data():
    path = "data/Titanic.csv"
    data = pd.read_csv(path)
    data = data[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    data["Sex"] = LabelEncoder().fit_transform(data["Sex"])
    X = data[["Pclass", "Sex", "Age", "Fare"]].astype(float)
    y = data["Survived"].astype(float)
    return X, y

def test_model_accuracy():
    model_path = "models/titanic_model.pkl"
    assert os.path.exists(model_path), f"{model_path} が見つかりません"

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    X, y = prepare_test_data()
    predictions = model.predict(X)
    acc = accuracy_score(y, predictions)
    
    # ✅ ここがポイント：精度が0.75以上であることをチェック
    assert acc >= 0.75, f"モデル精度が低すぎます: {acc}"

    print(f"✅ モデルの精度テスト成功: accuracy = {acc}")

