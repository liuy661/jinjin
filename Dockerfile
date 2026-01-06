# 1. 使用官方 Python 3.10 镜像，完美兼容 Gemini
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 设置腾讯云镜像源，让下载依赖飞快
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
    && pip config set global.trusted-host mirrors.cloud.tencent.com

# 4. 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 拷贝代码
COPY . .

# 6. 暴露微信云托管默认的 80 端口
EXPOSE 80

# 7. 启动 Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
