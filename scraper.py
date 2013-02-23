from lxml.html import fromstring
import requests
from ghost import Ghost
ghost = Ghost(download_images=False)

selectors = dict(name='h1.org-name', missionStatement='#mission .html-snippet')


def getDetailUrlForEIN(ein):
    page, resources = ghost.open('http://www.guidestar.org/AdvancedSearch.aspx')
    result, resources = ghost.evaluate('document.querySelector("#ctl00_phMainBody_orgSearchConfiguration_keywords_txtValue").value = "{}"'.format(ein))
    ghost.click('''form#aspnetForm div#ctl00_divPageContainer.page-container div.page-content div#ctl00_phMainBody_advSearches.adv-searches div#ctl00_phMainBody_2.tab-contents fieldset.one-col input.form-button''', expect_loading=True)
    return ghost.evaluate('''document.querySelector('#ctl00_phMainBody_rptSearchResults_ctl00_aOrganizationName').getAttribute('href')''')[0]


def scrape(href):
    r = requests.get('http://www.guidestar.org/'+href)
    root = fromstring(r.text)
    res = {}
    for name, selector in selectors.iteritems():
        res[name] = root.cssselect(selector)[0].text
    return res

def doBatch(filename):
    for line in open(filename):
        parts = line.split('|')
        ein = parts[0]
        url = getDetailUrlForEIN(ein)
        with open('urls/{}.txt'.format(ein), 'w') as f:
            f.write(url)

if __name__ == '__main__':
    import sys
    doBatch(sys.argv[1])
