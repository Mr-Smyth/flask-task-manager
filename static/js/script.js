
/** Make sure Dom has been loaded Then activate Materialize side bar 
 *  Code credit Materialize components - navbar - Mobile Collapse Button
*/
document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".sidenav");
  var instances = M.Sidenav.init(elems, {edge: "right", draggable: "true"});
});
