/** Recherche dans la liste list */
$("#searchseller").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterstore tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

/**administrateur mis a jour */
$(".updateSeller").on("click", function(e){
  e.preventDefault();
  var personid = $(this).data('personid');
  var firstname = $(this).data('firstname');
  var lastname = $(this).data('lastname');
  var ownersexe = $(this).data('ownersexe');
  var ownerbithday = $(this).data('ownerbithday');
  var email = $(this).data('email');
  var phone = $(this).data('phone');
  var address = $(this).data('address');
  var codepostal = $(this).data('codepostal');
  var country = $(this).data('country');
  var countryid = $(this).data('countryid');
  var city = $(this).data('city');
  var cityid = $(this).data('cityid');
  var pp = $(this).data('pp');
  var identification = $(this).data('identification');
  var type_identification = $(this).data('typeidentification');
  var documentrc = $(this).data('documentrc');
  var nametypeNID = '';
  if(type_identification === 1){
      nametypeNID = 'CNI'
  }else{
      nametypeNID = 'PassePort'
  }
  var nidnumber = $(this).data('nidnumber');
  var description = $(this).data('description');
  var storenumberrc = $(this).data('storenumberrc');
  var name = $(this).data('name');
  var googlemap = $(this).data('googlemap');
  var optionsexe = `<option value="`+ownersexe+`" selected>`+ownersexe+`</option>`;
  var optioncountry = `<option value="`+countryid+`" selected>`+country+`</option>`;
  var optioncity = `<option value="`+cityid+`" selected>`+city+`</option>`;
  var optionniddoc = `<option value="`+type_identification+`" selected>`+nametypeNID+`</option>`;

  const delta = quill.clipboard.convert(description)
  quill.setContents(delta, 'silent')
  $('.post-content-update').val(description);

  $('#sellerpersonid').val(personid);
  $('#sellerownerfirstnameid').val(firstname);
  $('#sellerownerlastnameid').val(lastname);
  $('#sellerownersexeid').append(optionsexe);    
  $('.sellercountry').append(optioncountry);
  $('.sellercityidvalue').append(optioncity);
  $('.typenidcart').append(optionniddoc);
  $('#sellerownerbirthdayid').val(ownerbithday);
  $('#selleremailid').val(email);
  $('#sellerphoneid').val(phone);
  $('#selleraddressid').val(address);
  $('#sellercodepostalid').val(codepostal);
  $('#sellernidnumberid').val(nidnumber);
  $('#sellerrcnumberid').val(storenumberrc);
  $('#sellergooglemapid').val(googlemap);
  $('#sellernameid').val(name);
  $('#phototoupdate').attr('src', pp);
  $('#nidtoupdate').attr('value', identification);
  $('#rctoupdate').attr('value', documentrc);
  $('#updateSellerModal').modal("show");
})