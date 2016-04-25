from flask import Flask
from blueprints.wiki.views import blueprint as wiki

app = Flask(__name__)
app.register_blueprint(wiki)

if __name__ == '__main__':
    app.run(debug=True)
