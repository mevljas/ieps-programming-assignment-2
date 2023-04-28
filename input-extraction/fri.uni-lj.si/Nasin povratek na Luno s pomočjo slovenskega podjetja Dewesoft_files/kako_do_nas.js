(function($, Drupal) {
	$(document).on("mouseenter click", "#kako-do-nas .menu .item-cell", function(e) {
		$(this).addClass("hovered");
		$(this).siblings().removeClass("hovered");
		
		// skrij/pokazi content glede na index taba
		var index = $(this).index() + 1;
		
		if (window.matchMedia('(max-width: 620px)').matches) {
	    	$(this).find(".responsive-small-content").html($("#kako-do-nas .content .content-single:nth-of-type(" + index + ")").html());
	    	
	    	$(this).find(".responsive-small-content").show();
	    	$(this).siblings().find(".responsive-small-content").hide();
	   	} else {
	   		$("#kako-do-nas .content .content-single:nth-of-type(" + index + ")").removeClass("hidden");
			$("#kako-do-nas .content .content-single:not(:nth-of-type(" + index + "))").addClass("hidden");
	   	}
		
	});

	
	$(window).resize(function(){
		if (window.matchMedia('(min-width: 620px)').matches) {
			$("#kako-do-nas .menu .item-cell").find(".responsive-small-content").hide();
		}
        
	});
	
})(jQuery, Drupal);