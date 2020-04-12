function redirectHTTPS() {  // forces https onto the site
    if (location.protocol !== 'https:' && window.location.hostname !== "localhost") {
        location.replace("https:" + location.href.substring(location.protocol.length));
    }
}

function printUrlDetails() { // debug only
    console.log("The URL of this page is: " + window.location.href);
    console.log("hostname " + window.location.hostname)
    console.log("HTTPS Version " + "https:" + location.href.substring(location.protocol.length))
}