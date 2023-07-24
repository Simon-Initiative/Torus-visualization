# coding: utf8
import pandas
import csv
import json
from pandas import json_normalize
import matplotlib.pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
import matplotlib.gridspec as gridspec
import io
import base64
from PIL import Image, ImageDraw

#fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))


#reading the files in DataFrame(df)
#df1 = pandas.read_csv("by_activity.csv")
df2 = pandas.read_csv("raw_analytics.csv")
df2 = df2.join(df2['Student Response'].apply(json.loads).apply(pandas.Series))
df3 = df2.join(df2['Activity Content'].apply(json.loads).apply(pandas.Series))
df_mcq = df3[df3['Activity Type'] == "Multiple Choice"]
df_single_response = df3[df3['Activity Type'] == "Single Response"]
df_cata = df3[df3['Activity Type'] == "Check All That Apply"]
df_mcq = df_mcq.sort_values(by=['Activity ID','Student Response'])
df_single_response = df_single_response.sort_values(by = ['Activity ID'])
df_cata = df_cata.sort_values(by = ['Activity ID'])
dict_of_mcqs = {k: v for k, v in df_mcq.groupby('Activity ID')}
pdf = FPDF()
pdf = FPDF(orientation="landscape")
pdf.add_font('Arial', '', 'C:/Windows/fonts/arial.ttf', uni=True)  # added line
#pdf.add_font("Arial", "", "./fonts/arial.ttf", uni=True)
#pdf.set_doc_option('core_fonts_encoding', 'utf-8')#
#temp_mcq['choice_a'] = pandas.Series(list_of_choices_a, index=temp_mcq.index)
#temp_mcq['choice_b'] = pandas.Series(list_of_choices_b, index=temp_mcq.index)
#temp_mcq['choice_c'] = pandas.Series(list_of_choices_c, index=temp_mcq.index)
#temp_mcq['choice_d'] = pandas.Series(list_of_choices_d, index=temp_mcq.index)
pdf.add_page()
pdf.set_font('Arial', size = 30)
pdf.multi_cell(200,10,'LearnLab Summer School' + '\n\n\n', align = 'C')
pdf.multi_cell(200, 10, '\n'+'Analyzing OLI Data' + '\n', align = 'C')
pdf.add_page()
pdf.set_font('Arial', size = 30)
pdf.multi_cell(200,10,'Item Analysis (MCQs)' + '\n\n\n', align = 'C')
#Step 1: mcq conversion to visualizations
#finding the number of students who attempted each choice in the mcq dataframe and then adding those results to a plot

# Initialize empty lists for choice ids
list_of_choices_a_id = []
list_of_choices_b_id = []
list_of_choices_c_id = []
list_of_choices_d_id = []
list_of_questions = []
list_of_choices_a = []
list_of_choices_b = []
list_of_choices_c = []
list_of_choices_d = []

