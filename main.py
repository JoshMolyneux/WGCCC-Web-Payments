from www import create_app, sql_connect
from flask import request
from urllib.parse import urlparse
from datetime import timedelta
import os

app = create_app()

app.permanent_session_lifetime = timedelta(days=7)


@app.before_first_request
def before_first_request_func():
    global LOCAL_SQL_MODE
    url = urlparse(request.base_url)
    hostname = url.hostname
    print("Connected to %s" % hostname)

    app.config['SQL_HOST'] = os.getenv("SQL_HOST")
    app.config['SQL_PORT'] = int(os.getenv("SQL_PORT"))
    app.config['SQL_USER'] = os.getenv("SQL_USER")
    app.config['SQL_PASSWORD'] = os.getenv("SQL_PASSWORD")

    connect = sql_connect(
        app.config['SQL_HOST'],
        app.config['SQL_PORT'],
        app.config['SQL_USER'],
        app.config['SQL_PASSWORD'],
        app.config['SQL_DATABASE']
    )

    cursor = connect.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS awestruck")
    connect.commit()
    connect.close()

    app.config['SQL_DATABASE'] = 'awestruck'

    connect = sql_connect(
        app.config['SQL_HOST'],
        app.config['SQL_PORT'],
        app.config['SQL_USER'],
        app.config['SQL_PASSWORD'],
        app.config['SQL_DATABASE']
    )

    cursor = connect.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users
        (id INT(6) PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(255),
        family_name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        address VARCHAR(255))''')
    connect.commit()
    connect.close()


if __name__ == '__main__':
    app.run(debug=True)
