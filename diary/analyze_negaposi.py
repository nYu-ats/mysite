import MeCab
from diary.models import WordDict

def parse(sample_file):
    EOS_DIC=['。','.','!','?','!?','？','！']
    Reverse=['しかし','しかしながら','だけど','けれども','でも','それでも',
            'だが','が']
    temp=[]
    sentence=[]
    basic_node=[]
    score_list=[]
    score=0
    deno=0

    sample_file+= '。'

    for w in sample_file:
        if (w != '\n') or (w != ' '):
            temp.append(w)
        if w in EOS_DIC:
            a=''.join(temp)
            sentence.append(a)
            temp=[]

    tagger = MeCab.Tagger()
    tagger.parse('')
    for o in sentence:
        node = tagger.parseToNode(o)
        while node:
            word_parse = node.feature.split(',')
            if word_parse[6] != '*':
                basic_node.append(word_parse[6])
            node=node.next
        for s in basic_node:
            word_obj=WordDict.objects.filter(word=s).values_list('negaposi')
            word_obj=list(word_obj)
            try:
                score+=word_obj[0][0]
                deno+=1
            except IndexError:
                pass

        try:
            score/=deno
        except ZeroDivisionError:
            pass

        if basic_node[0] in Reverse:
            score*=1.2
        score_list.append(score)
        score=0
        deno=0
        basic_node=[]

    fin_score=sum(score_list)/len(score_list)
    fin_score=fin_score*50
    posi=round(fin_score)+50
    if posi > 100:
        posi=100
    elif posi <0 :
        posi=0
    nega=100-posi
    return posi,nega
