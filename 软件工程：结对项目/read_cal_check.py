import re
import fractions

# 读文件
def ReadFile(q_path):
    with open(q_path, 'r', encoding='utf-8') as f:
        read_file = f.readlines() # 一行读取
    file_list = []
    # 删题号
    for single_question in read_file: # 对于每一行(题目)而言
        # 按照'.'进行分割，取'.'后面部分
        fileline = single_question.split('.')[-1]
        # 去除每行末的换行符，方便后续处理
        fileline = fileline.strip('\n')
        # 将处理后的每一行文本放入file_list中
        file_list.append(fileline)
    return file_list

# 保存改卷结果(比较结果)到文件
def saveresult_as_file(res_list, saved_path='Grade.txt'):
    # 规范输出格式
    def Output(out_result):
        formatted_res = ''
        if len(out_result) != 0: # 检查out_result列表是否为空
            formatted_res += ' (' # 如果有结果比较，将字符串'('追加到retstr中
            for i in out_result:
                formatted_res += str(i) # 转换为字符串
                formatted_res += ', ' # 在每个结果比较之后，追加逗号和空格，以分隔不同的评分结果
            if formatted_res[-2:] == ', ': # 检查retstr中的最后两个字符是否是逗号和空格
                formatted_res = formatted_res[:-2] # 如果是则移除，以确保最后一个结果比较之后没有多余的逗号和空格
            formatted_res += ')' # 以右括号结束输出字符串
        return formatted_res

    cor_list = 'Correct: ' + str(len(res_list[0])) + Output(res_list[0]) # 正确列表
    wro_list = 'Wrong: ' + str(len(res_list[1])) + Output(res_list[1]) # 错误列表
    with open(saved_path, 'w', encoding='utf-8') as f:
        f.write(cor_list+'\n'+wro_list) # 将结果写入Grade.txt中


# 阅卷操作
def CheckAnswers(qst_list, ans_list):
    cor_list = []
    wro_list = []
    for single in range(len(qst_list)):
        if CalAnswers(qst_list[single]) == CalAnswers(ans_list[single]): # 该题目结果正确，把题号写入correct_list
            cor_list.append(single+1)
        else: # 该题目结果错误，把题号写入wrong_list
            wro_list.append(single+1)

    return [cor_list, wro_list]


# 传入题目的字符串，得到处理后的结果
def CalAnswers(formula):
    # 删除空格，等号和换行符，并将字符 '×' 替换为 '*'，将字符 '÷' 替换为 '/'
    formula=formula.replace('×','*').replace('÷','/').replace('−','-').replace("\n", "").replace("\r", "").replace("=", "").replace(" ","")
    # 去除带分数
    mix = re.findall(r"\d+\'\d+/\d+", formula) # 在算式字符串中查找带分数的部分
    mix_list = [] # 存储处理后的带分数部分
    for i in range(len(mix)):
        mix_list.append('(' + mix[i].replace('\'', '+') + ')') # 将带分数转化为合适的形式
        formula = formula.replace(mix[i], mix_list[i]) # 替换为处理后的形式，以更新算式字符串
    find_frac = re.findall(r"\d+/\d+", formula) # 查找算式字符串中的分数形式
    processed_frac = [] # 存储处理后的分数形式
    def calculate_with_fractions(matched):
        value = matched.group('value')
        return 'fractions.Fraction(' + value + ',1)'
    formula = re.sub(r'(?P<value>\d+)', calculate_with_fractions, formula)
    # 将所有除法和分数替换为fractions.Fraction对象，目的是计算过程和结果保留分数
    loc = locals()
    exec("res = " + formula)
    cal_result = loc['res']
    return cal_result


if __name__ == '__main__':
    qst_list = ReadFile('Exercises.txt') # 读文件，并将结果存入qst_list
    ans_list = ReadFile('Answers.txt') # 读文件，并将结果存入ans_list
    result = CheckAnswers(qst_list, ans_list) # 进行结果的比较，并输出
    saveresult_as_file(result) # 保存阅卷结果到文件