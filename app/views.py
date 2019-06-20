from datetime import datetime
from flask import render_template, redirect, url_for

from app import app, vk, group_id, socketio
from app.forms import SearchPosts


@app.route("/")
def redirect_to_main_page():
    return redirect(url_for("index", page=0))


@app.route("/page_<page>", methods=["GET", "POST"])
def index(page):
    page = int(page)
    offset = page // 9
    if page % 9 != 0:
        offset += 1
    posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]
    form = SearchPosts()

    if form.validate_on_submit():
        if form.text_field.data != "":
            posts = vk.wall.search(owner_id=group_id, query=form.text_field.data, count=9, owners_only=1)
            count = posts["count"]
            
            if count == 0:
                return redirect(url_for("redirect_to_main_page"))
            
            return render_template("index.html", posts=posts["items"], page=0, form=form, count=count, search=True)
            

    return render_template("index.html", posts=posts, page=page, form=form)


@app.route("/sort_by_relevance_<page>")
def sort_by_relevance(page):
    page = int(page)
    posts = vk.wall.get(owner_id=group_id, count=9, offset=page*9)["items"]
    posts = sorted(posts, key=lambda post: post["likes"]["count"])[::-1]
    form = SearchPosts()

    return render_template("index.html", posts=posts, page=page, form=form)


@app.route("/post_<id>")
def post(id):
    post_id = group_id + "_" + id
    print(vk.wall.getById(posts=post_id))
    post = vk.wall.getById(posts=post_id)[0]
    
    return render_template("post.html", post=post)


# штука, которая переводит дату в читабельный вид
def format_datetime(date):
    return datetime.utcfromtimestamp(int(date)).strftime("%d %b %H:%M:%S")

app.jinja_env.filters['datetime'] = format_datetime
