jQuery(document).ready(function() {

	jQuery('.timepicker').datepicker();
	
		//Validation for Event form
	jQuery( "#id_username" ).addClass('required');
	jQuery( "#id_password" ).addClass('required');
	jQuery( "#id_email " ).addClass('required');
	requestor_validator=jQuery( "#user_form" ).validate({
		errorLabelContainer: "#user-form-errors",
		wrapper: "li",
		highlight: function(element, errorClass, validClass) {
			if(jQuery(element).is("input"))
				jQuery(element).addClass("form-input-error").removeClass("form-input");
			else if(jQuery(element).is("textarea"))
				jQuery(element).addClass("error").removeClass("default");
		},
		unhighlight: function(element, errorClass, validClass) {
			if(jQuery(element).is("input"))
				jQuery(element).addClass("form-input").removeClass("form-input-error");
			else if(jQuery(element).is("textarea"))
				jQuery(element).addClass("default").removeClass("error");
		},
		messages: {
			//ATTENTION: we are not using most of this logic/messages because fields are not required
			//But the implementation is here for future reference
			username: "Please specify the username",
			password: "Please specify the password",
			email: "Please specify the email",
		},
		submitHandler: function(form) {
			   form.submit();
		}
	});

})