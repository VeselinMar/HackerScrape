import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.titleline')
subtext = soup.select('.subtext')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    # create empty list
    hn = []
    # use enumerate to get indexes + items
    for idx, item in enumerate(links):
        # find the 'a tags'
        a_tag = item.find('a')
        # fetch title and href from 'a tags'
        if a_tag:
            title = a_tag.getText()
            href = a_tag.get('href', None)
            # select .score and append only if there is a score
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99 and 'https' in href:
                    hn.append({'title': title, 'link': href, 'votes': points})
    # return populated list
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(links, subtext))
