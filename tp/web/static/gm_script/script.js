// ==UserScript==
// @name        Differentiated score
// @namespace   dfsctp
// @include     http://www.trustpilot.dk/review/www.av-connection.dk
// @version     1
// @grant       GM_xmlhttpRequest
// @grant       GM_addStyle
// @grant       GM_getResourceText
// @resource    bscss   http://getbootstrap.com/dist/css/bootstrap.min.css
// @require     http://code.jquery.com/jquery-1.10.2.min.js
// ==/UserScript==
var jqUI_CssSrc = GM_getResourceText ("bscss");
GM_addStyle (jqUI_CssSrc);
this.$ = this.jQuery = jQuery.noConflict(true);

function generateProgressBar(score){
    $score_class = 'progress-bar-success';
    if (score >= 0 && score < 33){
        $score_class = 'progress-bar-danger';
    } else if (score >= 33 && score < 66){
        $score_class = 'progress-bar-warning';    
    }
    $html = '<div class="progress"><div class="progress-bar ' + $score_class + '" role="progressbar" aria-valuenow="' + score + '" aria-valuemin="0" aria-valuemax="100" style="width: ' + score + '%;"><span class="sr-only">' + score +'% Complete</span></div></div>';
    return $html;
}

function generateHTML(rma_score, price_score, delivery_score, general_score){
    $html = '<div itemref="support-box-companyinfo" class="overview sbox clearfix">';
    $html += '<div class="headline"><h1><span itemprop="name">Differentierede scores</span></h1>';
    $html += '<div>RMA: </div>' + generateProgressBar(rma_score);
    $html += '<div>Levering: </div>' + generateProgressBar(delivery_score);
    $html += '<div>Pris: </div>' + generateProgressBar(price_score);
    $html += '<div>Generelt: </div>' + generateProgressBar(general_score);
    $html += '</div>';
    return $html;
}

GM_xmlhttpRequest({
  method: "POST",
  url: "http://tp.test/ajax/review/",
  data: "url="+document.URL,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  onload: function(response) {
    data = JSON.parse(response.responseText)
    $( generateHTML(data['rma_score'], data['price_score'],data['delivery_score'],data['general_score']) ).insertAfter('div.overview');
  }
});