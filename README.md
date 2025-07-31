### Gemini
- Using Model : gemini-2.0-flash-lite
- Max Limit: 2GB(File)
- File Structure :``` {"key": "request-1", "request": {"contents": [{"parts": [{"text": "Describe the process of photosynthesis."}]}], "generation_config": {"temperature": 0.7}}}```
- Process
    1. Upload your batch input file and request batch api
    2. Check the status of a batch
    3. Save the results

> **Gemini Batch API Document is very good descriptions. You would go to this document and read a guide.**  [Go to Guide](https://ai.google.dev/gemini-api/docs/batch-mode?hl=ko)

### OpenAI
- Using Model : gpt-3.5-turbo / gpt-4o-mini
- Max Limit: 200MB(File) / 50,000 Request / 40,000TPM , 3RPM, 200RPD (3.5) / 200,000TPM, 500RPM, 10,000RPD (4o-mini)
- File Structure : ```{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}} ```
- Process
    1. Upload your batch input file
        - return : 
            ``` { "id": "file-abc123","object": "file","bytes": 120000,"created_at": 1677610602,"filename": "mydata.jsonl","purpose": "fine-tune",} ```
    2. Create the batch
        - return :
            ``` {   "id": "batch_abc123",   "object": "batch",   "endpoint": "/v1/chat/completions",   "errors": null,   "input_file_id": "file-abc123",   "completion_window": "24h",   "status": "validating",   "output_file_id": null,   "error_file_id": null,   "created_at": 1714508499,   "in_progress_at": null,   "expires_at": 1714536634,   "completed_at": null,   "failed_at": null,   "expired_at": null,   "request_counts": {     "total": 0,     "completed": 0,     "failed": 0   },   "metadata": null } ```
    3. Check the status of a batch
    4. Retrieve the results
    5. get a list of all batches

> [Refer Guide](https://platform.openai.com/docs/guides/batch)

### Together
- Using Model : Meta Llama 3.1 8B Instruct Turbo
- Max Limit: 100MB(File) / 50,000 Request / 10M Tokens (per Model)
- File Structure : ```{"custom_id": "request-1", "body": {"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Hello, world!"}], "max_tokens": 200}}```
- Process
    1. Upload your batch input file
        - return : 
            ```FileResponse(   id='file-fa37fdce-89cb-414b-923c-2add62250155',   object=<ObjectType.File: 'file'>, 	...   filename='batch_input.jsonl',   bytes=1268723,   line_count=0,   processed=True,   FileType='jsonl')```
    2. Create the batch
        - return :
            ``` {   "id": "batch-xyz789",   "status": "VALIDATING",   "endpoint": "/v1/chat/completions",   "input_file_id": "file-abc123",   "created_at": "2024-01-15T10:00:00Z",   "request_count": 0,   "model_id": null } ```
    3. Check the status of a batch
    4. Retrieve the results

> [Refer Guide](https://docs.together.ai/docs/batch-inference)

---
### Used Dataset
- Question Answering
    1. BoolQ
        - question	title	answer	passage ("True", "False")
        - [Dataset](https://huggingface.co/datasets/google/boolq)
        - [Ref](https://arxiv.org/abs/1905.10044)
    2. QNLI 
        - text1	text2	label	idx	label_text ("entailment" = 0, "not entailment" = 1)
        - [Dataset](https://huggingface.co/datasets/SetFit/qnli)
        - [Ref](https://arxiv.org/pdf/1804.07461)

- Similarity and Paraphrase Tasks
    1. MRPC
        - text1	text2	label	idx	label_text ("equivalent" = 1, "not equivalent" = 0)
        - [Dataset](https://huggingface.co/datasets/SetFit/mrpc)
        - [Ref](https://paperswithcode.com/dataset/mrpc)

- Single Sentence Task 
    1. SST-2
        - text	label	label_text ("positive" = 1, "negative" = 0)
        - [Dataset](https://huggingface.co/datasets/SetFit/sst2)
        - [Ref](https://github.com/YJiangcm/SST-2-sentiment-analysis)
---

