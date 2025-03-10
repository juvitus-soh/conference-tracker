import feedparser
from database import add_opportunity
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RSS_FEEDS = {
    'data_science': [
        'https://www.kdnuggets.com/feed',  # Valid RSS feed
        'http://arxiv.org/rss/stat.ML',  # Valid arXiv feed
    ],
    'ethical_ai': [
        'https://cacm.acm.org/feed/',  # Valid ACM feed
    ],
    'entrepreneurship': [
        'https://techcrunch.com/feed/',  # Valid TechCrunch feed
    ],
    'computer_engineering': [
        'https://queue.acm.org/rss/feeds/queuecontent.xml',  # Valid ACM Queue feed
    ]
}

DOMAIN_KEYWORDS = {
    'data_science': ['data science', 'machine learning', 'ai', 'deep learning', 'data analytics', 'statistics'],
    'ethical_ai': ['ethical ai', 'ai ethics', 'responsible ai', 'fairness in ai', 'bias in ai', 'ai governance'],
    'entrepreneurship': ['startups', 'entrepreneurship', 'venture capital', 'business ideas', 'innovation'],
    'computer_engineering': ['computer science', 'software engineering', 'computer engineering', 'programming',
                             'algorithms']
}

OPPORTUNITY_KEYWORDS = ['conference', 'symposium', 'workshop', 'summit', 'call for papers', 'submit a talk',
                        'registration open']
FUNDING_KEYWORDS = ['fully funded', 'scholarships available', 'travel grants', 'no registration fee']


def update_opportunities():
    logger.info("Starting opportunity update")
    for domain, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                logger.info(f"Parsing feed: {feed_url}")
                feed = feedparser.parse(feed_url)
                if feed.bozo:
                    logger.error(f"Feed {feed_url} is malformed: {feed.bozo_exception}")
                    continue
                for entry in feed.entries:
                    title = entry.get('title', '')
                    description = entry.get('description', entry.get('summary', ''))
                    link = entry.get('link', '')
                    pub_date = entry.get('published', entry.get('updated', datetime.now().isoformat()))

                    text = (title + ' ' + description).lower()
                    if any(keyword in text for keyword in DOMAIN_KEYWORDS[domain]):
                        opportunity_type = []
                        if any(keyword in text for keyword in OPPORTUNITY_KEYWORDS):
                            opportunity_type.append('conference')
                        if 'call for papers' in text or 'submit a talk' in text:
                            opportunity_type.append('speaker')
                        if 'registration' in text:
                            opportunity_type.append('attendee')

                        if opportunity_type:
                            fully_funded = 1 if any(keyword in text for keyword in FUNDING_KEYWORDS) else 0
                            opportunity_type_str = ','.join(opportunity_type)
                            add_opportunity(title, description, link, domain, opportunity_type_str, fully_funded,
                                            pub_date)
                            logger.info(f"Added opportunity: {title}")
            except Exception as e:
                logger.error(f"Error parsing {feed_url}: {e}")