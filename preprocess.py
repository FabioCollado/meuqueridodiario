import re

def remove_dash_n(text):
    return text.replace('/n', ' ')

def remove_spaces(text):
    return re.sub(r"\s+", " ", text).strip()

def remove_lots_of_points(text):
    return re.sub('\.{2,}', ' ', text)

def remove_bad_chars(text):
    return re.sub('[˜˚˝˙ˆˇ˚˘˘Œ˛œ_%ﬁﬂ‡š<>›„’]', ' ', text)

def remove_numbers(text):
    text = re.sub('[\(\)\[\]\{\}]', ' ', text)
    text = re.sub('[ \.,]((um|dois|três|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|quatorze|quinze|dezesseis|dezessete|dezoito|desenove|vinte|trinta|quarenta|cinquenta|cincoenta|cinqüenta|sessenta|oitenta|noventa|cem|duzentos|trezentos|quatrocentos|quinhentos|seiscentos|setecentos|oitocentos|novecentos|mil|milhão|bilhão|trilhão)[e \.,]*)+(?<=[ \.,])', ' 1', text)
    text = re.sub('\(?R *\$ *[0-9\.,]*\)?', ' valores ', text, flags=re.IGNORECASE)
    
    text = re.sub('[Nn§]? *[§º°]?\.? *[0-9]+([nN§º°\-0-9\.\,\/\\ ]|página)*[º°]?', ' número ', text)
    text = re.sub('[ \.,]( |,|e|número|reais|centavos|valores)*(reais|centavos)( |,|e|número|reais|centavos|valores)*[ \.,]', ' valores ', text)
    #Esse está removendo ponto final após o número. Seria bom que não removesse. Mas preciso remover no meio.
    text = re.sub('[ \.,](dias|número|e| )* *(dias)? *(d[oe])? *(mês)? *(de)? *(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) *(do)? *(ano)? *(de)? *(número)?', ' data ', text)
    text = re.sub('[ ,.](?=[CLXVI])(C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})[ ,.]', 
                  ' número romano ', text)
    text = re.sub('[ ,.](?=[clxvi])(c{0,3})(x[cl]|l?x{0,3})(i[xv]|v?i{0,3})[ ,.]', 
                  ' número romano ', text)
    text = re.sub('(http)[:\/w]*\.', 'http ', text, flags=re.IGNORECASE)
    text = re.sub('(\.com)(\.br)?', ' com ', text, flags=re.IGNORECASE)
    text = re.sub('[ \.](número) *(h|horas)( |,|número|minutos|m|min)*[ \.]', ' horas ', text, flags=re.IGNORECASE)
    
    #text = BeautifulSoup(text, 'html.parser').text
    return text

def spaced_letters(text):
    text = text.replace('A P O S E N T A R', ' aposentar ')
    return text

def join_words(text):
    # Há muitas palavras assim: "res - ponsável"
    # Vou ter algum problema juntando coisa que não devia
    # Espero que nesses casos o tokenizer resolva
    return re.sub(' - ?', '', text)

def separate_words(text):
    # Há muitas palavras assim: "FerrazPresidente" "FerrazAPresidente"
    # Vou supor que sempre que houver uma letra minúscula seguida de maiúscula é para separar
    text = re.sub('(?<=[a-záàâãéêíóôõú])(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚ])', ' ', text)
    text = re.sub('(?<=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ])(?=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ][a-záàâãéêíóôõú])', ' ', text)
    return text
def dots_that_mess_segmentation(text):
    text = re.sub('sec\.', 'Sec ', text, flags=re.IGNORECASE)
    text = re.sub('av\.', 'Avenida ', text, flags=re.IGNORECASE)
    text = re.sub('min\.', 'Ministro ', text, flags=re.IGNORECASE)
    text = re.sub('exmo\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('dr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sra\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('proc\.', ' processo ', text, flags=re.IGNORECASE)
    text = re.sub('reg\.', ' registro ', text, flags=re.IGNORECASE)
    text = re.sub('func\.', ' funcionário ', text, flags=re.IGNORECASE)
    text = re.sub('art\.', ' artigo ', text, flags=re.IGNORECASE)
    text = re.sub('inc\.', ' inciso ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=[ \.][A-Z])\.', ' ', text)
    text = re.sub('(?<=comp)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=insc)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('p[áa]g[\. ]', ' página ', text, flags=re.IGNORECASE) #Pág. N 5
    text = re.sub('\. *(n|n[uú]mero)[ \.°º]+', ' número ', text, flags=re.IGNORECASE) #. N°
    
    return text

def preprocess(text):
    text = remove_dash_n(text)
    #text = remove_breaks(text)
    text = remove_lots_of_points(text)
    #text = remove_duplicate_punctuation(text) #Está removendo o segundo parênteses
    text = remove_bad_chars(text)
    
    text = spaced_letters(text)
    text = dots_that_mess_segmentation(text)
    text = remove_spaces(text)
    text = join_words(text)
    text = separate_words(text)
    return text

def replaces(text):
    #tokenizador separa essas palavras em 3 tokens
    text = re.sub('teresina', 'cidade', text) 
    text = re.sub('piauí', 'estado', text)
    text = re.sub('c/c', 'concomitante', text)
    return text

def preprocess2(text):
    text = text.lower()
    text = remove_numbers(text)
    text = replaces(text)
    return text

def break_paragraphs(text: str):
    paragraphs = re.split('(?<=\.) *(?=[A-Z])', preprocess(page))
    #return [p.lower() for p in paragraphs]
    return paragraphs