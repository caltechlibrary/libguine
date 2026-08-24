import html
import re
import sys
import urllib.request

import bleach
import feedparser

from bs4 import BeautifulSoup

FEED_URL = "https://library.caltech.edu/blogs/rss.xml?blogConfigId=1449"
BLOG_URL = "https://library.caltech.edu/blog"
RECENT_COUNT = 3
EXCERPT_LENGTH = 200

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "libguine (Caltech Library)"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def strip_html(raw):
    text = html.unescape(bleach.clean(raw or "", tags=[], strip=True))
    return re.sub(r"\s+", " ", text).strip()


def slug(url):
    # the feed and the blog page use different paths for the same post
    return (url or "").rstrip("/").rsplit("/", 1)[-1]


def make_excerpt(text):
    if len(text) <= EXCERPT_LENGTH:
        return text
    cut = text[:EXCERPT_LENGTH].rfind(" ")
    return text[: cut if cut > 0 else EXCERPT_LENGTH] + "…"


def first_image(raw):
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', raw or "")
    return match.group(1) if match else None


def format_date(value):
    # feed dates are ISO; blog page dates are MM/DD/YYYY
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", value or "")
    if not match:
        match = re.match(r"(\d{2})/(\d{2})/(\d{4})", value or "")
        if not match:
            return ""
        month, day, year = match.groups()
    else:
        year, month, day = match.groups()
    return f"{MONTHS[int(month) - 1]} {int(day)}, {year}"


def parse_featured(html):
    # the featured post is only marked in the public blog page markup
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one("#featured_posts_container")
    if container is None:
        return None
    link = container.find("a", href=True)
    heading = container.find(["h1", "h2", "h3"])
    if link is None or heading is None:
        return None
    body = container.select_one(".post-text-content")
    body_html = body.decode_contents() if body else ""
    date = ""
    for span in container.select(".date-user-subjects-text"):
        if re.match(r"\d{2}/\d{2}/\d{4}", span.get_text(strip=True)):
            date = span.get_text(strip=True)
            break
    return {
        "title": heading.get_text(strip=True),
        "link": link["href"].strip(),
        "date": format_date(date),
        "excerpt": make_excerpt(strip_html(body_html)),
        "image": first_image(body_html),
    }


def parse_recent(feed_xml, exclude_slug):
    entries = []
    for entry in feedparser.parse(feed_xml).entries:
        link = entry.get("link", "").strip()
        if not link or slug(link) == exclude_slug:
            continue
        content = ""
        if entry.get("content"):
            content = entry["content"][0].get("value", "")
        entries.append(
            {
                "title": entry.get("title", "").strip(),
                "link": link,
                "date_sort": entry.get("updated", ""),
                "date": format_date(entry.get("updated", "")),
                "excerpt": make_excerpt(strip_html(content)),
            }
        )
    # the feed hoists a featured post to the top out of date order
    entries.sort(key=lambda item: item["date_sort"], reverse=True)
    return entries[:RECENT_COUNT]


def escape(value):
    return bleach.clean(value or "", tags=[], strip=True)


def render_post(post, featured=False):
    classes = "cl-blog-item cl-blog-item--featured" if featured else "cl-blog-item"
    parts = [f'  <li class="{classes}">']
    if featured:
        parts.append('    <p class="cl-blog-badge">Featured</p>')
        if post.get("image"):
            parts.append(f'    <img class="cl-blog-image" src="{escape(post["image"])}" alt="">')
    parts.append(
        f'    <h3 class="cl-blog-title"><a href="{escape(post["link"])}">{escape(post["title"])}</a></h3>'
    )
    if post.get("date"):
        parts.append(f'    <p class="cl-blog-meta text-secondary">{escape(post["date"])}</p>')
    if post.get("excerpt"):
        parts.append(f'    <p class="cl-blog-excerpt">{escape(post["excerpt"])}</p>')
    parts.append("  </li>")
    return "\n".join(parts)


# allow local files as arguments for offline testing
feed_xml = fetch(FEED_URL) if len(sys.argv) < 3 else open(sys.argv[1]).read()
blog_html = fetch(BLOG_URL) if len(sys.argv) < 3 else open(sys.argv[2]).read()

featured_post = parse_featured(blog_html)

if featured_post:
    # prefer the feed's link and date when it carries the same post
    for entry in feedparser.parse(feed_xml).entries:
        if slug(entry.get("link", "")) == slug(featured_post["link"]):
            featured_post["link"] = entry["link"].strip()
            featured_post["date"] = format_date(entry.get("updated", "")) or featured_post["date"]
            break

recent_posts = parse_recent(feed_xml, slug(featured_post["link"]) if featured_post else None)

rendered = []
if featured_post:
    rendered.append(render_post(featured_post, featured=True))
for recent_post in recent_posts:
    rendered.append(render_post(recent_post))

with open("fragments/blog/library.html", "w") as fp:
    if rendered:
        fp.write('<ul class="cl-blog-list">\n')
        fp.write("\n".join(rendered))
        fp.write("\n</ul>\n")
    else:
        fp.write("<!-- NO POSTS -->")

print(f"featured: {featured_post['title'] if featured_post else 'none'}")
print(f"recent: {len(recent_posts)}")
