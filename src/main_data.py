import os
import argparse
from data_process import BatchFileCreator


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
        default="qnli",
        help="Name of the dataset to process (default: mrpc)",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1000,
        help="Batch size for processing (default: 10)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Create an instance of BatchFileCreator
    batch_creator = BatchFileCreator(
        api_type=args.api_type,
        data_name=args.data_name,
        batch_size=args.batch_size,
    )

    # Make batch files
    batch_creator.make_batch_files()


if __name__ == "__main__":
    main()
