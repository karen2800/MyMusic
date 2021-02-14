
$(function() {

    $('#add_to_playlist').on('click', function() {
        // display loading
        document.getElementById('add_to_playlist').innerHTML = 'loading...';
        var show_data = document.getElementById('show_data').value;

        // post request
        req = $.ajax({
            url : '/actions/saved/playlists',
            type : 'POST',
            data : { show_data : show_data }
        });

        req.done(function(data) {
            // construct table
            var mytable = "";
            if (show_data != "True") {
                mytable += "<div class='table-padding'>"
            }
            mytable += "<table><tr>";
            mytable += "<th><h3><strong>Playlist Name</strong></h3></th>";

            if (show_data == "True") {
                mytable += "<th class='attr'><h3><strong>Valence</strong></h3></th>";
                mytable += "<th class='attr'><h3><strong>Tempo</strong></h3></th>";
                mytable += "<th class='attr'><h3><strong>Energy</strong></h3></th>";
                mytable += "<th class='attr'><h3><strong>Acousticness</strong></h3></th>";
                mytable += "<th class='attr'><h3><strong>Key</strong></h3></th></tr>";

                var attributes = ['valence', 'tempo', 'energy', 'acousticness', 'key'];

                // add attributes of saved songs
                mytable += "<tr><td><i>Averages</i></td>"; 
                for (var attr of attributes) {
                    mytable += "<td class='attr'>" + data.attr[attr] + "</td>";
                }
                mytable += "</tr>";
            }


            // add playlist data to table
            for (var p_id in data.data) {  
                mytable += "<tr><td><strong>" + data.data[p_id]['name'] + "</strong></td>"; 

                if (show_data == "True") {
                    for (var attr of attributes) {
                        var diff = data.attr[attr] - data.data[p_id]['attr'][attr];
                        if (data.data[p_id]['attr'][attr] < data.attr[attr]) {
                            if (diff <= 2) {
                                mytable += "<td class='attr less-1'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                            else if (diff <= 5) {
                                mytable += "<td class='attr less-2'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                            else {
                                mytable += "<td class='attr less-3'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                        } else {
                            if (diff * -1 <= 2) {
                                mytable += "<td class='attr greater-1'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                            else if (diff * -1 <= 5) {
                                mytable += "<td class='attr greater-2'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                            else {
                                mytable += "<td class='attr greater-3'>" + data.data[p_id]['attr'][attr] + "</td>";
                            }
                        }    
                    }
                }

                mytable += "<td><button>Select</button></td>";
                mytable += "</tr>";
            }
            mytable += "</table>";

            if (show_data != "True") {
                mytable += "</div>"
            }

            document.getElementById('add_to_playlist').innerHTML = 'Add to Existing Playlist';
            document.getElementById('top_playlists').innerHTML = mytable;
        });

    });

    $('a#heart_solid').on('click', function() {

        // get song data
        var song_id = $(this).attr('song_id');
        var artist = $(this).attr('artist');
        var title = $(this).attr('title');
        var loc = '#heart_solid' + song_id;

        // post request
        req = $.ajax({
            url : '/actions/saving',
            type : 'POST',
            data : { song_id : song_id, artist : artist, title : title }
        });

        req.done(function(data) {
            $(loc).fadeOut(25).fadeIn(200);
            
            // update icon to be filled in if song was added, or just an outline if song was removed
            if (data.song_added == true) {
                document.getElementById('heart_solid' + song_id).classList.add("solid");
            } else {
                document.getElementById('heart_solid' + song_id).classList.remove("solid");
            }
        });

    });

    $('a#heart').on('click', function() {

        // get song data
        var song_id = $(this).attr('song_id');
        var artist = $(this).attr('artist');
        var title = $(this).attr('title');
        var loc = '#heart' + song_id;

        // post request
        req = $.ajax({
            url : '/actions/saving',
            type : 'POST',
            data : { song_id : song_id, artist : artist, title : title }
        });

        req.done(function(data) {
            $(loc).fadeOut(25).fadeIn(200);

            // update icon to be filled in if song was added, or just an outline if song was removed
            if (data.song_added == true) {
                document.getElementById('heart' + song_id).classList.add("solid");
            } else {
                document.getElementById('heart' + song_id).classList.remove("solid");
            }
        });

    });

})(jQuery);