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
