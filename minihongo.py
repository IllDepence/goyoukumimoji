from unicodedata import decomposition

def get_kumimoji():
    """ Unicodeにある片仮名や平仮名を使用した組文字の配列を返す
    """

    return [chr(x) for x in range(13056, 13143+1)] + [chr(127488)]

def decomp(c):
    """ >>> decomp('㍗')
        ['ワ', 'ッ', 'ト']
    """

    return [chr(int(x, 16)) for x in decomposition(c).split(' ')[1:]]

def get_square_pattern_kumimoji():
    """ ㌐/㌃/㌀ ○
        ㌕/㌙/㌖ ☓
    """

    return [x for x in get_kumimoji() if len(decomp(x)) in [2, 3, 4]]

def build_marked_2gram_sets(spkm):
    """ 引数：　組文字の配列
        返り値：１行目・２行目・１列目・２列目それぞれの配列

        例：　　>>> build_marked_2gram_sets(['㌐','㌳'])
                [['ギ$','$フィ','フィ$','フィ'],
                 ['$ガ','$ート','ート$','ート'],
                 ['ギ$'],
                 ['$ガ','$ィト','ィト$','ィト']]

        注１：　㌳とかの「ー」は縦書きで使えない
        注２：　$は文字列の始まり・終わりを表す
    """

    yoko_t = []
    yoko_b = []
    tate_l = []
    tate_r = []
    for km in spkm:
        dc = decomp(km)
        if len(dc) == 2:    # 例：㌔
            yoko_t.append('{}$'.format(dc[0]))
            yoko_b.append('${}'.format(dc[1]))
            if 'ー' not in dc[0]:
                tate_l.append('{}$'.format(dc[0]))
            if 'ー' not in dc[1]:
                tate_r.append('${}'.format(dc[1]))
        elif len(dc) == 3:  # 例：㌵
            yoko_t.append('${}{}'.format(dc[0], dc[1]))
            yoko_t.append('{}{}$'.format(dc[0], dc[1]))
            yoko_t.append('{}{}'.format(dc[0], dc[1]))
            yoko_b.append('{}$'.format(dc[2]))
            if 'ー' not in dc[0]+dc[2]:
                tate_l.append('${}{}'.format(dc[0], dc[2]))
                tate_l.append('{}{}$'.format(dc[0], dc[2]))
                tate_l.append('{}{}'.format(dc[0], dc[2]))
            if 'ー' not in dc[1]:
                tate_r.append('{}$'.format(dc[1]))
        elif len(dc) == 4:  # 例：㌀
            yoko_t.append('${}{}'.format(dc[0], dc[1]))
            yoko_t.append('{}{}$'.format(dc[0], dc[1]))
            yoko_t.append('{}{}'.format(dc[0], dc[1]))
            yoko_b.append('${}{}'.format(dc[2], dc[3]))
            yoko_b.append('{}{}$'.format(dc[2], dc[3]))
            yoko_b.append('{}{}'.format(dc[2], dc[3]))
            if 'ー' not in dc[0]+dc[2]:
                tate_l.append('${}{}'.format(dc[0], dc[2]))
                tate_l.append('{}{}$'.format(dc[0], dc[2]))
                tate_l.append('{}{}'.format(dc[0], dc[2]))
            if 'ー' not in dc[1]+dc[3]:
                tate_r.append('${}{}'.format(dc[1], dc[3]))
                tate_r.append('{}{}$'.format(dc[1], dc[3]))
                tate_r.append('{}{}'.format(dc[1], dc[3]))
        else:
            print('{} is not usable. Ignoring'.format(km))
            continue

    return [yoko_t, yoko_b, tate_l, tate_r]

def gram_to_kumimoji(gram):
    # TODO
    return gram

def composable(word, grams, used, rest):
    if rest == '':
        components = [gram_to_kumimoji(g) for g in used]
        print('{} composable from {}'.format(word, components))
    if rest == False:
        rest = word
    if rest[0:4] in grams:
        used.append(rest[0:4])
        composable(word, grams, used, rest[4:])
    elif rest[0:3] in grams:
        used.append(rest[0:3])
        composable(word, grams, used, rest[3:])
    elif rest[0:2] in grams:
        used.append(rest[0:2])
        composable(word, grams, used, rest[2:])

spkm = get_square_pattern_kumimoji()
bags = build_marked_2gram_sets(spkm)

with open('kk_word_list_50k') as f:
    words = f.readlines()

words = [w.strip() for w in words if len(w.strip()) >= 3]
words = ['${}$'.format(w) for w in words]

for w in words:
    for bag in bags:
        composable(w, bag, [], False)
