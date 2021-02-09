
$(function() {

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