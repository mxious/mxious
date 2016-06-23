$(function () {
    $("#menu").tooltip('show');
});

var Mxious = {
	init: function (config) {
		this.parameters = config;
		this.csrf_config();
	},
	config: function (param) {
		return this.parameters[param]
	},

	bind: function () {
	},

	csrf_config: function () {
		function csrfSafeMethod(method) {
		    // these HTTP methods do not require CSRF protection
		    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", Mxious.config('csrf_token'));
		        }
		    }
		});
	}
}