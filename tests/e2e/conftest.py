"""Fixtures dos testes end-to-end (Playwright)."""

import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture(scope="session")
def live_server(tmp_path_factory):
    """Sobe o app real numa thread, com SQLite temporário e porta livre.

    Devolve a URL base, ex.: "http://127.0.0.1:54321".
    """
    banco = tmp_path_factory.mktemp("e2e") / "racha.db"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{banco.as_posix()}",
    })
    servidor = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{servidor.server_port}"
    servidor.shutdown()
    thread.join(timeout=5)
