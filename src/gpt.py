from openai import OpenAI

import time
import datetime
import os
import json
import pandas as pd
from dotenv import load_dotenv

# # --- Configuration ---
# print("Loading configuration...")
# script_dir = os.path.dirname(__file__)
# dotenv_path = os.path.join(script_dir, 'configs', '.env')
# load_dotenv(dotenv_path=dotenv_path)

# together_api_key = os.getenv("TOGETHER_API_KEY")
# if not together_api_key:
#     raise ValueError("TOGETHER_API_KEY not found in .env file or environment variables.")

# base_dir = os.path.abspath(os.path.join(script_dir, ".."))
# batch_results_dir = os.path.join(base_dir, "data", "batch_results")
# ids_filepath = os.path.join(batch_results_dir, "submitted_batch_ids.json")


root_path = os.path.join("../data/batch/gpt")


def input_batch(data_name, prompt_num, client: OpenAI):
    datetime1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(root_path, data_name, f"prompt_{prompt_num}/")
    file_list = os.listdir(file_path)

    batch_job_name = []

    for n, file_name in enumerate(file_list):
        batch_file_path = os.path.join(file_path, file_name)

        # Upload the file to the FILE API
        batch_input_file = client.files.create(
            file=open(batch_file_path, "rb"), purpose="batch"
        )

        batch_input_file_id = batch_input_file.id
        batch = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
        )
        batch_job_name.append(batch.id)

        print(f"Created batch job: {batch.id}")
        print("wating for 5 seconds to aviod rate limits...")

        time.sleep(5)

    return batch_job_name


def batch_scheduling(batch_id, client: OpenAI):
    while True:
        batch_job = client.batches.retrieve(batch_id)
        if batch_job.status in (
            "completed",
            "failed",
            "cancelled",
            "cancelling",
            "expired",
        ):
            break
        print(
            f"Job not finished. Current state: {batch_job.status}. Waiting 40 seconds..."
        )
        time.sleep(40)

    print(f"Job finished with state: {batch_job.status}")
    print(f"check this job! {batch_id}")


def batch_results(batch_id, client: OpenAI):
    batch_job = client.batches.retrieve(batch_id)

    if batch_job.status == "completed":
        # Download the output file
        file_response = client.files.content(batch_job.output_file_id)
        return file_response.text


def check_your_batch_list(client: OpenAI):
    ## List all batches
    batches = client.batches.list_batches()

    for batch in batches:
        print(batch)
