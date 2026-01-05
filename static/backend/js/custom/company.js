$('#updateInfoModal').on('show.bs.modal', function(e) {
    var vision = $(e.relatedTarget).data('vision');
    var mission = $(e.relatedTarget).data('mission');

    const delta1 = quillvision.clipboard.convert(vision)
    quillvision.setContents(delta1, 'silent')
    $('.post-content-vision').val(vision);

    const delta2 = quillmission.clipboard.convert(mission)
    quillmission.setContents(delta2, 'silent')
    $('.post-content-mission').val(mission);
});

$('#updateCommissionCompanyModal').on('show.bs.modal', function(e) {
    var commissionexchange = $(e.relatedTarget).data('commissionexchange');
    var commissionsales = $(e.relatedTarget).data('commissionsales');
    var commissionproduct = $(e.relatedTarget).data('commissionproduct');
    var commissiondeposit = $(e.relatedTarget).data('commissiondeposit');
    var commissionwithdrawal = $(e.relatedTarget).data('commissionwithdrawal');
    $(e.currentTarget).find('#companycommissionsales').val(commissionsales);
    $(e.currentTarget).find('#companycommissionexchange').val(commissionexchange);
    $(e.currentTarget).find('#companycommissionproduct').val(commissionproduct);
    $(e.currentTarget).find('#companycommissiondeposit').val(commissiondeposit);
    $(e.currentTarget).find('#companycommissionwithdrawal').val(commissionwithdrawal);
});

$('#updatenPlanningCompanyModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var day = $(e.relatedTarget).data('day');
    var openhour = $(e.relatedTarget).data('openhour');
    var closehour = $(e.relatedTarget).data('closehour');
    $(e.currentTarget).find('#companyplanningid').val(id);
    $(e.currentTarget).find('#companyplanningday').val(day);
    $(e.currentTarget).find('#companyplanningopenhour').val(openhour);
    $(e.currentTarget).find('#companyplanningclosehour').val(closehour);
});

$('#updateConditionModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var title = $(e.relatedTarget).data('title');
    var description = $(e.relatedTarget).data('description');
    var producttitle = $(e.relatedTarget).data('producttitle');
    var productid = $(e.relatedTarget).data('productid');
    var servicetitle = $(e.relatedTarget).data('servicetitle');
    var serviceid = $(e.relatedTarget).data('serviceid');

    const delta = quill.clipboard.convert(description)
    quill.setContents(delta, 'silent')
    $('.post-content-update').val(description);

    var optionproduct = `<option value="${productid}" selected>${producttitle}</option>`;
    if(productid){
        $(e.currentTarget).find('#companyconditionproduct').append(optionproduct);
    }

    var optionservice = `<option value="${serviceid}" selected>${servicetitle}</option>`;
    if(serviceid){
        $(e.currentTarget).find('#companyconditionservice').append(optionservice);
    }

    $(e.currentTarget).find('#companyconditionid').val(id);
    $(e.currentTarget).find('#companyconditiontitle').val(title);
});

$('#updatePolicyModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var title = $(e.relatedTarget).data('title');
    var description = $(e.relatedTarget).data('description');

    const delta = quill.clipboard.convert(description)
    quill.setContents(delta, 'silent')
    $('.post-content-update').val(description);

    $(e.currentTarget).find('#companypolicyid').val(id);
    $(e.currentTarget).find('#companypolicytitle').val(title);
});

$('#updateAddressCompanyModal').on('show.bs.modal', function(e) {
    var id = $(e.relatedTarget).data('id');
    var continent = $(e.relatedTarget).data('continent');
    var country = $(e.relatedTarget).data('country');
    var city = $(e.relatedTarget).data('city');
    var address = $(e.relatedTarget).data('address');
    var postal = $(e.relatedTarget).data('postal');

    $(e.currentTarget).find('#companyaddressid').val(id);
    $(e.currentTarget).find('#companyaddresscontinent').val(continent);
    $(e.currentTarget).find('#companyaddresscountry').val(country);
    $(e.currentTarget).find('#companyaddresscity').val(city);
    $(e.currentTarget).find('#companyaddressaddress').val(address);
    $(e.currentTarget).find('#companyaddresspostal').val(postal);
});