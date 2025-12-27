#!/usr/bin/env python3
"""
wxr_to_markdown.py
Convert a WordPress WXR (export XML) to Markdown:
- Keep only the written words from each post (strip HTML, Gutenberg block comments, shortcodes).
- Use the local post time (wp:post_date) as the heading for each post.
- Include all posts, ordered by date ascending.

Usage:
  python wxr_to_markdown.py input.xml output.md
"""

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Namespaces used in WXR files
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

def strip_html_to_text(raw_html: str) -> str:
    """Remove Gutenberg block comments, shortcodes, and HTML tags. Return plain text paragraphs."""
    if not raw_html:
        return ""

    text = raw_html

    # Remove HTML comments, including Gutenberg block markers like <!-- wp:paragraph --> ... <!-- /wp:paragraph -->
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Remove common shortcodes like [contact-field ...] and generic [shortcode] patterns
    text = re.sub(r"\[[^\[\]\n\r]*\]", "", text)

    # Convert block-level separators to newlines before stripping tags
    # Handle <p>, </p>, <br>, <br/>, <div>, <li> etc.
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<p\s*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</div\s*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</li\s*>", "\n", text, flags=re.IGNORECASE)

    # Strip all remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape HTML entities
    text = html.unescape(text)

    # Normalize whitespace
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Trim trailing spaces on each line
    text = "\n".join(line.strip() for line in text.split("\n"))
    # Collapse many blank lines to at most one blank line
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text

def parse_posts(tree_root):
    """Extract posts (type=post) with (date, content) from the WXR XML root."""
    channel = tree_root.find("channel")
    if channel is None:
        return []

    posts = []
    for item in channel.findall("item"):
        ptype_el = item.find("wp:post_type", NS)
        if ptype_el is None or (ptype_el.text or "").strip() != "post":
            continue

        date_el = item.find("wp:post_date", NS)
        date_text = (date_el.text or "").strip() if date_el is not None else ""
        # Fallback to pubDate if wp:post_date missing
        if not date_text:
            pub_el = item.find("pubDate")
            date_text = (pub_el.text or "").strip() if pub_el is not None else ""

        # Parse date if possible; keep original string as fallback
        dt = None
        dt_out = date_text
        for fmt in ("%Y-%m-%d %H:%M:%S", "%a, %d %b %Y %H:%M:%S %z"):
            try:
                dt_obj = datetime.strptime(date_text, fmt)
                # Store formatted consistently without timezone: YYYY-MM-DD HH:MM:SS
                dt = dt_obj if "%z" not in fmt else dt_obj.astimezone(tz=None).replace(tzinfo=None)
                dt_out = dt.strftime("%Y-%m-%d %H:%M:%S")
                break
            except Exception:
                pass

        content_el = item.find("content:encoded", NS)
        content_raw = content_el.text if content_el is not None else ""
        content_text = strip_html_to_text(content_raw)

        # Skip empty posts (no words)
        if not content_text.strip():
            continue

        posts.append((dt if dt else date_text, dt_out, content_text))

    # Sort by parsed datetime if available; otherwise by the string
    posts.sort(key=lambda x: (x[0], x[1]))
    return posts

def to_markdown(posts):
    """Format posts into Markdown. Each post gets a '## TIMESTAMP' heading and plain text body."""
    parts = []
    for _, dt_out, body in posts:
        parts.append(f"## {dt_out}\n\n{body}\n")
    return "\n".join(parts).strip() + "\n"

def main():
    ap = argparse.ArgumentParser(description="Convert WordPress WXR XML to Markdown (words only, date as heading).")
    ap.add_argument("input_xml", help="Path to WordPress export XML (WXR)")
    ap.add_argument("output_md", help="Path to output Markdown file")
    args = ap.parse_args()

    try:
        tree = ET.parse(args.input_xml)
        root = tree.getroot()
    except Exception as e:
        print(f"Error: failed to parse XML: {e}", file=sys.stderr)
        sys.exit(1)

    posts = parse_posts(root)
    if not posts:
        print("Warning: no posts found.", file=sys.stderr)

    md = to_markdown(posts)

    try:
        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write(md)
    except Exception as e:
        print(f"Error: failed to write Markdown: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Done. Wrote {len(posts)} posts to {args.output_md}")

if __name__ == "__main__":
    main()
