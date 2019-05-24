from flask import Flask, render_template
import vk_api



app = Flask(__name__)

group_id = "-26406986"


@app.route("/page_<page>")
def index(page):
    page = int(page)
    offset = page // 9
    if page % 9 != 0:
        offset += 1
    posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]

    return render_template("index.html", posts=posts, page=page)


@app.route("/sort_by_relevance_<page>")
def sort_by_relevance(page):
    page = int(page)
    posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]
    posts = sorted(posts, key=lambda post: post["likes"]["count"])[::-1]
    
    return render_template("index.html", posts=posts, page=page)


@app.route("/post_<id>")
def post(id):
    post_id = group_id + "_" + id
    post = vk.wall.getById(posts=post_id)[0]
    return render_template("post.html", post=post)


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
 