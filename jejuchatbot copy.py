# 백엔드 프레임 워크인 fastapi 모듈 불러오기
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
import uvicorn
#from typing_extensions import Annotated
from typing import Annotated # 3.9 이상 버전부터는 이렇게 불러와야 함
from sqlalchemy import create_engine
import os 
import torchvision.transforms as transforms
from PIL import Image
import torch


import os
from fastapi import FastAPI, HTTPException
import openai

# 랜덤 시드 고정
torch.manual_seed(777)

app = FastAPI()


templates = Jinja2Templates(directory = "templates") # rendering할 때 필요함

from pydantic import BaseModel

class UserInput(BaseModel):
    user_input: str


openai.api_key = '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'

# 키 입력하는 다른 방법
# 터미널에서 키 입력 : export OPENAI_API_KEY='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'
# openai.api_key = os.getenv("OPENAI_API_KEY")

# API 키가 제대로 설정되었는지 확인
if not openai.api_key:
    print("OpenAI API key is missing. Please check your environment variables.")
    exit(1)

@app.get("/openai")
def read_root(request: Request):
    return templates.TemplateResponse("chatbotfinal.html", {"request": request})

@app.get("/map")
def read_root(request: Request):
    return templates.TemplateResponse("map_based_v2.html", {"request": request})

@app.post("/chat")
async def chat_bot(user_input: UserInput):
    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",   # GPT-3 챗 모델 사용
          messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant providing recommendations for 제주도 travel courses and tourist attractions."
                },
                {
                    "role": "user",
                    "content": user_input.user_input
                }
            ]
        )
        if response and response['choices'] and response['choices'][0]['message']['content']:
            return {"response": response['choices'][0]['message']['content']}
        else:
            return {"response": "OpenAI에서 응답을 받지 못했습니다."}
    except Exception as e:
        print("오류 발생:", e)  # 오류 메시지 출력
        raise HTTPException(status_code=500, detail=str(e))
    



if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)