for i in dict_of_mcqs:
    dict_of_mcqs[i].to_csv("All_mcqs" + str(i) + ".csv", index = False)
    temp_mcq = dict_of_mcqs[i]
    list_of_choices_a_id = []
    list_of_choices_b_id = []
    list_of_choices_c_id = []
    list_of_choices_d_id = []
    list_of_choices_a = []
    list_of_choices_b = []
    list_of_choices_c = []
    list_of_choices_d = []
    list_of_questions = [] 
    temp_mcq['question'] = ''
    for y in temp_mcq.index:
        problem = temp_mcq.loc[y,"authoring"]["previewText"]
        temp_mcq.loc[y, 'question'] = problem
        list_of_questions.append(problem)
        #list_of_questions.insert(y, problem)
        #print(temp_mcq.loc[y, "choices"])
        
        if isinstance(temp_mcq.loc[y, "choices"][0]['content'], dict):
            choice_a_id = temp_mcq.loc[y, "choices"][0]['id']
            choice_a = temp_mcq.loc[y, "choices"][0]['content']['model'][0]['children'][0]['text']
        else:
            choice_a_id = temp_mcq.loc[y, "choices"][0]['id']
            choice_a = temp_mcq.loc[y, "choices"][0]['content'][0]['children'][0]['text']

        #print (choice_a)
    
        if isinstance(temp_mcq.loc[y, "choices"][1]['content'], dict):
            choice_b_id = temp_mcq.loc[y, "choices"][1]['id']
            choice_b = temp_mcq.loc[y, "choices"][1]['content']['model'][0]['children'][0]['text']
        else:
            choice_b_id = temp_mcq.loc[y, "choices"][1]['id']
            choice_b = temp_mcq.loc[y, "choices"][1]['content'][0]['children'][0]['text']
        #print (choice_b)
    
        if len(temp_mcq.loc[y, "choices"]) > 2:
            if isinstance(temp_mcq.loc[y, "choices"][2]['content'], dict):
                choice_c_id = temp_mcq.loc[y, "choices"][2]['id']
                choice_c = temp_mcq.loc[y, "choices"][2]['content']['model'][0]['children'][0]['text']
            else:
                choice_c_id = temp_mcq.loc[y, "choices"][2]['id']
                choice_c = temp_mcq.loc[y, "choices"][2]['content'][0]['children'][0]['text']
        #print (choice_c)
        
        if len(temp_mcq.loc[y, "choices"]) > 3:
            if isinstance(temp_mcq.loc[y, "choices"][3]['content'], dict):
                choice_d_id = temp_mcq.loc[y, "choices"][3]['id']
                choice_d = temp_mcq.loc[y, "choices"][3]['content']['model'][0]['children'][0]['text']
            else:
                choice_d = temp_mcq.loc[y, "choices"][3]['content'][0]['children'][0]['text']
                choice_d_id = temp_mcq.loc[y, "choices"][3]['id']
            #print (choice_d)

    
        else:
            choice_d = "not present"
            choice_d_id = ""
    else:
        choice_c = "not present"
        choice_c_id = ""
        choice_d = "not present"
        choice_d_id = ""
    
        #list_of_choice_a_id.append(y, choice_a_id)
        #list_of_choice_b_id.append(y, choice_b_id)
        #list_of_choice_c_id.append(y, choice_c_id)
        #list_of_choice_d_id.append(y, choice_d_id)
        #list_of_choices_a.append(y, choice_a)
        #list_of_choices_b.append(y, choice_b)
        #list_of_choices_c.append(y, choice_c)
        #   list_of_choices_d.append(y, choice_d)
        #list_of_choices_a_id.insert(y, choice_a_id)
        #list_of_choices_b_id.insert(y, choice_b_id)
        #list_of_choices_c_id.insert(y, choice_c_id)
        #list_of_choices_d_id.insert(y, choice_d_id)
        #list_of_choices_a.insert(y, choice_a_id)
        #list_of_choices_b.insert(y, choice_b_id)
        #list_of_choices_c.insert(y, choice_c_id)
        #list_of_choices_d.insert(y, choice_d_id)
        
    
    temp_mcq['choice_a_id'] = temp_mcq['choices'].apply(lambda choices: choices[0]['id'] if len(choices) > 0 else '')
    temp_mcq['choice_b_id'] = temp_mcq['choices'].apply(lambda choices: choices[1]['id'] if len(choices) > 1 else '')
    temp_mcq['choice_c_id'] = temp_mcq['choices'].apply(lambda choices: choices[2]['id'] if len(choices) > 2 else '')
    temp_mcq['choice_d_id'] = temp_mcq['choices'].apply(lambda choices: choices[3]['id'] if len(choices) > 3 else '')

    temp_mcq['choice_a'] = temp_mcq['choices'].apply(lambda choices: choices[0]['content']['model'][0]['children'][0]['text'] if len(choices) > 0 and isinstance(choices[0]['content'], dict) else '')
    temp_mcq['choice_b'] = temp_mcq['choices'].apply(lambda choices: choices[1]['content']['model'][0]['children'][0]['text'] if len(choices) > 1 and isinstance(choices[1]['content'], dict) else '')
    temp_mcq['choice_c'] = temp_mcq['choices'].apply(lambda choices: choices[2]['content']['model'][0]['children'][0]['text'] if len(choices) > 2 and isinstance(choices[2]['content'], dict) else '')
    temp_mcq['choice_d'] = temp_mcq['choices'].apply(lambda choices: choices[3]['content']['model'][0]['children'][0]['text'] if len(choices) > 3 and isinstance(choices[3]['content'], dict) else '')

    print(temp_mcq["question"])
    print(temp_mcq['choice_a'])
    print(temp_mcq['choice_b'])
    print(temp_mcq['choice_c'])
    print(temp_mcq['choice_d'])
    
    correct_choice = ""
    for x in temp_mcq.index:
        count_number_of_attempts = 0
        count_a_choice = 0
        count_b_choice = 0
        count_c_choice = 0
        count_d_choice = 0
        single_response = ""
        list_of_single_responses = []
        for y in temp_mcq.index:
            if (temp_mcq.loc[x,'Activity ID'] == temp_mcq.loc[y, 'Activity ID']):
                count_number_of_attempts = count_number_of_attempts + 1
                # if student selects option A, count number of option As to +1
                #print(df3.loc[x, 'choice_a'].key)
                print(temp_mcq.loc[y,'input'])
                if(temp_mcq.loc[y,'input'] == temp_mcq.at[y,'choice_a_id']):
                    count_a_choice = count_a_choice + 1
                    print(temp_mcq.loc[y, 'Activity Score'])
                    if (temp_mcq.loc[y, 'Activity Score'] == 1):
                        correct_choice = "Choice A"
                elif (temp_mcq.loc[y,'input'] == temp_mcq.at[y,'choice_b_id']):
                    count_b_choice = count_b_choice + 1
                    if (temp_mcq.loc[y, 'Activity Score'] == 1):
                        correct_choice = "Choice B"
                elif (temp_mcq.loc[y,'input'] == temp_mcq.at[y,'choice_c_id']):
                    count_c_choice = count_c_choice + 1
                    if (temp_mcq.loc[y, 'Activity Score'] == 1):
                        correct_choice = "Choice C"
                elif (temp_mcq.loc[y,'input'] == temp_mcq.at[y,'choice_d_id']):
                    count_d_choice = count_d_choice + 1
                    if (temp_mcq.loc[y, 'Activity Score'] == 1):
                        correct_choice = "Choice D"          
        temp_mcq.loc[x,'count_a'] = count_a_choice
        print(temp_mcq.loc[x,'count_a'])
        temp_mcq.loc[x,'count_b'] = count_b_choice
        print(temp_mcq.loc[x,'count_b'])
        temp_mcq.loc[x,'count_c'] = count_c_choice
        print(temp_mcq.loc[x,'count_c'])
        temp_mcq.loc[x,'count_d'] = count_d_choice
        print(temp_mcq.loc[x,'count_d'])
        temp_mcq.loc[x,'correct_choice'] = correct_choice
        print(temp_mcq.loc[x,'correct_choice'])
    temp_mcq.to_csv("All_mcqs4" +str(i) + ".csv", index = False)
    pdf.add_page()
    pdf.set_font('Arial', size = 10)
    pdf.multi_cell(150,10,temp_mcq['question'].values[0] + '\n', align = 'L')
    pdf.multi_cell(150,10,'\u2022 '+ str(temp_mcq['choice_a'].astype(str).values[0]), align = 'L')
    pdf.multi_cell(150,10,'\u2022 '+ str(temp_mcq['choice_b'].astype(str).values[0]), align = 'L')
    pdf.multi_cell(150,10,'\u2022 '+ str(temp_mcq['choice_c'].astype(str).values[0]), align = 'L')
    pdf.multi_cell(150,10,'\u2022 '+ str(temp_mcq['choice_d'].astype(str).values[0]), align = 'L')
    pdf.cell(200,10,'\n')
    fig, ax = plot.subplots(figsize=(11,9))
    ax.set_xlim(200,1200)
    ax.set_ylim(0,300)
    bar_data = {"Options": ['Option A','Option B','Option C','Option D'], "Number_of_Attempts": [temp_mcq['count_a'].values[0], temp_mcq['count_b'].values[0], temp_mcq['count_c'].values[0], temp_mcq['count_d'].values[0]]}
    dataFrame  = pandas.DataFrame(data = bar_data)
    plot.figure(figsize=(11,9))
    if(temp_mcq['correct_choice'].values[0] == "Choice A"):
        dataFrame.plot.barh(x='Options', y='Number_of_Attempts', title="Student attempt for Q.", width = 0.5, color=['#5cb85c','#d9534f','#d9534f','#d9534f'])
    if(temp_mcq['correct_choice'].values[0] == "Choice B"):
        dataFrame.plot.barh(x='Options', y='Number_of_Attempts', title="Student attempt for Q.", width = 0.5, color=['#d9534f','#5cb85c','#d9534f','#d9534f'])
    if(temp_mcq['correct_choice'].values[0] == "Choice C"):
        dataFrame.plot.barh(x='Options', y='Number_of_Attempts', title="Student attempt for Q.", width = 0.5, color=['#d9534f','#d9534f','#5cb85c','#d9534f'])
    if(temp_mcq['correct_choice'].values[0] == "Choice D"):
        dataFrame.plot.barh(x='Options', y='Number_of_Attempts', title="Student attempt for Q.", width = 0.5, color=['#d9534f','#d9534f','#d9534f','#5cb85c'])
    
    #plot.rcParams.update({'axes.facecolor':'lightgreen'})
    plot.title(temp_mcq['Activity Title'].values[0])
    font = {'family': 'cursive',
            'color':  'darkred',
            'weight': 'bold',
            'size': 6,
            }

        #plot.subplot(2,1,2)
    
    plot.tight_layout()
    #plot.figtext(0.05, -0.18, temp_mcq['question'].values[0], fontdict = font, ha='center', wrap = True,va='bottom', bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    q_number = temp_mcq['Activity ID'].values[0]
    #img_buf = io.BytesIO()
    #plot.savefig(img_buf, dpi=500, format = 'png')
    #img_buf.seek(0)
    plot.savefig(str(q_number)+'.png', dpi=500)
    plot.close(fig)
    #convert to base64
    #data1 = img_buf.read()              # get data from file (BytesIO)
    #data1 = base64.b64encode(data1)  # convert to base64 as bytes
    #data1 = data1.decode()# convert bytes to string
    #img = '<img src="data:im/png_buf.png;base64,{}">'.format(data1)
    pdf.image(str(q_number)+'.png', x = 130, y = 60, h=100, w=130)
    pdf.cell(200,10,'\n')
    
    #img_buf.close()



