/* add tablesorter to tables */
  $(document).ready(function()
    {
        $("#domaintable").addClass('tablesorter');
        $("#assignments").addClass('tablesorter');
        $("#domaintable").tablesorter();
        $("#assignments").tablesorter({
		headers: {
		2: { sorter: 'digit' } // should sort by number
 		}});
    }
  );

/* add bootstrap layout */
$("div.everything").addClass('row');
$("nav").wrap('<div class="span2">');
$(".main").wrap('<div class="span9 offset1">');

$("header").addClass('page-header');


$(".main table").wrap('<div class="row">').wrap('<div class="offset1 span8">');
$("table").addClass('table');
$("table").addClass('table-condensed');
$("table").addClass('table-hover');

$("tr.disclaim").addClass('success');
$("tr.nodisclaim").addClass('error');
$("tr.external").addClass('warning');
$("tr.external-present").addClass('info');

