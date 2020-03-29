$(document).ready(function(){
	'use strict';
	//Login Register Validation
	if($("form.form-horizontal").attr("novalidate")!==undefined){
		$("input,select,textarea").not("[type=submit]").jqBootstrapValidation();
	}

	// Remember checkbox
	let $check_remember = $('.chk-remember');
	if($check_remember.length){
		$check_remember.iCheck({
			checkboxClass: 'icheckbox_square-blue',
			radioClass: 'iradio_square-blue',
		});
	}
});
