/** Recherche dans la liste list */
$("#searchtrafic").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtertrafic tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});