from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Ashwath!\nHosting this on Vercel using flask framework as a backend. Lets do this team!'


if __name__ == '__main__':
    app.run()
