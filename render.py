import os
import shutil
import pygments
import pygments.lexers
import pygments.formatters
from pathlib import Path
from datetime import datetime
from css_html_js_minify import html_minify, css_minify

html_base = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital@0;1&display=swap" rel="stylesheet"><title>'
navbar = '<nav><h1><a href="/">Misha\'s blog</a></h1><div><p><a href="/articles">Articles</a></p><p><a href="/about">About</a></p></div></nav>'

css_base = css_minify("""
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
center, dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, section {
	display: block;
}

body {
	line-height: 1;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}

body {
    background: #fafafa;
    font-family: 'IBM Plex Serif', serif;
    font-size: 20px;
}

nav {
    display: flex;
    background: #171717;
    color: white;
    z-index: 1;
    position: relative;
    align-items: center;
    justify-content: space-between;
}

nav > div {
    display: flex;
}

nav h1 {
    margin: 0 8px;
    font-size: 28px;
    line-height: 1.6;
}

nav p {
    margin: 0px 12px 0 6px;
}

nav h1, nav p {
    cursor: pointer;
}
nav h1:hover, nav p:hover {
    text-decoration: underline;
}
nav a {
    color: inherit;
    text-decoration: inherit;
}

a {
    color: #29B6F6;
}
""")

article_style = css_minify(css_base + """
.titledate {
    text-align: center;
    background: #222;
    color: white;
    padding: 32px;
    margin-bottom: 10px;
    box-shadow: 0 0 8px #444;
}

.title, .author {
    margin-bottom: 18px;
    font-size: 22px;
}

.title {
    font-size: 34px;
}

.date {
    color: gray;
    font-style: italic;
}

article {
    padding: 32px;
    line-height: 1.3;
    margin: 0 auto;
    max-width: 1200px;
}

@media only screen and (max-width: 700px) {
    article {
        padding: 12px;
    }
}

h2, h3 {
    font-size: 32px;
    font-weight: bold;
    padding: 32px 0;
}
h3 {
    font-size: 24px;
    padding: 16px 0;
}
article .standard {
    padding: 4px 0;
}

table {
    margin: 4px auto;
}
td {
    padding: 4px 6px;
    border: 1px black solid;
}

ul {
    list-style-type: disc;
}
ol {
    list-style-type: decimal;
}
ul ul, ul ol, ol ol, ol ul {
    padding-left: 32px;
}
/* increase spacing */
li::before {
    content: "";
    display: inline-block;
    width: 8px;
}""")
code_style = css_minify("""
.highlight pre {
    font-family: monospace;
    background: #fdfdfd;
    border: #aaa 1px solid;
    padding: 8px;
    margin: 8px 0;
    border-radius: 4px;
    white-space: pre-wrap;
}
.highlight .hll { background-color: #ffffcc }
.highlight .c { color: #999988; font-style: italic } /* Comment */
.highlight .err { color: #a61717; background-color: #e3d2d2 } /* Error */
.highlight .k { color: #000000; font-weight: bold } /* Keyword */
.highlight .o { color: #000000; font-weight: bold } /* Operator */
.highlight .cm { color: #999988; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #999999; font-weight: bold; font-style: italic } /* Comment.Preproc */
.highlight .c1 { color: #999988; font-style: italic } /* Comment.Single */
.highlight .cs { color: #999999; font-weight: bold; font-style: italic } /* Comment.Special */
.highlight .gd { color: #000000; background-color: #ffdddd } /* Generic.Deleted */
.highlight .ge { color: #000000; font-style: italic } /* Generic.Emph */
.highlight .gr { color: #aa0000 } /* Generic.Error */
.highlight .gh { color: #999999 } /* Generic.Heading */
.highlight .gi { color: #000000; background-color: #ddffdd } /* Generic.Inserted */
.highlight .go { color: #888888 } /* Generic.Output */
.highlight .gp { color: #555555 } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #aaaaaa } /* Generic.Subheading */
.highlight .gt { color: #aa0000 } /* Generic.Traceback */
.highlight .kc { color: #000000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #000000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #000000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #000000; font-weight: bold } /* Keyword.Pseudo */
.highlight .kr { color: #000000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #445588; font-weight: bold } /* Keyword.Type */
.highlight .m { color: #009999 } /* Literal.Number */
.highlight .s { color: #d01040 } /* Literal.String */
.highlight .na { color: #008080 } /* Name.Attribute */
.highlight .nb { color: #0086B3 } /* Name.Builtin */
.highlight .nc { color: #445588; font-weight: bold } /* Name.Class */
.highlight .no { color: #008080 } /* Name.Constant */
.highlight .nd { color: #3c5d5d; font-weight: bold } /* Name.Decorator */
.highlight .ni { color: #800080 } /* Name.Entity */
.highlight .ne { color: #990000; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #990000; font-weight: bold } /* Name.Function */
.highlight .nl { color: #990000; font-weight: bold } /* Name.Label */
.highlight .nn { color: #555555 } /* Name.Namespace */
.highlight .nt { color: #000080 } /* Name.Tag */
.highlight .nv { color: #008080 } /* Name.Variable */
.highlight .ow { color: #000000; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mf { color: #009999 } /* Literal.Number.Float */
.highlight .mh { color: #009999 } /* Literal.Number.Hex */
.highlight .mi { color: #009999 } /* Literal.Number.Integer */
.highlight .mo { color: #009999 } /* Literal.Number.Oct */
.highlight .sb { color: #d01040 } /* Literal.String.Backtick */
.highlight .sc { color: #d01040 } /* Literal.String.Char */
.highlight .sd { color: #d01040 } /* Literal.String.Doc */
.highlight .s2 { color: #d01040 } /* Literal.String.Double */
.highlight .se { color: #d01040 } /* Literal.String.Escape */
.highlight .sh { color: #d01040 } /* Literal.String.Heredoc */
.highlight .si { color: #d01040 } /* Literal.String.Interpol */
.highlight .sx { color: #d01040 } /* Literal.String.Other */
.highlight .sr { color: #009926 } /* Literal.String.Regex */
.highlight .s1 { color: #d01040 } /* Literal.String.Single */
.highlight .ss { color: #990073 } /* Literal.String.Symbol */
.highlight .bp { color: #999999 } /* Name.Builtin.Pseudo */
.highlight .vc { color: #008080 } /* Name.Variable.Class */
.highlight .vg { color: #008080 } /* Name.Variable.Global */
.highlight .vi { color: #008080 } /* Name.Variable.Instance */
.highlight .il { color: #009999 } /* Literal.Number.Integer.Long */""")

