import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_knowledge_manifest_and_metadata():
    manifest=json.loads((ROOT/'knowledge/MANIFEST.json').read_text())
    assert len(manifest['documents'])==25
    for item in manifest['documents']:
        p=ROOT/'knowledge'/item['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
        text=p.read_text(encoding='utf-8');metadata=text.split('---',2)[1]
        for key in ['doc_id','title','category','source_type','source_url','version','updated_at','confidentiality','public_safe']:
            assert re.search('^'+key+':',metadata,re.M)
        assert 'confidentiality: public' in metadata and 'public_safe: true' in metadata
def test_widget_is_safe_and_bounded():
    text=(ROOT/'web/consultant.js').read_text(encoding='utf-8')
    assert 'textContent' in text and '.innerHTML' not in text
    assert '.slice(0,3)' in text and '/session/clear' in text
    assert '/api/v1/commercial/leads' not in text
def test_embedding_endpoint_requires_explicit_configuration(monkeypatch):
    import pytest
    from unittest.mock import patch
    from portfolio_rag.embeddings import Embeddings
    monkeypatch.delenv('RAG_TEI_URL',raising=False)
    with patch('portfolio_rag.embeddings.bounded_request') as network:
        with pytest.raises(KeyError):Embeddings()
        network.assert_not_called()
