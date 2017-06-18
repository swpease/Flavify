// NB: There is a file main.js that just houses the sort function for my
// table as of now. This file will use jQuery, and if it is small,
// I will just load it in base.html footer (which is where it currently is loaded)

$(document).ready(function() {
  $('#combos-table').on('click', '.table-btn', function(event) {
    event.preventDefault();
    var target = $(this);
    console.log($(this).data('btn-on'));
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
  console.log($row.data('ajax-url'))
  $.ajax({
    url: $row.data('ajax-url'),
    type: "POST",
    data: JSON.stringify({
      'ucd_id': $row.data('ucd'),
      'like': $siblings.filter('.like-btn').data('btn-on'),
      'dislike': $siblings.filter('.dislike-btn').data('btn-on'),
      'save': $siblings.filter('.save-btn').data('btn-on'),
      // 'note':
    }),
    success: function(data) {
      console.log(data);
    },
    error: function(xhr, status, error) {
      console.log("Status: " + status);
      console.log("Error: " + error);
      console.dir(xhr);
    }
  }
  )
}
