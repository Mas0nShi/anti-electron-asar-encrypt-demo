# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@Name: win_x64_analysis
@Time: 2022/4/3 18:26
@Desc: It's all about getting better.
"""
import struct
import r2pipe


def regex_key_iv(asm_obj):
    asm_regex = []
    for body in asm_obj:
        if "=[4]" in body["esil"] and body['type'] == 'mov':
            opcode, value = body["disasm"].split(", ")
            if "0x" in value:
                asm_regex.append({"opcode": opcode, "value": value})
    return asm_regex


def get_aes_key_and_iv(file_path):
    r = r2pipe.open(file_path)
    r.cmd("aaa")
    regex = r.cmdj("axtj @@ str.base64")
    assert len(regex) == 1

    func = regex[0]["fcn_name"]
    r.cmd(f"s {func}")
    asm = r.cmdj("pdfj")['ops']
    assert len(asm) != 0

    asm_regex = regex_key_iv(asm)
    assert len(asm_regex) == 12

    iv = struct.pack("<4L", *[int(asm_regex[i]['value'], 16) for i in range(4)])
    key = struct.pack("<8L", *[int(asm_regex[i]['value'], 16) for i in range(4, 12)])
    return key, iv