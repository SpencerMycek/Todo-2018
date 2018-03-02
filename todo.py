from app import create_app, db, cli
from app.models import User, Todo


app = create_app()
cli.refister(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Todo': Todo}
