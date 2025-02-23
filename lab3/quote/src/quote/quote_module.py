import requests
import opencc

converter = opencc.OpenCC('s2t')

def get_quote():
    """A function to get poisoned chicken soup through api"""
    try:
        url = "https://api.oick.cn/dutang/api.php"
        simplified_text = requests.get(url).text
        return converter.convert(simplified_text)
    except:
        return "三百六十行，行行出BUG。"

if __name__ == "__main__":
    quote = get_quote()
    print(quote)