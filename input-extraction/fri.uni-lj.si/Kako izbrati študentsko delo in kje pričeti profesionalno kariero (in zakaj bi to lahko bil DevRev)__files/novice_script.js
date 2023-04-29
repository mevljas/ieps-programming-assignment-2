(function($) {
	
/*$(window).bind("pageshow", function(event) {
    if (event.originalEvent.persisted) {window.location.reload();}
});

window.onunload = function(){};*/


$(document).on("change", "#news-taxonomy .term", function(e) {
	var terms = getCheckedTermsNews();
	
	if(terms.length > 0) {
		$("#news-taxonomy .show-all").show();
		$("#news-taxonomy").css("padding-bottom", "40px");
	} else {
		$("#news-taxonomy .show-all").hide();
		$("#news-taxonomy").css("padding-bottom", "15px");
	}

	var lang = $('html').attr('xml:lang');

	$.ajax({
  		type: 'POST',
      	url: "/" + lang + '/test',
      	dataType: 'json', 
		data: {'terms': JSON.stringify(terms)},
      	success: function(data) {
            var h = $(data);
            var i = 0;
            
            h.each(function(){
                if($(this).attr("class") == "news-item"){
                    i++;
                }
            });
            if(i<9)
                $(".news_load_more .text_button").fadeOut(1);
            else
                $(".news_load_more .text_button").fadeIn(1);
      		$("#news-container .news").html(data);
            $(".news_load_more .text_button").attr("val", 1);
     	},
     	error: function(data) {
     		console.log(data);
     	}
	});
});

function getCheckedTermsNews() {
	var terms = [];
	
	$("#news-taxonomy .term").each(function() {
		if($(this).find(".term-check").is(':checked')) {
			var tmp_term = $(this).find(".term-name").attr("data-tid");
			
			if($.inArray(tmp_term, terms) == -1) {
				terms.push(tmp_term);
			}
		}
	});
	
	return terms;
}

$(document).ready(function() {
	if(getCheckedTermsNews().length > 0) {
		$("#news-taxonomy .show-all").show();
		$("#news-taxonomy").css("padding-bottom", "40px");
	} else {
		$("#news-taxonomy .show-all").hide();
		$("#news-taxonomy").css("padding-bottom", "15px");
	}
	
	// ponovno zalaufamo ajax - back button cache
	$("#news-taxonomy .term").eq(0).trigger("change");
});

$(document).on("click", "#news-taxonomy .show-all", function(evt){
	$("#news-taxonomy .term").each(function() {
		$(this).find(".term-check").prop('checked', false);
		
	});
	$("#news-taxonomy .term").eq(0).trigger("change"); 
});

$(document).on("click", ".news_load_more .text_button", function(evt){
    var page2 = $(this).attr("val"); 
    var terms = getCheckedTermsNews();
    var lang = $('html').attr('xml:lang');
    
    $.ajax({
        type: 'POST',
        url: "/" + lang + '/test2/'+page2,
        dataType: 'json', 
		data: {'page': page2, 'terms': JSON.stringify(terms)},
        success: function(data) {
            if(data.hide_button){
                $(".news_load_more .text_button").fadeOut();
            }
            $("#news-container .news").append(data.data);
            $(".news_load_more .text_button").attr("val", parseInt($(".news_load_more .text_button").attr("val" ))+1);
        },
        error: function(data) {
            console.log(data);
        }
    });
});

})(jQuery);
