import feedparser
from database import add_opportunity
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# RSS feeds with source sites, including LinkedIn placeholder
RSS_FEEDS = {
    'data_science': [
        {'url': 'https://www.kdnuggets.com/feed', 'source_site': 'https://www.kdnuggets.com'},
        {'url': 'https://arxiv.org/rss/stat.ML', 'source_site': 'https://arxiv.org'},
    ],
    'ethical_ai': [
        {'url': 'https://cacm.acm.org/feed/', 'source_site': 'https://cacm.acm.org'},
    ],
    'entrepreneurship': [
        {'url': 'https://techcrunch.com/feed/', 'source_site': 'https://techcrunch.com'},
    ],
    'computer_engineering': [
        {'url': 'https://queue.acm.org/rss/feeds/queuecontent.xml', 'source_site': 'https://queue.acm.org'},
    ],
    'all_domains': [  # LinkedIn placeholder
        {'url': 'https://rss.app/feeds/your-linkedin-feed-id.xml',  # Replace with actual RSS URL
         'source_site': 'https://www.linkedin.com'},
    ]
}

DOMAIN_KEYWORDS = {
    'data_science': ['data science', 'machine learning', 'ai', 'deep learning', 'data analytics', 'statistics'],
    'ethical_ai': ['ethical ai', 'ai ethics', 'responsible ai', 'fairness in ai', 'bias in ai', 'ai governance'],
    'entrepreneurship': ['startups', 'entrepreneurship', 'venture capital', 'business ideas', 'innovation'],
    'computer_engineering': ['computer science', 'software engineering', 'computer engineering', 'programming',
                             'algorithms'],
    'all_domains': ['conference', 'workshop', 'summit', 'data science', 'ai', 'ethics', 'startup', 'engineering']
    # Broader for LinkedIn
}

OPPORTUNITY_KEYWORDS = ['conference', 'symposium', 'workshop', 'summit', 'call for papers', 'submit a talk',
                        'registration open']
FUNDING_KEYWORDS = ['fully funded', 'scholarships available', 'travel grants', 'no registration fee']


def update_opportunities():
    logger.info("Starting opportunity update")
    for domain, feeds in RSS_FEEDS.items():
        for feed in feeds:
            feed_url = feed['url']
            source_site = feed['source_site']
            try:
                logger.info(f"Parsing feed: {feed_url}")
                feed_data = feedparser.parse(feed_url)
                if feed_data.bozo:
                    logger.error(f"Feed {feed_url} is malformed: {feed_data.bozo_exception}")
                    continue
                for entry in feed_data.entries:
                    title = entry.get('title', '')
                    description = entry.get('description', entry.get('summary', ''))
                    link = entry.get('link', '')
                    pub_date = entry.get('published', entry.get('updated', datetime.now().isoformat()))

                    text = (title + ' ' + description).lower()
                    logger.info(f"Feed entry: {title} - {description[:100]}")

                    if any(keyword in text for keyword in DOMAIN_KEYWORDS[domain]):
                        opportunity_type = ['conference']  # Default for testing
                        fully_funded = 1 if any(keyword in text for keyword in FUNDING_KEYWORDS) else 0
                        opportunity_type_str = ','.join(opportunity_type)
                        add_opportunity(title, description, link, domain, opportunity_type_str, fully_funded, pub_date,
                                        source_site)
                        logger.info(f"Added opportunity: {title}")
            except Exception as e:
                logger.error(f"Error parsing {feed_url}: {e}")