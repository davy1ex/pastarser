from threading import Thread
from time import sleep
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO
import vk_api

from app import app, views, vk, group_id, socketio
from vk_settings import Config


def check_new_posts(old_list_posts):
    while True:
        new_posts = vk.wall.get(owner_id=int(group_id))["items"]
        # print(len(old_list_posts), len(new_posts))
        # print(posts)
        
        if int(old_list_posts[0]["id"]) != int(new_posts[0]["id"]):
            old_list_posts = new_posts
            print("\nНОВЫЙ ПОСТ\n")
            
            socketio.emit("check_posts", namespace="/posts")
        # socketio.emit("check_posts", namespace="/posts")
        # socketio.emit("test", namespace="/posts")

        sleep(15000)


# @app.route("/")
# def redirect_to_main_page():
#     return redirect(url_for("index", page=1))


# @app.route("/page_<page>")
# def index(page):
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


if __name__ == "__main__":
    #vk_session = vk_api.VkApi(login, password)
    
    posts = vk.wall.get(owner_id=int(group_id))["items"]

    socketio.start_background_task(check_new_posts, posts)
    socketio.run(app)

 