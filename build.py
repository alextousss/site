import os
import yaml
from jinja2 import Environment, FileSystemLoader
import markdown
import markdown_katex
import datetime
import PyRSS2Gen as RSS2


def get_article_env(filename):
    meta = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            if line.startswith("-"):
                return yaml.load(meta, Loader=yaml.FullLoader)
            meta += line
    return {}


def get_article_content(filename):
    content = ""
    with open(filename, "r") as f:
        contentStarted = False
        for line in f.readlines():
            if contentStarted:
                content += line
            if line.startswith("-"):
                contentStarted = True
    return content


file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

os.system("rm -r build/*")
os.system("cp favicon.ico build/favicon.ico")
os.system("ln -s $PWD/images $PWD/build/images")
os.system("ln -s $PWD/css $PWD/build/css")

# On fait les pages normales
for filename in os.listdir("."):
    if filename.endswith(".html") and filename != "post-base.html":
        with open("build/" + filename, "w") as f:
            f.write(env.get_template(filename).render())
            print("Built " + filename)


# On fait la liste des posts
posts = []
rss_items = []
for filename in os.listdir("posts"):
    date = filename.split("_")[0]
    subject = filename.split("_")[1].split(".")[0].replace("-", " ")
    post = {
        "date": date,
        "subject": subject,
        "url": filename.replace("md", "html"),
        "filename": filename,
    }

    meta = get_article_env("posts/" + filename)
    if meta is not None:
        post.update(meta)
    print(meta)
    try:
        if meta["published"] is False:
            continue
    except Exception:
        pass
    print(date)
    rss_items.append(
        RSS2.RSSItem(
            title=subject,
            link="https://alextoussaint.com/" + filename.replace("md", "html"),
            description=meta["description"],
            pubDate=datetime.datetime.strptime(date, "%Y-%m-%d"),
        )
    )
    posts.append(post)

posts.sort(key=lambda post: post["date"])
posts.reverse()
print(posts)
# On fait la page d'acceuil des posts
with open("build/blog.html", "w") as f:
    string = env.get_template("blog.html").render(posts=posts)
    f.write(string)
    print("Built blog.html")


# On build chaque post
for post in posts:
    with open("build/" + post["filename"].replace("md", "html"), "w") as f:
        with open("posts/" + post["filename"], "r") as f_source:
            html = markdown.markdown(
                get_article_content("posts/" + post["filename"]),
                extensions=["markdown_katex", "footnotes"],
            )
            f.write(env.get_template("post-base.html").render(post=html, env=post))
        print("Built " + post["filename"])

rss = RSS2.RSS2(
    title="Alex Toussaint's feed",
    link="alextoussaint.com",
    description="Life can be much broader once you discover one simple fact: Everything around you that you call life was made up by people that were no smarter than you. And you can change it, you can influence it... Once you learn that, you'll never be the same again. -- Steve Jobs ",
    lastBuildDate=datetime.datetime.now(),
    items=rss_items,
)

rss.write_xml(open("build/feed.xml", "w"))
