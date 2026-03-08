class Topic:
    def __init__(self):
        self._id = None
        self._topic_name = None
        self._sources = None
        self._source_links = None
        self._sentiment = None

    # ---------- Constructors ----------

    @classmethod
    def create_topic(cls, topic_name, sources, source_links, sentiment):
        topic = cls()
        topic.set_topic_name(topic_name)
        topic.set_sources(sources)
        topic.set_source_links(source_links)
        topic.set_sentiment(sentiment)
        return topic

    # ---------- Getters ----------
    def get_id(self):
        return self._id

    def get_topic_name(self):
        return self._topic_name

    def get_sources(self):
        return self._sources

    def get_source_links(self):
        return self._source_links

    def get_sentiment(self):
        return self._sentiment

    # ---------- Setters ----------
    def set_id(self, topic_id):
        self._id = topic_id

    def set_topic_name(self, topic_name):
        self._topic_name = topic_name

    def set_sources(self, sources):
        self._sources = sources

    def set_source_links(self, source_links):
        self._source_links = source_links

    def set_sentiment(self, sentiment):
        self._sentiment = sentiment

    # ---------- Utility ----------

    def to_dict(self):
        return {
            "id": self._id,
            "TopicName": self._topic_name,
            "Sources": self._sources,
            "SourceLinks": self._source_links,
            "sentiment": self._sentiment
        }

    @staticmethod
    def from_dict(data):
        topic = Topic()
        topic.set_id(data.get("id"))
        topic.set_topic_name(data.get("TopicName"))
        topic.set_sources(data.get("Sources"))
        topic.set_source_links(data.get("SourceLinks"))
        topic.set_sentiment(data.get("sentiment"))
        return topic
