from app import app, db
from flask.cli import FlaskGroup

cli = FlaskGroup(app)

@cli.command('debug')
def runserver():
    app.run(debug=True, host="0.0.0.0", port=5000)

@cli.command('run')
def runworker():
    app.run(debug=False)

@cli.command('recreate_db')
def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()
