from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware


from core import doiInfo


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

@app.get("/doiCheck")
def doiCheck(doi:str):
    return doiInfo(doi)


