var Feed = {
	init: function (container, type, offset, selector) {
		this.feed_type = type;
		this.container_string = container;
		this.container = $(container);
		this.offset = offset;
		this.item_selector = selector;
		this.bind();
	},

	bind: function () {
		console.log("Binding everything.")
		var grid = this.masonry(this.container, '.grid-item');

		// do imagesloaded things
		grid.imagesLoaded().progress( function() {
		  grid.masonry('layout');
		});

		this.grid = grid;

		$(window).scroll(function(){
			if ($(window).scrollTop() == $(document).height() - $(window).height()){
				Feed.ajax.load_more(Feed.offset, Feed.feed_type);
			}
		});

		this.ajax.poll.begin();
	},

	masonry: function (container, selector) {
		var grid = container.masonry({
		    itemSelector: selector,
		    isFitWidth: true,
		});

		return grid;
	},

	ajax: {
		load_more: function () {
			$.post('posts/load_more', {offset: Feed.offset, type: Feed.feed_type}).done(this.load_more_callback)
		},

		load_more_callback: function (data) {
			Feed.offset = Feed.offset + data.count;
			var debug = {
				offset: Feed.offset,
				count: data.count,
				success: data.success
			};
			console.log("Loading more: " + debug)
			var elem = jQuery(data.html);
			Feed.container.append(elem).imagesLoaded(function () {
				Feed.container.masonry('appended', elem);
			});
		},

		poll: {
			interval: 1000,
			begin: function () {
				this.setIntervalObject = setTimeout(this.fetch, this.interval);
			},
			fetch: function () {
				console.log("Ran a fetch cycle.")
				// I HATE JS, WHY DOES IT NOT HAVE A FORMAL CONCATENATION FUNCTION?!?
				// THE F^%# IS THIS?
				var latest_id = $("" + Feed.container_string + " " + Feed.item_selector).first().data('id');
				var type = Feed.feed_type;
				var data = {
					last_id: latest_id,
					feed_type: type
				}
				$.ajax({
					url: 'posts/poll',
					type: 'POST',
					data: data,
					success: Feed.ajax.poll.callback,
					error: Feed.ajax.poll.error_callback
				}).done(function () {
					setTimeout(Feed.ajax.poll.fetch, Feed.ajax.poll.interval)
				})
			},
			callback: function (data) {
				if (data.count != 0) {
					console.log("Ayy lmao, there's new data on the server! Adding it to your feed.")
					elem = jQuery(data.html)
					Feed.container.prepend(elem).imagesLoaded(function () {
						Feed.container.masonry('prepended', elem);
					})
					Feed.offset = Feed.offset + data.count;
					// force redraw to fix overlaps TODO @critical
				}	
			}
		}
	}
}