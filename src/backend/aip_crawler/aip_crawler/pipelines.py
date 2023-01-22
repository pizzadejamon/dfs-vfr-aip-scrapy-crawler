# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from aip_crawler.items import AIPPageItem
from pathlib import Path
import base64
import codecs


class AipPagePipeline:
    def process_item(self, item, spider):
        if isinstance(item, AIPPageItem):
            actualsrc = item['src'][22:]
            path = Path(item['filename'])
            print(path)
            path.parents[0].mkdir(parents=True, exist_ok=True)


            path.write_bytes(base64.decodebytes(codecs.encode(actualsrc)))
        return item
