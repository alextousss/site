import os
from jinja2 import Environment, FileSystemLoader
import markdown

file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)


# On fait la liste des posts
posts = []
for filename in os.listdir("posts"):
    index = filename.split(".")[0]
    subject = filename.split(".")[1].replace("-", " ")
    posts.append((subject, filename))

# On fait la page d'acceuil des posts
with open("build/thoughts.html", "w") as f:
    f.write(env.get_template("thoughts.html").render(posts=posts))
    print("Built thoughts.html")


# On build chaque post
for post in posts:
    with open("build/" + post[1].replace("md", "html"), "w") as f:
        with open("posts/" + post[1], "r") as f_source:
            html = markdown.markdown(f_source.read())
            f.write(env.get_template("post-base.html").render(post=html))
        print("Built thoughts.html")


# On fait les pages normales
for filename in os.listdir("."):
    with open("build/" + filename, "w") as f:
        f.write(env.get_template("thoughts.html").render())
        print("Built thoughts.html")
