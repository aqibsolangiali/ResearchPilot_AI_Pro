import io, os
os.environ['RESEARCHPILOT_DATA_DIR']='/tmp/researchpilot-test-data'
from fastapi.testclient import TestClient
from app.main import app
import fitz
client=TestClient(app)

def test_health():
    assert client.get('/api/health').json()['status']=='ok'

def test_pdf_workflow():
    pdf=fitz.open()
    p=pdf.new_page()
    p.insert_text((72,72),'The climate study measured rainfall and temperature changes. ' * 5)
    data=pdf.tobytes();pdf.close()
    response=client.post('/api/documents',files={'file':('paper.pdf',data,'application/pdf')})
    assert response.status_code==201,response.text
    doc=response.json()
    result=client.post('/api/ask',json={'question':'What does the climate study measure?', 'document_ids':[doc['id']]}).json()
    assert result['grounded'] and result['citations'][0]['page']==1
    assert client.delete('/api/documents/'+doc['id']).status_code==200

def test_reject_non_pdf():
    assert client.post('/api/documents',files={'file':('malware.txt',b'not pdf','text/plain')}).status_code==400
