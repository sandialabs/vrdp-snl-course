/* This creates the ability to make a container in Sphinx toggleable
   just create a structure like:

   .. container:: toggle

     .. container:: toggle-header

        Show/Hide

     .. container:: toggle-body

        My hiddent content

   The container after the header can be a code-block or equivalent
   but won't be styled unless it has the toggle-body class.
*/

$(document).ready(function() {
	$(".toggle > *").hide();
	$(".toggle .toggle-header").show();
	$(".toggle .toggle-header").click(function() {
		$(this).parent().children().not(".toggle-header").toggle(400);
		$(this).parent().children(".toggle-header").toggleClass("open");
	})
});
