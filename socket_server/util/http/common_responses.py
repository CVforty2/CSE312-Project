from util.http.Response import Response
from util.static_info import static_variables as sv

def plain_text(message: str) -> Response:
    return Response(
        headerdict={
            "Content-Type": "text/plain"
        }, body=message.encode()
    )

def static_html(html_file: str) -> Response:
    return Response(
        headerdict={
            "Content-Type": "text/html;charset=utf-8"
        }, body=open(html_file, 'rb').read()
    )

def static_css(css_file: str) -> Response:
    return Response(
        headerdict={
            "Content-Type": "text/css;charset=utf-8"
        }, body=open(css_file, 'rb').read()
    )

def static_js(js_file: str) -> Response:
    return Response(
        headerdict={
            "Content-Type": "text/javascript;charset=utf-8"
        }, body=open(js_file, 'rb').read()
    )

def static_image(img_path: str, img_ext: str) -> Response:
    return Response(
        headerdict={
            "Content-Type": sv.Image_Ext_To_Mime[img_ext.lower()]
        }, body=open(f"{img_path}.{img_ext}", 'rb').read()
    )
