$( document ).ready(function(){

var team = "Giants";

var value = "32";

var pattern = new RegExp(" " + 
              team, "g");
$("body").html($("body").html().replace(pattern,' '+team+' ('+value + '%) '));

});

/*$(function(){
 
	$( "html" ).each(
		function(){
			var clonedTree = $( this )
			.clone()
			.find( "script" )
			.remove()
			.end()
			;
			alert(clonedTree.text())
		}
	)
});*/


