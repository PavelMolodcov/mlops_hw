import os
import warnings
from datetime import datetime
from json import dump, loads

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore", category=UserWarning)


# Make prediction
def make_pred(path_to_file):
    print("Importing pretrained model...")
    # Import model
    timestamp = datetime.now().strftime("%Y.%m.%d_%H:%M")
    output_directory = "output"

    model = joblib.load("./models/model.pkl")

    top_features = (
        model.get_feature_scores("fast")
        .set_index("Feature")["Importance"]
        .iloc[:5]
        .to_json(force_ascii=False, orient="split")
    )

    top_features = loads(top_features)
    _ = top_features.pop("name")
    top_features["key"] = top_features.pop("index")
    top_features["value"] = top_features.pop("data")

    json_name = f"{timestamp}_top_feachers.json"
    json_path = os.path.join(output_directory, json_name)
    with open(json_path, "w") as outfile:
        dump(top_features, outfile, ensure_ascii=False)
    # Define optimal threshold
    model_th = 0.33

    # Make submission dataframe

    data = pd.read_csv(path_to_file)

    test_pred = model.predict(data)

    sns.histplot(test_pred.data[:, 0], kde=True)
    plt.title("Грфик распределения скоров")
    plt.xlabel("Скор")
    plt.ylabel("Количество")
    jpg_name = f"{timestamp}_score.jpg"
    jpg_path = os.path.join(output_directory, jpg_name)
    plt.savefig(jpg_path)

    submission = pd.DataFrame(
        {"client_id": data.client_id, "preds": (test_pred.data[:, 0] > model_th) * 1}
    )
    print("Prediction complete!")

    # Return proba for positive class
    return submission, json_path, jpg_path
