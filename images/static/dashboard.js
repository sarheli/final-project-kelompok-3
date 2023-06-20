/* script.js */

$(document).ready(function() {
    // Fungsi untuk memuat komentar saat halaman dimuat
    function loadComments() {
      $.ajax({
        url: '/get-comments',
        type: 'GET',
        success: function(response) {
          var commentList = $('#comment-list');
          commentList.empty();
  
          for (var i = 0; i < response.length; i++) {
            var comment = response[i];
            var commentItem = $('<li class="comment-item"></li>');
            $('<div class="comment-info">Pengirim: Pasien</div>').appendTo(commentItem);
            $('<div class="comment-text">' + comment + '</div>').appendTo(commentItem);
            commentItem.appendTo(commentList);
          }
        }
      });
    }
  
    // Memuat komentar saat halaman pertama kali dimuat
    loadComments();
  
    // Menangani pengiriman komentar melalui AJAX
    $('#comment-form').submit(function(e) {
      e.preventDefault();
      var commentInput = $('#comment-input').val().trim();
  
      if (commentInput !== '') {
        $.ajax({
          url: '/save-comment',
          type: 'POST',
          data: {
            comment: commentInput
          },
          success: function(response) {
            var commentList = $('#comment-list');
            var commentItem = $('<li class="comment-item"></li>');
            $('<div class="comment-info">Pengirim: Pasien</div>').appendTo(commentItem);
            $('<div class="comment-text">' + commentInput + '</div>').appendTo(commentItem);
            commentItem.appendTo(commentList);
            $('#comment-input').val('');
          }
        });
      }
    });
  });
  