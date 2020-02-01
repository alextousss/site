const nunjucks = require("nunjucks");
const markdown = require('nunjucks-markdown')
const marked = require('marked')


var env = nunjucks.configure('', {autoescape: false, throwOnUndefined: true})

markdown.register(env, marked)

const fs = require("fs");
const { exec } = require('child_process');

let posts = []




fs.readdirSync("posts").forEach(file => {
    console.log(file)
    let index = file.split(".")[0]
    let subject = file.split(".")[1].replace("-", " ")
    posts.push([subject,  file])
})


setTimeout(usePosts, 500)


function usePosts() {
    console.log(posts)
    fs.writeFile("build/thoughts.html", nunjucks.render("thoughts.html", {posts}), function(err, data) {
        console.log(posts)
        console.log("Rendering post (build/thoughts.html), (" + posts + ")");
        if (err) console.log(err);
    });


    posts.forEach(post => {
        fs.writeFile("build/" + post[1].replace("md", "html"), nunjucks.render("post-base.html", {post: "posts/" + post[1]}), function(err, data) {
            console.log("Rendering post " + post[1]);
            if (err) console.log(err);
        });
    })


    fs.readdirSync(".").forEach(file => {
        var extension = file.substr(file.length - 4);
        if (extension === "html") {
            fs.writeFile("build/" + file, nunjucks.render(file), function(err, data) {
                console.log("Rendering " + "build/" + file);
                if (err) console.log(err);
            });
        }
        });


    exec('cp -r images build')
}
