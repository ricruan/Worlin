# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 9099

# 防止Python在容器中生成.pyc文件
ENV PYTHONDONTWRITEBYTECODE=1

# 关闭缓冲以方便容器日志记录
ENV PYTHONUNBUFFERED=1

# 创建虚拟环境
RUN python -m venv /app/.venv

# 激活虚拟环境并安装依赖
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 安装 python3-dev，用于编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends python3-dev

# 安装C编译器， pandas包需要C编译器
RUN apt-get update && apt-get install -y --no-install-recommends build-essential g++ && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# --bind 改成 --reload 可以支持热重载
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9099"]
