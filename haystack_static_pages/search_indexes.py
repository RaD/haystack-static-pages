from haystack import indexes
from haystack_static_pages.models import StaticPage


class StaticPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True, use_template=True,
        template_name='staticpage_text.txt'
    )
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')
    content = indexes.CharField(model_attr='content')
    description = indexes.CharField(model_attr='description')
    language = indexes.CharField(model_attr='language')
    
    def get_model(self):
        return StaticPage
