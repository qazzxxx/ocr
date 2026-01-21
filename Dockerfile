# 使用官方Python镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    # 显式安装gunicorn，确保它被安装
    && pip install --no-cache-dir gunicorn


# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=ocr.settings

# 暴露端口
EXPOSE 6632

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:6632", "ocr.wsgi:application"]
    