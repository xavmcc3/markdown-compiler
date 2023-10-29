from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urljoin
import markdown as md
import minify_html
import base64
import io
import re

extensions = ['admonition', 'tables', 'extra', 'attr_list', 'def_list', 'footnotes', 'md_in_html', 'fenced_code', 'sane_lists', 'codehilite', 'meta']
def load_html_from_md(path):
    with open(path, 'r', encoding='utf8') as f:
        text = f.read()
        converter = md.Markdown(extensions=extensions)
        html = converter.convert(text)
        f.close()
    return (html, converter.Meta)


def url_can_be_converted_to_data(tag):
    return tag.name.lower() == "img" and tag.has_attr('src') and not re.match('^data:', tag['src'])

def is_url(url):
    return urlparse(url).scheme != ""

def set_data_uri(link):
    image_url = urljoin("./src/", link.get('data-src') or link['src'])
    if is_url(image_url):
        image_data = urlopen(image_url).read()
    else:
        image_data = open(image_url, 'rb').read()
    
    ext = image_url.split('.')[-1]
    encoded = base64.b64encode(image_data).decode('utf-8')
    link['src'] = f'data:image/{ext};base64,{encoded}'

def set_data_uris(html):
    soup = bs(html, features="html.parser")
    for link in soup.find_all(url_can_be_converted_to_data):
        set_data_uri(link)
    return soup.prettify(formatter="html")


def is_link_tag(tag):
    return tag.name.lower() == "link" and tag.has_attr('href')

def insert_links(html):
    soup = bs(html, features="html.parser")
    for link in soup.find_all(is_link_tag):
        if link['rel'][0] == 'stylesheet':
            style = soup.new_tag('style')
            path = link['href']
            if is_url(path):
                content = urlopen(path).read().decode('utf8')
            else:
                content = open(path, 'rb').read().decode('utf8')
            style.string = content
            link.replaceWith(style)
    return soup.prettify(formatter="html")


def is_check_tag(tag):
    return tag.name.lower() == "li" and (str(tag.string).strip().startswith('[ ]') or str(tag.string).strip().startswith('[x]'))

def fix_checklists(html):
    soup = bs(html, features="html.parser")
    for li in soup.find_all(is_check_tag):
        checkbox = soup.new_tag('input')
        checkbox['type'] = 'checkbox'
        if li.string.strip().startswith('[x]'):
          checkbox['checked'] = None  
        
        span = soup.new_tag('span')
        span.string = li.string.strip()[3:].strip()
        
        label = soup.new_tag('label')
        label.append(checkbox)
        label.append(span)
        
        new_li = soup.new_tag('li')
        new_li.append(label)
        
        li.replaceWith(new_li)
    return soup.prettify(formatter="html")


def is_header_tag(tag):
    return tag.name.lower() == "li" and (str(tag.string).strip().startswith('[ ]') or str(tag.string).strip().startswith('[x]'))

def insert_hr(html):
    soup = bs(html, features="html.parser")
    for li in soup.find_all(is_header_tag):
        checkbox = soup.new_tag('input')
        checkbox['type'] = 'checkbox'
        if li.string.strip().startswith('[x]'):
          checkbox['checked'] = None  
        
        span = soup.new_tag('span')
        span.string = li.string.strip()[3:].strip()
        
        label = soup.new_tag('label')
        label.append(checkbox)
        label.append(span)
        
        new_li = soup.new_tag('li')
        new_li.append(label)
        
        li.replaceWith(new_li)
    return soup.prettify(formatter="html")


def setup_headers(html, meta):
    with open('./template.html', 'r', encoding='utf8') as f:
        text = f.read()
        f.close()
    for key in meta:
        text = re.sub(rf"{key}(?![^<]*?>)", str(meta[key][0]), text, flags=re.IGNORECASE)
    text = text.replace('*', html)
    return text


html, meta = load_html_from_md("./src/main.md")
html = set_data_uris(html)
html = fix_checklists(html)

html = setup_headers(html, meta)
html = insert_links(html)
html = minify_html.minify(html, minify_js=True, remove_processing_instructions=True)
with io.open('./out/md.html', 'w', encoding='utf8') as file:
    file.write(html)
