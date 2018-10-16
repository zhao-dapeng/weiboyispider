import re


def deal_pack_name(pack_name):
    """
    处理&#x字符以及去掉span表情标签
    :param pack_name: 不规范的用户名
    :return: 处理后的用户名
    """
    if type(pack_name) is str:
        two_list = re.findall('&#x(\w{2});', pack_name)
    else:
        return pack_name
    for i in range(len(two_list)):
        pack_name = re.sub('&#x\w{2};', '&#x00%s', pack_name, count=1) % two_list[i]

    pack_name = pack_name.replace('&#x', r'\u').replace(';', '').encode('utf-8').decode('unicode_escape')
    pack_name = re.sub('(<span.*?</span></span>)', '', pack_name)
    return pack_name


if __name__ == '__main__':
    print(deal_pack_name('&#x4e00;&#x6761;'))