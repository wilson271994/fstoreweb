/** Recherche dans la liste list */
$("#searchzone").on("keyup", function() {
  var value = $(this).val().toLowerCase();
  $("#filterzone tr").filter(function() {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
  });
});

/** creation */
$("#addzone").on("click", function(e){
  e.preventDefault();
  $("#zoneCreation").modal("show");
})

/**distributor mis a jour */
$(".updatezone").on("click", function(e){
  e.preventDefault();
  var id            = $(this).data('id');
  var title         = $(this).data('title');
  var description   = $(this).data('description');
  var price         = $(this).data('price');
  var map           = $(this).data('map');

  const delta = quill.clipboard.convert(description)
  quill.setContents(delta, 'silent')
  $('.post-content-update').val(description);

  $('#zoneid').val(id);
  $('#zonetitle').val(title);
  $('#zoneprice').val(price.split(',')[0]+'.'+price.split(',').pop());
  $('#zonemap').val(map);

  $('#zoneUpdate').modal("show");
})

