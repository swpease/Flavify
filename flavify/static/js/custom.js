// NB: There is a file main.js that just houses the sort function for my
// table as of now. This file will use jQuery, and if it is small,
// I will just load it in base.html footer (which is where it currently is loaded)

$(document).ready(function() {
  colorButtons();
})

function colorButtons() {
  $(".table-btn[data-user-like='True']").addClass("like-icon");
  $(".table-btn[data-user-dislike='True']").addClass("dislike-icon");
  $(".table-btn[data-user-save='True']").addClass("star-icon");
}
