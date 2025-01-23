import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

def generate_by_text(prompt):
  genai.configure(api_key=os.getenv("GENAI-API-KEY"))
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content(prompt)
  return response

def generate_by_image(prompt, image_path):
  genai.configure(api_key=os.getenv("GENAI-API-KEY"))
  model = genai.GenerativeModel("gemini-1.5-flash")
  uploaded_file = genai.upload_file(image_path)
  content = [prompt, uploaded_file]
  response = model.generate_content(content)
  return response

if __name__ == "__main__":
  prompt = "自己紹介してください。"
  print(generate_by_text(prompt).text)
