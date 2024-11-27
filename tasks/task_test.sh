#!/bin/bash


# 登陆并保存Token
ACCESS_TOKEN=$(curl -X POST http://127.0.0.1:8000/api/users/login/ \
	-H "Content-Type: application/json" \
	-d '{"username":"testuser","password":"password123"}' | jq -r '.access')


echo -e "\nAccess Token:$ACCESS_TOKEN\n" 

# 获取任务列表
echo -e "Fetching tasks...\n" 
curl -X GET http://127.0.0.1:8000/api/tasks/ \
	-H "Authorization: Bearer $ACCESS_TOKEN"

# 获取筛选后的任务列表
echo -e "Fetching tasks with  the condition...\n"
curl -X GET http://127.0.0.1:8000/api/tasks/ \
	-H "Authorization: Bearer $ACCESS_TOKEN" \
	-H "Content-Type:application/json" \
	-d '{
			"status":"completed",
			"priority":"low"
	}'
# 创建新任务
#echo "creating new task..."
#curl -X POST http://127.0.0.1:8000/api/tasks/ \
#	-H "Authorization: Bearer $ACCESS_TOKEN" \
#	-H "Content-Type: application/json" \
#	-d '{"title":"New Task","description":"Complete project"}'

# 更新单个任务的所有信息
echo -e "\nupdate task pk\n"
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
	-H "Authorization: Bearer $ACCESS_TOKEN" \
	-H "Content-Type:application/json" \
	-d '{
		"title":"Updated Task Title",
		"desription":"Updated Task Description",
		"status":"completed"
	}'
# 更新单个任务的部分信息
echo -e "\nupdate partial task\n" 
curl -X PATCH http://127.0.0.1:8000/api/tasks/2/ \
	-H "Authorization: Bearer $ACCESS_TOKEN" \
	-H "Content-Type:application/json" \
	-d '{
		"status":"completed"
	}'

# 删除单个任务
echo -e "\ndelete task\n" 
curl -X DELETE http://127.0.0.1:8000/api/tasks/3/ \
	-H "Authorization:Bearer $ACCESS_TOKEN" 

