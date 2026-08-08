#!/bin/bash
set -e

echo "=========================================="
echo "  头条新闻后端 - 服务器部署脚本"
echo "=========================================="

# ---------- 1. 系统更新 & 安装依赖 ----------
echo "[1/5] 安装系统依赖..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nginx git 2>&1 | tail -1

# ---------- 2. 创建项目目录 ----------
echo "[2/5] 创建项目目录..."
mkdir -p /opt/toutiao_backend
cd /opt/toutiao_backend

# ---------- 3. 安装 Python 依赖 ----------
echo "[3/5] 安装 Python 依赖..."
pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple 2>&1 | tail -3

# ---------- 4. 创建 systemd 服务 ----------
echo "[4/5] 配置 systemd 服务..."
cat > /etc/systemd/system/toutiao.service << 'SERVICE'
[Unit]
Description=Toutiao News FastAPI Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/toutiao_backend
Environment=MYSQL_HOST=172.17.0.14
Environment=MYSQL_PORT=3306
Environment=MYSQL_USER=toutiao_user
Environment=MYSQL_PASSWORD=Toutiao@2026!
Environment=MYSQL_DATABASE=cloud1-5gh0r8j0272e1c10
Environment=SQL_ECHO=false
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

# ---------- 5. 启动服务 ----------
echo "[5/5] 启动服务..."
systemctl daemon-reload
systemctl enable toutiao
systemctl restart toutiao

# ---------- 验证 ----------
echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo "  服务状态:"
systemctl status toutiao --no-pager 2>&1 | head -8
echo ""
echo "  访问地址: http://43.142.85.218:8000"
echo "  健康检查: curl http://localhost:8000/"
echo "=========================================="
