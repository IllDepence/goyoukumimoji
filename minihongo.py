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

def fill_gram_set(aset, gram, km):
    aset['list'].append(gram)
    aset['map'][gram] = km
    return aset

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

    yoko_t = {'label':'横書き１行目','list':[], 'map':{}}
    yoko_b = {'label':'横書き２行目','list':[], 'map':{}}
    tate_l = {'label':'縦書き２列目','list':[], 'map':{}}
    tate_r = {'label':'縦書き１列目','list':[], 'map':{}}
    for km in spkm:
        dc = decomp(km)
        if len(dc) == 2:    # 例：㌔
            if dc[0] == 'ほ':
                dc = ['ホ','カ']
            yoko_t = fill_gram_set(yoko_t, '{}$'.format(dc[0]), km)
            yoko_b = fill_gram_set(yoko_b, '${}'.format(dc[1]), km)
            if 'ー' not in dc[0]:
                tate_l = fill_gram_set(tate_l, '{}$'.format(dc[0]), km)
            if 'ー' not in dc[1]:
                tate_r = fill_gram_set(tate_r, '${}'.format(dc[1]), km)
        elif len(dc) == 3:  # 例：㌵
            yoko_t = fill_gram_set(yoko_t, '${}{}'.format(dc[0], dc[1]), km)
            yoko_t = fill_gram_set(yoko_t, '{}{}$'.format(dc[0], dc[1]), km)
            yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
            yoko_b = fill_gram_set(yoko_b, '{}$'.format(dc[2]), km)
            if 'ー' not in dc[0]+dc[2]:
                tate_l = fill_gram_set(tate_l, '${}{}'.format(dc[0], dc[2]), km)
                tate_l = fill_gram_set(tate_l, '{}{}$'.format(dc[0], dc[2]), km)
                tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
            if 'ー' not in dc[1]:
                tate_r = fill_gram_set(tate_r, '{}$'.format(dc[1]), km)
        elif len(dc) == 4:  # 例：㌀
            yoko_t = fill_gram_set(yoko_t, '${}{}'.format(dc[0], dc[1]), km)
            yoko_t = fill_gram_set(yoko_t, '{}{}$'.format(dc[0], dc[1]), km)
            yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
            yoko_b = fill_gram_set(yoko_b, '${}{}'.format(dc[2], dc[3]), km)
            yoko_b = fill_gram_set(yoko_b, '{}{}$'.format(dc[2], dc[3]), km)
            yoko_b = fill_gram_set(yoko_b, '{}{}'.format(dc[2], dc[3]), km)
            if 'ー' not in dc[0]+dc[2]:
                tate_l = fill_gram_set(tate_l, '${}{}'.format(dc[0], dc[2]), km)
                tate_l = fill_gram_set(tate_l, '{}{}$'.format(dc[0], dc[2]), km)
                tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
            if 'ー' not in dc[1]+dc[3]:
                tate_r = fill_gram_set(tate_r, '${}{}'.format(dc[1], dc[3]), km)
                tate_r = fill_gram_set(tate_r, '{}{}$'.format(dc[1], dc[3]), km)
                tate_r = fill_gram_set(tate_r, '{}{}'.format(dc[1], dc[3]), km)
        else:
            print('{} is not usable. Ignoring'.format(km))
            continue

    return [yoko_t, yoko_b, tate_l, tate_r]

def composable(word_kat, word_norm, grams, used, rest):
    if rest == '':
        components = [grams['map'][g] for g in used]
        #components = [g for g in used]
        print('{} composable as: {}'.format(word_norm, ''.join(components)))
    if rest == False:
        rest = word_kat
    if rest[0:4] in grams['list']:
        used.append(rest[0:4])
        composable(word_kat, word_norm, grams, used, rest[4:])
    elif rest[0:3] in grams['list']:
        used.append(rest[0:3])
        composable(word_kat, word_norm, grams, used, rest[3:])
    elif rest[0:2] in grams['list']:
        used.append(rest[0:2])
        composable(word_kat, word_norm, grams, used, rest[2:])

spkm = get_square_pattern_kumimoji()
sets = build_marked_2gram_sets(spkm)

with open('wikipedia-frequency-list-japanese-41k-both.tsv') as f:
    words = f.readlines()

# words = [w.strip() for w in words if len(w.strip()) >= 3]
words = [w.strip() for w in words if len(w.strip())]

for aset in sets:
    print('- - - - - - - - - - - - - - - - - - -')
    print('- - - - - - -{}- - - - - - -'.format(aset['label']))
    print('- - - - - - - - - - - - - - - - - - -')
    for w in words:
        parts = w.split('\t')
        if len(parts) == 2:
            kat = parts[0]
            norm = parts[1]
        else:
            kat = parts[0]
            norm = parts[0]
        kat = '${}$'.format(kat)
        composable(kat, norm, aset, [], False)
