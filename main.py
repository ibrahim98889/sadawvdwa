from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import subprocess
import json
import os

app = FastAPI(title='Bulk Email Verification API')

class EmailRequest(BaseModel):
    emails: List[str]

@app.post('/verify')
def verify_bulk(request: EmailRequest):
    results = []
    binary_path = '/usr/local/bin/reacher-cli'

    for email in request.emails:
        try:
            process = subprocess.run(
                [binary_path, 'validate', email, '--json'],
                capture_output=True,
                text=True
            )
            output = process.stdout.strip().split('\n')[-1]
            results.append(json.loads(output))
        except Exception as e:
            results.append({'email': email, 'error': str(e)})

    return {'status': 'completed', 'data': results}

@app.get('/')
def health_check():
    return {'status': 'active'}
