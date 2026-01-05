$('#updateMenuModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var title = $(e.relatedTarget).data('title');
    var code = $(e.relatedTarget).data('code');
    var link = $(e.relatedTarget).data('link');
    $(e.currentTarget).find('#menuid').val(id);
    $(e.currentTarget).find('#menutitle').val(title);
    $(e.currentTarget).find('#menucode').val(code);
    $(e.currentTarget).find('#menulink').val(link);
});

$('#updateParentMenuModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var title = $(e.relatedTarget).data('title');
    var label = $(e.relatedTarget).data('label');
    var icon = $(e.relatedTarget).data('icon');
    $(e.currentTarget).find('#parentmenuid').val(id);
    $(e.currentTarget).find('#parentmenutitle').val(title);
    $(e.currentTarget).find('#parentmenulabel').val(label);
    $(e.currentTarget).find('#parentmenuicon').val(icon);
});

$('#updateMenuRuleModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var label = $(e.relatedTarget).data('label');
    var canread = $(e.relatedTarget).data('canread');
    var cancreate = $(e.relatedTarget).data('cancreate');
    var canupdate = $(e.relatedTarget).data('canupdate');
    var candelete = $(e.relatedTarget).data('candelete');
    var menu = `<option value="${$(e.relatedTarget).data('menuid')}" selected>${$(e.relatedTarget).data('menu')}</option>`;
    $(e.currentTarget).find('#menuruleid').val(id);
    $(e.currentTarget).find('#menurulelabel').val(label);
    $(e.currentTarget).find('#menurulemenu').append(menu);
    $(e.currentTarget).find('#menurulecanread').prop('checked', canread === 'True' ? true : false);
    $(e.currentTarget).find('#menurulecancreate').prop('checked', cancreate === 'True' ? true : false);
    $(e.currentTarget).find('#menurulecanupdate').prop('checked', canupdate === 'True' ? true : false);
    $(e.currentTarget).find('#menurulecandelete').prop('checked', candelete === 'True' ? true : false);
});

$('#updateProfilModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var title = $(e.relatedTarget).data('title');
    var description = $(e.relatedTarget).data('description');
    $(e.currentTarget).find('#profilid').val(id);
    $(e.currentTarget).find('#profiltitle').val(title);

    $('.ql-editor p').html(description);
    $('.post-content-update').val(description);
});

$('#updateUserProfilModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var description = $(e.relatedTarget).data('description');
    var profil = `<option value="${$(e.relatedTarget).data('profilid')}" selected>${$(e.relatedTarget).data('profil')}</option>`;
    var person = `<option value="${$(e.relatedTarget).data('personid')}" selected>${$(e.relatedTarget).data('person')}</option>`;
    $(e.currentTarget).find('#userprofilid').val(id);
    $(e.currentTarget).find('#userprofilprofil').append(profil);
    $(e.currentTarget).find('#userprofilperson').append(person);
    $('.ql-editor p').html(description);
    $('.post-content-update').val(description);
});

