from google import genai
from google.genai import types

import time
import datetime
import os
import json
import pandas as pd
from dotenv import load_dotenv

root_path = os.path.join("../data/batch/gemini")


def input_batch(data_name, prompt_num, client: genai.Client):
    datetime1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(root_path, data_name, f"prompt_{prompt_num}/")
    file_list = os.listdir(file_path)

    batch_job_name = []

    for n, file_name in enumerate(file_list):
        batch_file_path = os.path.join(file_path, file_name)
        display_name = file_name.removesuffix(".jsonl") + f"-{datetime1}"

        # Upload the file to the File API
        uploaded_file = client.files.upload(
            file=batch_file_path,
            config=types.UploadFileConfig(display_name=display_name, mime_type="jsonl"),
        )
        print(f"Uploaded file: {uploaded_file.name}")
        # time.sleep(10)  # Sleep to avoid hitting rate limits

        # Assumes `uploaded_file` is the file object from the previous step
        file_batch_job = client.batches.create(
            model="gemini-2.0-flash-lite",
            src=uploaded_file.name,
            config={
                "display_name": display_name,
            },
        )
        batch_job_name.append(file_batch_job.name)

        print(f"Created batch job: {file_batch_job.name}")
        print("Waiting for 5 seconds to avoid rate limits...")

        time.sleep(5)

    return batch_job_name


def batch_scheduling(job_name, client: genai.Client):
    while True:
        batch_job = client.batches.get(name=job_name)
        if batch_job.state.name in (
            "JOB_STATE_SUCCEEDED",
            "JOB_STATE_FAILED",
            "JOB_STATE_CANCELLED",
        ):
            break
        print(
            f"Job not finished. Current state: {batch_job.state.name}. Waiting 30 seconds..."
        )
        time.sleep(30)

    print(f"Job finished with state: {batch_job.state.name}")
    print(f"check this job! {batch_job.name}")


def batch_results(job_name, client: genai.Client):
    batch_job = client.batches.get(name=job_name)
    if batch_job.state.name == "JOB_STATE_SUCCEEDED":

        # If batch job was created with a file
        if batch_job.dest and batch_job.dest.file_name:
            # Results are in a file
            result_file_name = batch_job.dest.file_name
            print(f"Results are in file: {result_file_name}")

            print("Downloading result file content...")
            file_content = client.files.download(file=result_file_name)
            # Process file_content (bytes) as needed
            # print(file_content.decode("utf-8"))

        # # If batch job was created with inline request
        # elif batch_job.dest and batch_job.dest.inlined_responses:
        #     # Results are inline
        #     print("Results are inline:")
        #     for i, inline_response in enumerate(batch_job.dest.inlined_responses):
        #         print(f"Response {i+1}:")
        #         if inline_response.response:
        #             # Accessing response, structure may vary.
        #             try:
        #                 print(inline_response.response.text)
        #             except AttributeError:
        #                 print(inline_response.response)  # Fallback
        #         elif inline_response.error:
        #             print(f"Error: {inline_response.error}")
        # else:
        #     print("No results found (neither file nor inline).")
    else:
        print(f"Job did not succeed. Final state: {batch_job.state.name}")
        if batch_job.error:
            print(f"Error: {batch_job.error}")

    return file_content.decode("utf-8")
