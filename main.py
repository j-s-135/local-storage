from fastapi import FastAPI, File, Query, Form, UploadFile, HTTPException, APIRouter, Request, Response
import requests
import asyncio
import aiofiles
import os
import shutil
import logging
import time
import datetime
import hashlib
import typing

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload(file: UploadFile = File(...), filename: str = Form(...), filehash: str = Form(...)):
    try:
        data = await file.read()
        with open(f"./uploads/{filehash}", "wb") as w:
            w.write(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": filename}

@app.get("/download")
async def download(filename: str = Query(...), filehash: str = Query(...)):
    data = None
    try:
        async with aiofiles.open(f"./uploads/{filehash}", "rb") as r:
            data = await r.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return Response(content=data, media_type="application/octet-stream")
