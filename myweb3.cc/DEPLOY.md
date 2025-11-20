# 3am Club 门户网站部署指南 (Apache 版)

本文档详细说明如何在已安装 Apache 的 Ubuntu 服务器上，从 GitHub 拉取代码并部署 `myweb3.cc`。

## 1. 准备工作

*   **服务器**: Ubuntu (已安装 Apache/httpd)。
*   **域名**: `myweb3.cc` (请确保已解析到服务器 IP)。
*   **代码库**: [https://github.com/zlexdl/myweb3_homepage](https://github.com/zlexdl/myweb3_homepage)
*   **现状**: 服务器上已有 `alpha.myweb3.cc` 在运行，本部署将新增 `myweb3.cc`，两者互不干扰。

## 2. 获取网站文件 (推荐方案)

为了方便日后一键更新，我们直接将仓库克隆到服务器，并让 Apache 直接读取仓库中的发布目录。

1.  **安装 Git** (如果未安装):
    ```bash
    sudo apt update
    sudo apt install git -y
    ```

2.  **克隆仓库**:
    我们将仓库克隆到 `/var/www/myweb3_repo`。

    ```bash
    cd /var/www
    # 克隆整个仓库
    sudo git clone https://github.com/zlexdl/myweb3_homepage.git myweb3_repo
    ```

3.  **设置权限**:
    把所有权交给 Apache 用户 (`www-data`)，以便它能读取和写入日志，同时允许我们后续 pull 更新。
    ```bash
    sudo chown -R www-data:www-data /var/www/myweb3_repo
    # 赋予写权限以便 git pull (可选，或使用 sudo git pull)
    sudo chmod -R 755 /var/www/myweb3_repo
    ```

## 3. 配置 Apache (VirtualHost)

我们需要修改 Apache 配置，使其**只对外展示仓库里的 `myweb3.cc` 子目录**，这样源代码和PPT文件不会被公开。

1.  **创建/修改配置文件**:
    ```bash
    sudo nano /etc/apache2/sites-available/myweb3.cc.conf
    ```

2.  **写入配置**:
    注意 `DocumentRoot` 的路径指向了子目录。

    ```apache
    <VirtualHost *:80>
        ServerAdmin webmaster@myweb3.cc
        ServerName myweb3.cc
        ServerAlias www.myweb3.cc

        # [关键] 网站根目录指向仓库下的 myweb3.cc 子文件夹
        DocumentRoot /var/www/myweb3_repo/myweb3.cc

        # 目录权限设置
        <Directory /var/www/myweb3_repo/myweb3.cc>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        # 安全设置：禁止访问 .git 目录 (防止代码泄露)
        <DirectoryMatch "/\.git">
            Require all denied
        </DirectoryMatch>

        # 日志文件
        ErrorLog ${APACHE_LOG_DIR}/myweb3.cc_error.log
        CustomLog ${APACHE_LOG_DIR}/myweb3.cc_access.log combined
    </VirtualHost>
    ```
    *按 `Ctrl+O`, `Enter` 保存，`Ctrl+X` 退出。*

3.  **启用站点**:
    ```bash
    sudo a2ensite myweb3.cc.conf
    sudo systemctl reload apache2
    ```

## 4. 配置 HTTPS (SSL 证书)

(此步骤不变，Certbot 会自动读取新的 Apache 配置)

1.  **申请证书**:
    ```bash
    sudo certbot --apache -d myweb3.cc -d www.myweb3.cc
    ```

## 5. 极简更新指南

将来您更新了 GitHub 上的代码后，在服务器上只需执行一条命令即可完成更新：

```bash
# 1. 进入仓库目录
cd /var/www/myweb3_repo

# 2. 拉取最新代码 (Apache 会立即读取到新内容)
sudo git pull
```

无需复制，无需重启服务（除非修改了 .htaccess 或 apache 配置），**立即生效**。
