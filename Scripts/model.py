import pandas as pd
import numpy as np
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from typing import Any


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path from the relative path of the file
    :param relative_path: The relative path of the file
    :return: Absolute path of the file
    """
    import sys
    import os

    try:
        base_path: str = sys._MEIPASS

    except AttributeError:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)


class Model:
    """
    This contains the Logistic Regression model
    """
    def __init__(self) -> None:
        self.model: LogisticRegression = LogisticRegression()
        self.vectorizer: TfidfVectorizer = TfidfVectorizer()
        self.emails: pd.DataFrame = pd.read_csv(resource_path("Datasets/emails.csv"))

        self.x: Any = self.vectorizer.fit_transform(self.emails["text"])
        self.y: np.ndarray[tuple[int, ...], np.dtype[Any]] = self.emails["spam/ham"].values

        le: LabelEncoder = LabelEncoder()
        self.y = le.fit_transform(self.y)

    def train(self) -> None:
        """
        Train the Logistic Regression model
        :return: This doesn't return anything
        """
        self.model.fit(self.x, self.y)

    def evaluate(self, text: str) -> str:
        """
        Evaluate the Logistic Regression model
        :return: This returns a short str telling the user is the text is a spam or not with the chances in percentage values
        """
        new_x: list[str] = [text]

        y_pred: int = self.model.predict(self.vectorizer.transform(new_x))[0]
        y_proba: int = self.model.predict_proba(self.vectorizer.transform(new_x)).max()

        if y_pred == 0:
            return f"This text is {(y_proba * 100):.2f}% not a spam"

        else:
            return f"This text is {(y_proba * 100):.2f}% a spam"


    def save(self) -> None:
        """
        Save this class
        :return: This doesn't return anything
        """
        dump(self, resource_path("Model/model.pkl"))

    @staticmethod
    def load() -> Model:
        """
        Load the Logistic Regression model and the TfidfVectorizer
        :return: This returns the Logistic Regression model and the TfidfVectorizer
        """
        model: Model = load(resource_path("Model/model.pkl"))
        return model


def main() -> None:
    m: Model = Model()
    m.train()
    m.save()


if __name__ == "__main__":
    main()