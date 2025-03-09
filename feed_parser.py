import feedparser
from database import add_opportunity
from datetime import datetime

# RSS feeds for your domains (add more as needed)
RSS_FEEDS = {
    'data_science': [
        'https://www.datasciencecentral.com/page/news-feeds',  # Data Science Central
        'https://www.kdnuggets.com/feed',  # KDNuggets
        'http://arxiv.org/rss/stat.ML',  # arXiv Machine Learning
    ],
    'ethical_ai': [
        'https://www.artificial-intelligence.blog/rss-feeds/ai.xml',  # AI Blog
        'https://cacm.acm.org/feed/',  # ACM Communications
    ],
    'entrepreneurship': [
        'https://www.entrepreneur.com/page/215927',  # Entrepreneur.com
        'https://techcrunch.com/feed/',  # TechCrunch
    ],
    'computer_engineering': [
        'https://ieeetv.ieee.org/rssfeeds',  # IEEE Spectrum
        'https://queue.acm.org/rss/feeds/queuecontent.xml',  # ACM Queue
    ]
}

# Keywords for filtering
DOMAIN_KEYWORDS = {
    'data_science': ['data science', 'machine learning', 'AI', 'deep learning', 'data analytics', 'statistics'],
    'ethical_ai': ['ethical AI', 'AI ethics', 'responsible AI', 'fairness in AI', 'bias in AI', 'AI governance'],
    'entrepreneurship': ['startups', 'entrepreneurship', 'venture capital', 'business ideas', 'innovation'],
    'computer_engineering': ['computer science', 'software engineering', 'computer engineering', 'programming',
                             'algorithms']
}

OPPORTUNITY_KEYWORDS = ['conference', 'symposium', 'workshop', 'summit', 'call for papers', 'submit a talk',
                        'registration open']
FUNDING_KEYWORDS = ['fully funded', 'scholarships available', 'travel grants', 'no registration fee']


def update_opportunities():
    for domain, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title = entry.get('title', '')
                    description = entry.get('description', entry.get('summary', ''))
                    link = entry.get('link', '')
                    pub_date = entry.get('published', entry.get('updated', datetime.now().isoformat()))

                    # Check if relevant to domain
                    text = (title + ' ' + description).lower()
                    if any(keyword in text for keyword in DOMAIN_KEYWORDS[domain]):
                        # Determine opportunity type
                        opportunity_type = []
                        if any(keyword in text for keyword in OPPORTUNITY_KEYWORDS):
                            opportunity_type.append('conference')
                        if 'call for papers' in text or 'submit a talk' in text:
                            opportunity_type.append('speaker')
                        if 'registration' in text:
                            opportunity_type.append('attendee')

                        if opportunity_type:
                            # Check funding status
                            fully_funded = 1 if any(keyword in text for keyword in FUNDING_KEYWORDS) else 0
                            opportunity_type_str = ','.join(opportunity_type)

                            # Store in database
                            add_opportunity(title, description, link, domain, opportunity_type_str, fully_funded,
                                            pub_date)
            except Exception as e:
                print(f"Error parsing {feed_url}: {e}")