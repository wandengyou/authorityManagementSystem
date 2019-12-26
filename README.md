# authorityManagementSystem
## 1、实现前后端权限分离
    原理：不强行绑定前后端权限关系(即：菜单对应接口权限)，将前端菜单权限、后台接口权限统一放到权限表中进行分配
    <br>
    permission_type：确定权限类型[菜单、接口]， identifier:确定菜单级别(xx:一级，xx.xx:二级)
## 2、管理多个平台的权限管理、认证
## 3、接口安全认证
    a、请求身份是否合法， b、请求参数是否被篡改，请求是否唯一
## 4、用户权限管理
    a、接口(数据)权限，b、用户权限


