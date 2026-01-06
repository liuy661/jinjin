# 1. 使用官方 Python 3.10 轻量级镜像，兼容性极好
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 设置国内镜像源加速下载
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
    && pip config set global.trusted-host mirrors.cloud.tencent.com

# 4. 先安装基础依赖（减少构建时间）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 拷贝所有代码到镜像中
COPY . .

# 6. 暴露 80 端口（微信云托管默认端口）
EXPOSE 80

# 7. 启动 Django 服务
# 注意：helloworld 替换为你实际存放 settings.py 的文件夹名
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
