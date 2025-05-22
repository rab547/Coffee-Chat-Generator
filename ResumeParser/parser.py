from groq import Groq
import os

def parse_resume(pdf_bytes):
    text_data = pdf_bytes.decode("utf-8")
    return text_data
    # client = Groq(api_key=os.getenv("API_KEY_GROQ"))
    # prompt = "Parse the following resume into a text description of its contents" + text_data
    # completion = client.chat.completions.create(
    # model="meta-llama/llama-4-scout-17b-16e-instruct",
    # messages=[
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "text",
    #                 "text": prompt
    #             }
    #         ]
    #     }
    # ],
    # temperature=1,
    # max_completion_tokens=1024,
    # top_p=1,
    # stream=False,
    # stop=None,
    # )
    # return completion.choices[0].message


