from flask import Flask

from resources.users import users_api
from resources.game_data import game_api
# from resources.reviews import reviews_api
from flask_cors import CORS
from flask_login import LoginManager, login_required, logout_user


login_manager = LoginManager()


import models
import config

app = Flask(__name__)


app.secret_key = config.SECRET_KEY
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None





CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
# CORS(reviews_api, origins=["https://localhost:3000"], supports_credentials=True)
CORS(game_api, origins=["http://localhost:3000"], supports_credentials=True)


app.register_blueprint(users_api, url_prefix='/api/v1')
# app.register_blueprint(reviews_api, url_prefix='/api/v1')
app.register_blueprint(game_api, url_prefix='/api/v1')



if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
