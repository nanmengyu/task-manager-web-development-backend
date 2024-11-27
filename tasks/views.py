from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerilizer
from datetime import datetime
# Create your views here.

class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取查询参数，默认值为空
        status_filter = request.query_params.get('status',None)
        priority_filter = request.query_params.get('priority',None)

        # 初始查询
        tasks = Task.objects.filter(user=request.user)

        # 如果传递了status筛选条件，过滤任务
        if status_filter:
            tasks = tasks.filter(status=status_filter)
    
        # 如果传递了priority筛选条件，过滤任务
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
       
        serializer = TaskSerilizer(tasks,many=True)
       
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request):
        data = request.data
        data['user'] = request.user.id
        serializer = TaskSerilizer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk,user):
        try:
            return Task.objects.get(pk=pk,user=user)
        except Task.DoesNotExist:
            return None
    
    def put(self,request,pk):
        task = self.get_object(pk,request.user)
        if not task:
            return Response({"error":"Task not found or not accesssible"},status=status.HTTP_404_NOT_FOUND)


        serializer = TaskSerilizer(task,data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        task = self.get_object(pk,request.user)
        if not task:
            return Response({"error":"Task not found or not accessible"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerilizer(task,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        task = self.get_object(pk,request.user)
        if not task:
            return Response({"error":"Task not found or not accessible"},status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response({"message":"Task deleted successfully"},status=status.HTTP_204_NO_CONTENT)