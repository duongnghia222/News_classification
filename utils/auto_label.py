import os
import openai
from dotenv import load_dotenv
import json
# Load .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY_FREE")
openai.api_base = "https://api.chatanywhere.cn/v1"

context = "Tôi sẽ đưa cho bạn một bài báo, chỉ ra mã chứng khoán của công ty được nói đến trong bài báo. Sau đây là bài báo: "
article = ""
post_context = ". Hãy chỉ ra mã chứng khoán của công ty được nói đến trong bài báo trên, câu trả lời chỉ 1 từ"

with open('../data/contents/data_vietnambiz_1_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def process(content):
    a = content.split(' ')
    b = ' '.join(a[0:900])
    return b


article = process(data[4]['Content'])

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=context + article + post_context,
  temperature=0,
  max_tokens=50,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

generated_text = response.choices[0].text.strip()

print(generated_text)
