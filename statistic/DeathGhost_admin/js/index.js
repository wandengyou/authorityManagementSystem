function fill_paltform_table(form_handle, ajax_response){
	if(ajax_response['code'] == 200){
		form_handle.empty()
		var platforms = ajax_response['data']['data']
		$.each(platforms, function(index, platform){
			var tr = '<tr class="cen">'+
				'<td class="current_platform_code" name="'+platform['platform_code']+'"><input type="checkbox"/></td>'+
				'<td class="platform_update" name="platform_name">'+platform['platform_name']+'</td>'+
				'<td>'+platform['platform_code']+'</td>'+
				'<td class="platform_update" name="description">'+platform['description']+'</td>'+
				'<td><a class="platform_user" name="'+platform['platform_code']+'">'+platform['user_total']+'</a></td>'+
				'<td><a class="platform_role" name="'+platform['platform_code']+'">'+platform['role_total']+'</a></td>'+
				'<td><a class="platform_permission" name="'+platform['platform_code']+'" >'+platform['permission_total']+'</a></td>'+
				'<td>'+
					'<a title="禁用" class="mr-5 platform_forbidden" name="'+platform['platform_code']+'">禁用</a>'+
				'</td>'+
			'</tr>'
			form_handle.append(tr)
		})
	}
}

function fill_role_table(form_handle, ajax_response){
	if(ajax_response['code'] == 200){
		form_handle.empty()
		var roles = ajax_response['data']['data']
		$.each(roles, function(index, role){
			var tr = '<tr class="cen">'+
				'<td class="current_role_code" name="'+role['role_code']+'"><input type="checkbox"/></td>'+
				'<td class="role_update" name="role_name">'+role['role_name']+'</td>'+
				'<td>'+role['role_code']+'</td>'+
				'<td><a class="role_permission" name="'+role['role_code']+'" >'+role['permission_total']+'</a></td>'+
				'<td>'+
					'<a title="权限分配" class="mr-5 assign_permission" name="'+role['role_code']+'">分配权限</a>'+
					'<a title="删除" class="mr-5">删除</a>'+
				'</td>'+
			'</tr>'
			form_handle.append(tr)
		})
	}
}

function fill_permission_table(form_handle, ajax_response){
	if(ajax_response['code'] == 200){
		form_handle.empty()
		var permissions = ajax_response['data']['data']
		$.each(permissions, function(index, permission){
			var tr = '<tr class="cen">'+
				'<td class="current_permission_code" name="'+permission['permission_code']+'"><input type="checkbox"/></td>'+
				'<td class="permission_update" name="permission_name">'+permission['permission_name']+'</td>'+
				'<td>'+permission['permission_code']+'</td>'+
				'<td class="permission_update" name="permission_type">'+permission['permission_type']+'</td>'+
				'<td  class="permission_update" name="identifier">'+permission['identifier']+'</td>'+
				'<td>'+
					'<a title="删除" class="mr-5">删除</a>'+
				'</td>'+
			'</tr>'
			form_handle.append(tr)
		})
	}
}

function fill_user_table(form_handle, ajax_response){
	if(ajax_response['code'] == 200){
		form_handle.empty()
		var users = ajax_response['data']['data']
		$.each(users, function(index, user){
			var tr = '<tr class="cen">'+
				'<td class="current_user_code" name="'+user['user_code']+'"><input type="checkbox"/></td>'+
				'<td class="user_update" name="role_name">'+user['user_code']+'</td>'+
				'<td>'+user['created_time']+'</td>'+
				'<td><a class="user_role" name="'+user['user_code']+'" >'+user['role_total']+'</a></td>'+
				'<td>'+
					'<a title="角色分配" class="mr-5 assign_role" name="'+user['user_code']+'">分配角色</a>'+
					'<a title="编辑" class="mr-5 audit_user" name="'+user['user_code']+'" >编辑</a>'+
					'<a title="删除" class="mr-5">删除</a>'+
				'</td>'+
			'</tr>'
			form_handle.append(tr)
		})
	}	
}