#Step 2: single responses table visualization
dfs_singles = dict(tuple(df_single_response.groupby('Activity ID')))
print("enter singles section")
pdf.add_page()
pdf.set_font('Arial', size = 30)
pdf.multi_cell(200,10,'Answers from Single Response Questions' + '\n\n\n', align = 'C')
for i, df in dfs_singles.items():
    pdf.add_page()
    question = []
    single_responses = []    
    x1 = 0
    for x in df.index:
        question = df.loc[x,'authoring']['previewText']
        response = df.loc[x,'input']
        single_responses.insert(x,response)
        x1=x1+1
        print("response")
    pdf.set_font('Arial', size=10)
    pdf.multi_cell(200,10,question + '\n', align = 'L')
    for i in range(len(single_responses)):
        pdf.multi_cell(200,10,single_responses[i], align = 'L', border = 1)
    #the_table = ax.table(cellText=df_table.values,colLabels=df_table.columns,loc='center',rowLoc='right', colLoc='right', cellLoc='left', edges = 'open')
    #the_table.set_fontsize(25)
    pdf.cell(200,10,'\n')

#Step 3: Check All That Apply Visualization





#converting output dataframes to csvs
#df_mcq.to_csv("All_mcqs3.csv", index = False)
pdf.output('torus_visualize_output.pdf')
df_single_response.to_csv("All_single_responses3.csv", index = False)
