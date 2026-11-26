"""App factory do Racha Conta."""

from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    banco_padrao = Path(app.instance_path) / "racha.db"
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{banco_padrao}",
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from app.routes import bp

    app.register_blueprint(bp)
    return app
