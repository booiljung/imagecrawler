def write_image_urls_as_file(keyed_image_urls, filename):
    with open(filename, 'w') as f:
        for key, value in keyed_image_urls.items():
            f.write('---' + key + '\n')
            for url in value:
                f.write(url + '\n')


def read_image_urls_from_file(filename):
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