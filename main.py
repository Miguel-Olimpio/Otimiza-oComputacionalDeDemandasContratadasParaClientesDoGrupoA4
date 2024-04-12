import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import pyautogui
from PIL import Image

def read(icms,tarifa_i,demanda_inicial):

    data = pd.read_csv("tarifas.csv", sep=";", header=None, dtype='float')
    data1 = pd.read_csv("dados.csv", sep=" ", header=None)

    # icms = int(input("Qual a taxa de ICMS da instalação? \n -> 0 - s/ICMS \n -> 1 - 18% \n -> 2 - 25% \n --->" ))
    # tarifa_i = input("Qual a tarifa da instalação: \n Azul ou Verde? \n --->")


    dhfp = []
    dhp = []
    ehfp = []
    ehp = []
    Mes = []
    # demanda_inicial = []
    tarifa = {}

    # if tarifa_i=='verde':
    #     demanda_inicial.append(float(input("Qual a demanda única contratada Atualalmente? \n --->")))
    # elif tarifa_i=='azul':
    #     demanda_inicial.append(float(input("Qual a demanda HFP contratada Atualmente? \n --->")))
    #     demanda_inicial.append(float(input("Qual a demanda HP contratada Atualmente? \n  --->")))


    for i in range(1,13):

        dhfp.append(float(data1[2][13-i]))
        dhp.append(float(data1[1][13-i]))
        ehfp.append(float(data1[4][13-i])*1000)
        ehp.append(float(data1[3][13-i])*1000)
        Mes.append(data1[0][13-i])

    consumo =    {
                'demanda HFP': dhfp,
                'demanda HP': dhp, 
                'consumo HFP': ehfp,
                'consumo HP': ehp,    
                'mes' :  Mes                  
                }


    TA =    {
                'demanda HFP': float(data[icms][2]) ,
                'demanda HFP s/icms': float(data[0][2]),
                'demanda HFP ultrapassagem': float(data[icms][2])*2,
                'demanda HP': float(data[icms][1]),
                'demanda HP s/icms': float(data[0][1]),
                'demanda HP ultrapassagem':float(data[icms][1])*2 , 
                'consumo HFP': float(data[icms][4]),
                'consumo HP': float(data[icms][3])                       
            }

    TV =    {
                'demanda unica': data[icms][7],
                'demanda unica s/icms': data[0][7],
                'demanda unica ultrapassagem':data[icms][7]*2 ,
                'consumo HFP': data[icms][9],
                'consumo HP': data[icms][8]
            }
    
    tarifa.update({"Tarifa Azul":TA})
    tarifa.update({"Tarifa Verde":TV})    
    tarifa.update({"Tarifa Atual":tarifa_i})

    #______________________________________________________________________________________________________________________________________________
    # CRIAÇÃO DOS VETORES DE DEMANDAS PARA CALCULO DOS CUSTOS MINIMOS
    # demanda HFP: Vetor com registros entre os minimos valores registrados -10 e os máximos valores registrados +10 (MELHORAR ESSE +/- 10)
    # demanda HP: Vetor com registros entre os minimos valores registrados -10 e os máximos valores registrados +10  (MELHORAR ESSE +/- 10)
    # demanda atual HFP: Demanda atualmente contratada HFP, para utilizar em calculo de economia
    # demanda atual HP: Demanda atualmente contratada HFP, para utilizar em calculo de economia

    contratado = {'demanda HFP': np.arange(min(dhfp)-10,max(dhfp)+10,1,dtype='float'),
                  'demanda HP': np.arange(min(dhp)-10,max(dhp)+10,1,dtype='float'),
                  'demanda atual HFP/unica': demanda_inicial[0],
                  'demanda atual HP': demanda_inicial[1],}

    return consumo, tarifa, contratado


#_________________________________________________________________________________________________________________
# FUNÇÃO QUE CALCULA OS CUSTOS PARA TARIFA AZUL

