import gensim

# [('queen', 0.6892049908638), ('monarch', 0.6506222486495972), ('prince', 0.6396005749702454), ('kings',
# 0.6317541599273682), ('princess', 0.609298050403595)] [('man', 0.6628609299659729), ('queen', 0.643856406211853),
# ('girl', 0.6136074662208557), ('princess', 0.6087510585784912), ('monarch', 0.5900577306747437)] [('man',
# 0.6628609299659729), ('queen', 0.643856406211853), ('girl', 0.6136074662208557), ('princess', 0.6087510585784912),
# ('monarch', 0.5900577306747437)]

emotions = ['disgust', 'happy', 'sad', 'angry', 'fear', 'surprise']


def get_inference(origin_pool, model):
    avg_score = sum([y for (x, y) in origin_pool]) / len(origin_pool)
    infer_pool = model.most_similar(positive=origin_pool, topn=5)
    infer_pool = [(x, y * avg_score) for (x, y) in infer_pool if y > 0.7]
    return infer_pool + origin_pool


def get_emotion_distribution(origin_pool):
    ret = {}
    total = 0
    for item in origin_pool:
        for emotion in emotions:
            score = model.wmdistance(item, emotion)
            score = 1 / score
            total += score
            if emotion in ret:
                ret[emotion] += score
            else:
                ret[emotion] = score
    for item in ret:
        ret[item] /= total
    return ret


if __name__ == '__main__':
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)
    # model = gensim.models.Word2Vec.load('data/model/word2vec_gensim')

    # pool = [('tree', 1)]
    # infer = get_inference(pool,model)
    # # infer = pool
    # print(infer)
    # res = get_emotion_distribution(infer)
    # print(res)

    # res = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=5)
    # print(res)

    # res = model.most_similar(positive=['cake', 'birthday', 'balloon'], topn=15)
    # print(res)

    # res = model.most_similar(positive=['thug', 'life'], topn=15)
    # for r in res:
    #     print(r)

    # res = model.most_similar(positive=['fuck', 'you'], topn=15)
    # print(res)

    # res = model.most_similar(positive=['pumpkin', 'lantern'], topn=15)
    # print(res)

    # res = model.most_similar(positive=['better','bad'], negative=['good'], topn=15)
    # for r in res:
    #     print(r)

    # res = model.most_similar_cosmul('halloween')
    # print(res)

    # res = model.most_similar(positive=['nekopara'], topn=150)
    # print(res)

    res = model.doesnt_match(['gun', 'war', 'cake', 'death'])

    # res = [x[0] for x in res]
    # res = model.doesnt_match(res)
    print(res)
