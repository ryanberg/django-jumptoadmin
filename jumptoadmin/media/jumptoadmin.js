/* The code for overlaying /admin/ pages over the current page
has been adapted from the Thickbox code
avilable at http://jquery.com/demo/thickbox/thickbox-code/thickbox.js */

var overlay_pathToImage = "{{ MEDIA_URL }}thickbox/loadingAnimation.gif";
var overlay_reloadOnRemove = false;

var flagActionsListOpacity = 0.25;

function overlay(link) {
	var t = link.title || link.name || null;
	var a = link.href || link.alt;
	//console.debug(t, a);
	
	imgLoader = new Image();// preload image
	imgLoader.src = overlay_pathToImage;
	
	overlay_show(t,a);
	this.blur();
	
	
}

function overlay_show(caption, url) {
	try {
		if (typeof document.body.style.maxHeight === "undefined") {
			// if IE6
			$("body","html").css({height: "100%", width: "100%"});
			$("html").css("overflow", "hidden");
			if (document.getElementById("overlay_HideSelect") === null) {
				// iframe to hide select elements in ie6
				$("body").append("<iframe id='overlay_HideSelect'></iframe><div id='overlay_overlay'></div><div id='overlay_window'></div>");
				$("#overlay_overlay").click(overlay_remove);
			}
			
		} else {
			// All other browsers
			if (document.getElementById("overlay_overlay") === null) {
				$("body").append('<div id="overlay_overlay"></div><div id="overlay_window"></div>');
				$("#overlay_overlay").click(overlay_remove);
			}
		}
		
		if (overlay_detectMacXFF()) {
			$("#overlay_overlay").addClass("overlay_overlayMacFFBGHack"); // Use PNG overlay to hide flash
			
		} else {
			$("overlay_overlay").addClass("overlay_overlayBG"); // Use background and opacity
		}
		
		if (caption === null) { caption = ''; }
		
		$("body").append('<div id="overlay_load"><img src="' + imgLoader.src + '" /></div>'); // Add loader
		$("overlay_load").show(); // Show loader
		
		var baseURL;
		if (url.indexOf("?")!==-1) {
			// There is a query string involved
			baseURL = url.substr(0, url.indexOf("?"));
		} else {
			baseURL = url;
		}
		
		var queryString = url.replace(/^[^\?]+\??/, '');
		var params = overlay_parseQuery(queryString);
		
		OVERLAY_WIDTH = (params['width']*1) + 30 || 800; //defaults to 800 if no paramaters were added to URL
		OVERLAY_HEIGHT = (params['height']*1) + 40 || 600; //defaults to 600 if no paramaters were added to URL
		
		urlNoQuery = url.split('OVERLAY_');
		$("#overlay_iframeContent").remove(); // Remove a lingering overlay
		$("#overlay_window").append("<div id='overlay_title'><div id='overlay_ajaxWindowTitle'>"+caption+"</div><div id='overlay_closeAjaxWindow'><a href='#' id='overlay_closeWindowButton' title='Close'>close</a> or Esc Key</div></div><iframe frameborder='0' hspace='0' src='"+urlNoQuery[0]+"' id='overlay_iframeContent' name='overlay_iframeContent"+Math.round(Math.random()*1000)+"' onload='overlay_showIframe()' style='width:"+OVERLAY_WIDTH+"px;height:"+OVERLAY_HEIGHT+"px;' > </iframe>")
		
		$("#overlay_closeWindowButton").click(overlay_remove); // Close when clicking close link
		
		document.onkeydown = function(e){
			// Close on esc key
			if (e == null) { // ie
				keycode = event.keyCode;
			} else { // mozilla
				keycode = e.which;
			}
			
			if(keycode == 27){ // close
				overlay_remove();
			}
		};
		
		overlay_position();
		
		if($.browser.safari){//safari needs help because it will not fire iframe onload
			$("#overlay_load").remove();
			$("#overlay_window").css({display:"block"});
		}
	} catch (e) {
		// Do nothing with the error
		//console.debug("Error: %s", e);
	}
}

// Helper Functions
function overlay_showIframe(){
	$("#overlay_load").remove();
	$("#overlay_window").css({display:"block"});
}

