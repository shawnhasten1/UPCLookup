var upc = '070847017554';
var app = new Vue({
    el: '#itemDetails',
    delimiters: ['[[', ']]'],
    data: {
      item: {}
    }
})

function getItem(){
    var url = '/api/v1/getEdamam?upc='+upc;
    $.get(url, function( data ) {
        app.item = data;
    });
}

$("#submitUPC").click(function(){
    upc = document.getElementById("upcInput").value;
    getItem();
})

setInterval(function(){
    var bars = document.getElementsByClassName("progress-bar");
    for(var i = 0; i<bars.length; i++){
        var value = $(bars[i]).attr("aria-valuenow");
        bars[i].style.width = value+"%";
        console.log(value);
    }
},100)