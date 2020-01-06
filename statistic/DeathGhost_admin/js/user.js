function fill_user_table(form_handle, ajax_response){
	if(ajax_response['code'] == 200){
		form_handle.empty()
		var users = ajax_response['data']['data']
		$.each(users, function(index, user){
			var tr = '<tr class="cen">'+
				'<td><input type="checkbox"/></td>'+
				'<td>'+user['platform_code']+'</td>'+
				'<td>'+user['user_code']+'</td>'+
				'<td>'+user['created_time']+'</td>'+
				'<td>'+
					'<a title="编辑" class="mr-5">编辑</a>'+
					'<a title="删除" class="mr-5">删除</a>'+
				'</td>'+
			'</tr>'
			form_handle.append(tr)
		})
	}	
}


$(function(){
	
	var response = ajax(request_urls['user'], 'get', null)
	fill_user_table($("#user tbody"), response)
	
})