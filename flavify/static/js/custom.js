// NB: There is a file main.js that just houses the sort function for my
// table as of now. This file will use jQuery, and if it is small,
// I will just load it in base.html footer (which is where it currently is loaded)

$(document).ready(function() {
  $('#combos-table').on('click', '.table-btn', function(event) {
    event.preventDefault();
    var target = $(this);
    update_ucd(event, target);
  })

  $('#combos-table').on('editable-save.bs.table', function(editable, field, row, oldValue, $el) {
    // console.log("editable:", editable);
    // console.log("field: ", field);
    // console.log("row: ", row);
    // console.log("el: ", $el);
    // console.log(row.notes);
    // console.log("\n\n\n");
    update_ucd(editable, $el, row.notes);
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

function testFormatter(value, row, index) {
  console.log("value: " + value);
  console.log("row: ", row);
  console.log(index);
  console.log(this);
  // var content = '<span data-numings=' +  0 data-cid=0></span>
  var btn = '<span>test this</span>'
  // var btn = '<button type="button" class="table-btn like-btn" data-btn-on="x" aria-label="Like">' +
  //            '<span class="glyphicon glyphicon-thumbs-up table-icon" aria-hidden="true"></span>' +
  //           '</button>'
  return value;
}


function update_ucd(event, target, note = "") {
  var which_changed = get_which_changed(target);
  var $row = target.closest('tr');
  var $siblings = $row.find('.table-btn');
  $.ajax({
    url: $row.data('ajax-url'),
    type: "POST",
    data: JSON.stringify({
      'ucd_id': $row.attr('data-ucd'),
      'combo_id': $row.attr('data-cid'),
      'which_changed': which_changed,
      'note': note
    }),
    context: $row,
    success: function(data) {
      // this == context == $row
      this.find('.like-btn').attr('data-btn-on', data.like);
      this.find('.dislike-btn').attr('data-btn-on', data.dislike);
      this.find('.favorite-btn').attr('data-btn-on', data.favorite);
      this.attr('data-ucd', data.ucd_id);
      var $note = this.find('a');
      if ($note.hasClass('editable-unsaved')) {
        $note.removeClass('editable-unsaved');
        // $note.removeAttr('style');
      }
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
  if (target.hasClass('favorite-btn')) {
    return "favorite";
  }
  if (target.hasClass('editable')) {
    return "note";
  }
}
