# farmdsl/signals.py

from farm.es.index_initializer import create_crop_index

def create_elasticsearch_index(sender, **kwargs):
    create_crop_index()