/** gestion des tables list */
$("#searchblog").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterblog tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

/**blog creation */
$("#addblog").on("click", function(e){
    e.preventDefault();
    $("#blogCreation").modal("show");
})

/** blog update */
$(".updateblog").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var title           = $(this).data('title');
    var label           = $(this).data('label');
    var description     = $(this).data('description');
    var cover           = $(this).data('cover');

    $('.ql-editor p').html(description);
    $('.post-content-update').val(description);

    $('#blogid').val(id);
    $('#blogtitle').val(title);
    $('#bloglabel').val(label);
    $('#blogcover').attr('src', cover);
    $('#blogUpdate').modal("show");
})