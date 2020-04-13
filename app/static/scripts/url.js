function isHTTPS(url) {
    /*takes in a string (ideally a url) and returns true if starts with https*/
    return /^(https)/.test(url);
}

function isHTTP(url) {
    /*takes in a string (ideally a url) and returns true if it doesn't start with https*/
    return !isHTTPS(url)
}

function redirectHTTPS() {  
    /*redirects site to https version if the site is in http*/
    if (location.protocol !== 'https:' && window.location.hostname !== "localhost") {
        location.replace("https:" + location.href.substring(location.protocol.length));
    }
}

/*test object*/
urlTest = {
    httpURL: "http://google.com", httpsURL: "https://google.com", domainUrl: "google.com",
    logTestResult(isSuccess) {
        /* Taketests in a boolean value of if a test is successful and logs the information*/
        if(isSuccess) {
            console.log("Test success!!")
        } else {
            console.log("Test fail!!")
        }
    },
    testHTTP: function() { 
        /*isHTTPS and isHTTP test*/

        console.log("Testing isHTTPS and isHTTP")

        console.log("testing if" + urlTest.httpURL + " matches for http");
        urlTest.logTestResult(isHTTP(urlTest.httpURL))

        console.log("testing if" + urlTest.httpURL + " does not match for https");
        urlTest.logTestResult(!isHTTPS(urlTest.httpURL))

        console.log("testing if" + urlTest.httpsURL + " matches for https");
        urlTest.logTestResult(isHTTPS(urlTest.httpsURL));

        console.log("testing if" + urlTest.domainUrl + " matches for http");
        urlTest.logTestResult(isHTTP(urlTest.domainUrl));
    },
    etc: function() {
        console.log("Miscalaneous testing");
        console.log("The URL of this page is: " + window.location.href);
        console.log("hostname " + window.location.hostname);
        console.log("HTTPS Version " + "https:" + location.href.substring(location.protocol.length));
    }

} 