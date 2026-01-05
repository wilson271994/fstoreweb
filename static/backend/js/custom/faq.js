/** gestion des tables list */
$("#searchfaq").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterfaq tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

/**blog creation */
$("#addfaq").on("click", function(e){
    e.preventDefault();
    $("#faqCreation").modal("show");
})

/** faq update */
$(".updatefaq").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var title           = $(this).data('title');
    var label           = $(this).data('label');
    var subject         = $(this).data('subject');
    var content         = $(this).data('content');
    var category        = $(this).data('category');
    var categoryid      = $(this).data('categoryid');

    $('.ql-editor p').html(content);
    $('.post-content-update').val(content);

    $('#faqid').val(id);
    $('#faqtitle').val(title);
    $('#faqlabel').val(label);
    $('#faqsubject').val(subject);
    $('#faqcategory').append(`<option value="`+categoryid+`" selected>`+category+`</option>`)
    $('#faqUpdate').modal("show");
})

/** gestion des tables list */
$("#searchcatfaq").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtercatfaq tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

/**faq category creation */
$("#addcatfaq").on("click", function(e){
    e.preventDefault();
    $("#faqCategoryCreation").modal("show");
})

/** faq category update */
$(".updatecatfaq").on("click", function(e){
    e.preventDefault();
    var id              = $(this).data('id');
    var title           = $(this).data('title');
    var description     = $(this).data('description');

    $('.ql-editor p').html(description);
    $('.post-content-update').val(description);

    $('#faqcatid').val(id);
    $('#faqcattitle').val(title);
    $('#faqCategoryUpdate').modal("show");
})