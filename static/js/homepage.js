
AOS.init({
 duration: 1500;
});
/*
$("#showdescbtn").on({
     mouseenter: function() {
         $("#desc3inner").show();
     },
     mouseleave: function() {
         $("#desc3inner").hide();
     },
     click: function() {
         alert('Holy crap! Someone clicked me!');
     }
});
*/

$("#showdescbtn1").click(function(){
  alert('clicked');
  $("#desc3inner1").show();
  $("#showdescbtn1").hide();
});
