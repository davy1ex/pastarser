from threading import Thread
from time import sleep
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO
import vk_api

from app import app, views, vk, group_id, socketio


def check_new_posts(older_post):
    while True:
        new_posts = vk.wall.get(owner_id=int(group_id), count=2)["items"]

        # выбор самого нового поста, если он закреплён, то он не новый (лол)
        if new_posts[0]["is_pinned"]:
            new_post = new_posts[1]

        else:
            new_post = new_posts[0]
       
        # если новый пост не новый, то пушить уведомление
        if int(older_post["id"]) != int(new_post["id"]):
            older_post = new_post
            print("\nНОВЫЙ ПОСТ\n")            
            socketio.emit("check_posts", namespace="/posts")

        sleep(90)


if __name__ == "__main__":    
    posts = vk.wall.get(owner_id=int(group_id), count=2)["items"]

    # выбор самого нового поста, если он закреплён, то он не новый (лол)
    if posts[0]["is_pinned"]:
        older_post = posts[1]

    else:
        older_posts = posts[0]

    socketio.start_background_task(check_new_posts, older_post)
    socketio.run(app)

 