def compile_lyx_file(filename):
    if os.popen(f"lyx --export xhtml {filename}").close() != None:
        raise Exception("WTF")

    xhtml_filename = filename.parent / f"{filename.stem}.xhtml"
    with open(xhtml_filename, "r") as xhtml_f:
        lyx_output = xhtml_f.readlines()

    Path(xhtml_filename).unlink()
    # look for images
    potential_images = list(filename.parent.glob("**/*.svg")) + list(filename.parent.glob("**/*.png")) + list(filename.parent.glob("**/*.jpg")) + list(filename.parent.glob("**/*.jpeg"))
    images = [x for x in potential_images if len(x.name.split("_")) > 1 and x.name.split("_")[0].isdigit()]

    # take only the body
    lyx_output = lyx_output[(lyx_output.index('<body dir="auto">\n') + 1):lyx_output.index('</body>\n')]
    # syntax highlighting for pre class="listings programming-language"
    code_changes = []
    for index, line in enumerate(lyx_output):
        if "float-listings" in line:
            # first line in code
            _ = "<div class='float-listings'><pre class ='listings"
            after_start = line[(line.find(_) + len(_)):]
            first_index = index
            lang = "raw"
            if after_start[0] == ' ':
                lang = after_start[1:].split(" ")[0]
                lang = lang[:lang.index("'")]

            code_inside = after_start[(after_start.index(">") + 1):]

            line = lyx_output[index]
            while True:
                index += 1
                line = lyx_output[index]
                if line.endswith("</pre></div>\n"):
                    code_inside += line[:-13]
                    break
                else:
                    code_inside += line

            # we have the language and the code
            try:
                new_code = pygments.highlight(code_inside,
                                pygments.lexers.get_lexer_by_name(lang), pygments.formatters.HtmlFormatter())
            except:
                print("Error in", code_inside)
            code_changes.append((new_code, first_index, index))
    # apply code changes
    for change_code, change_start, change_end in code_changes:
        lyx_output[change_start] = change_code
        for i in range(change_start + 1, change_end + 1):
            lyx_output[i] = "REMOVE_THIS"

    extra_style = ""
    if len(code_changes) > 0:
        extra_style += code_style

    lyx_output = list(filter(lambda x: x != "REMOVE_THIS", lyx_output))
    return lyx_output, extra_style, images

