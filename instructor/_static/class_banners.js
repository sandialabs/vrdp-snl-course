/* Adds elemeents to the default RTD theme to allow for classification banners. */

$(document).ready(function() {
	$("body").prepend('<div class="class-banner class-banner-top"> UNCLASSIFIED </div>');
	$("body").append('<div class="class-banner class-banner-bottom"> UNCLASSIFIED </div>');
});
