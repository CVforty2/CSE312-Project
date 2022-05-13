from typing import *
import re
# All image mime types
Image_Ext_To_Mime: Dict[str, str] = {
    "bmp": "image/bmp",
    "gif": "image/gif", 
    "ico": "image/vnd.microsoft.icon",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "webp": "image/webp"
}
boundary_gex = re.compile(r'boundary=(.+)$')
filename_gex = re.compile(r"; ?filename=\"([^\"]+)\"")
httpheader = re.compile("([A-Z]+)\s+(\/[^\s]*)\s+(.+)")
keyvalue = re.compile("([^:]+):\s?(.+)")
name_gex = re.compile(r'; ?name=\"([^\"]+)\"')

multiform_names: Set[str] = {"comment", "upload", "xsrf_token"}

def get_regex_image_extensions() -> str:
    return '(' + '|'.join(f'{img.lower()}|{img.upper()}' for img in Image_Ext_To_Mime.keys()) + ')'
        
