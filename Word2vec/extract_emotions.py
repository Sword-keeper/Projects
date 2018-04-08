import gensim
from Word2vec.word2Vec_sample import get_inference

sentences = ['im so heartbreaking today.', 'wow! proud of you!', 'this guy is noisy, plz just shutup and go to hell.']
emotions = ['sad', 'happy', 'angry', 'fear', 'disgust', 'surprise']

if __name__ == '__main__':

    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)

    emo_dir = {}
    for em in emotions:
        sim = model.most_similar(positive=em, topn=30)
        extra = []
        for base in sim:
            extra.extend(model.most_similar(positive=base[0], topn=30))
        extra.extend(sim)
        emo_dir[em] = [pair[0] for pair in extra]
        print(emo_dir[em])

    for sentence in sentences:
        print(sentence)
        words = sentence.replace(',','').replace('.', '').replace('!', '').split(' ')
        print(words)
        for word in words:
            found = False
            for em in emotions:
                if word in emo_dir[em]:
                    print(f"'{word}':{em}")
                    found = True
            if not found:
                print(f"'{word}:0'")
