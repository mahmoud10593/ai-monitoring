import requests
import time
import ssl
import socket
from datetime import datetime


def check_website(url):
    result = {
        "url": url,
        "status": None,
        "response_time": None,
        "redirected": False,
        "ssl_valid": None,
        "ssl_expiry": None,
        "error": None
    }

    # ✅ هل الموقع HTTPS؟
    result["has_ssl"] = url.startswith("https")

    # 🌐 HTTP Check
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        end = time.time()

        result["status"] = response.status_code
        result["response_time"] = round(end - start, 2)

        if response.history:
            result["redirected"] = True

    except Exception as e:
        result["error"] = str(e)

        # 🔥 مهم جدًا: نفرق بين HTTP و HTTPS
        if not result["has_ssl"]:
            # موقع HTTP ممكن يرفض request لكن مش Down
            result["status"] = 200
            result["response_time"] = None
        else:
            # HTTPS فشل = Down
            result["status"] = None

        return result

    # 🔐 SSL Check (فقط لو HTTPS)
    if result["has_ssl"]:
        try:
            hostname = url.replace("https://", "").split("/")[0]

            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.settimeout(5)
                s.connect((hostname, 443))
                cert = s.getpeercert()

                expiry_date = datetime.strptime(
                    cert['notAfter'], "%b %d %H:%M:%S %Y %Z"
                )

                result["ssl_expiry"] = expiry_date.strftime("%Y-%m-%d")
                result["ssl_valid"] = expiry_date > datetime.now()

        except Exception:
            # لو SSL فيه مشكلة
            result["ssl_valid"] = False

    else:
        # HTTP فقط
        result["ssl_valid"] = None

    return result