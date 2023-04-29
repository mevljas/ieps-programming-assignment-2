 //ob spremembi v selectu

var timeout = false;
//ob tipkanju imena
jQuery('#osebjeSearchInput').keyup(function () { 
	
	var besedilo = jQuery('#osebjeSearchInput').val(); 
	
	var indexSelected = jQuery('#osebjeSelectFilter').prop("selectedIndex");
    console.log(indexSelected);
	var lang = jQuery('html').attr('xml:lang');

	jQuery.ajax({
  		type: 'POST',
      	url: '/' + lang + '/ajax/search',
      	dataType: 'json', 
		data: {"text":besedilo,"selected":indexSelected},
      	success: function(dataa) {
          	console.log(dataa)
          	jQuery('#staffListContainer').html(dataa);
          	jQuery("#activity-indicator-container").html('');
          	jQuery("#activity-indicator-container").css('height', '0px');
          	
          	if(!timeout) {
				timeout = true;

				window.setTimeout(function() {
					timeout = false;
					
					$OsebjeListMasonry.masonry('reloadItems');   
	           		$OsebjeListMasonry.masonry('layout');
				}, 300);
			}

          	
     	}
	});
	
});
jQuery(document).ready(function () {

	jQuery('#osebjeSelectFilter').on('change', function (e) {

		var indexSelected = jQuery('#osebjeSelectFilter').prop("selectedIndex");

		jQuery("#activity-indicator-container").html('<div class="loader"><div class="loader-inner ball-spin-fade-loader"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>');
		jQuery("#activity-indicator-container").css('height', '60px');
		console.log(indexSelected);
		var lang = jQuery('html').attr('xml:lang');
		window.location.hash = indexSelected;
		jQuery.ajax({
			type: 'POST',
			url: '/' + lang + '/ajax/selected',
			dataType: 'json',
			data: {"selected":indexSelected},
			success: function(dataa) {
				console.log(dataa);

				jQuery('#staffListContainer').html(dataa);

				jQuery("#activity-indicator-container").html('');
				jQuery("#activity-indicator-container").css('height', '0px');

				jQuery('#osebjeSearchInput').val('');

				$OsebjeListMasonry.masonry('reloadItems');
				$OsebjeListMasonry.masonry('layout');

			}
		});
	});



    if(window.location.href.indexOf("#1") > -1) // This doesn't work, any suggestions?
    {
            jQuery("#activity-indicator-container").html('<div class="loader"><div class="loader-inner ball-spin-fade-loader"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>');
        jQuery("#activity-indicator-container").css('height', '60px');
		var lang = jQuery('html').attr('xml:lang');

        jQuery.ajax({
            type: 'POST',
            url: '/' + lang + '/ajax/selected',
            dataType: 'json', 
            data: {"selected":1},
            success: function(dataa) {


                jQuery('#staffListContainer').html(dataa);

                jQuery("#activity-indicator-container").html('');
                jQuery("#activity-indicator-container").css('height', '0px');

                jQuery('#osebjeSearchInput').val('');

                $OsebjeListMasonry.masonry('reloadItems');   
                $OsebjeListMasonry.masonry('layout');

            }
        });
    } if(window.location.href.indexOf("#2") > -1)  // This doesn't work, any suggestions?
    {
            jQuery("#activity-indicator-container").html('<div class="loader"><div class="loader-inner ball-spin-fade-loader"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>');
        jQuery("#activity-indicator-container").css('height', '60px');
		var lang = jQuery('html').attr('xml:lang');

        jQuery.ajax({
            type: 'POST',
            url: '/' + lang + '/ajax/selected',
            dataType: 'json', 
            data: {"selected":2},
            success: function(dataa) {


                jQuery('#staffListContainer').html(dataa);

                jQuery("#activity-indicator-container").html('');
                jQuery("#activity-indicator-container").css('height', '0px');

                jQuery('#osebjeSearchInput').val('');
                $OsebjeListMasonry.masonry('reloadItems');   
                $OsebjeListMasonry.masonry('layout');

            }
        });
    }
});