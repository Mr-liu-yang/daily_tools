#!/usr/bin/env python
# encoding: utf-8

import requests
import tqdm
import sys


def download_from_url(url, dst):
    response = requests.get(url, stream=True) #(1)
    file_size = int(response.headers['content-length']) #(2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst) #(3)
    else:
        first_byte = 0
    if first_byte >= file_size: #(4)
        return file_size
    header = {"Range": f"bytes={first_byte}-{file_size}"}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True) #(5)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024): #(6)
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == '__main__':
    url = sys.argv[1]
    path = '/Users/rt_u/Desktop/夏目友人帐第一集.mp4'
    download_from_url(url, path)
