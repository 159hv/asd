from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create tables within application context
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from . import models
        db.create_all()
        
        # Initialize default data if needed
        if not models.Role.query.first():
            admin_role = models.Role(name='Administrator')
            user_role = models.Role(name='User')
            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.commit()

            # Create default admin user
            if not models.User.query.filter_by(username='admin').first():
                admin = models.User(username='admin', email='admin@example.com', role=admin_role)
                admin.password = 'admin123'
                db.session.add(admin)
                db.session.commit()

        # Initialize default system settings
        if not models.SystemSetting.query.first():
            default_setting = models.SystemSetting(app_name='舆情分析系统')
            db.session.add(default_setting)
            db.session.commit()

    return app
