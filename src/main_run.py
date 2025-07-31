# gemini
from google import genai
from google.genai import types
from openai import OpenAI
from together import Together

import gemini
import gpt
import llama

import time
import datetime
import os
import json
import pandas as pd
from dotenv import load_dotenv

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--api_type",
        type=str,
        choices=["gemini", "gpt", "llama"],
        default="gemini",
        help="Type of API to use (default: gemini)",
    )

    parser.add_argument(
        "--data_name",
        type=str,
        default="mrpc",
        help="Name of the dataset to process (default: mrpc)",
    )
    parser.add_argument(
        "--repeat_num",
        type=int,
        default=15,
        help="num of repeating  (default: 15)",
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["input", "check", "output"],
        default=None,
        help="batch_job mode has input, check, output",
    )

    parser.add_argument(
        "--prompt_num",
        type=str,
        default="1",
        help="Prompt_number",
    )

    parser.add_argument(
        "--time", type=int, default=30, help="time of interval batch input"
    )

    parser.add_argument("--try_num", type=int, default=1, help="indexing num")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # # --- Configuration ---
    print("Loading configuration...")
    dotenv_path = os.path.join("./", ".env")
    load_dotenv(dotenv_path=dotenv_path)

    # 설정파일
    data_name = args.data_name  # Example data name
    prompt_num = args.prompt_num  # Example prompt number
    repeat_num = args.repeat_num

    if args.api_type == "gemini":
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file or environment variables."
            )
        os.makedirs(f"../results/gemini/{data_name}", exist_ok=True)
        results_path = os.path.join(f"../results/gemini/{data_name}")

        client = genai.Client(api_key=gemini_api_key)

        if args.mode == "input":
            for num in prompt_num:
                batch_job_names = []
                os.makedirs(
                    f"../results/gemini/{data_name}/prompt_{num}", exist_ok=True
                )

                for i in range(repeat_num):
                    batch_job_names.extend(gemini.input_batch(data_name, num, client))
                    print("completed input_batch for prompt", num, "iteration", i + 1)
                    # break
                    time.sleep(args.time)

                # save the batch job names to a file
                with open(
                    f"../results/gemini/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "w",
                ) as f:
                    json.dump(batch_job_names, f)

        elif args.mode == "check":
            results_cnt = 0
            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/gemini/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                for job_name in batch_job_names:
                    gemini.batch_scheduling(job_name, client)

                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")

        elif args.mode == "output":
            results_cnt = 0

            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/gemini/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                os.makedirs(
                    f"../results/gemini/{data_name}/prompt_{num}/output", exist_ok=True
                )

                for job_name in batch_job_names:
                    result = gemini.batch_results(job_name, client)

                    with open(
                        f"../results/gemini/{data_name}/prompt_{num}/output/result_{job_name.removeprefix('batches/')}.jsonl",
                        "w",
                    ) as f:
                        f.write(result)

                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")

    elif args.api_type == "gpt":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env file or environment variables."
            )
        os.makedirs(f"../results/gpt/{data_name}", exist_ok=True)
        results_path = os.path.join(f"../results/gpt/{data_name}")

        client = OpenAI(api_key=openai_api_key)

        if args.mode == "input":
            for num in prompt_num:
                batch_job_names = []
                os.makedirs(f"../results/gpt/{data_name}/prompt_{num}", exist_ok=True)

                for i in range(repeat_num):
                    batch_job_names.extend(gpt.input_batch(data_name, num, client))
                    print("completed input_batch for prompt", num, "iteration", i + 1)
                    # break
                    time.sleep(args.time)

                # save the batch job names to a file
                with open(
                    f"../results/gpt/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "w",
                ) as f:
                    json.dump(batch_job_names, f)

        elif args.mode == "check":
            results_cnt = 0
            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/gpt/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                for batch_id in batch_job_names:
                    gpt.batch_scheduling(batch_id, client)

                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")

        elif args.mode == "output":
            results_cnt = 0

            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/gpt/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                os.makedirs(
                    f"../results/gpt/{data_name}/prompt_{num}/output", exist_ok=True
                )

                for batch_id in batch_job_names:
                    result = gpt.batch_results(batch_id, client)
                    # print(type(result))
                    with open(
                        f"../results/gpt/{data_name}/prompt_{num}/output/result_{batch_id}.jsonl",
                        "w",
                    ) as f:
                        f.write(result)

                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")

    elif args.api_type == "llama":
        together_api_key = os.getenv("TOGETHER_API_KEY")
        if not together_api_key:
            raise ValueError(
                "TOGETHER_API_KEY not found in .env file or environment variables."
            )
        os.makedirs(f"../results/llama/{data_name}", exist_ok=True)
        results_path = os.path.join(f"../results/llama/{data_name}")

        client = client = Together(api_key=together_api_key)

        if args.mode == "input":
            for num in prompt_num:
                batch_job_names = []
                os.makedirs(f"../results/llama/{data_name}/prompt_{num}", exist_ok=True)

                for i in range(repeat_num):
                    batch_job_names.extend(llama.input_batch(data_name, num, client))
                    print("completed input_batch for prompt", num, "iteration", i + 1)
                    # break
                    time.sleep(args.time)

                # save the batch job names to a file
                with open(
                    f"../results/llama/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "w",
                ) as f:
                    json.dump(batch_job_names, f)

        elif args.mode == "check":

            results_cnt = 0
            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/llama/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                for batch_id in batch_job_names:
                    llama.batch_scheduling(batch_id, client)
                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")

            print()
            # print("and your list of batches")
            # llama.check_your_batch_list(client)

        elif args.mode == "output":
            results_cnt = 0

            for num in prompt_num:
                # for i in range(repeat_num):
                with open(
                    f"../results/llama/{data_name}/prompt_{num}/submitted_batch_ids_{args.try_num}.json",
                    "r",
                ) as f:
                    batch_job_names = json.load(f)

                os.makedirs(
                    f"../results/llama/{data_name}/prompt_{num}/output", exist_ok=True
                )

                for batch_id in batch_job_names:
                    result = llama.batch_results(
                        batch_id,
                        file_path=f"../results/llama/{data_name}/prompt_{num}/output/result_{batch_id}.jsonl",
                        client=client,
                    )
                    results_cnt += 1

            print(f"Total results processed: {results_cnt}")
