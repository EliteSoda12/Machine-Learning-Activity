from icrawler.builtin import BingImageCrawler
import os

keywords = [
    "bass fish","widemouth bass","smallmouth bass","striped bass","largemouth bass"
]

root_dir = "bass_fish_images"

for k in keywords:
    # Make a folder for each keyword
    folder = os.path.join(root_dir, k.replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    crawler = BingImageCrawler(storage={'root_dir': folder})
    crawler.crawl(keyword=k, max_num=60)  # start with 50 to test first