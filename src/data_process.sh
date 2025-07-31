# python main_data.py --api_type "gemini" --data_name "mrpc" --batch_size 6000
# python main_data.py --api_type "gemini" --data_name "sst2" --batch_size 6000
# python main_data.py --api_type "gemini" --data_name "qnli" --batch_size 6000
# python main_data.py --api_type "gemini" --data_name "boolq" --batch_size 6000

python main_data.py --api_type "gpt" --data_name "mrpc" --batch_size 6000
python main_data.py --api_type "gpt" --data_name "sst2" --batch_size 6000
python main_data.py --api_type "gpt" --data_name "qnli" --batch_size 6000
python main_data.py --api_type "gpt" --data_name "boolq" --batch_size 6000

# python main_data.py --api_type "llama" --data_name "mrpc" --batch_size 6000
# python main_data.py --api_type "llama" --data_name "sst2" --batch_size 6000
# python main_data.py --api_type "llama" --data_name "qnli" --batch_size 6000
# python main_data.py --api_type "llama" --data_name "boolq" --batch_size 6000



