from datetime import datetime
from flask import render_template, redirect, url_for

from app import app, vk, group_id, socketio





@app.route("/")
def redirect_to_main_page():
    return redirect(url_for("index", page=1))


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


# group_id = "-92157416"


def format_datetime(date):
    return datetime.utcfromtimestamp(int(date)).strftime("%d %b %H:%M:%S")
app.jinja_env.filters['datetime'] = format_datetime


# @app.route("/")
# def index():
#     return redirect(url_for("page", page=0))

# @app.route("/page_<page>")
# def page(page):
    
#     page = int(page)
#     offset = page // 9
#     if page % 9 != 0:
#         offset += 1
#     posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]

#     return render_template("index.html", posts=posts, page=page)


# @app.route("/sort_by_relevance_<page>")
# def sort_by_relevance(page):
#     page = int(page)
#     posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]
#     posts = sorted(posts, key=lambda post: post["likes"]["count"])[::-1]
    
#     return render_template("index.html", posts=posts, page=page)


# @app.route("/post_<id>")
# def post(id):
#     post_id = group_id + "_" + id
#     post = vk.wall.getById(posts=post_id)[0]
#     return render_template("post.html", post=post)