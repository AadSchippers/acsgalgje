$(function(){
	var $write = $('#write'),
		shift = false,
		capslock = false;
	
	$('#keyboard li').click(function(){
		var $this = $(this),
			$form = $(this).closest("form"),
			character = $this.html(); 
			$form.append("<input type='hidden' name='letter' value='"+character+"'/>")
			if ($(this).hasClass("enabled")) {  	
				$form.submit();
			} 
	});
});