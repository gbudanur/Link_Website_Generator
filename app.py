from flask import Flask, render_template, request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def generate_page():
    if request.method == "POST":
        meta_title = request.form.get("meta_title")
        title = request.form.get("title")
        link_names = request.form.getlist("link_name[]")
        link_urls = request.form.getlist("link_url[]")

        links = [{"name": name, "url": url} for name, url in zip(link_names, link_urls)]

        html_code = generate_html_code(meta_title, title, links)

        return render_template(
            "result.html", title=title, links=links, html_code=html_code
        )

    return render_template("index.html")


def generate_html_code(meta_title, title, links):
    template = """
<!DOCTYPE html>
<html lang="tr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title}</title>
    <style>
        {style}
    </style>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
</head>

<body>
    <div class="container">
        <div class="jumbotron">
            <h1 class="display-4">{title}</h1>
            <div class="button-container">
                {links}
            </div>
        </div>
    </div>
</body>

</html>
    """

    style = """
body {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: 'Montserrat', sans-serif;
            background: #000000; 
            user-select: none;
        }

        .jumbotron {
            background-color: transparent;
            text-align: center;
            padding: 2rem;
        }

        .display-4,
        .website-url {
            color: #ffffff;
            cursor: default; 
        }

        .display-4 {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10rem;
            margin-top: -2rem; 
        }
        
        .button-container {
            display: flex;
            flex-direction: column;
            gap: 1rem; 
        }

        .website-url {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 4rem; 
            font-size: 1.5rem;
            text-decoration: none;
            background-color: #333333; 
            border: none;
            color: #ffffff;
            opacity: 0;
            animation: fade-in 1s ease-in-out forwards;
            transition: transform 0.3s;
        }

        .website-url:hover {
            transform: scale(1.2);
            text-decoration: none;
        }

        @keyframes fade-in {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
    """

    link_elements = ""
    for link in links:
        link_elements += (
            f'<a href="{link["url"]}" class="website-url">{link["name"]}</a>\n'
        )

    return template.format(
        meta_title=meta_title, title=title, style=style, links=link_elements
    )


if __name__ == "__main__":
    app.run(debug=True)
