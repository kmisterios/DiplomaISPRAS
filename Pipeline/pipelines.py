# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests
import logging


class VerificationPipeline(object):
    def __init__(self, id_of_crawler, collection_len, test_len, service_url, path_to_data_folder):
        self.is_empty = 1
        self.items = []
        self.id_of_crawler = id_of_crawler
        self.collection_len = collection_len
        self.test_len = test_len
        self.service_url = service_url
        self.path_to_data_folder = path_to_data_folder
        file_test = open(path_to_data_folder + '/anomaly42_id_' + str(id_of_crawler) + '.json', 'w')
        file_test.close()
        file_collection = open(path_to_data_folder + '/collection'+str(id_of_crawler)+'.json', 'w')
        file_collection.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            id_of_crawler=crawler.settings.get('ID_OF_CRAWLER'),
            collection_len=crawler.settings.get('COLLECTION_LEN'),
            test_len=crawler.settings.get('TEST_LEN'),
            service_url=crawler.settings.get('SERVICE_URL'),
            path_to_data_folder=crawler.settings.get('PATH_TO_DATA_FOLDER')
        )

    def process_item(self, item, spider):
        self.items.append(dict(item))
        if len(self.items) == self.collection_len and self.is_empty:
            with open(self.path_to_data_folder + '/collection'+str(self.id_of_crawler)+'.json', 'w') as f:
                json.dump(self.items, f)
            self.items = []
            self.is_empty = 0

        if len(self.items) == self.test_len and not self.is_empty:
            with open(self.path_to_data_folder + '/anomaly42_id_' + str(self.id_of_crawler) + '.json', 'w') as f:
                json.dump(self.items, f)
            print('ВОШЕЛ')
            response = requests.post(self.service_url + '/requests/' + str(self.id_of_crawler) + '/verify', data='42')
            predicted_results = json.loads(response.content)
            try:
                prediction = predicted_results["prediction"]
                if sum(prediction) != 0:
                    error_index = prediction.index(1)
                    with open(self.path_to_data_folder + '/collection' + str(self.id_of_crawler) + '.json', 'r') as f:
                        data = json.loads(f.read())
                    error_index += len(data)
                    data = data + self.items
                    # you can also print other items here in case the algorithm is slightly wrong
                    print(data[error_index][self.key])
                    logging.error('Anomaly was found')
                else:
                    print('ВСЕ ОТЛ')
                    with open(self.path_to_data_folder + '/collection' + str(self.id_of_crawler) + '.json', 'r') as f:
                        data = json.loads(f.read())
                    if len(data) > self.collection_len:
                        with open(self.path_to_data_folder + '/collection' + str(self.id_of_crawler) + '.json', 'w') as f:
                            json.dump(data[-self.collection_len:], f)
                    self.items = []
            except KeyError:
                logging.error(predicted_results)
        return item