$(function(){
	fill_paltform_table($('#platform tbody'), ajax(request_urls['platform'], 'get', {'status': 1}))
	
	/**获取在线平台数据*/
	$('#online').click(function(){
		var response = ajax(request_urls['platform'], 'get', {'status': 1})
		fill_paltform_table($('#platform tbody'), response)
		$("#platform").css({'display': 'block'})
		$("#user").css({'display': 'none'})
		$("#role").css({'display': 'none'})
		$("#permission").css({'display': 'none'})
	})
	/**获取离线平台数据*/
	$('#offline').click(function(){
		var response = ajax(request_urls['platform'], 'get', {'status': 0})
		fill_paltform_table($('#platform tbody'), response)
		$("#platform").css({'display': 'block'})
		$("#user").css({'display': 'none'})
		$("#role").css({'display': 'none'})
		$("#permission").css({'display': 'none'})
	})
	/**获取平台用户*/
	$('#platform').on('click', '.platform_user', function(){
		$("#platform").css({'display': 'none'})
		var user = $('#user')
		user.css({'display': 'block'})
		user.find('.current_platform').val($(this).attr('name'))
		var response = ajax(request_urls['user'], 'get', {'platform_code': $(this).attr('name')})
		fill_user_table($('#user tbody'), response)
	})
	/**获取平台角色*/
	$("#platform").on('click', '.platform_role', function(){
		$("#platform").css({'display': 'none'})
		var role = $("#role")
		role.css({'display': 'block'})
		role.find('.current_platform').val($(this).attr('name'))
		$('#btn_role').css({'display': 'block'})
		var response = ajax(request_urls['role'], 'get', {'platform_code': $(this).attr('name')})
		fill_role_table($('#role tbody'), response)
		
	})
	/**获取平台权限*/
	$("#platform").on('click', '.platform_permission', function(){
		$("#platform").css({'display': 'none'})
		var permission = $("#permission")
		permission.css({'display': 'block'})
		permission.find('.current_platform').val($(this).attr('name'))
		$('#btn_permission').css({'display': 'block'})
		$('#import_permission').css({'display': 'block'})
		var response = ajax(request_urls['permission'], 'get', {'platform_code': $(this).attr('name')})
		fill_permission_table($('#permission tbody'), response)
	})
	/**获取角色下的权限*/
	$("#role").on('click', '.role_permission', function(){
		$("#role").css({'display': 'none'})
		var platform_code = $("#role").find('.current_platform').val()
		var permission = $("#permission")
		permission.find('.current_platform').val(platform_code)
		var response = ajax(request_urls['assign'], 'get', {'role_code': $(this).attr('name')})
		$('#btn_permission').css({'display': 'none'})
		$('#import_permission').css({'display': 'none'})
		fill_permission_table($('#permission tbody'), response)
		permission.css({'display': 'block'})
	})
	/**获取用户下的角色*/
	$("#user").on('click', '.user_role', function(){
		$("#user").css({'display': 'none'})
		var role = $("#role")
		role.css({'display': 'block'})
		role.find('.current_user').val($(this).attr('name'))
		var platform = $("#user").find('.current_platform').val()
		role.find('.current_platform').val(platform)
		$('#btn_role').css({'display': 'none'})
		var response = ajax(request_urls['role']+$(this).attr('name'), 'get', null)
		fill_role_table($('#role tbody'), response)
		
	})
	
	/**分配角色*/
	$("#user").on('click', '.assign_role', function(){
		var user_url = request_urls['user']
		var assign_role_url = request_urls['assign_role']
		var user_code = $(this).attr('name')
		var platform_code = $("#user").find('.current_platform').val()
		var tbody = $('#user tbody')
		layer.open({
		  type: 2,
		  title: "角色分配",
		  area: ['700px', '450px'],
		  fixed: false, //不固定
		  maxmin: true,
		  content: 'role.html?platform_code='+ platform_code +"&user_code=" + user_code,
		  btn: ['确定', '取消'],
		  yes: function(index, layero){
			  var body = layer.getChildFrame('body', index);  //此处加载目标页面(ifreme)的内容
			  $.each(body.find('input:checkbox:checked'),function(){
				  ajax(assign_role_url + user_code+"/"+$(this).attr('name')+"/", 'post')
			  });
			  layer.close(index)
			  layerPopup("角色分配成功")
			  //刷新当前模块
			  var response = ajax(user_url, 'get', {'platform_code': platform_code})
			  fill_user_table(tbody, response)
		  }
		});
	})

	/**分配权限*/
	$("#role").on('click', '.assign_permission', function(){
		var url = request_urls['assign']
		var role_code = $(this).attr('name')
		var role_url = request_urls['role']
		var platform_code = $("#role").find('.current_platform').val()
		var tbody = $('#role tbody')
		layer.open({
		  type: 2,
		  title: "权限分配",
		  area: ['700px', '450px'],
		  fixed: false, //不固定
		  maxmin: true,
		  content: 'permission.html?platform_code='+$("#role").find('.current_platform').val()+"&role_code="+$(this).attr('name'),
		  btn: ['确定', '取消'],
		  yes: function(index, layero){
			  var permission_code_list = []
			  var body = layer.getChildFrame('body', index);  //此处加载目标页面(ifreme)的内容
			  $.each(body.find('input:checkbox:checked'),function(){
				  permission_code_list.push($(this).attr('name'))
			  });
			  var permissions = ""
			  for(var i=0; i<permission_code_list.length; i++){
				  permissions+=permission_code_list[i]+','
			  }
			  var response = ajax(url, 'post', {'role_code': role_code, 'permission_code': permissions.substr(0, permissions.length-1)})
			  if(response['code'] == 200){
				  layer.close(index)
				  layerPopup("权限分配成功")
				  //刷新当前模块
				  var response = ajax(role_url, 'get', {'platform_code': platform_code})
				  fill_role_table(tbody, response)
			  }else{
				  alert(JSON.stringify(response))
			  }
		  }
		});
	})
	
	
	/**返回上一级*/
	$('#role_next').click(function(){
		var response = ajax(request_urls['platform'], 'get', {'status': 1})
		fill_paltform_table($('#platform tbody'), response)
		$("#platform").css({'display': 'block'})
		$("#role").css({'display': 'none'})
	})
	/**返回上一级*/
	$('#permission_next').click(function(){
		var response = ajax(request_urls['platform'], 'get', {'status': 1})
		fill_paltform_table($('#platform tbody'), response)
		$("#platform").css({'display': 'block'})
		$("#permission").css({'display': 'none'})
	})
	/**返回上一级*/
	$('#user_next').click(function(){
		var response = ajax(request_urls['platform'], 'get', {'status': 1})
		fill_paltform_table($('#platform tbody'), response)
		$("#platform").css({'display': 'block'})
		$("#user").css({'display': 'none'})
	})
	
	
	/**新增平台*/
	$('#btn_platform').click(function(){
		var url = request_urls['platform']
		layer.prompt({title: '平台名称'}, function(pass, index){
		  var response = ajax(url, 'post', {'platform_name': pass})
		  if(response['code'] == 200){
			  layer.close(index);
			  refreshPage()
		  }else{
			  layer.close(index);
		  }
		});
	});
	/**新增用户*/
	$("#btn_user").click(function(){
		var url = request_urls['user']
		var platform_code = $(this).prevAll('.current_platform').val()
		layer.prompt({title: '用户标识'}, function(pass, index){
			  var response = ajax(url, 'post', {'user_code': pass, 'platform_code': platform_code})
			  if(response['code'] == 200){
				  layer.close(index);
				  var response = ajax(url, 'get', {'platform_code': platform_code})
				  fill_user_table($('#user tbody'), response)
			  }else{
				  layer.close(index);
			  }
		});
	})
	/**新增角色*/
	$("#btn_role").click(function(){
		var url = request_urls['role']
		var platform_code = $(this).prevAll('.current_platform').val()
		layer.prompt({title: '角色名称'}, function(pass, index){
			  var response = ajax(url, 'post', {'role_name': pass, 'platform_code': platform_code})
			  if(response['code'] == 200){
				  layer.close(index);
				  var response = ajax(url, 'get', {'platform_code': platform_code})
				  fill_role_table($('#role tbody'), response)
			  }else{
				  layer.close(index);
			  }
		});
	})
	
	
	/**平台禁用*/
	$("#platform").on('click', '.platform_forbidden', function(){
		var url = request_urls['platform']
		var platform_code = $(this).attr('name')
		layer.confirm('确定禁用该平台？', {
		  btn: ['禁用', '取消'] //按钮
		}, function(){
			var response = ajax(url, 'DELETE', {'platform_code': platform_code})
			layer.msg('禁用成功', {icon: 1});
			window.history.go(0)
		}, function(){
			layer.close()
		});
	})

	/**平台信息修改*/
	$("#platform").on("dblclick",".platform_update",function(){
		var params = {'platform_code': $(this).siblings('.current_platform_code').attr('name')}
		doubleClickUpadte($(this), request_urls['platform'], $(this).attr('name'), params)
	})
	/**权限信息修改*/
	$("#permission").on("dblclick",".permission_update",function(){
		var params = {'permission_code': $(this).siblings('.current_permission_code').attr('name')}
		doubleClickUpadte($(this), request_urls['permission'], $(this).attr('name'), params)
	})
	/**角色信息修改*/
	$("#role").on("dblclick",".role_update",function(){
		var params = {'role_code': $(this).siblings('.current_role_code').attr('name')}
		doubleClickUpadte($(this), request_urls['role'], $(this).attr('name'), params)
	})
	/**用户信息修改*/
	$("#user").on("dblclick",".user_update",function(){
		// var params = {'user_code': $(this).siblings('.current_user_code').attr('name')}
		var params = {}
		doubleClickUpadte($(this), request_urls['user'], $(this).attr('name'), params)
	})
	/**权限导入*/
	$("#import_permission").click(function(){
		var platform_code = $(this).siblings('.current_platform').val()
		var permission_url = request_urls['permission']
		layer.open({
		  type: 2,
		  title: "权限导入",
		  area: ['700px', '450px'],
		  fixed: false, //不固定
		  maxmin: true,
		  content: 'upload.html?platform_code='+platform_code,
		  btn: ['导入', '取消'],
		  yes: function(index, layero){
			  var body = layer.getChildFrame('body', index);  //此处加载目标页面(ifreme)的内容
			  var file_obj = body.find("#file").get(0).files[0];
			   // 将文件对象打包成form表单类型的数据
			  var formdata = new FormData;
			  formdata.append('file',file_obj);
			  // 进行文件数据的上传
			  $.ajax({
			      url:host+'import/'+platform_code+"/?storage=1",
			      type:'post',
			      data:formdata,
			      processData:false,
			      contentType:false,
			      success:function(res) {
					layer.close(index)
					refreshPage()
			      },
			  });
		  }
		});
	})
})