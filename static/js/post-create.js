var PostModal = {
	init: function (modal, button) {
		this.modal_id = modal;
		this.button = button;
		this.bind();
	},
	bind: function () {
		$('.unpublished').hide();
		$('#canload').hide();
		$(this.button).click(this.modal.open);
		event = debounce(this.typing, 350)
		$("#post-live-input").keypress(event);
		$("#post-button").click(this.ajax.send);
	},
	typing: function (e) {
		PostModal.artwork.search({
			query: this.value,
			beforeSend: function (event) {
				$('#canload').show();
			},
			success: function (data) {
				$('.unpublished').show();
				$('#canload').hide();
				$('#post-button').removeAttr('disabled');
				$('#post-live-image').attr('src', data.artwork);
				$('#post-live-title').text(data.name);
				$(".wrap-title").tooltip('show');
				this.api_name = data.full_name;
			}
		})
	},
	modal: {
		open: function (e) {
			console.log("Open method triggered.")
			$(PostModal.modal_id).modal('show');
		},
		close: function (e) {
			console.log("Closing modal.")
			$(PostModal.modal_id).modal('hide');
		}
	},

	artwork: {
		search: function (params) {
			var url = Mxious.url('covers/search');
			var artwork = $.get({
				url: url,
				data: {query: params.query},
				success: params.success,
				beforeSend: params.beforeSend
			});
		}
	},

	ajax: {
		send: function () {
			form = {
				'title': $('#post-live-title').text(),
				'content': $('#post-text').val(),
				'image': $('#post-live-image').attr('src'),
				'api_name': PostModal.api_name
			}

			if (form.content == '') {
				$('#post-text').addClass('danger');
				return false;
			}

			$.post({
				url: Mxious.url('posts/create'),
				data: form,
				success: PostModal.ajax.success
			})
		},

		success: function (e) {
			$("#post-live-input").val('');
			$("#post-text").val('');
			$('.unpublished').hide();
			PostModal.modal.close();
		}
	}
}

PostModal.init('#post-modal', '#open-modal');

// cody is epic
canLoad('chrome', {
	id:'canload',
	speed:'Medium',
	color:'rgb(230, 151, 35)',
	size:'20',
	line:'3',
	length:'31'
});