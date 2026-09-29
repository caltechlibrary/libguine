import html
import re
import sys
import urllib.request

import bleach
import feedparser

from bs4 import BeautifulSoup

FEED_URL = "https://library.caltech.edu/blogs/rss.xml?blogConfigId=1449"
BLOG_URL = "https://library.caltech.edu/blog"
POST_COUNT = 2
EXCERPT_LENGTH = 400
# only posts carrying this LibGuides subject reach the home page
SUBJECT = "Library News"

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
    return text[: cut if cut > 0 else EXCERPT_LENGTH] + "..."


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


def subjects_of(node):
    # multiple subjects are comma-separated inside the link text, and the
    # featured block repeats its subject links for the responsive layout
    names = []
    for link in node.select("a.post-subjects-link"):
        name = link.get_text(strip=True).rstrip(",").strip()
        if name and name not in names:
            names.append(name)
    return names


def post_link(node):
    for parent in [node] + list(node.parents):
        link = parent.find("a", href=True)
        if link and "/blog" in link["href"]:
            return link["href"].strip()
    return None


def subject_slugs(html):
    # subjects exist only in the blog page markup, never in the feed
    soup = BeautifulSoup(html, "html.parser")
    slugs = set()
    for link in soup.select("a.post-subjects-link"):
        if link.get_text(strip=True).rstrip(",").strip() != SUBJECT:
            continue
        href = post_link(link)
        if href:
            slugs.add(slug(href))
    return slugs


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
    if SUBJECT not in subjects_of(container):
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


def parse_recent(feed_xml, allowed, exclude_slug, limit):
    entries = []
    for entry in feedparser.parse(feed_xml).entries:
        link = entry.get("link", "").strip()
        if not link or slug(link) == exclude_slug:
            continue
        if slug(link) not in allowed:
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
                "image": first_image(content),
            }
        )
    # the feed hoists a featured post to the top out of date order
    entries.sort(key=lambda item: item["date_sort"], reverse=True)
    return entries[:limit]


def escape(value):
    return bleach.clean(value or "", tags=[], strip=True)


def render_post(post, index):
    # matches the markup libguides.js builds from the SpringShare blog widget
    parts = [f'  <li id="lib-blogpost{index}">']
    parts.append(
        f'    <h3><a href="{escape(post["link"])}">{escape(post["title"])}</a></h3>'
    )
    if post.get("date"):
        parts.append(f'    <div class="post-date text-secondary">{escape(post["date"])}</div>')
    if post.get("image"):
        parts.append(f'    <img class="lib-blogpost-img" src="{escape(post["image"])}" alt="">')
    if post.get("excerpt"):
        parts.append(f'    <p>{escape(post["excerpt"])}</p>')
    parts.append(f'    <a href="{escape(post["link"])}" class="read-more">View Full Post</a>')
    parts.append("  </li>")
    return "\n".join(parts)


# allow local files as arguments for offline testing
feed_xml = fetch(FEED_URL) if len(sys.argv) < 3 else open(sys.argv[1]).read()
blog_html = fetch(BLOG_URL) if len(sys.argv) < 3 else open(sys.argv[2]).read()

allowed_slugs = subject_slugs(blog_html)
featured_post = parse_featured(blog_html)

if featured_post:
    # prefer the feed's link and date when it carries the same post
    for entry in feedparser.parse(feed_xml).entries:
        if slug(entry.get("link", "")) == slug(featured_post["link"]):
            featured_post["link"] = entry["link"].strip()
            featured_post["date"] = format_date(entry.get("updated", "")) or featured_post["date"]
            break

recent_posts = parse_recent(
    feed_xml,
    allowed_slugs,
    slug(featured_post["link"]) if featured_post else None,
    POST_COUNT - 1 if featured_post else POST_COUNT,
)

posts = ([featured_post] if featured_post else []) + recent_posts
rendered = [render_post(post, index) for index, post in enumerate(posts)]

with open("fragments/blog/library.html", "w") as fp:
    if rendered:
        fp.write('<ul class="cl-blog-widget">\n')
        fp.write("\n".join(rendered))
        fp.write("\n</ul>\n")
    else:
        fp.write("<!-- NO POSTS -->")

print(f"subject: {SUBJECT} ({len(allowed_slugs)} tagged posts on the blog page)")
print(f"featured: {featured_post['title'] if featured_post else 'none'}")
print(f"recent: {len(recent_posts)}")
