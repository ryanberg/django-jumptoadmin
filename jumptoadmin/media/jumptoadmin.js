var overlay_reloadOnRemove = false;

var flagActionsListOpacity = 0.25;

function showJumpToAdminLinks(flaggedObject) {
	/*
	flaggedObject should be a jQuery object
	*/
	
	var re = /jumptoadminflag_[\w\d-]+/;
	var classString = flaggedObject.attr('class').match(re)[0]; // Will look like jumptoadminflag_app-model-id
	
	function getFlaggedObjectDetails(classString) {
		/*
		Loop through each of the flags from the global jumpFlagList variable
		Until we find one with a 'class' attribute equal to the above classString
		*/
		for (var i = 0; i < jumpFlagList.length; i++) {
			var flaggedObjectDetails = jumpFlagList[i];
			if (flaggedObjectDetails['class'] == classString) {
				return flaggedObjectDetails;
			}
		}
		return null;
	}
	
	flaggedObjectDetails = getFlaggedObjectDetails(classString);
	
	if (flaggedObjectDetails && flaggedObjectDetails['actions'].length) {
		/*
		Create the unordered list of actions
		flaggedObjectDetails should have 'name', 'class', and 'actions'
		*/
		var flagActionsList = $('<ul class="jumptoadminlinks"></ul>');
		flagActionsList.append($('<li class="jumptoadminlinks_li_title">' + flaggedObjectDetails['name'] + '<a href="#jumptoadminlinks" class="jumptoadminlinks_li_close">x</a></li>'));
		
		// Loop through each action for this flagged object
		
		for (var a = 0; a < flaggedObjectDetails['actions'].length; a++ ) {
			var flagAction = flaggedObjectDetails['actions'][a];
			var flagActionName = flagAction['name'];
			var flagActionURL = flagAction['url'];
			var flagActionAction = flagAction['action'];
			
			// This is only used for styling purposes
			var lastClass = '';
			if (a == flaggedObjectDetails['actions'].length - 1) { lastClass = ' class="jumptoadmin_li_last"'}
			
			// Create the string thickbox will use to properly display the admin page
			var flagActionURLParameters = '?';
			if (flagActionAction == '') {
				// Since there's no post data, an iframe can be used 
				flagActionURLParameters += 'TB_iframe=true';
				var flagActionPostParameters = null;
			} else {
				// Admin will be retrieved via AJAX instead of an iframe so we can send POST data
				var flagActionPostParameters = {
					'action': flagActionAction, // Name of the registered action
					'_selected_action': flaggedObjectDetails['pk'], // PK of the object on which to perform the action
				}
			}
			flagActionURLParameters += 'height=400&width=800';
			
			// Create the list item
			var flagActionLI = $('<li' + lastClass + '><a href="' + flagActionURL + flagActionURLParameters + '' + '" class="jumptoadmin">' + flagActionName.substr(0,1).toUpperCase() + flagActionName.substring(1) + '</a></li>');
			
			// Handle clicks on the action's link
			flagActionLI.children('a:first').click(function() {
				var clickedLink = $(this);
				clickedLink.parents('.jumptoadminlinks').animate({'opacity': 0}, 100).remove(); // Remove the list
				tb_show(null, clickedLink.attr("href"), flagActionPostParameters, false); // Show the thickbox
				return false;
			});
			
			// Append the list item to the list
			flagActionsList.append(flagActionLI);
		}
		
		// Handle opacity of the jumptoadminlinks
		flagActionsList.css("opacity", 0).hover(function() {
			// On hover, set opacity to 1
			$(this).animate({'opacity': 1}, 100);
		}, function() {
			// On hover-off set opacity back to default
			$(this).animate({'opacity': flagActionsListOpacity}, 100);
		});
		
		// Show the jumptoadminlinks
		flaggedObject.addClass('jumptoadminflag_display');
		flagActionsList.prependTo(flaggedObject).animate({"opacity": flagActionsListOpacity}, 100);

		// Handle the close button
		$('a.jumptoadminlinks_li_close').click(function(e) {
			// Set up the poof
			var poof = $('<div class="poof"></div>');
			var xOffset = 24;
			var yOffset = 24;
			
			// Unbind the hover for this flag and remove the jumptoadminlinks
			$(this).parents('.jumptoadminflag_display').eq(0).unbind('mouseenter mouseleave')
			.removeClass('jumptoadminflag_display').children('ul.jumptoadminlinks').remove();
			
			poof.css({ 
				left: e.pageX - xOffset + 'px', 
				top: e.pageY - yOffset + 'px' 
			}).appendTo($('body')).show();
			
			animatePoof(poof);

			return false;
		});
		
	}
	
}

$(document).ready(function() {
	var flaggedObjects = $('.jumptoadminflag');
	
	if (flaggedObjects.length) {
		flaggedObjects.hover(function() {
			showJumpToAdminLinks($(this));
		}, function() {
			$(this).removeClass('jumptoadminflag_display').children('ul.jumptoadminlinks').animate({'opacity': 0}, 100).remove();
		});
	}
});

/* Poof effect from http://www.kombine.net/jquery/jquery-poof-effect */
function animatePoof(poof) {
    var bgTop = 0; 
    var frames = 5; 
    var frameSize = 32; 
    var frameRate = 60; 
  
    for(i = 1; i < frames; i ++) { 
        poof.animate({ 
            backgroundPosition: '0 ' + (bgTop - frameSize) + 'px' 
        }, frameRate); 
  
        bgTop -= frameSize; 
    } 
  
    setTimeout('removePoof()', frames * frameRate); 
}
function removePoof(poof) {
	$('.poof').remove();
}