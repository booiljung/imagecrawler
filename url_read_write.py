"""
keyed_urls 포맷은 검색엔진에서 키워드를 주고 얻은 이미지 링크 리스트를 저장 한다.
파이썬 구조는 { key: [], ... } 이다.

텍스트 파일 구조는 아래와 같다.
---검색키워드
url
url
.
.
.
---검색키워드
url
url
url
.
.
.
"""

def write_image_urls_as_file(keyed_urls, filename):
    """지정한 filename에 keyed_urls을 저장한다.
    """
    with open(filename, 'w') as f:
        for key, value in keyed_urls.items():
            f.write('---' + key + '\n')
            for url in value:
                f.write(url + '\n')


def read_image_urls_from_file(filename):
    """지정한 파일이름으로 텍스트 파일을 읽어 keyed_urls에 저장 한다.
    """
    keyed_urls = {}
    with open(filename, 'r') as f:
        key = None
        urls = []
        for line in f:
            line = line.strip()
            if line.startswith('---'):
                if key is not None:
                    keyed_urls[key] = urls
                    key = None
                    urls = []
                key = line[3:]
                key = key.strip()
            else:
                urls.append(line)
        if key is not None:
            keyed_urls[key] = urls
    return keyed_urls