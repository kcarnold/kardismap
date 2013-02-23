var server = require('webserver').create()
var fs = require('fs');

function getDetailUrlforEin(ein, callback) {
var page = require('webpage').create();
page.open('http://www.guidestar.org/AdvancedSearch.aspx', function (status) {
    console.log("before document call " + ein);
    var pass;
    var fn = '(function(){ein="'+ein+'";})()';
    page.evaluate(new Function(fn));

    var tmp = page.evaluate(function(){
        document.getElementById("ctl00_phMainBody_orgSearchConfiguration_keywords_txtValue").value = ein;
        document.querySelector('form#aspnetForm div#ctl00_divPageContainer.page-container div.page-content div#ctl00_phMainBody_advSearches.adv-searches div#ctl00_phMainBody_2.tab-contents fieldset.one-col input.form-button').click();
    });

    console.log(tmp);

    page.onLoadFinished = function(staus) {
        var url = page.evaluate(function(){
            return document.querySelector('#ctl00_phMainBody_rptSearchResults_ctl00_aOrganizationName').getAttribute('href');
        });
        //console.log("After load, I got: " + url);
        callback(url);
    };
    return foundUrl;
});
};

server.listen(12345, function(request, response) {
    var ein = request.post.request;
    console.log("got request");
    getDetailUrlforEin(ein, function(url) {
        console.log("done looking up URL");
        response.statusCode = 200;
        response.write(url);
        response.close();
        console.log("Sent response");
    });
});
