$(function () {
    $("#menu").tooltip('show');
});

var Mxious = {
	init: function (config) {
		this.parameters = config;
		this.csrf_config();
	},
	config: function (param) {
		if (this.parameters[param] != undefined) {
			// The fact that I have to do this, is testament  to how much JS sucks as a language
			return this.parameters[param];
		} else {
			throw new Error("Couldn't find configuration value that was called.")
		}
	},

	bind: function () {
	},

	url: function (str) {
		// Because concatenation hurts
		return Mxious.config('BASE_URL') + str;
	},

	csrf_config: function () {
		function csrfSafeMethod(method) {
		    // these HTTP methods do not require CSRF protection
		    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", Mxious.config('CSRF_TOKEN'));
		        }
		    }
		});
	}
}