def calc_azul(consumo, tarifa, contratado):

#_________________________________________________________________________________________________________________
# FUNÇÃO QUE CALCULA MÊS A MÊS AS DEMANDAS

    def calc_mes(consumo, tarifa, contratado):

        c = []
        cS = []
        cU = []
        custos = {}
        
        if(consumo <= 1.05*contratado):
            c.append(consumo*tarifa[0])
            if (contratado - consumo)>=0:
                cS.append((contratado - consumo)*tarifa[1])
            else:
                cS.append(0)
            cU.append(0)


        else:
            c.append(consumo*tarifa[0])
            cS.append(0)
            cU.append((consumo - contratado)*tarifa[2])

        custos={'Custo demanda':c[0],
                'Custo demanda s/ICMS':cS[0],
                'Custo demanda Ultrapassagem':cU[0],
                'Custo Total mensal':c[0]+cS[0]+cU[0]}  
        
        return custos

#_________________________________________________________________________________________________________________
# CALCULO DA DEMANDA HFP

    tarifa1 = []
    ano = []
    ano1 = []
    x =[]
    a = 0
    output = {}
    demanda = []
    custo = []
    
    tarifa1.append(tarifa['Tarifa Azul']['demanda HFP'])
    tarifa1.append(tarifa['Tarifa Azul']['demanda HFP s/icms'])
    tarifa1.append(tarifa['Tarifa Azul']['demanda HFP ultrapassagem'])

    

    for k in range(len(contratado['demanda HFP'])):
        mes = []
        mes1 = []
        for i in range(len(consumo['demanda HFP'])):
            mes.append(float(calc_mes(consumo['demanda HFP'][i],tarifa1,contratado['demanda HFP'][k])['Custo Total mensal']))
            mes1.append(calc_mes(consumo['demanda HFP'][i],tarifa1,contratado['demanda HFP'][k]))
        ano.append(sum(mes))
        ano1.append(mes1)
        demanda.append(contratado['demanda HFP'][k])
        custo.append(sum(mes))

    for i in range(len(consumo['demanda HFP'])):
                x.append(calc_mes(consumo['demanda HFP'][i],tarifa1,contratado['demanda atual HFP/unica']))

    a = ano.index(min(ano))
    output.update({'Anual Ótima HFP': ano1[a]})
    output.update({'Anual Atual HFP': x})
    output.update({'Demanda HFP Ótima': contratado['demanda HFP'][a]})
    output.update({'Demanda HFP':demanda})
    output.update({'Custo HFP':custo})
#_________________________________________________________________________________________________________________
# CALCULO DA DEMANDA HP

    tarifa1 = []
    ano = []
    ano1 = []
    x =[]
    a = 0
    demanda = []
    custo = []

    tarifa1.append(tarifa['Tarifa Azul']['demanda HP'])
    tarifa1.append(tarifa['Tarifa Azul']['demanda HP s/icms'])
    tarifa1.append(tarifa['Tarifa Azul']['demanda HP ultrapassagem'])

    

    for k in range(len(contratado['demanda HP'])):
        mes = []
        mes1 = []
        for i in range(len(consumo['demanda HP'])):
            mes.append(float(calc_mes(consumo['demanda HP'][i],tarifa1,contratado['demanda HP'][k])['Custo Total mensal']))
            mes1.append(calc_mes(consumo['demanda HP'][i],tarifa1,contratado['demanda HP'][k]))
        ano.append(sum(mes))
        ano1.append(mes1)
        demanda.append(contratado['demanda HP'][k])
        custo.append(sum(mes))

    for i in range(len(consumo['demanda HP'])):
        x.append(calc_mes(consumo['demanda HP'][i],tarifa1,contratado['demanda atual HP']))

    a = ano.index(min(ano))
    ano = []
    ano.append(ano1[a])
    ano.append(x)
    ano.append(contratado['demanda HP'][a])
    output.update({'Anual Ótima HP': ano1[a]})
    output.update({'Anual Atual HP': x})
    output.update({'Demanda HP Ótima': contratado['demanda HP'][a]})
    output.update({'Demanda HP':demanda})
    output.update({'Custo HP':custo})
    
    return output

