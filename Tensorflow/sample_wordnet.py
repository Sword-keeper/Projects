from nltk.corpus import wordnet

# s-形容词-？
# a-形容词-？
# v-动词
# n-名词
# r-副词

if __name__ == '__main__':
    x = wordnet.synsets('seal')[1]
    print(x)
    y = wordnet.synsets('me')[-1]
    dis = x.shortest_path_distance(y)
    print(dis)