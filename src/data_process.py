import os
import pandas as pd
from utils import *


class BatchFileCreator:
    def __init__(self, api_type, data_name, batch_size=None):
        self.api_type = api_type
        self.data_name = data_name
        self.batch_size = batch_size
        self.batch_files = []

    def make_batch_files(self):
        self.data = self.load_data()
        self.prompt = self.load_prompt()

        print(f"Data loaded for {self.data_name} with {len(self.data)} records.")

        try:
            if self.api_type == "gemini":
                os.makedirs("../data/batch/gemini/boolq", exist_ok=True)
                os.makedirs("../data/batch/gemini/mrpc", exist_ok=True)
                os.makedirs("../data/batch/gemini/qnli", exist_ok=True)
                os.makedirs("../data/batch/gemini/sst2", exist_ok=True)
                self._gemini_batch_file()

            elif self.api_type == "gpt":
                os.makedirs("../data/batch/gpt/boolq", exist_ok=True)
                os.makedirs("../data/batch/gpt/mrpc", exist_ok=True)
                os.makedirs("../data/batch/gpt/qnli", exist_ok=True)
                os.makedirs("../data/batch/gpt/sst2", exist_ok=True)
                self._gpt_batch_file()
            elif self.api_type == "llama":
                os.makedirs("../data/batch/llama/boolq", exist_ok=True)
                os.makedirs("../data/batch/llama/mrpc", exist_ok=True)
                os.makedirs("../data/batch/llama/qnli", exist_ok=True)
                os.makedirs("../data/batch/llama/sst2", exist_ok=True)
                self._llama_batch_file()
            else:
                raise ValueError(f"Unsupported API type: {self.api_type}")
        except Exception as e:
            print(f"Error creating batch files: {e}")
            raise

    def load_data(self) -> pd.DataFrame:
        data_path = os.path.join("../data/raw", f"{self.data_name}.jsonl")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file {data_path} does not exist.")
        print(f"Loading data from {data_path}...")
        return load_jsonl(data_path)

    def load_prompt(self):
        prompt_path = [
            f"../prompt/{self.data_name}/prompt1.md",
            f"../prompt/{self.data_name}/prompt2.md",
            f"../prompt/{self.data_name}/prompt3.md",
        ]

        prompts = []
        for path in prompt_path:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    prompts.append(f.read())
            else:
                print(f"Prompt file {path} does not exist.")
        return prompts

    def _gemini_batch_file(self):
        # Placeholder for Gemini batch file creation logic
        # Jsonl structure for Gemini API
        # ex    {"key": "request-1", "request": {"contents": [{"parts": [{"text": "Describe the process of photosynthesis."}]}]}}
        # 5GB
        gemini_max_size = 2 * 1024 * 1024 * 1024  # 5 GB in bytes

        if self.batch_size is None:
            self.batch_size = 1000

        if self.data_name == "boolq":

            questions = self.data["question"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, question in enumerate(questions):
                    request = {
                        "key": f"request-{n+1}",
                        "request": {
                            "contents": [
                                {"parts": [{"text": self.prompt[i] + question}]}
                            ]
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "mrpc":
            sentence1, sentence2 = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (s1, s2) in enumerate(zip(sentence1, sentence2)):
                    request = {
                        "key": f"request-{n+1}",
                        "request": {
                            "contents": [
                                {"parts": [{"text": self.prompt[i] + s1 + " " + s2}]},
                            ]
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentence1):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "sst2":
            self.batch_files = []

            sentences = self.data["text"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, sentence in enumerate(sentences):
                    request = {
                        "key": f"request-{n+1}",
                        "request": {
                            "contents": [
                                {"parts": [{"text": self.prompt[i] + sentence}]}
                            ]
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentences):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "qnli":
            self.batch_files = []

            questions, passage = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (q, p) in enumerate(zip(questions, passage)):
                    request = {
                        "key": f"request-{n+1}",
                        "request": {
                            "contents": [
                                {
                                    "parts": [
                                        {
                                            "text": self.prompt[i]
                                            + "Question : "
                                            + q
                                            + "\nSentence : "
                                            + p
                                        }
                                    ]
                                }
                            ]
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        else:
            raise ValueError(f"Unsupported data name: {self.data_name}")

    def _save_batch_file(self, prompt_i, requests_n):
        os.makedirs(
            f"../data/batch/{self.api_type}/{self.data_name}/prompt_{prompt_i}",
            exist_ok=True,
        )

        with open(
            f"../data/batch/{self.api_type}/{self.data_name}/prompt_{prompt_i}/prompt_{prompt_i}_batch_{requests_n//self.batch_size + 1}.jsonl",
            "w",
        ) as f:
            for batch_request in self.batch_files:
                f.write(json.dumps(batch_request, ensure_ascii=False) + "\n")
        # Here you would write the batch file to disk or process it
        print(f"Created batch file with {len(self.batch_files)} requests.")
        self.batch_files = []

    def _gpt_batch_file(self):
        # 200MB(File) / 50,000 Request
        gpt_max_size = 200 * 1024 * 1024  # 200 MB in bytes
        gpt_max_requests = 50000  #

        if self.batch_size is None:
            self.batch_size = 1000
        if self.data_name == "boolq":
            # {"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}]}}

            questions = self.data["question"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, question in enumerate(questions):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {"role": "user", "content": self.prompt[i] + question}
                            ],
                        },
                    }

                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "mrpc":
            sentence1, sentence2 = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (s1, s2) in enumerate(zip(sentence1, sentence2)):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": self.prompt[i] + s1 + " " + s2,
                                }
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentence1):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "sst2":
            self.batch_files = []

            sentences = self.data["text"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, sentence in enumerate(sentences):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {"role": "user", "content": self.prompt[i] + sentence}
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentences):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "qnli":
            self.batch_files = []

            questions, passage = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (q, p) in enumerate(zip(questions, passage)):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": self.prompt[i]
                                    + "Question : "
                                    + q
                                    + "\nSentence : "
                                    + p,
                                }
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        else:
            raise ValueError(f"Unsupported data name: {self.data_name}")

    def _llama_batch_file(self):
        # 100MB(File) / 50,000 Request
        llama_max_size = 100 * 1024 * 1024
        llama_max_requests = 50000

        if self.batch_size is None:
            self.batch_size = 1000

        if self.data_name == "boolq":
            # {"custom_id": "request-1", "body": {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": self.prompt[i] + question}]}}
            questions = self.data["question"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, question in enumerate(questions):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "body": {
                            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                            "messages": [
                                {"role": "user", "content": self.prompt[i] + question}
                            ],
                        },
                    }

                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "mrpc":
            sentence1, sentence2 = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (s1, s2) in enumerate(zip(sentence1, sentence2)):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "body": {
                            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": self.prompt[i] + s1 + " " + s2,
                                }
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentence1):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "sst2":
            self.batch_files = []

            sentences = self.data["text"].tolist()
            for i in range(3):
                self.batch_files = []
                for n, sentence in enumerate(sentences):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "body": {
                            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                            "messages": [
                                {"role": "user", "content": self.prompt[i] + sentence}
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(sentences):
                        self._save_batch_file(i, n + 1)

        elif self.data_name == "qnli":
            self.batch_files = []

            questions, passage = (
                self.data["text1"].tolist(),
                self.data["text2"].tolist(),
            )
            for i in range(3):
                self.batch_files = []
                for n, (q, p) in enumerate(zip(questions, passage)):
                    request = {
                        "custom_id": f"request-{n+1}",
                        "body": {
                            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": self.prompt[i]
                                    + "Question : "
                                    + q
                                    + "\nSentence : "
                                    + p,
                                }
                            ],
                        },
                    }
                    self.batch_files.append(request)

                    if (n + 1) % self.batch_size == 0:
                        self._save_batch_file(i, n)
                    elif n + 1 == len(questions):
                        self._save_batch_file(i, n + 1)

        else:
            raise ValueError(f"Unsupported data name: {self.data_name}")

        # Placeholder for llama batch file creation logic
        # Jsonl structure for llama API
        # ex   {"custom_id": "request-1", "body": {"model": "deepseek-ai/DeepSeek-V3",  [{"role": "system", "content": "You are a cat. Your name is Neko."},{"role": "user", "content": "'Write a short poem about a cat."}]}}
