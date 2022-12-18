import os

import sdtools
import sdtools.config_gen
import sdtools.sdt
from sdtools.bench_settings import BenchSettings
from sdtools.config_bench import *
from sdtools.config_gen import *
from sdtools.prompt_settings import PromptSettings
from sdtools.utils import *


def gen_prompt(tag_count, line_count, gs):

    src_dir = "D:\Andrew\Pictures\Grabber\c123Eagle.OG"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, gs=gs)

    line = sdt.gen_prompt(tag_count=tag_count, line_count=line_count)
    line2 = sdt.get_txt_prompt(line_count=5)

    paste_list_to_clipboard(line)

    # bs = BenchSettings()


def image_aug():
    # 只能原地覆写, 运行前先手动保存一份备份
    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=None)

    # 复制文件夹prompt到剪贴板
    # sdt.do_get_prompts()

    # 去除metadatam, 覆盖原文件(不添加suffix)
    sdt.do_remove_info(add_suffix = False, new_meta="")

    # 创建翻转
    sdt.do_flip()

    # 打乱图片
    sdt.do_shuffle()

def do_random_test():
    gs = sdtools.config_gen.main_settings
    bs = BenchSettings(preset_QUICK_SAMPLERS)
    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

    sdt.do_random_benchmark()


def do_fixed_prompt_test():
    gs = sdtools.config_gen.intricate_settings
    bs = BenchSettings(preset_QUICK_SAMPLERS)
    bs.prompt_list=["(best quality:1.3), (masterpiece:0.5), (close-up:0.3), by sks,  (detailed:0.3), 1girl, (intricate:0.6), grey eyes, 1girl, bikini, hair between eyes, blue eyes, long hair, breasts, white dress, crying, close-up, yuge\(mkmk\), aqua ribbon, sitting, outstretched hand, frills, bow, halo, fish, green hair, monitor, frilled apron, facing away, anchor, :t, shoes, very long hair, blue nails, fork, bandaid, hexagon, carrying, rolua, blue flower, skirt, neckerchief, hair ornament, neco, original, highres"]
    bs.resolution=resolution_random
    # bs.seed=3364944276

    src_dir = dst_dir ="D:\Andrew\Pictures\Grabber\c123Eagle.OG - 副本"
    sdt = sdtools.sdt.SDTools(src_dir=src_dir, dst_dir=dst_dir, gs=gs, bs=bs)

    for i in range (99):
        sdt.do_fixed_prompt_benchmark(model_name="edc30110")


def read_txt_prompts_to_clipboard():
    pass



if __name__ == '__main__':
    # d0c_nice, colab, hires fix, 很nb
    bench_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), beautiful detailed eyes",
        end_tags="mechari, arutera, z3zz4, original, highres",
        taboo_tags=longer_taboo_tags
    )
    sexy_words = "sexy, medium breasts, legs, nice body, thighhighs, " \
                 "(masterpiece:0.1), skindentation".split()
    sexy_words_new = " ".join(i for i in sexy_words)

    sexy_settings = PromptSettings(
        start_word="",
        vital_tags="1girl, (best quality), beautiful detailed eyes" + sexy_words_new,
        end_tags="original, highres",
        taboo_tags=longer_taboo_tags
    )
    gs = sexy_settings
    gen_prompt(tag_count=35, line_count=40, gs=gs)