icms = 1
tarifa_i = 'azul'
demanda_inicial = [145,145]

input = read(icms,tarifa_i,demanda_inicial)
print(input[1])
a = calc_azul(input[0],input[1],input[2])
print('A demanda ótima para o posto HP é de: ', a['Demanda HP Ótima'],' kW')
print('A demanda ótima para o posto HFP é de: ', a['Demanda HFP Ótima'], ' kW')

#Exemplo de Fator de Carga alto
import plotly.graph_objs as go

x       = []
y1      = [100,91,93,105,98,100,95,90,105,99,101,98]
y3 = []
y2 = 0
for i in range(len(y1)):
    y1.append(float(y1[i]))
    x.append(input[0]['mes'][i])
    y2 = y2 + float(y1[i])
for i in range(len(input[0]['demanda HFP'])):
    y3.append(y2/12)

FC = y3[0]/max(y1)
    
plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y3, name='Demanda Média               ', marker=dict(color='darkred')))
plot.add_trace(go.Bar(x=x, y=y1, name='Demandas Registradas', marker=dict(color='blue')))
plot.add_annotation(x=4, y=y2/12, text=str(f'Fator de Carga = {round(FC,4)}'), font=dict(size=20),
                   showarrow=True, arrowhead=5)
plot.update_layout(yaxis_range=[0,120], 
                   title='Demanda Média e Fator de Carga - Ex 1',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(font=dict(size=15)) 
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Demanda Média Ex 1.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()


#Exemplo de Fator de Carga Baixo
import plotly.graph_objs as go
x       = []
y1      = [52,45,47,42,45,50,79,102,100,99,72,61]
y3 = []
y2 = 0
for i in range(len(y1)):
    y1.append(float(y1[i]))
    x.append(input[0]['mes'][i])
    y2 = y2 + float(y1[i])
for i in range(len(input[0]['demanda HFP'])):
    y3.append(y2/12)

FC = y3[0]/max(y1)
    
plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y3, name='Demanda Média               ', marker=dict(color='darkred')))
plot.add_trace(go.Bar(x=x, y=y1, name='Demandas Registradas', marker=dict(color='blue')))
plot.add_annotation(x=3, y=y2/12, text=str(f'Fator de Carga = {round(FC,4)}'), font=dict(size=20),
                   showarrow=True, arrowhead=5)
plot.update_layout(yaxis_range=[0,120], 
                   title='Demanda Média e Fator de Carga - Ex 2',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(font=dict(size=15)) 
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Demanda Média Ex 2.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

plot = go.Figure()
plot.add_trace(go.Scatter(x=a['Demanda HFP'], y=a['Custo HFP'] ,mode='lines', name='Custo Variavél', marker=dict(color='green')))
plot.add_annotation(x=93, y=24113.23, text=str(f'Ponto ótimo = 93 kW'), font=dict(size=16),
                   showarrow=True, arrowhead=5)
plot.update_layout(title='Variação Custo x Demanda Contratada HFP',
                   yaxis_title='Custo (R$)',
                   xaxis_title='Demanda Contratada HFP (kW)',
                   yaxis=dict(tickmode='linear',dtick=2000))
plot.update_layout(font=dict(size=12))
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Custos HFP.png", format="png", scale=10, width=854, height=480)                    
plot.show()

plot = go.Figure()
plot.add_trace(go.Scatter(x=a['Demanda HP'], y=a['Custo HP'] ,mode='lines', name='Custo Variavél', marker=dict(color='blue')))
plot.add_annotation(x=82, y=67211.63, text=str(f'Ponto ótimo = 82 kW'), font=dict(size=16),
                   showarrow=True, arrowhead=5,ax=30)
plot.update_layout(title='Variação Custo x Demanda Contratada HP', 
                   yaxis_title='Custo (R$)',
                   xaxis_title='Demanda Contratada HP (kW)',
                   yaxis=dict(tickmode='linear',dtick=3000))
plot.update_layout(font=dict(size=12))
plot.update_layout(legend=dict(x=0.80, y=0.99, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Custos HP.png", format="png", scale=10, width=854, height=480)                    
plot.show()

#Fator de Carga HFP
x       = []
y1      = []
y3      = []
y2 = 0
for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(input[0]['demanda HFP'][i]))
    x.append(input[0]['mes'][i])
    y2 = y2 + float(input[0]['demanda HFP'][i])
for i in range(len(input[0]['demanda HFP'])):
    y3.append(y2/12)

FC = y3[0]/max(y1)
    
plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y3, name='Demanda Média               ', marker=dict(color='darkred')))
plot.add_trace(go.Bar(x=x, y=y1, name='Demandas Registradas HFP', marker=dict(color='blue')))
plot.add_annotation(x=4, y=y2/12, text=str(f'Fator de Carga = {round(FC,4)}'), font=dict(size=20),
                   showarrow=True, arrowhead=5)
