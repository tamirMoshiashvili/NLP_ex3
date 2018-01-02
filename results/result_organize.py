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
    partial_name = '../features/features_part'
    ending = '.txt'
    d1 = get_dict_for(partial_name + '1' + ending)
    d2 = get_dict_for(partial_name + '2' + ending)
    d3 = get_dict_for(partial_name + '3' + ending)
    ds = [d1, d2, d3]

    output_file = open('../features/most_common_features.csv', 'w')
    for key in d1:
        # sort lists of each key
        for d in ds:
            d[key].sort()

        output_file.write(key + '\n')
        for a, b, c in zip(d1[key], d2[key], d3[key]):
            output_file.write(',' + a + ',' + b + ',' + c + '\n')

    output_file.close()
