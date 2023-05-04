import PyPDF2
import openai
from time import sleep
import os

pdf_file = open('EDITAL.pdf', 'rb') # Load PDF file

pdf_reader = PyPDF2.PdfReader(pdf_file) # Read PDf file

texto_inicio = '14.2.1.1 CONHECIMENTOS BÁSICOS'
texto_fim = 'MapReduce.'

# looking for the PDF pages between first and last page (in_page and out_page)

in_page =0
out_page =0
for idx in range(len(pdf_reader.pages)):
    pagina = pdf_reader.pages[idx]
    if texto_inicio in pagina.extract_text():
        in_page = idx
        print('Página_inicial=', idx)
    if texto_fim in pagina.extract_text():
        out_page = idx
        print('Pagina_Final=', idx)

texto=''
for paginas in range(in_page, out_page+1):
    pagina = pdf_reader.pages[paginas]
    texto += pagina.extract_text()

pdf_file.close()

print(texto)
print()
print(type(texto))

# I make use of split function to separate the pages which I desire

divisor = '71 e 72.'

texto1 = texto.split(divisor)[1]
texto2 = texto1.split('MARCELO BATISTA DE NORONHA')[0]
print(texto2)

texto3 = texto2.split('. ')
print()
print(texto3)

for i in range(len(texto3)):
    print(texto3[i])
    print()


openai.api_key = os.environ["OPENAI_API_KEY"] # Personal openAI key.
#openai.api_key = chave

def perguntar_ao_GPT(pergunta):
    Completions = openai.Completion.create(
        engine='text-davinci-002',
        prompt=f'Ola ChatGPT, eu estou fazendo uma pesquisa acâdemica e preciso do máximo de informações sobre o assunto abaixo:\n{pergunta}. Os números não são importantes',
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.95,
    )
    message = Completions.choices[0].text # get the first word present in the set of texts. According with "n"

    return message.strip()

lista_perguntas = texto3


Questions, Awsers = [], []
for pergunta in lista_perguntas:
    resposta = perguntar_ao_GPT(pergunta)
    Questions.append(pergunta)
    Awsers.append(resposta)
    sleep(2)

    print(f"Pergunta: {pergunta}\nResposta: {resposta}\n")
