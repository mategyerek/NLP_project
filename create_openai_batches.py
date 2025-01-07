from create_labels import Labeler, LABELS
import sys
import json
from os import path

if len(sys.argv) < 2:
    print("Give filename (such as data/cf_by_user.ndjson) as command line argument")
    sys.exit()

filename = sys.argv[1]
source_f = open(filename, "r")

data_dir = path.join(path.dirname(__file__), "data")
dest_n = 1
dest_f = open(path.join(data_dir, "openai_batch0.ndjson"), "wb")


for line in source_f:
    # print("line:", line)
    user_data = json.loads(line)
    username = user_data["username"]
    posts = user_data["posts"]

    job = {
        "custom_id": username,
        "method": "POST",
        "url": "/v1/vhat/completions", #TODO this is a placeholder, change it
        "body": {
            "model": "gpt-3.5", #TODO placeholder
            "messages": [
                {"role": "system", "content": "classify this"}, #TODO placeholder
                {"role": "user", "content": "\n---\n".join([ str(post["Text"]) for post in posts ])}
            ],
            "max_tokens": 100 #TODO placeholder
        }
    }
    job_json = bytes(json.dumps(job), "ascii")
    if len(job_json) + dest_f.tell() > 180000000:
        dest_f.close()
        dest_f = open(path.join(data_dir, f"openai_batch{dest_n}.ndjson"), "wb") 
        dest_n += 1
    
    dest_f.write(job_json)
    dest_f.write(b"\n")

dest_f.close()

if dest_n == 1:
    print("Job has been written to batch file openai_batch0.ndjson")
else:
    print(f"Job has been written to batch files openai_batch0.ndjson -> openai_batch{dest_n - 1}.ndjson")
