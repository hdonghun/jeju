# Import necessary modules
from sqlalchemy import create_engine, text
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import folium
import uvicorn
import pymysql

# FastAPI application and template setup
app = FastAPI()

# Database connection setup using pymysql
db_connection = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/test5')

# Kakao Map API key
kakao_map_api_key = "ea528b04a0ffc2d34d585012bde67640"

# # Content IDs to be used
# content_ids = [
#     "CNTS_300000000015764",
#     "CNTS_000000000022942",
#     # ... (other content IDs)
# ]

# Template setup
templates = Jinja2Templates(directory="templates")

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# GET method definition for the /jeju endpoint
@app.get("/jeju", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        # Folium map creation
        m = folium.Map(location=[33.389074, 126.548862], zoom_start=12)

        # Fetching place information from Kakao Map API and adding markers
        for content_id in content_ids:
            kakao_map_params = {
                "id": content_id,
                "key": kakao_map_api_key,
            }
            response = requests.get("https://dapi.kakao.com/v2/local/geo/coord2address.json", params=kakao_map_params)

            # Check response status code
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()

                # Adjust template based on data structure
                place = data.get("documents", [])[0]
                if 'x' in place and 'y' in place:
                    # Extract latitude and longitude information
                    latitude = place['y']
                    longitude = place['x']

                    # Add marker for each place
                    folium.Marker(location=[latitude, longitude], popup=place['address_name']).add_to(m)
            else:
                # Return error message
                return f"Error: {response.status_code}<br>{response.text}"

        # Save the map as an HTML file
        map_file_path = "templates/jeju.html"
        m.save(map_file_path)

        return templates.TemplateResponse("jeju.html", {"request": request, "map_file_path": map_file_path})

    except requests.RequestException as e:
        # Return error message for request exception
        return f"Request Exception: {e}"


#인구혼잡도api
@app.get("/test6")
def test(request: Request):
    return templates.TemplateResponse("jeju_2.html", {"request": request})

#실시간교통api
@app.get("/test7")
def test(request: Request):
    return templates.TemplateResponse("traffic_API.html", {"request": request})

#마커표시
@app.get("/test2")
def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


#마커 여러개 표시
@app.get("/test10")
def test(request: Request):
    return templates.TemplateResponse("various_map.html", {"request": request})

#마커 여러개 표시 + 맵 크기 조정
@app.get("/test11")
def test(request: Request):
    return templates.TemplateResponse("various_map_mobile.html", {"request": request})

### 소민 : 마커 최종 5개 확정 
@app.get("/test12")
def test(request: Request):
    return templates.TemplateResponse("5icon_map.html", {"request": request})

### 소민 : 관광지(이미지, 주소, 장소명 등)
@app.get("/test13")
def test(request: Request):
    return templates.TemplateResponse("imagetap_map.html", {"request": request})

### 소민 : 마커 최종 5개 확정 + 관광지(이미지, 주소, 장소명 등) 진행중...
@app.get("/test14")
def test(request: Request):
    return templates.TemplateResponse("jjambong_map.html", {"request": request})

### 소민 : 불러와서 100개 마커 하기! 진행중...
@app.get("/test15")
def test(request: Request):
    return templates.TemplateResponse("100upload_map.html", {"request": request})

@app.get("/test3")
def test(request: Request):
    return templates.TemplateResponse("test2.html", {"request": request})

#카카오map api
@app.get("/test4")
def test(request: Request):
    return templates.TemplateResponse("marker.html", {"request": request})

# @app.get("/test5")
# async def test5_get(request: Request):
#     # Query data from the database
#     query = text("SELECT * FROM destination")
#     result = db_connection.execute(query).fetchall()

    # Print the data
    for data in result:
        print(data)

    return templates.TemplateResponse("jeju_4.html", {"request": request})


@app.get("/test8")
def test(request: Request):
    return templates.TemplateResponse("image_upload.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)