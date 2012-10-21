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
