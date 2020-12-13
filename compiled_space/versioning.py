""" Versioning - as in res_mods/ """

from sections import (
    all_sections_cls_0_9_12, all_sections_cls_0_9_14,
    all_sections_cls_0_9_16, all_sections_cls_0_9_20,
    all_sections_cls_1_0_0, all_sections_cls_1_0_1,
    all_sections_cls_1_1_0, all_sections_cls_1_2_0,
    all_sections_cls_1_4_0, all_sections_cls_1_5_0,
    all_sections_cls_1_5_1, all_sections_cls_1_6_0,
    all_sections_cls_1_6_1, all_sections_cls_1_7_0,
    all_sections_cls_1_11_0)



WOT_VERSIONS = [
    {
        'sections': all_sections_cls_0_9_12,
        'versions': (
            '0.9.12', # WoT init space.bin
            '0.9.13',
        )
    },
    {
        'sections': all_sections_cls_0_9_14,
        'versions': (
            '0.9.14',
        )
    },
    {
        'sections': all_sections_cls_0_9_16,
        'versions': (
            '0.9.16',
        )
    },
    {
        'sections': all_sections_cls_0_9_20,
        'versions': (
            '0.9.17.0', '0.9.17.1',
            '0.9.20.0', '0.9.20.1.4'
            '0.9.21.0', '0.9.21.0.1', '0.9.21.0.2'
            '0.9.22.0', '0.9.22.0.1'
        )
    },
    {
        'sections': all_sections_cls_1_0_0,
        'versions': (
            '1.0.0', '1.0.0.2', '1.0.0.3',
        )
    },
    {
        'sections': all_sections_cls_1_0_1,
        'versions': (
            '1.0.1.0', '1.0.1.1',
            '1.0.2.0', '1.0.2.1',
        )
    },
    {
        'sections': all_sections_cls_1_1_0,
        'versions': (
            '1.1.0', '1.1.0.1',
        )
    },
    {
        'sections': all_sections_cls_1_2_0,
        'versions': (
            '1.2.0', '1.2.0.1',
            '1.3.0.0', '1.3.0.1',
        )
    },
    {
        'sections': all_sections_cls_1_4_0,
        'versions': (
            '1.4.0.0', '1.4.0.1',
            '1.4.1.0', '1.4.1.1',
        )
    },
    {
        'sections': all_sections_cls_1_5_0,
        'versions': (
            '1.5.0.4',
        )
    },
    {
        'sections': all_sections_cls_1_5_1,
        'versions': (
            '1.5.1.1', '1.5.1.3',
        )
    },
    {
        'sections': all_sections_cls_1_6_0,
        'versions': (
            '1.6.0.0',
        )
    },
    {
        'sections': all_sections_cls_1_6_1,
        'versions': (
            '1.6.1.0', '1.6.1.1', '1.6.1.2', '1.6.1.3',
        )
    },
    {
        'sections': all_sections_cls_1_7_0,
        'versions': (
            '1.7.0.1', '1.7.0.2',
            '1.7.1.0', '1.7.1.1', '1.7.1.2',
            '1.8.0.0', '1.8.0.1',
            '1.10.1.4',
        )
    },
    {
        'sections': all_sections_cls_1_11_0,
        'versions': (
            '1.11.0.0', # actual
        )
    }
]



def get_sections(ver):
    for it in WOT_VERSIONS:
        if ver in it['versions']:
            return it['sections']
    raise Exception(f'WoT version "{ver}" is not supported')
