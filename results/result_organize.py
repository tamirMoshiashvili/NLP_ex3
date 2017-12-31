def get_dict_for(filename):
    d = dict()
    key = None
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if ':' in line:
                key = line.split(':')[0]
                d[key] = []
            elif line:
                d[key].append(line.strip())
    return d


if __name__ == '__main__':
    d1 = get_dict_for('word2vec_bow5.txt')
    d2 = get_dict_for('word2vec_deps.txt')
    ds = [d1, d2]

    output_file = open('word2vec_most_common.csv', 'w')
    for key in d1:
        # sort lists of each key
        for d in ds:
            d[key].sort()

        output_file.write(key + '\n')
        for a, b in zip(d1[key], d2[key]):
            output_file.write(',' + a + ',' + b + '\n')

    output_file.close()
