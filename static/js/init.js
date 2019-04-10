(function($) {
  $(function() {
    $(".dropdown-trigger").dropdown({ hover: false }, { coverTrigger: false });
    $(".sidenav").sidenav();
    $(".modal").modal({ opacity: 0.7 });
  }); // end of document ready
})(jQuery); // end of jQuery name space

document.addEventListener("DOMContentLoaded", function() {
  var elems = document.querySelectorAll(".modal");
  var instances = M.Modal.init(elems, options);
});
