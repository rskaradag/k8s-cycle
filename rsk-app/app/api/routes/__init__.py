from .resource_routes import resource_bp
from .user_routes import user_bp

def register_routes(app):
    app.register_blueprint(resource_bp)
    app.register_blueprint(user_bp)