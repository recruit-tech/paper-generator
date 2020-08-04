# -*- coding: utf-8 -*-
import numpy as np
import cv2
import glob
import random
import os
import sys

# jis(X0208 -> X0201)
code_map = {0x2156:0xA2,0x2157:0xA3,0x2572:0xA6,0x2522:0xB1,0x2524:0xB2,0x2526:0xB3,0x2528:0xB4,0x252A:0xB5,0x252B:0xB6,0x252D:0xB7,0x252F:0xB8,0x2531:0xB9,0x2533:0xBA,0x2535:0xBB,0x2537:0xBC,0x2539:0xBD,0x253B:0xBE,0x253D:0xBF,0x253F:0xC0,0x2541:0xC1,0x2544:0xC2,0x2546:0xC3,0x2548:0xC4,0x254A:0xC5,0x254B:0xC6,0x254C:0xC7,0x254D:0xC8,0x254E:0xC9,0x254F:0xCA,0x2552:0xCB,0x2555:0xCC,0x2558:0xCD,0x255B:0xCE,0x255E:0xCF,0x255F:0xD0,0x2560:0xD1,0x2561:0xD2,0x2562:0xD3,0x2564:0xD4,0x2566:0xD5,0x2568:0xD6,0x2569:0xD7,0x256A:0xD8,0x256B:0xD9,0x256C:0xDA,0x256D:0xDB,0x256F:0xDC,0x2573:0xDD,0x212B:0xDE,0x212C:0xDF}

# 全角英数の半角化データ
# 現状小文字データが無いため、大文字に寄せる
IN_CHAR = 'ぁぃぅぇぉゃゅょっ' \
          'ァィゥェォャュョッ' \
          'ガギグゲゴザジズゼゾダジヅデドバビブベボパピプペポヴー' \
          '！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～abcdefghijklmnopqrstuvwxyz'
#INPUT_CHAR = "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］ ＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～"

OUT_CHAR = 'あいうえおやゆよつ' \
           'アイウエオヤユヨツ' \
           'カキクケコサシスセソタチツテトハヒフヘホハヒフヘホウ-' \
           '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`ABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#OUT_CHAR = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

REP_CHAR = str.maketrans(IN_CHAR, OUT_CHAR)



SPACE_CODE = 0x20
CHECK_CODE_DUMMY = 0x21
CIR_CODE_DUMMY = 0x23

# 文字列から文字列の画像リストを取得
def getETLImages(text):

    images = []
    for i, char in enumerate(text):
        images.append(code2img(char2jis_code(char.translate(REP_CHAR))))

    return images

# JISコードを指定し該当するETL画像を取得
def code2img(jis_code):

    #print('jis_code:', jis_code)

    etl6_dir = 'ETL6_img'
    #etl9_dir = 'ETL9B_img'
    etl9_dir = 'ETL9G_img'
    symbol_dir = 'symbol_img'

    font_img_dir = etl6_dir
    code = jis_code

    # チェックと丸印のの暫定対応（ "!"：チェック、"#"：丸印）
    if jis_code == CHECK_CODE_DUMMY or jis_code == CIR_CODE_DUMMY:
        font_img_dir = symbol_dir
    # スペース
    elif jis_code == SPACE_CODE:
        code = 0x00 # スペースの場合は無効となるコードを設定し空白を返却
    elif jis_code in code_map.keys():
    #if jis_code in code_map.keys():
        code = code_map[jis_code]
        font_img_dir = etl6_dir
    elif jis_code < 0x00FF:
        font_img_dir = etl6_dir
    else:
        font_img_dir = etl9_dir

    target_dir = os.path.join(font_img_dir, hex(code)[2:])

    #print('target:', target_dir)

    if os.path.exists(target_dir):
        img_file = get_rand_file(target_dir)
        char_img = cv2.imread(img_file, 0)
    else:
        char_img = np.ones((64, 64),np.uint8) * 255

    return char_img

# 指定したディレクトリ内からランダムにファイルを取得
def get_rand_file(img_dir):
    files = glob.glob(os.path.join(img_dir, '*.png'))

    return random.choice(files)

# 文字（1文字：システムのUTF-8）からJISコードを取得
def char2jis_code(char):

    return int(char.encode('euc-jp').hex(), 16) & ~0x8080

def trim_img(img):
    cv
    return

def main():

    args = sys.argv
    # test sample
    text = args[1] if len(args) > 1 else 'あいうえお'

    img_list = getETLImages(text)

    for img in img_list:
        cv2.imshow('window', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':

    main()
