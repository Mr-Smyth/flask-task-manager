
/** Make sure Dom has been loaded Then activate Materialize side bar 
 *  Code credit Materialize components - navbar - Mobile Collapse Button
*/
document.addEventListener("DOMContentLoaded", function () {
    var elems = document.querySelectorAll(".sidenav");
    var instances = M.Sidenav.init(elems, { edge: "right", draggable: "true" });
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, {format: "dd mmmm, yyyy", yearRange: 3, showClearBtn: true, i18n: {done: "Select"}});
});


