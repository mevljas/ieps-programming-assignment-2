var veryfiyMe=function(){
	grecaptcha.render('veryfier', {'sitekey':'6Lc0UAEVAAAAAN7TRsGyuC1UgGSHOmzRi2vNAmqG'});
	//console.log('Test');
}
jQuery(document).ready(function() {
	//Vue and vee validate
	Vue.component('validation-provider', VeeValidate.ValidationProvider);
	new Vue({
		el: '#read',
		data: {
			showform: false,
			value: "",
		}
	});

	//Code
	var url=window.location.pathname.substr(0,3)+'/email2form';


	if (url.substr(1,2)=='sl'){
		jQuery('#sendid').on('change invalid mouseover', function() {
 		   	var textfield = jQuery(this).get(0);

 		   	textfield.setCustomValidity('');

 		   	if (!textfield.validity.valid) {
 	     		textfield.setCustomValidity('Vnesite veljavni email naslov. To polje je obvezno!');  
 		   	}
		});
		jQuery('#sendcore').on('change invalid mouseover', function() {
 		   	var textfield = jQuery(this).get(0);

 		   	textfield.setCustomValidity('');

 		   	if (!textfield.validity.valid) {
 	     		textfield.setCustomValidity('To polje je obvezno!');  
 		   	}
		});
	}
	else{
		jQuery('#sendid').on('change invalid mouseover', function() {
 		   	var textfield = jQuery(this).get(0);

 		   	textfield.setCustomValidity('');

 		   	if (!textfield.validity.valid) {
 	     		textfield.setCustomValidity('Please provide a valid email address. This field is required!');  
 		   	}
		});
		jQuery('#sendcore').on('change invalid mouseover', function() {
 		   	var textfield = jQuery(this).get(0);

 		   	textfield.setCustomValidity('');

 		   	if (!textfield.validity.valid) {
 	     		textfield.setCustomValidity('This field is required!');  
 		   	}
		});
	}
	jQuery('#mail').click(function(p) {
		p.preventDefault();
		if (jQuery('#veryfier').is(':empty')){
			grecaptcha.render('veryfier', {'sitekey':'6Lc0UAEVAAAAAN7TRsGyuC1UgGSHOmzRi2vNAmqG'});
		}
		jQuery('#write').html('');

	});
	jQuery('#sendb').click(function(p) {
		var validEmail=jQuery('#sendid:invalid');
		var fdata=jQuery('form#send').serialize();
		var fval=['sender=','core='];
		var fsplit=fdata.split('&');
		var ftick=0;
		for (var i=0; i<fsplit.length-1; i++){
			var fremove=fsplit[i].replace(fval[i],'');
			if (fremove==''){
				ftick++;
			}
		}
		if(ftick==0 && validEmail.length==0){
			if (fsplit[fsplit.length-1].replace('g-recaptcha-response=','')==''){
				p.preventDefault();
			}
			else{
				p.preventDefault();
				jQuery.ajax({
					type: 'POST',
					url: url,
					data: fdata,
					success: function (result){
						grecaptcha.reset();
						document.getElementById('mail').click();
						jQuery('#sendid').val('');
						jQuery('#sendcore').val('');
						jQuery('#write').html(result);
					},
					error: function (error){
						if (url.substr(1,2)=='sl'){
							jQuery('#write').html('<p style="border: 2px solid #999999;border-radius: 10px;padding: 10px;margin: 10px;">Prišlo je do napake.</p>');
						}
						else{
							jQuery('#write').html('<p style="border: 2px solid #999999;border-radius: 10px;padding: 10px;margin: 10px;">An error has occurred.</p>');
						}
					}
				});
			}
		}
	});
});
;
