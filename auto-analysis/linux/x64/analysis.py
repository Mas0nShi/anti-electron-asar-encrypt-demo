# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@Name: linux_x64_analysis
@Time: 2022/4/4 19:48
@Desc: It's all about getting better.
"""
import json
import r2pipe


def get_aes_key_and_iv(file_path):
    r = r2pipe.open(file_path)

    r.cmd("aaa")
    regex = r.cmdj("axtj @@ str.base64")
    assert len(regex) == 1

    func = regex[0]["fcn_name"]
    r.cmd(f"s {func}")
    asm = r.cmdj("pdfj")['ops']
    assert len(asm) != 0

    if 'str.dip3' in json.dumps(asm):
        r.cmd('s str.dip3 - 32')
        data = r.cmdj('xj 48')
        key = bytearray(data[0:32])
        iv = bytearray(data[32:48])
    else:
        raise "need rewrite scripts for linux x64"

    return key, iv
