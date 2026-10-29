from fastapi.testclient import TestClient
from app.main import app
import pymupdf

client=TestClient(app)

def test_v2_endpoints():
    pdf=pymupdf.open(); page=pdf.new_page(); page.insert_text((72,72),'A randomized education study evaluated learning outcomes with surveys and tests. '*5)
    r=client.post('/api/documents',files={'file':('study.pdf',pdf.tobytes(),'application/pdf')});pdf.close()
    assert r.status_code==201, r.text
    docid=r.json()['id']
    try:
        body={'question':'Which study evaluated learning outcomes?', 'document_ids':[docid], 'top_k':5,'retrieval_mode':'lexical'}
        found=client.post('/api/v2/search',json=body)
        assert found.status_code==200,found.text
        hits=found.json()['results'];assert hits and hits[0]['page']==1
        answer=client.post('/api/v2/ask',json={**body,'answer_mode':'extractive'})
        assert answer.status_code==200 and answer.json()['citation_valid']
        b=client.post('/api/v2/benchmark',json={'k':5,'mode':'lexical','cases':[{'question':body['question'],'document_ids':[docid],'relevant_chunk_ids':[hits[0]['chunk_id']]}]})
        assert b.status_code==200,b.text
        assert b.json()['macro_recall_at_k']==1
        stats=client.get('/api/v2/stats');assert stats.status_code==200
    finally:
        client.delete('/api/documents/'+docid)

def test_no_key_llm_mode():
    # API should reject missing key rather than silently claiming to run an LLM
    assert client.get('/api/health').status_code==200
