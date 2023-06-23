import os
import openai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="i will provide you an article, you have to classify which company is being discussed in the article, just the name only. Here is the article: "
         "Công ty Xây dựng Hoà Bình ghi nhận năm lỗ kỷ lục trong bối cảnh ngành xây dựng được đánh giá là \"bê bết nhất từ trước tới nay và chưa có năm nào nhà thầu xây dựng trải qua tình trạng khốc liệt như năm nay\" theo nhận định của ông Nguyễn Quốc Hiệp - Chủ tịch Hiệp hội các Nhà thầu Xây dựng Việt Nam",
  max_tokens=10,
  temperature=0
)

generated_text = response.choices[0].text.strip()

print(generated_text)
