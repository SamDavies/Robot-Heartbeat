# Run server.
from app import app
from app import database

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
