function doubleClickUpadte(element, url,chang_field , params){
	if(element.children("input").length>0){ 
		return false; 
	} 
	var tdDom = element; 
	// tdDom.focus()
	//保存初始值 
	var tdPreText = element.text(); 
	//给td设置宽度和给input设置宽度并赋值 
	element.width(100).html("<input type='text' style='border:none'>").find("input").width(100).val(tdPreText); 
	//失去焦点的时候重新赋值 
	var inputDom = element.find("input"); 
	inputDom.blur(function(){ 
		var newText = $(this).val(); 
		$(this).remove(); 
		tdDom.text(newText); 
		params[chang_field] = newText
		if(tdPreText != newText){
			ajax(url, 'put', params)
		}
	})
}
function getRequest() {
	var url = decodeURI(location.search); //获取url中"?"符后的字串
	var theRequest = new Object();
	if (url.indexOf("?") != -1) {
			var str = url.substr(1);
			strs = str.split("&");
			for(var i = 0; i < strs.length; i ++) {
					theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
			}
	}
	return theRequest;
}
				
function ajax(url, method, params){
	var response = null
	$.ajax({
	   type: method,
	   url: url,
	   data: params,
	   async: false,
	   success: function(msg, status, xhr){
		   if(xhr.status == 200){
			   response = msg
		   }else{
			   alert(msg)
		   }
	   },
	   error: function(msg){
		   alert(msg)
	   }
	});
	return response
}

function refreshPage(){
	window.history.go(0)
}


function layerPopup(message){
	layer.alert(''+message+'', {
		skin: 'layui-layer-lan'
		,closeBtn: 0
	});
}