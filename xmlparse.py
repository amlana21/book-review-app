import requests
from lxml import html
import xml.etree.ElementTree as ET

def parse_response(api_url):
    resp = requests.get(api_url)
    tree = html.fromstring(resp.content)
    img_url = tree.xpath('//search/results/work/best_book/image_url')
    shrt_img_url = tree.xpath('//search/results/work/best_book/small_image_url')
    image_urls = []

    for elem in img_url:
        image_urls.append(elem.text)
    for elem in shrt_img_url:
        image_urls.append(elem.text)
    return image_urls