# OCR API Service

这个项目提供了一个基于 RapidOCR 的文字识别 API 服务，支持 Docker 部署。

## 部署说明 (Deployment)

### 使用 Docker Compose 部署 (推荐)

该项目可以使用 Docker Compose 快速部署。

1.  **准备环境**:
    确保你已经安装了 Docker 和 Docker Compose。

    创建 `docker-compose.yml` 文件:
    ```yaml
    version: "3.8"

    services:
      ocr-api:
        image: ghcr.io/qazzxxx/ocr:main
        container_name: ocr
        restart: always
        ports:
          - "6632:6632"
        environment:
          - TOKEN=${TOKEN}
    ```

## 接口调用说明 (API Usage)

所有 API 请求都需要在 Header 中携带 `token` 进行验证。

### 识别图片文字

- **URL**: `/recognize`
- **Method**: `POST`
- **Header**:
    - `token`: 你的 API Token (需要在环境变量中设置)
- **Body**:
    - `image`: 图片文件 (multipart/form-data)

### 示例代码

#### 使用 CURL

```bash
# 请将 your_secure_token 替换为你设置的 TOKEN
# 请将 image.png 替换为你要识别的图片路径

curl -X POST http://localhost:6632/recognize \
  -H "token: your_secure_token" \
  -F "image=@image.png"
```

#### 使用 Python (Requests)

```python
import requests

url = "http://localhost:6632/recognize"
token = "your_secure_token"
image_path = "path/to/image.png"

headers = {
    "token": token
}

files = {
    "image": open(image_path, "rb")
}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

### 返回结果示例

```json
{
    "status": "success",
    "full_text": "识别出的文字内容...",
    "details": [
        {
            "box": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]],
            "text": "识别出的文字内容...",
            "confidence": 0.98
        }
    ]
}
```
