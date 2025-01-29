<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">RuoYi-Vue3-FastAPI v1.5.1</h1>
<h4 align="center">基于-Vue3+FastAPI前后端分离的快速开发框架</h4>

## 项目开发及发布相关

#### 开发参考
``` bash
#  将最新后端资源包到出到 requirements.txt
pip freeze > requirements.txt
```

#### 前端
```bash
# 进入前端目录
cd ruoyi-fastapi-frontend

# 安装依赖
npm install 或 yarn --registry=https://registry.npmmirror.com

# 建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev 或 yarn dev
```

#### 后端
```bash
# 进入后端目录
cd ruoyi-fastapi-backend

# 启动虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

 *   请使用你实际的虚拟环境路径。
 
# 安装依赖项
pip install -r requirements.txt


# (已弃用，仅参考)如果使用的是MySQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements.txt
# (已弃用，仅参考)如果使用的是PostgreSQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements-pg.txt

# 配置环境
在.env.dev文件中配置开发环境的数据库和redis

# Redis配置说明
1. 确保Redis服务已经正确安装并运行
2. 检查.env.dev文件中的Redis配置，默认配置如下：
   ```
   REDIS_HOST=127.0.0.1  # Redis服务器地址
   REDIS_PORT=6379       # Redis端口
   REDIS_DB=0           # Redis数据库编号
   REDIS_PASSWORD=      # Redis密码（如果有）
   ```

# 启动Redis服务
# Linux/Mac环境
redis-server

# 或使用Docker运行Redis（确保Docker已安装）
docker run -d --name ruoyi-redis \
  -p 6379:6379 \
  --restart always \
  redis:latest

# 运行sql文件
1.新建数据库ruoyi-fastapi(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ruoyi-fastapi.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ruoyi-fastapi-pg.sql

# 运行后端
# 确保Redis服务正在运行后再启动后端服务
python3 app.py --env=dev

# 以热加载模式运行后端
uvicorn app:app --reload
```

#### 访问
```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://localhost:80
```

### 发布

#### 前端
```bash
# 构建测试环境
npm run build:stage 或 yarn build:stage

# 构建生产环境
npm run build:prod 或 yarn build:prod
```

#### 后端
```bash
# 配置环境
1. 在.env.prod文件中配置生产环境的数据库和redis
2. 确保Redis服务正常运行且可访问
3. 检查Redis连接配置是否正确

# 使用Docker运行Redis（生产环境）
docker run -d --name ruoyi-redis \
  -p 6379:6379 \
  --restart always \
  -v /path/to/redis/data:/data \
  redis:latest

# 运行后端
python3 app.py --env=prod
```

#### 技术介绍





