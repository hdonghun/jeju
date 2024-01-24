# conda activate fast_web 
# 웹 백엔드 프레임 워크인 fastapi 모듈 불러오기

# sudo lsof -i :8001
# kill -9 124742


import numpy as np


from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from typing_extensions import Annotated
import os

import uvicorn

from sqlalchemy import create_engine
import torchvision.transforms as transforms
from PIL import Image
import torch
import os

from pydantic import BaseModel
from fastapi.responses import JSONResponse

from typing import List, Optional, Any
from typing import Dict

from fastapi import HTTPException

import pandas as pd


# SQLAlchemy 연결 설정
DATABASE_URL = "mysql+pymysql://alpaco:1234@112.175.29.231:50003/tourist_destination?charset=utf8mb4"
engine = create_engine(DATABASE_URL)

app = FastAPI()

# Templates 설정
templates = Jinja2Templates(directory="templates")

# Pydantic 모델 정의 (request body를 검증하기 위해)
class DestinationCreate(BaseModel):
    contentsid: int
    title: str
    introduction: str
    address: str
    roadaddress: str
    phoneno: str
    alltag: str
    tag: str
    latitude: float
    longitude: float
    imgpath: str
    thumbnailpath: str

class DestinationResponse(BaseModel):
    message: str

# FastAPI 엔드포인트 - 데이터 삽입 0 Mysql
@app.post("/create_destination")
async def create_destination(destination: DestinationCreate):
    try:
        # DataFrame 생성
        df = pd.DataFrame([destination.dict()])

        # 데이터베이스 세션 생성
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # 데이터베이스에 데이터 삽입
        df.to_sql(name="destination", con=engine, if_exists="append", index=False)

        return JSONResponse(content={"message": "데이터가 성공적으로 삽입되었습니다."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"오류: {str(e)}"}, status_code=500)
    
    

# FastAPI 경로 수정
@app.get("/")
def hello(request: Request):
    return templates.TemplateResponse("1_v4.html", context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", context={'request': request})

@app.get("/logged_page")
def logged_page(request: Request):
    return templates.TemplateResponse("logged_page.html", context={'request': request})

@app.get("/create_account")
def create_account(request: Request):
    return templates.TemplateResponse("create_account.html", context={'request': request})


# 지도 기반 추천
@app.get("/map_based")
def map_based(request: Request):
    query = "SELECT * FROM jeju_dataset_hdh"
    df = pd.read_sql(query, engine)
    df = df.dropna(subset=["latitude", "longitude"])
    
    query_1 = "SELECT * FROM barrier_free"
    df_1 = pd.read_sql(query_1, engine)
    df_1 = df_1.dropna(subset=["latitude", "longitude"])
    

# 데이터를 HTML 템플릿에 전달
    # myqsql에서 기본 관광지 데이터 100개
    dataset_list = []
    dataset_latitude_longitude = []
    for _, row in df.iterrows():
        destination_info = {
            "title": row["title"],
            "introduction": row["introduction"],
            "address": row["address"],
            "phoneno": row["phoneno"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "imgpath": row["imgpath"],  # 이미지 경로 추가
        }
        
        dataset_list.append(destination_info)
        dataset_latitude_longitude.append(destination_info['latitude'])
        dataset_latitude_longitude.append(destination_info['longitude'])
        
    dataset_barrier_free = []
    for _, row in df_1.iterrows():
        barrier_free_info = {
            "title": row["title"],
            "introduction": row["introduction"],
            "address": row["address"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],

        }
        dataset_barrier_free.append(barrier_free_info)
    

    return templates.TemplateResponse(
        "map_based_v5.html",
        {"request": request, "places": dataset_list, "map_info": dataset_latitude_longitude, "barrier_free":dataset_barrier_free}
    )


# # 지도 기반 추천 테스트용
# @app.get("/map_test")
# def map_based(request: Request):
#     query = "SELECT * FROM dataset"
#     df = pd.read_sql(query, engine)
#     df = df.dropna(subset=["latitude", "longitude"])
#     dataset_list = []
#     dataset_latitude_longitude = []
#     for _, row in df.iterrows():
#         destination_info = {
#             "title": row["title"],
#             "introduction": row["introduction"],
#             "address": row["address"],
#             "phoneno": row["phoneno"],
#             "latitude": row["latitude"],
#             "longitude": row["longitude"],
#             "imgpath": row["imgpath"],  # 이미지 경로 추가
#         }
        
#         dataset_list.append(destination_info)
#         dataset_latitude_longitude.append(destination_info['latitude'])
#         dataset_latitude_longitude.append(destination_info['longitude'])

#     return templates.TemplateResponse(
#         "map_test.html",
#         {"request": request, "places": dataset_list, "map_info": dataset_latitude_longitude}
#     )
    
        
@app.get("/map_test")
def map_test(request: Request):
    return templates.TemplateResponse("map_test.html", {"request": request})
    
    
    
@app.get("/detailed_info")
def detailed_info(request: Request, title: str):
    query = f"SELECT * FROM jeju_dataset_hdh WHERE title = '{title}'"
    df = pd.read_sql(query, engine)

    if df.empty:
        return {"error": "No information found for the specified title"}

    row = df.iloc[0]
    destination_info = {
        "title": row["title"],
        "introduction": row["introduction"],
        "address": row["address"],
        "phoneno": row["phoneno"],
        "imgpath": row["imgpath"],
        "latitude": row["latitude"],
        "longitude": row["longitude"]
    }

    return templates.TemplateResponse(
        "detailed_info.html",
        {"request": request, "places": destination_info}
    )





if __name__ == '__main__':
                     # ip 설정,          port 설정하는 곳
    uvicorn.run(app, host= "localhost", port = 8001)
    
    
    
    
    
# fetchall()은 데이터베이스 커서에서 모든 결과를 한 번에 가져오는 메서드입니다. 이 메서드는 SELECT 쿼리를 실행하고 그 결과 집합의 모든 행을 리스트로 반환합니다.