def render_one_article(filename):
    lyx_output, extra_style, images = compile_lyx_file(filename)
    title = lyx_output[0][(lyx_output[0].index(">") + 1):lyx_output[0].index("</")]
    # put the title and the date (and author) in one titledate, and the rest into <article>
    if 'class="author"' in lyx_output[1]:
        date = lyx_output[2][(lyx_output[2].index(">") + 1):lyx_output[2].index("</")]
        lyx_output = ['<div class="titledate">', lyx_output[0], lyx_output[1], lyx_output[2], '</div class="titledate">', '<article>'] + lyx_output[3:] + ['</article>']
    else:
        date = lyx_output[1][(lyx_output[1].index(">") + 1):lyx_output[1].index("</")]
        lyx_output = ['<div class="titledate">', lyx_output[0], lyx_output[1], '</div class="titledate">', '<article>'] + lyx_output[2:] + ['</article>']
    # add the website navbar
    lyx_output = [navbar] + lyx_output

    result = html_minify(html_base + f"{title}</title><style>" + article_style + extra_style + "</style></head><body>" + "".join(lyx_output) + "</body></html>")
    return result, title, date, images

# Remove existing render
try:
    shutil.rmtree(Path("./docs"))
except:
    pass
Path("./docs").mkdir()
with open("./docs/CNAME", "w") as f:
    f.write("misha.farberbrodsky.com")
Path("./docs/articles/").mkdir()

article_metadata = {}

def parse_date(date_str):
    for date_format in ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"]:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            pass
    return "NULL"

# Go over every article and render it
for article_path in list(Path("./articles").iterdir()):
    if article_path.suffix != ".lyx":
        continue
    with open(Path("./docs/articles/") / (article_path.stem + ".html"), "w") as article_file:
        content, title, date, images = render_one_article(article_path)
        for image in images:
            shutil.move(str(image), str(Path("./docs/articles/")))
        article_metadata[article_path.stem] = {"title": title, "date": parse_date(date)}
        article_file.write(content)

# Create the article index.html

article_index_base_css = """
.meta_article_container {
    margin: 16px;
}
.meta_article {
    padding: 32px;
    margin: auto;
    max-width: 600px;
    background: #41414141;
    display: block;
    color: black;
    text-decoration: none;
    border-radius: 4px;
}
.meta_article:hover .meta_name {
    text-decoration: underline;
}
.meta_name {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 8px;
    line-height: 1.2;
}
.meta_date {
    color: gray;
    font-style: italic;
}
"""
article_index_css = css_minify(css_base + article_index_base_css + "nav { margin-bottom: 24px; }")
article_index = html_base + f"Misha's blog - Articles</title><style>{css_minify(css_base + article_index_css)}</style></head><body>"
article_index += navbar
article_index_content = ""
sorted_article_lst = list(reversed(sorted(article_metadata.items(), key=lambda x: x[1]["date"].timestamp())))
for article_name, article_metadata in sorted_article_lst:
    article_index_content += f'<div class="meta_article_container"><a href="/articles/{article_name}" class="meta_article"><div class="meta_name">{article_metadata["title"]}</div><div class="meta_date">{article_metadata["date"].strftime("%B %d, %Y")}</div></a></div>'

article_index += article_index_content + "</body></html>"
with open("./docs/articles/index.html", "w") as f:
    f.write(article_index)

# About page
now = datetime.now()
my_age = now.year - 2005
if now.month < 4 or (now.month == 4 and now.day < 20):
    my_age -= 1

compiled_about, compiled_about_extra_style, _ = compile_lyx_file(Path("./about.lyx"))
about_lyx = "".join(compiled_about).replace("INSERT_AGE_HERE", str(my_age))
about_page = html_base + f"Misha Farber Brodsky - About page</title><style>{article_style + compiled_about_extra_style}</style></head><body>{navbar}<article>{about_lyx}</article></body></html>"
with open("./docs/about.html", "w") as f:
    f.write(html_minify(about_page))

# Index page has both
index_page = html_base + f'Misha Farber Brodsky - About page</title><style>{css_minify(article_style + article_index_base_css)}</style></head><body>{navbar}<article>{about_lyx}<h2>Articles</h2></article>{article_index_content}</body></html>'
with open("./docs/index.html", "w") as f:
    f.write(html_minify(index_page))
