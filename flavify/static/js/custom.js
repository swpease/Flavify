// NB: There is a file main.js that just houses the sort function for my
// table as of now. This file will use jQuery, and if it is small,
// I will just load it in base.html footer (which is where it currently is loaded)

$(document).ready(function() {
  $('#combos-table').on('click', '.table-btn', function(event) {
    event.preventDefault();
    var target = $(this);
    update_ucd(event, target);
  })

  // csrf setup for ajax
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
})

function update_ucd(event, target) {
  var $row = target.closest('tr');
  var $siblings = $row.find('.table-btn');
  var which_changed = get_which_changed(target);
  console.log($row)
  $.ajax({
    url: $row.data('ajax-url'),
    type: "POST",
    data: JSON.stringify({
      'ucd_id': $row.data('ucd'),
      'which_changed': which_changed
    }),
    context: $row,
    success: function(data) {
      // this == context == $row
      this.find('.like-btn').attr('data-btn-on', data.like);
      this.find('.dislike-btn').attr('data-btn-on', data.dislike);
      this.find('.save-btn').attr('data-btn-on', data.favorite);
    },
    error: function(xhr, status, error) {
      console.log("Status: " + status);
      console.log("Error: " + error);
      console.dir(xhr);
    }
  }
  )
}

function get_which_changed(target) {
  if (target.hasClass('like-btn')) {
    return "like";
  }
  if (target.hasClass('dislike-btn')) {
    return "dislike";
  }
  if (target.hasClass('save-btn')) {
    return "favorite";
  }
}
