const nunjucks = require("nunjucks");
const fs = require("fs");
const { exec } = require('child_process');


fs.readdir(".", (err, files) => {
    files.forEach(file => {
        var extension = file.substr(file.length - 4);
        if (extension === "html") {
            fs.writeFile("build/" + file, nunjucks.render(file), function(err, data) {
                console.log("Rendering " + "build/" + file);
                if (err) console.log(err);
                console.log("Compiled the Nunjucks, captain.");
            });
        }
    });
});


exec('cp -r images build')
