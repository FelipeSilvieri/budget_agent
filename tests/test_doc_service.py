import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from pydantic import ValidationError

from services.doc_service import BudgetItem, BudgetRequest, generate_document


def test_generate_document(tmp_path):
    item = BudgetItem(descricao="Camera", qtde=2, preco_unitario=100.0)
    req = BudgetRequest(itens=[item])
    path = generate_document(req)
    assert path.startswith("/static/")
    file_path = path.lstrip("/")
    assert file_path.endswith(".docx")


def test_generate_document_requires_items():
    with pytest.raises(ValidationError):
        BudgetRequest(itens=None)  # type: ignore[arg-type]


def test_generate_document_upload(monkeypatch, tmp_path):
    item = BudgetItem(descricao="Camera", qtde=1, preco_unitario=50.0)
    req = BudgetRequest(itens=[item])
    called = {}

    def fake_upload(filepath: str, folder_id: str) -> None:
        called["args"] = (filepath, folder_id)

    monkeypatch.setenv("GOOGLE_DRIVE_FOLDER_ID", "FOLDER")
    monkeypatch.setattr("services.doc_service.upload_file", fake_upload)

    result = generate_document(req)

    assert called["args"][1] == "FOLDER"
    assert called["args"][0].endswith(result.lstrip("/"))
