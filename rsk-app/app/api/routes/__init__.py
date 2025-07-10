from .resource_routes import resource_bp

def register_routes(app):
    app.register_blueprint(resource_bp)