function overlay_remove() {
 	$("#overlay_imageOff").unbind("click");
	$("#overlay_closeWindowButton").unbind("click");
	$("#overlay_window").fadeOut("fast",function(){$('#overlay_window,#overlay_overlay,#overlay_HideSelect').trigger("unload").unbind().remove();});
	$("#overlay_load").remove();
	if (typeof document.body.style.maxHeight == "undefined") {//if IE 6
		$("body","html").css({height: "auto", width: "auto"});
		$("html").css("overflow","");
	}
	document.onkeydown = "";
	document.onkeyup = "";
	
	if (overlay_reloadOnRemove == true) { window.location.reload(true); }
	
	return false;
}

function overlay_position() {
$("#overlay_window").css({marginLeft: '-' + parseInt((OVERLAY_WIDTH / 2),10) + 'px', width: OVERLAY_WIDTH + 'px'});
	if ( !(jQuery.browser.msie && jQuery.browser.version < 7)) { // take away IE6
		$("#overlay_window").css({marginTop: '-' + parseInt((OVERLAY_HEIGHT / 2),10) + 'px'});
	}
}

function overlay_parseQuery ( query ) {
   var Params = {};
   if ( ! query ) {return Params;}// return empty object
   var Pairs = query.split(/[;&]/);
   for ( var i = 0; i < Pairs.length; i++ ) {
      var KeyVal = Pairs[i].split('=');
      if ( ! KeyVal || KeyVal.length != 2 ) {continue;}
      var key = unescape( KeyVal[0] );
      var val = unescape( KeyVal[1] );
      val = val.replace(/\+/g, ' ');
      Params[key] = val;
   }
   return Params;
}

function overlay_getPageSize(){
	var de = document.documentElement;
	var w = window.innerWidth || self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth;
	var h = window.innerHeight || self.innerHeight || (de&&de.clientHeight) || document.body.clientHeight;
	arrayPageSize = [w,h];
	return arrayPageSize;
}

function overlay_detectMacXFF() {
  var userAgent = navigator.userAgent.toLowerCase();
  if (userAgent.indexOf('mac') != -1 && userAgent.indexOf('firefox')!=-1) {
    return true;
  }
}

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
		var flagUL = '<ul class="jumptoadminlinks"><li class="jumptoadminlinks_li_title">' + flaggedObjectDetails['name'] + '<a href="#jumptoadminlinks" class="jumptoadminlinks_li_close">x</a></li>';
		
		// Loop through each action for this flagged object
		
		for (var a = 0; a < flaggedObjectDetails['actions'].length; a++ ) {
			var flagAction = flaggedObjectDetails['actions'][a];
			var flagActionName = flagAction['name'];
			var flagActionURL = flagAction['url'];
			
			var lastClass = '';
			if (a == flaggedObjectDetails['actions'].length - 1) { lastClass = ' class="jumptoadmin_li_last"'}

			flagUL += '<li' + lastClass + '><a href="' + flagActionURL + '?OVERLAY_iframe=true&height=400&width=800' + '" class="jumptoadmin">' + flagActionName.substr(0,1).toUpperCase() + flagActionName.substring(1) + '</a></li>';
		}

		flagUL += '</ul>';

		// Get the actions into a jQuery object
		var flagActionsList = $(flagUL);
		
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
		$('a.jumptoadminlinks_li_close').click(function() {
			// Unbind the hover for this flag and remove the jumptoadminlinks
			$(this).parents('.jumptoadminflag_display').eq(0).unbind('mouseenter mouseleave')
			.removeClass('jumptoadminflag_display').children('ul.jumptoadminlinks').remove();

			return false;
		});

		$(".jumptoadminlinks a.jumptoadmin").click(function(e) {
			//console.debug("Clicked!");
			flagActionsList.remove();
			overlay(this);
			//console.debug("Init!");
			return false;
		});
	}
	
	
}

$(document).ready(function() {
	var flaggedObjects = $('.jumptoadminflag');
	
	flaggedObjects.hover(function() {
		showJumpToAdminLinks($(this));
	}, function() {
		$(this).removeClass('jumptoadminflag_display').children('ul.jumptoadminlinks').animate({'opacity': 0}, 100).remove();
	});
});