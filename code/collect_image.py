# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from PIL import Image
from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler

#定数
GOOGLE_CRAWLER_LIBRARY = 'GOOGLE'
BING_CRAWLER_LIBRARY   = 'BING'
BAIDU_CRAWLER_LIBRARY  = 'BAIDU'
PATH_TMP_IMAGE_FOLDER  = '/root/app/code/images/tmp/'
PATH_SAVE_IMAGE_FOLDER = '/root/app/code/images/'

# ファイル削除
def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)

# フォルダ作成とファイル移動
def mkdir_folder_and_move_file(save_image):
    save_image_path = PATH_SAVE_IMAGE_FOLDER + save_image
    images = os.listdir(PATH_TMP_IMAGE_FOLDER)
    if len(images) > 1:
        os.mkdir(save_image_path)
        for image in images:
            tmp_image_path = PATH_TMP_IMAGE_FOLDER + image
            if os.path.isfile(tmp_image_path) and os.path.isdir(save_image_path):
                shutil.move(tmp_image_path, save_image_path)

# Google
def crawler_image_google(input_search_world, input_download_cnt):
    google_crawler = GoogleImageCrawler(
        feeder_threads = 1,
        parser_threads = 1,
        downloader_threads = 4,
        storage = {'root_dir': PATH_TMP_IMAGE_FOLDER}
        )
    google_crawler.crawl(
        keyword = input_search_world,
        filters = None,
        offset = 0,
        max_num = input_download_cnt,
        min_size = None,
        max_size = None,
        file_idx_offset = 0
        )

# Bing
def crawler_image_bing(input_search_world, input_download_cnt):
    bing_crawler = BingImageCrawler(
        storage = {"root_dir": PATH_TMP_IMAGE_FOLDER}
        )
    bing_crawler.crawl(
        keyword = input_search_world,
        filters = None,
        offset = 0,
        max_num = input_download_cnt
        )

# Baidu
def crawler_image_baidu(input_search_world, input_download_cnt):
    baidu_crawler = BaiduImageCrawler(
        storage = {"root_dir": PATH_TMP_IMAGE_FOLDER}
        )
    baidu_crawler.crawl(
        keyword = input_search_world,
        filters = None,
        offset = 0,
        max_num = input_download_cnt,
        min_size = None,
        max_size = None
        )

# crawler処理開始
def start_crawler(input_params, input_search_world, input_download_cnt, select_search_engine):
    # 画像の一時保管先のtmp領域を構築
    if os.path.isdir(PATH_TMP_IMAGE_FOLDER):
        shutil.rmtree(PATH_TMP_IMAGE_FOLDER)
    os.mkdir(PATH_TMP_IMAGE_FOLDER)

    if select_search_engine == GOOGLE_CRAWLER_LIBRARY:
        crawler_image_google(input_search_world, input_download_cnt)
    if select_search_engine == BING_CRAWLER_LIBRARY:
        crawler_image_bing(input_search_world, input_download_cnt)
    if select_search_engine == BAIDU_CRAWLER_LIBRARY:
        crawler_image_baidu(input_search_world, input_download_cnt)
    # 画像のバリデーションチェックと不要画像の削除
    images = os.listdir(PATH_TMP_IMAGE_FOLDER)
    for image in images:
        # pathを結合
        tmp_image_path = PATH_TMP_IMAGE_FOLDER + image
        if os.path.isfile(tmp_image_path):
            # 画像の形式と縦横pxを取得
            im = Image.open(tmp_image_path)
            # 画像のbyteサイズを取得
            image_byte_size = os.path.getsize(tmp_image_path)
            if im.format in image_type[input_image_type]:
                # pxのチェック
                if im.size[0] >= input_max_image_px or im.size[1] >= input_max_image_px or im.size[0] <= input_min_image_px or im.size[1] <= input_min_image_px:
                    remove_file(tmp_image_path)
                    print(image + ' => Pixel size is over limits')
                    continue
                # ByteSizeのチェック
                if image_byte_size >= input_max_image_size or image_byte_size <= input_min_image_size:
                    remove_file(tmp_image_path)
                    print(image + ' => Byte size is over limits')
                    continue
                print(image + ' => No problem')
            else:
                remove_file(tmp_image_path)
                print(image + ' => ImageType is problem')
    # tmp領域から新規保存フォルダに画像を移行
    mkdir_folder_and_move_file(input_params + select_search_engine + '_IMG_' + str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
    print(select_search_engine + ' => Crawling is finished')

# ユーザ入力による画像バリデーションチェックのパラメータ
input_search_world   = str(input('SearchWord >>> '))
input_download_cnt   = int(input('DLCount >>> '))
input_max_image_size = int(input('MaxByte >>> '))
input_min_image_size = int(input('MinByte >>> '))
input_max_image_px   = int(input('MaxPxSize >>> '))
input_min_image_px   = int(input('MinPxSize >>> '))
input_image_type     = int(input('1: JPG(JPEG)&&PNG 2: JPG(JPEG) 3: PNG >>> '))

# とりあえずjpegとpng
image_type = {
    1:[
        "JPEG",
        "JPG",
        "PNG"
    ],
    2:[
        "JPEG",
        "JPG"
    ],
    3:[
        "PNG"
    ]
}

input_params = input_search_world + '_' + str(input_max_image_size) + '_' + str(input_min_image_size) + '_' + str(input_max_image_px) + '_' + str(input_min_image_px) + '_' + '_'.join(image_type[input_image_type]) + '_' 

# google
start_crawler(input_params, input_search_world, input_download_cnt, GOOGLE_CRAWLER_LIBRARY)
# bing
start_crawler(input_params, input_search_world, input_download_cnt, BING_CRAWLER_LIBRARY)
# baidu
start_crawler(input_params, input_search_world, input_download_cnt, BAIDU_CRAWLER_LIBRARY)

print('Processing completed successfully')