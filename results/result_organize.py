
DELIM = '='
def get_dict_for(filename):
    d = dict()
    key = None
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if DELIM in line:
                key = line.split(DELIM)[0]
                d[key] = []
            elif line:
                d[key].append(line.strip())
    return d

#FILE_NAME = "first_order_for_part"
FILE_NAME = "features_word2vec_"
#RESULT_NAME = "first_order"
RESULT_NAME = "features_word2vec"
if __name__ == '__main__':
    partial_name = '../features/'+ FILE_NAME
    ending = '.txt'
    #d1 = get_dict_for(partial_name + '1' + ending)
    d1 = get_dict_for(partial_name + 'bow5' + ending)
    #d2 = get_dict_for(partial_name + '2' + ending)
    d2 = get_dict_for(partial_name + 'deps' + ending)
    #d3 = get_dict_for(partial_name + '3' + ending)
    ds = [d1, d2]
    #ds = [d1, d2, d3]

    output_file = open('../features/most_common_'+ RESULT_NAME +'.csv', 'w')
    for key in d1:
        # sort lists of each key
        for d in ds:
            d[key].sort()

        output_file.write(key + ',bow5 ,deps\n')
        #for a, b, c in zip(d1[key], d2[key], d3[key]):
        #    output_file.write(',' + a + ',' + b + ',' + c + '\n')
        for a, b in zip(d1[key], d2[key]):
            output_file.write(',' + a + ',' + b  + '\n')
        output_file.write("\n")
    output_file.close()
