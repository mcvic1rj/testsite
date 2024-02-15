import requests
import json
from datetime import datetime
kevdb=json.loads(requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json').text)
from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('github-rss-kev')
fg.title('CISA KEV Rss Feed')
fg.author( {'name':'Ryan McVicar','email':'ryan@mcvicar.io'} )
fg.link( href='https://www.cisa.gov/known-exploited-vulnerabilities-catalog', rel='alternate' )
fg.logo('https://mcvic1rj.github.io/testsite/63107699-dcce-4688-a94a-6afa238d59b4.webp')
fg.subtitle('An alternate way to get your KEV Data')
fg.link( href='https://mcvic1rj.github.io/testsite/cisa-kev-rss.xml', rel='self' )
fg.language('en')
def add_feed_entry(feed, kev_item):
    fe=feed.add_entry()
    content_blob=''
    fe.author({"name":"CISA","uri":"cisa.gov"})
    if (kev_item['knownRansomwareCampaignUse'] == "Known"):
        fe.category({"term":"RansonwareCampaign"})
        content_blob+='<b>Known to be used in ransomware campaigns (per CISA)</b><br><br>'
    if (kev_item['product']):
        fe.category({"term":kev_item['product']})
    if (kev_item['vendorProject']):
        fe.category({"term":kev_item['vendorProject']})
    content_blob+=f'{kev_item["shortDescription"]}<br><br><b>Required Action(s):</b> {kev_item["requiredAction"]}'
    if (kev_item['dueDate']):
        content_blob+=f'<br><br><b>Due Date:</b> {kev_item["dueDate"]}'
    fe.content(content_blob)
    fe.description(kev_item['shortDescription'])
    fe.pubDate(datetime.strptime(kev_item['dateAdded'], "%Y-%m-%d").astimezone())
    fe.id(kev_item['cveID'])
    fe.link({"href":f"https://nvd.nist.gov/vuln/detail/{kev_item['cveID']}"})
    fe.title(kev_item['vulnerabilityName'])
[add_feed_entry(fg, x) for x in kevdb['vulnerabilities']]
fg.rss_file('feeds/cisa-kev-rss.xml')