// ==UserScript==
// @name        Test2
// @namespace   Test
// @include     http://www.trustpilot.dk/review/www.av-connection.dk
// @version     1
// @grant       GM_xmlhttpRequest
// ==/UserScript==
GM_xmlhttpRequest({
  method: "GET",
  url: "http://tp.runetm.dk/ajax/review/",
  onload: function(response) {
    data = JSON.parse(response.responseText)
    console.log(data);
    alert(data['result']);
  }
});
