import requests
import zhconv


def get_quote():
    """A function to get poisoned chicken soup through api"""
    try:
        url = "https://api.oick.cn/dutang/api.php"
        simplified_text = requests.get(url).text
        return zhconv.convert(simplified_text, 'zh-tw')
    except:
        return "三百六十行，行行出BUG。"

if __name__ == "__main__":
    quote = get_quote()
    print(quote)