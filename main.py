from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import json
import os

app = FastAPI(title='Bulk Email Verification API')

VALID_TOKEN = 'kuni88si73mos37gfo6ph9aecu61x4zo'

class EmailRequest(BaseModel):
    emails: List[str]

class SingleEmailRequest(BaseModel):
    email: str

@app.get('/health')
def health():
    return {'status': 'healthy'}

@app.post('/api/verify')
def verify_single(request: SingleEmailRequest, authorization: Optional[str] = Header(None)):
    if authorization != VALID_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid token')
    # Mocking reacher-cli logic for demonstration
    return {'email': request.email, 'status': 'valid'}

@app.post('/api/verify/bulk')
def verify_bulk(request: EmailRequest, authorization: Optional[str] = Header(None)):
    if authorization != VALID_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid token')
    results = [{'email': e, 'status': 'valid'} for e in request.emails]
    return {'results': results}
