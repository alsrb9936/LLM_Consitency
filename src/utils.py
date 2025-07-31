import pandas as pd
import numpy as np
import os
import json


def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line.strip()))

    # convert data_list to DataFrame
    df = pd.DataFrame(data)

    return df


def clean_punctuation(text):
    if not isinstance(text, str):
        return text
    return text.translate(str.maketrans("", "", ".,!?;:()[]{}\"'"))
