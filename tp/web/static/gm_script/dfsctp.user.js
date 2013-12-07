// ==UserScript==
// @name        Differentiated score
// @namespace   dfsctp
// @include     http://www.trustpilot.dk/*
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

function generateScores(rma_score, price_score, delivery_score, general_score){
    $html = '<div>RMA: </div>' + generateProgressBar(rma_score);
    $html += '<div>Levering: </div>' + generateProgressBar(delivery_score);
    $html += '<div>Pris: </div>' + generateProgressBar(price_score);
    $html += '<div>Generelt: </div>' + generateProgressBar(general_score);
    return $html;
}
function errorMessage(message){
    return '<div>Det var ikke muligt at indlæse resultater for denne side' + message + '</div>';
}

function generateHTML(status, rma_score, price_score, delivery_score, general_score){
    $html = '<div itemref="support-box-companyinfo" class="overview sbox clearfix">';
    switch(status){
      case 10:
        $html += '<div class="headline"><h1><span itemprop="name">Differentierede scores</span></h1>';
        $html += generateScores(rma_score, price_score, delivery_score, general_score);
        break;
      case 20:
        $html += errorMessage(", da firmaets anmeldelser ikke er blevet læst.");
        break;
      case 21:
        $html += errorMessage(", da firmaet ikke er blevet indekseret.");
        break;
      default:
        $html += errorMessage(", da der er sket en ukendt fejl.");
    }
    $html += '</div>';
    return $html;
}

GM_xmlhttpRequest({
  method: "POST",
  url: "http://tp.runetm.dk/ajax/review/",
  data: "url="+document.URL,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  onload: function(response) {
    data = JSON.parse(response.responseText)
    $( generateHTML(data['status'], data['rma_score'], data['price_score'],data['delivery_score'],data['general_score']) ).insertAfter('div.overview');
  }
});