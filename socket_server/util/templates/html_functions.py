from typing import *
import os

def write_comments_image(comments: Set[str], image_path: str) -> str:
    return f"<h2>Comments about {os.path.splitext(image_path[len('/uimage/'):])[0].replace('_', ' ') if image_path != 'NO_IMAGE' else 'No Particular Image'}</h2>\n" + \
         "<div>" + (f"<img src={image_path} />" if image_path != "NO_IMAGE" else '') + "<h3>Comments:</h3><ul>\n" + \
             (''.join(f"<li>{comment}</li>\n" for comment in comments)) + "</ul>\n</div>"