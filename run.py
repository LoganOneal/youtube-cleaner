from app import app, conn
from rq import Connection

if __name__ == '__main__':
    with Connection(conn):
        app.run()
