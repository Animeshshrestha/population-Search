$(".btn").click(function() {
  $(".btn").removeClass("active");
  $(this).addClass("active");
});

$(function() {
  $('[data-toggle="tooltip"]').tooltip();
});
