# ocr_api/api.py
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from rapidocr_onnxruntime import RapidOCR
import io
from PIL import Image

# 初始化Ninja API和RapidOCR
api = NinjaAPI(title="图片文字识别API", description="接收图片并返回识别出的文字")
ocr = RapidOCR()

@api.post("/recognize", summary="识别图片中的文字")
def recognize_text(request, image: UploadedFile = File(...)):
    """
    接收图片文件并识别其中的文字
    
    - 接收: 图片文件(支持常见格式如jpg, png等)
    - 返回: JSON格式的识别结果，包含识别到的文字和详细信息
    """
    try:
        # 读取图片内容
        image_data = image.read()
        
        # 验证图片格式
        try:
            # 尝试打开图片以验证格式
            img = Image.open(io.BytesIO(image_data))
            img.verify()  # 验证图片完整性
        except Exception as e:
            return {
                "status": "error",
                "message": f"无效的图片文件: {str(e)}"
            }
        
        # 使用RapidOCR进行文字识别
        result, _ = ocr(image_data)
        
        # 处理识别结果
        if result:
            # 提取所有识别到的文本
            full_text = "\n".join([line[1] for line in result])
            
            return {
                "status": "success",
                "full_text": full_text,
                "details": [
                    {
                        "box": line[0],  # 文字区域坐标
                        "text": line[1],  # 识别的文字
                        "confidence": line[2]  # 置信度
                    } for line in result
                ]
            }
        else:
            return {
                "status": "success",
                "message": "未识别到任何文字",
                "full_text": "",
                "details": []
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"处理图片时出错: {str(e)}"
        }