plot.update_layout(yaxis_range=[0,120], 
                   title='Demanda Média e Fator de Carga - HFP',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(font=dict(size=15)) 
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Demanda Média HFP.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

#Fator de Carga HP

x       = []
y1      = []
y3      = []
y2 = 0
for i in range(len(input[0]['demanda HP'])):
    y1.append(float(input[0]['demanda HP'][i]))
    x.append(input[0]['mes'][i])
    y2 = y2 + float(input[0]['demanda HP'][i])
for i in range(len(input[0]['demanda HP'])):
    y3.append(y2/12)

FC = y3[0]/max(y1)
    
plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y3, name='Demanda Média               ', marker=dict(color='darkred')))
plot.add_trace(go.Bar(x=x, y=y1, name='Demandas Registradas HP', marker=dict(color='darkblue')))
plot.add_annotation(x=4, y=y2/12, text=str(f'Fator de Carga = {round(FC,4)}'), font=dict(size=20),
                   showarrow=True, arrowhead=5)
plot.update_layout(yaxis_range=[0,120], 
                   title='Demanda Média e Fator de Carga - HP',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(font=dict(size=15)) 
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Demanda Média HP.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

x       = []
y1      = []
y2      = []
y3      = []
y4      = []  


for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(input[2]['demanda atual HFP/unica']))
    y2.append(float(input[2]['demanda atual HP']))

for i in range(len(input[0]['demanda HFP'])):
    y3.append(float(input[0]['demanda HFP'][i]))
    x.append(input[0]['mes'][i])

for i in range(len(input[0]['demanda HP'])):
    y4.append(float(input[0]['demanda HP'][i]))


plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HFP      ', marker=dict(color='orange')))
plot.add_trace(go.Scatter(x=x, y=y2, name='Demanda Contratada HP', marker=dict(color='red')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HFP', marker=dict(color='blue')))
plot.add_trace(go.Bar(x=x, y=y4, name='Demandas Registradas HP', marker=dict(color='darkblue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas e Contratadas - Atual',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15)) 
plot.write_image("Demandas Atualmente.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

x       = []
y1      = []
y3      = []

for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(input[2]['demanda atual HFP/unica']))

for i in range(len(input[0]['demanda HFP'])):
    y3.append(float(input[0]['demanda HFP'][i]))
    x.append(input[0]['mes'][i])

plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HFP      ', marker=dict(color='orange')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HFP', marker=dict(color='blue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas HFP - Atualmente',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15)) 
plot.write_image("Demandas HFP - Atualmente.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

x       = []
y1      = []
y3      = []

for i in range(len(input[0]['demanda HP'])):
    y1.append(float(input[2]['demanda atual HP']))

for i in range(len(input[0]['demanda HP'])):
    y3.append(float(input[0]['demanda HP'][i]))
    x.append(input[0]['mes'][i])

plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HP      ', marker=dict(color='red')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HP', marker=dict(color='darkblue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas HP - Atualmente',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15))
plot.write_image("Demandas HP - Atualmente.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

x       = []
y1      = []
y2      = []
y3      = []
y4      = []  


for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(a['Demanda HFP Ótima']))
    y2.append(float(a['Demanda HP Ótima']))

for i in range(len(input[0]['demanda HFP'])):
    y3.append(float(input[0]['demanda HFP'][i]))
    x.append(input[0]['mes'][i])

for i in range(len(input[0]['demanda HP'])):
    y4.append(float(input[0]['demanda HP'][i]))


plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HFP      ', marker=dict(color='orange')))
plot.add_trace(go.Scatter(x=x, y=y2, name='Demanda Contratada HP', marker=dict(color='red')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HFP', marker=dict(color='blue')))
plot.add_trace(go.Bar(x=x, y=y4, name='Demandas Registradass HP', marker=dict(color='darkblue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas e Contratadas - Otimizadas',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15))
plot.write_image("Demandas Otimizadas.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

x       = []
y1      = []
y3      = []

for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(a['Demanda HFP Ótima']))

for i in range(len(input[0]['demanda HFP'])):
    y3.append(float(input[0]['demanda HFP'][i]))
    x.append(input[0]['mes'][i])

plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HFP      ', marker=dict(color='orange')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HFP', marker=dict(color='blue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas HFP - Após Otimização',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15))
plot.write_image("Demandas HFP - Otimizadas.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()


x       = []
y1      = []
y3      = []

for i in range(len(input[0]['demanda HFP'])):
    y1.append(float(a['Demanda HP Ótima']))

for i in range(len(input[0]['demanda HP'])):
    y3.append(float(input[0]['demanda HP'][i]))
    x.append(input[0]['mes'][i])

plot = go.Figure()
plot.add_trace(go.Scatter(x=x, y=y1, name='Demanda Contratada HP      ', marker=dict(color='red')))
plot.add_trace(go.Bar(x=x, y=y3, name='Demandas Registradas HP', marker=dict(color='darkblue')))
plot.update_layout(yaxis_range=[0,160], 
                   title='Demandas Registradas HP - Após Otimização',
                   yaxis_title='Demanda (kW)',
                   xaxis_title='Tempo (Meses)')
plot.update_layout(legend=dict(x=0.01, y=0.01, bgcolor='rgba(255, 255, 255,0.95)'))
plot.update_layout(font=dict(size=15)) 
plot.write_image("Demandas HP - Otimizadas.jpg", format="jpg", scale=10, width=854, height=480)

plot.show()

df = pd.DataFrame(a['Anual Atual HFP'], index=input[0]['mes'])
df.loc['TOTAL'] = df.sum()
df.style.highlight_max(subset=['Custo Total mensal'], props='background-color: red; color: white'
       ).set_caption('Custo Atual: Demanda HFP'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: red; color: white'
       ).set_table_styles([{ 'selector':'caption',
           'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })

df1 = pd.DataFrame(a['Anual Ótima HFP'], index=input[0]['mes'])
df1.loc['TOTAL'] = df1.sum()
df1.style.highlight_max(subset=['Custo Total mensal'], props='background-color: green; color: white'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: blue; color: white'
       ).set_caption('Custo Ótimo: Demanda HFP'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })

df2 = pd.DataFrame(a['Anual Atual HP'], index=input[0]['mes'])
df2.loc['TOTAL'] = df2.sum()
df2.style.highlight_max(subset=['Custo Total mensal'], props='background-color: red; color: white'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: red; color: white'
       ).set_caption('Custo Atual: Demanda HP'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })
df3 = pd.DataFrame(a['Anual Ótima HP'], index=input[0]['mes'])
df3.loc['TOTAL'] = df3.sum()
df3.style.highlight_max(subset=['Custo Total mensal'], props='background-color: green; color: white'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: blue; color: white'
       ).set_caption('Custo Ótimo: Demanda HP'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })
df_soma_atual = df + df2
df_soma_atual.style.highlight_max(subset=['Custo Total mensal'], props='background-color: red; color: white'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: red; color: white'
       ).set_caption('Custo Atual Total: Demandas HFP e HP'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })
df_soma_otimo = df1 + df3
df = df_soma_otimo.style.highlight_max(subset=['Custo Total mensal'], props='background-color: green; color: white'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: blue; color: white'
       ).set_caption('Custo Ótimo Total: Demandas HFP e HP'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })
df

df = df.style.highlight_max(subset=['Custo Total mensal'], props='background-color: green; color: white; font-size: 14px; font-weight: bold'
       ).highlight_max(subset=['Custo demanda s/ICMS'], props='background-color: blue; color: white'
       ).highlight_min(subset=['Custo demanda Ultrapassagem'], props='background-color: red; color: white'
       ).set_caption('Economia Anual'
       ).set_table_styles([{ 'selector':'caption',
            'props':'font-size: 20px; font-weight: bold; text-align: center; color: black;font-style: italic'}]
       ).format({'Custo demanda':'{:.2f}', 'Custo demanda s/ICMS':'{:.2f}', 'Custo demanda Ultrapassagem':'{:.2f}', 'Custo Total mensal':'{:.2f}' })
df
#fig = df.to_latex()
#print(fig)

atual = df_soma_atual.iloc[12,3]
novo = df_soma_otimo.iloc[12,3]
economia = atual - novo 
economiap = economia/atual

print(f"A economia gerada atráves da otimização das demandas é de R$ {economia:.2f}")
print(f"Esta economia corresponde a um total de {economiap*100:.2f}% sobre o montante das demandas!")

plot = go.Figure()
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_atual.iloc[:,0], name='Custo demanda', marker=dict(color='blue')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_atual.iloc[:,1], name='Custo demanda s/ICMS', marker=dict(color='red')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_atual.iloc[:,2], name='Custo demanda Ultrapassagem', marker=dict(color='orange')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_atual.iloc[:,3], name='Custo Total mensal', marker=dict(color='gray')))
plot.update_layout(yaxis_range=[0,17000], 
                  title='Custos Anuais - Cenário Atual',
                   yaxis_title='Custo (R$)',
                   xaxis_title='Tempo (Meses)',
                   yaxis=dict(tickmode='linear',dtick=2000))
plot.update_layout(font=dict(size=12)) 
plot.update_layout(legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Custos Anuais - Cenário Atual.jpg", format="jpg", scale=10, width=854, height=480)



                    
plot.show()

plot = go.Figure()
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_otimo.iloc[:,0], name='Custo demanda', marker=dict(color='blue')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_otimo.iloc[:,1], name='Custo demanda s/ICMS', marker=dict(color='red')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_otimo.iloc[:,2], name='Custo demanda Ultrapassagem', marker=dict(color='orange')))
plot.add_trace(go.Bar(x=input[0]['mes'], y=df_soma_otimo.iloc[:,3], name='Custo Total mensal', marker=dict(color='gray')))
plot.update_layout(yaxis_range=[0,17000], 
                   title='Custos Anuais - Cenário Otimizado',
                   yaxis_title='Custo (R$)',
                   xaxis_title='Tempo (Meses)',
                   yaxis=dict(tickmode='linear',dtick=2000))
plot.update_layout(font=dict(size=12)) 
plot.update_layout(legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255,0.95)'))
plot.write_image("Custos Anuais - Cenário Otimizado.jpg", format="jpg", scale=10, width=854, height=480)
                    
plot.show()

# Salvar o dataframe estilizado em um arquivo HTML temporário
temp_file = 'temp.html'
df.to_html(temp_file)