from flask import Flask, render_template
<<<<<<< HEAD
from app import app, views
=======
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
>>>>>>> bbf0bc5603c3103a371c9cdc471754cfb021d965


if __name__ == "__main__":
    
    
    app.run(debug=True)
 