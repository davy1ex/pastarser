from flask import Flask, render_template
import vk_api

app = Flask(__name__)

@app.route("/")
def index():
    posts = vk.wall.get(owner_id="415754216")["items"]
    # for post in posts:/
        # return str(post["id"])
    return render_template("index.html", posts=posts)


if __name__ == "__main__":
    # auth vk
    login, password = '89879191850', 'guburo42'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        exit()

    vk = vk_session.get_api()

    app.run(debug=True)