from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import json
import os

app = FastAPI(title='Bulk Email Verification API')

# The token from your JavaScript example
VALID_TOKEN = 'kuni88si73mos37gfo6ph9aecu61x4zo'

class EmailRequest(BaseModel):
    emails: List[str]

@app.post('/api/verify/bulk')
def verify_bulk(request: EmailRequest, authorization: Optional[str] = Header(None)):
    # Basic security check
    if authorization != VALID_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid Authorization Token')

    results = []
    binary_path = '/usr/local/bin/reacher-cli'
    
    summary = {"total": len(request.emails), "valid": 0, "invalid": 0, "unknown": 0}

    for email in request.emails:
        try:
            process = subprocess.run(
                [binary_path, 'validate', email, '--json'],
                capture_output=True,
                text=True
            )
            output_json = json.loads(process.stdout.strip().split('\n')[-1])
            results.append(output_json)
            
            # Update summary based on reachability
            status = output_json.get('is_reachable', 'unknown')
            if status == 'safe':
                summary['valid'] += 1
            elif status == 'invalid':
                summary['invalid'] += 1
            else:
                summary['unknown'] += 1
        except Exception as e:
            results.append({'email': email, 'error': str(e)})
            summary['unknown'] += 1

    return {'status': 'completed', 'summary': summary, 'data': results}

@app.get('/')
def health_check():
    return {'status': 'active'}
