import os
from jinja2 import Environment, FileSystemLoader
import markdown

file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

os.system("rm -r build/*")
os.system("cp -r images build/images")

# On fait les pages normales
for filename in os.listdir("."):
    if filename.endswith(".html"):
        with open("build/" + filename, "w") as f:
            f.write(env.get_template(filename).render())
            print("Built " + filename)


# On fait la liste des posts
posts = []
for filename in os.listdir("posts"):
    date = filename.split("_")[0]
    subject = filename.split("_")[1].split(".")[0].replace("-", " ")
    posts.append(
        {
            "date": date,
            "subject": subject,
            "url": filename.replace("md", "html"),
            "filename": filename,
        }
    )
print(posts)

# On fait la page d'acceuil des posts
with open("build/thoughts.html", "w") as f:
    string = env.get_template("thoughts.html").render(posts=posts)
    f.write(string)
    print("Built thoughts.html")


# On build chaque post
for post in posts:
    with open("build/" + post["filename"].replace("md", "html"), "w") as f:
        with open("posts/" + post["filename"], "r") as f_source:
            html = markdown.markdown(f_source.read())
            f.write(env.get_template("post-base.html").render(post=html))
        print("Built " + post["filename"])
