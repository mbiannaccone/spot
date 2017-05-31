// JavaScript for photo galleries

// var slideIndex = 1;
// showDivs(slideIndex);

// function plusDivs(n) {
//   showDivs(slideIndex += n);
// }

// function showDivs(n) {
//   var i;
//   var x = document.getElementsByClassName("mySlides");
//   if (n > x.length) {slideIndex = 1;}
//   if (n < 1) {slideIndex = x.length;}
//   for (i = 0; i < x.length; i++) {
//      x[i].style.display = "none";
//   }
//   x[slideIndex-1].style.display = "block";
// }

var slideIndex = 1;
var gallery = $(".photoGallery").data("gallery");
showDivs(slideIndex, gallery);

function plusDivs(n, gallery) {
  showDivs(slideIndex += n, gallery);
}

function showDivs(n, gallery) {
  var i;
  var x = document.getElementsByClassName("mySlides-"+gallery);
  if (n > x.length) {slideIndex = 1;}
  if (n < 1) {slideIndex = x.length;}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";
  }
  x[slideIndex-1].style.display = "block";
}
