from lxml.html import fromstring
import requests
from ghost import Ghost
ghost = Ghost(download_images=False)
print 'initial'
page, resources = ghost.open('http://www.guidestar.org/AdvancedSearch.aspx')


def getDetailUrlForEIN(ein):
    print 'search'
    result, resources = ghost.evaluate('document.querySelector("#ctl00_phMainBody_orgSearchConfiguration_keywords_txtValue").value = "{}"'.format(ein))
    ghost.click('''form#aspnetForm div#ctl00_divPageContainer.page-container div.page-content div#ctl00_phMainBody_advSearches.adv-searches div#ctl00_phMainBody_2.tab-contents fieldset.one-col input.form-button''', expect_loading=True)
    return ghost.evaluate('''document.querySelector('#ctl00_phMainBody_rptSearchResults_ctl00_aOrganizationName').getAttribute('href')''')[0]


def scrape(href):
    r = requests.get('http://www.guidestar.org/'+href)
    root = fromstring(r.text)
    return dict(name=root.cssselect('h1.org-name')[0].text)

