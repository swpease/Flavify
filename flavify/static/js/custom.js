// NB: There is a file main.js that just houses the sort function for my
// table as of now. This file will use jQuery, and if it is small,
// I will just load it in base.html footer (which is where it currently is loaded)

$(document).ready(function() {
  $('#ingredients-selector').select2({
    ajax: {
      url: $('#ingredients-selector').data('ajax-select2'),
      dataType: 'json',
      delay: 250,
      data: function (params) {
              return {
                q: params.term, // search term
                page: params.page
              };
            }
    },
    minimumInputLength: 1,
    placeholder: "Pick your ingredients..."
  });

  /* Refreshes table data and goes to first page of table upon
     selecting ingredient.
  */
  $('#ingredients-selector').on('change', function(e) {
    // console.log($(this).val());
    // console.log($(this));  // #ingredients-selector
    var ids = $(this).val().join(',');
    $('#combos-table').bootstrapTable('selectPage', 1);
    // $('#combos-table').bootstrapTable('refresh', {query: {altnameids: ids}});
  });

  /* Goes to first page of table upon sorting. bootstrap-table event.
  */
  $('#combos-table').on('sort.bs.table', function(e, name, order) {
    $('#combos-table').bootstrapTable('selectPage', 1);
  });

  /* Saves user input when they click like or dislike or star.
  */
  $('#combos-table').on('click', '.table-btn', function(event) {
    event.preventDefault();
    var target = $(this);
    update_ucd(event, target);
  })

  /* Saves user input when they edit a note. bootstrap-table event.
  */
  $('#combos-table').on('editable-save.bs.table', function(editable, field, row, oldValue, $el) {
    // console.log("editable:", editable);
    // console.log("field: ", field);
    // console.log("row: ", row);
    // console.log("el: ", $el);
    // console.log(row.notes);
    // console.log("\n\n\n");
    update_ucd(editable, $el, row.notes);
  })

  // csrf setup for ajax. From Django docs.
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

/* Adds the select2 ingredients list to the params passed for bootstrap-table population.
*/
function queryParams(params) {
  var ids = $('#ingredients-selector').val().join(',');
  params.altnameids = ids;
  // console.log(JSON.stringify(params));
  return params;
}

// Formatters for bootstrap-table table cells.
function ingredientsFormatter(value, row, index) {
  // console.log(value);
  var content = '<span class="js-ingredients-entry" data-ucd="' + value.ucd +
                '" data-cid="' + value.cid + '">' +
                value.ingredients + '</span>'
  // console.log(content);
  return content;
}

function likeFormatter(value, row, index) {
  var btn = '<button type="button" class="table-btn like-btn" data-btn-on="' + value.like + '" aria-label="Like">' +
              '<span class="glyphicon glyphicon-thumbs-up table-icon" aria-hidden="true"></span>' +
            '</button>' +
            '<button type="button" class="table-btn dislike-btn" data-btn-on="' + value.dislike + '" aria-label="Dislike">' +
              '<span class="glyphicon glyphicon-thumbs-down table-icon" aria-hidden="true"></span>' +
            '</button>'
  // console.log(btn);
  return btn;
}

function favoriteFormatter(value, row, index) {
  // console.log("value: " + value);
  // console.log("row: ", row);
  // console.log(index);
  // console.log(this);
  var btn = '<button type="button" class="table-btn favorite-btn" data-btn-on="' + value + '" aria-label="Star">' +
              '<span class="glyphicon glyphicon-star table-icon" aria-hidden="true"></span>' +
            '</button>'
  // console.log(btn);
  return btn;
}
// End formatters

/* Updates user's db data.
*/
function update_ucd(event, target, note = "") {
  var which_changed = get_which_changed(target);
  var $table = $('#combos-table');
  var $row = target.closest('tr');
  var $ingredients = $row.find('.js-ingredients-entry');
  $.ajax({
    url: $table.data('ajax-url'),
    type: "POST",
    data: JSON.stringify({
      'ucd_id': $ingredients.attr('data-ucd'),
      'combo_id': $ingredients.attr('data-cid'),
      'which_changed': which_changed,
      'note': note
    }),
    context: $row,
    success: function(data) {
      // this == context == $row
      this.find('.like-btn').attr('data-btn-on', data.like);
      this.find('.dislike-btn').attr('data-btn-on', data.dislike);
      this.find('.favorite-btn').attr('data-btn-on', data.favorite);
      this.find('.js-ingredients-entry').attr('data-ucd', data.ucd_id);
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
  })
}

// Helper fn for update_ucd.
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
