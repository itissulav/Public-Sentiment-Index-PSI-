from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(auth_bp)      # auth blueprint
    app.register_blueprint(main_bp)      # main blueprint

    return app