import requests as reqs 
import json 
import openai
from config import config 

TOKEN = config.TOKEN     
URL = config.URL 

def generateResponse(question:str,temp,prevConvo=None):
    print(f"{prevConvo} {question}")
    openai.api_key = TOKEN
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=f"{prevConvo} {question}",
      temperature=int(float(temp)),
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0].text)
    return (response.choices[0].text).strip()

def gen_image(prompt):
    openai.api_key = TOKEN
    response = openai.Image.create(
        
      prompt=prompt,
      n=1,
      size="1024x1024"
    )
    image_url = response['data'][0]['url']
    r = reqs.get(image_url)
    o = 'a'
    with open(f'images/{o}.jpg','wb') as f:
        f.write(r.content)
    return True 

