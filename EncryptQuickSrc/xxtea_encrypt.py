# encoding=utf-8
__author__ = 'dongxurr123'

import zipfile
import os
import shutil
import struct
import xxtea


# 加密
def encrypt(args):
    src_dir = args.i
    output_zip_path = args.o
    xxtea_key = args.k
    sign = args.s

    print("src dir:%s, output zip path:%s, xxtea_key:%s, sign:%s" % (src_dir, output_zip_path, xxtea_key, sign))

    pdir, src_dir_name = os.path.split(src_dir)
    # 生成一个临时目录，与src目录平级，用以存放临时的每一个加密并改变命名的lua文件
    temp_dir = os.path.join(pdir, ".zip_temp")
    # 若临时文件夹存在，则删除
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    # 若输出zip文件存在，则删除
    if os.path.exists(output_zip_path):
        os.remove(output_zip_path)

    # 加密src_dir，并输出temp_dir下
    encrypt_dir(src_dir, temp_dir,  xxtea_key, sign)

    # 压缩temp_dir到 output_zip_path
    zip_dir(output_zip_path, temp_dir)

    # 加密output_zip_path
    encrypt_zip(output_zip_path, xxtea_key, sign)


# 加密zip文件
def encrypt_zip(zip_path, xxtea_key = "", sign = ""):
    zip_file = open(zip_path, 'rb')
    try:
        content = zip_file.read()
        # 若xxtea_key不为""，则对源文件内容进行加密并写入签名
        if xxtea_key != "":
            encrypt_data = xxtea.encrypt(content, xxtea_key)
            data_len = len(encrypt_data)
            sign_len = len(sign)
            if sign_len > 0:
                encrypt_data = struct.pack("=%ds%ds" % (sign_len, data_len), sign, encrypt_data)
            output_data = encrypt_data
        else:
            output_data = content
    finally:
        zip_file.close()

    os.remove(zip_path)

    out_file = open(zip_path, 'wb')
    try:
        out_file.write(output_data)
    finally:
        out_file.close()


def encrypt_dir(src_dir, temp_dir, xxtea_key, sign):
    for dir_path, dir_names, file_names in os.walk(src_dir):
        for f in file_names:
            if f.endswith(".lua"):
                encrypt_file(src_dir, os.path.join(dir_path, f), temp_dir, xxtea_key, sign)


def encrypt_file(src_dir, file_path, temp_dir,  xxtea_key = "", sign = ""):
    if not file_path.startswith(src_dir):
        print("%s is not parent dir of %s, can not do encrypt" % (src_dir, file_path))

    # 将 X:/game/src/pkg1/pkg2/Module.lua 转换为 pkg1.pkg2.Module的形式
    start_index = len(src_dir)
    encrypt_file_name = file_path[start_index: len(file_path)]
    if encrypt_file_name.startswith(os.path.sep):
        encrypt_file_name = encrypt_file_name[1:len(encrypt_file_name)]
    encrypt_file_name = encrypt_file_name.replace(os.path.sep, ".")

    # 去除.lua扩展名
    encrypt_file_name = encrypt_file_name[0: -4]

    encrypt_file_path = os.path.join(temp_dir, encrypt_file_name)
    print("encrypt file:%s ==============> %s" % (file_path, encrypt_file_path))
    src_file = open(file_path, 'rb')
    output_file = open(encrypt_file_path, 'wb')
    try:
        file_content = src_file.read()
        # 若xxtea_key不为""，则对源文件内容进行加密并写入签名
        if xxtea_key != "":
            encrypt_data = xxtea.encrypt(file_content, xxtea_key)
            data_len = len(encrypt_data)
            sign_len = len(sign)
            if sign_len > 0:
                encrypt_data = struct.pack("=%ds%ds" % (sign_len, data_len), sign, encrypt_data)
            output_data = encrypt_data
        else:
            output_data = file_content

        output_file.write(output_data)
    finally:
        output_file.close()
        src_file.close()


def zip_dir(output_zip_path, file_dir):
    f = zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED)
    for filename in os.listdir(file_dir):
        f.write(os.path.join(file_dir, filename), filename)
    f.close()
