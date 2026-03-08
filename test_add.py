import os, sys, dotenv
dotenv.load_dotenv()
from app.services.admin_service import add_topic
data = {
    'TopicName': 'Test Topic 2',
    'Sources': [{'source1': 'Test'}],
    'SourceLinks': {'link1': 'http://test.com'},
    'Sentiment': 0
}
res = add_topic(data)
print("Result:", res)
