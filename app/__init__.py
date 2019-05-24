from flask import Flask
import vk_api
from config import Config
from config import Vk_settings


app = Flask(__name__)
app.config.from_object(Config)


# auth vk

vk_session = vk_api.VkApi(Vk_settings.login, Vk_settings.password)

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
    exit()

vk = vk_session.get_api()