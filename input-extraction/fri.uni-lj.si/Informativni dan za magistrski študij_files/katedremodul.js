(function($) {

/*window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload() 
    }
};*/
$(window).bind("pageshow", function(event) {
    if (event.originalEvent.persisted) {window.location.reload();}
});

window.onunload = function(){};

var terms = [];

$(document).on("change", "#katedre-taxonomy .term", function(e) {
	terms = getCheckedTermsKatedre();
	
	if(terms.length > 0) {
		$("#katedre-taxonomy .show-all").show();
		$("#katedre-taxonomy").css("padding-bottom", "40px");
	} else {
		$("#katedre-taxonomy .show-all").hide();
		$("#katedre-taxonomy").css("padding-bottom", "15px");
	}
	
	ajaxKatedre();
});

$(document).on("click", "#katedre-taxonomy .show-all", function(evt){
	$("#katedre-taxonomy .term").each(function() {
		$(this).find(".term-check").prop('checked', false);
		
	});
	$("#katedre-taxonomy .term").eq(0).trigger("change"); 
});
	
$(document).ready(function() {
	
	terms = getCheckedTermsKatedre();
	
	if(terms.length > 0) {
		$("#katedre-taxonomy .show-all").show();
		$("#katedre-taxonomy").css("padding-bottom", "40px");
	} else {
		$("#katedre-taxonomy .show-all").hide();
		$("#katedre-taxonomy").css("padding-bottom", "15px");
	}
	
	ajaxKatedre();
	
	
});
	
function getCheckedTermsKatedre() {
	var terms = [];
	
	$("#katedre-taxonomy .term").each(function() {
		if($(this).find(".term-check").is(':checked')) {
			var tmp_term = $(this).find(".term-name").attr("data-tid");
			
			if($.inArray(tmp_term, terms) == -1) {
				terms.push(tmp_term);
			}
		}
	});
	
	return terms;
}

function ajaxKatedre() {
	
	var lang = $('html').attr('xml:lang');
	
	$.ajax({
  		type: 'GET',
      	url: "/" + lang + '/ajax/katedre',
      	dataType: 'json', 
		data: {
			'terms': terms
		},
      	success: function(data) {
       		$("#katedra-items.laboratoriji-page").html($(data).find(".katedra-item"));
     	},
     	error: function(data) {
     		console.log(data);
     	}
	});
}

	
})(jQuery);