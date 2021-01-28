// my songs
var x = "";
var songs = JSON.parse('{{my_songs | tojson | safe}}');
//start = "<li class=\"list-group-item\"><a class=\"nav-link\" onclick=\"location.href='http:\/\/127.0.0.1:5000\/actions'\" type=\"submit\">"; 
//end = "</a></li>";

var start = "<a class=\"btn btn-outline-dark\" onclick=\"location.href='http:\/\/127.0.0.1:5000\/actions'\" type=\"submit\">"; 
var end = "</a>";

var i = 0;
for(i=0; i < songs.length; i++){
    x = x + start + songs[i] + end;
}

document.getElementById("my_songs").innerHTML = x;