from read_cal_check import *
import argparse
import random
import fractions

def main():
    # 接收,处理命令行参数
    cmd_args = get_arguments()
    # 模式：生成题目
    if cmd_args.mode == 1:
        # 生成题目
        question = get_question(cmd_args)
        # 生成答案
        answer = get_answer(question)
        # 保存题目和答案
        save_as_file(answer, cmd_args.anssavepath)
        save_as_file(question,cmd_args.qstsavepath)
    # 模式：改卷
    elif cmd_args.mode == 2:
        # 读题目、答案文件
        question = ReadFile(cmd_args.qstpath)
        answer = ReadFile(cmd_args.anspath)
        # 检查答案
        check_results = CheckAnswers(question, answer)
        # 保存结果
        saveresult_as_file(check_results)


# 接收,处理命令行参数函数
    #  1.出题模式
    # -n 控制生成题目的个数
    # -r 控制数值（自然数、真分数和真分数分母）的范围，该参数必须给定，否则程序报错。
    #  2.改卷模式：程序支持对给定的题目文件和答案文件判定对错并进行数量统计
def get_arguments():
    parser = argparse.ArgumentParser(description='calculater')
    parser.add_argument('-r', dest='maxnumber', help='数据大小范围', type=int , default=None)
    parser.add_argument('-n', dest='qstnumber', help='问题数量', type=int , default=None)
    parser.add_argument('-a', dest='anspath', help='答案文件路径',  type=str , default=None)
    parser.add_argument('-e', dest='qstpath', help='题目文件路径',  type=str , default=None)
    parser.add_argument('-mode', dest='mode', help='程序模式', type=int ,  default=None)
    parser.add_argument('-qstsavepath', dest='qstsavepath', help='path of saving questions', type=str ,  default='Exercises.txt')
    parser.add_argument('-anssavepath', dest='anssavepath', help='path of saving answers', type=str ,  default='Answers.txt')
    m_args = parser.parse_args()
    if m_args.qstnumber != None or m_args.maxnumber != None:
        assert m_args.qstnumber != None and m_args.maxnumber != None, "错误:缺少题目数量或数字范围"
        m_args.mode = 1
        return m_args
    elif m_args.qstpath != None or m_args.anspath != None:
        assert m_args.qstpath != None, "错误:没有题目文件路径"
        assert m_args.anspath != None, "错误:没有答案文件路径"
        m_args.mode = 2
        return m_args
    else:
        assert False, "未输入命令行参数，无法运行"


# 生成题目
def get_question(args):
    # 四则运算
    symbol_list = ['+', '−', '×', '÷']
    question_num = args.qstnumber
    max_num = args.maxnumber
    # 用于存储生成的数学题目
    test_list = []
    for i in range(question_num):
        while True:
            calculates = ''
            mathnum = random.randint(2, 4)   # 随机生成2-4个数字
            symbolnum = mathnum - 1
            # 运算符号
            sym_list = []
            # 运算数字
            numbers_list = []
            question_list = []
            # 括号数
            cumulate = 0
            brackets = 0
            if mathnum == 3:
                brackets = random.randint(0, 1)
            elif mathnum == 4:
                brackets = random.randint(0, 2)
            if brackets == 1:
                cumulate = random.randint(1, mathnum - 1)
            for j in range(symbolnum):
                iindex = random.randint(0, 3)
                sym_list.append(symbol_list[iindex])
            for k in range(mathnum):
                numberfm = random.randint(1, 2)
                # 生成自然数
                if numberfm == 1:
                    num_str = random.randint(1, max_num - 1)
                # 生成真分数
                elif numberfm == 2:
                    nume = random.randint(1, max_num - 1)
                    deno = random.randint(1, max_num - 1)
                    # 真分数，不需要转换格式
                    if nume < deno:
                        num_str = str(nume) + '/' + str(deno)
                        # 等于1
                    elif nume == deno:
                        num_str = str(1)
                        # 假分数，转换为正确格式
                    else:
                        if nume % deno == 0:
                            num_str = str(int(nume / deno))
                        else:
                            sname = nume // deno
                            last = nume % deno
                            num_str = str(sname) + "'" + str(fractions.Fraction(last, deno))
                numbers_list.append(num_str)
            # 标记，是否需要添加括号：1为需要，0为不需要
            flag = 0
            if cumulate == 1 or brackets == 2: # 需要添加括号
                calculates = "(" + str(numbers_list[0])
                flag = 1 # 已添加括号
            else:
                calculates = numbers_list[0]
            for index in range(1, mathnum): # 生成 mathnum 次number，并填入
                if brackets == 2 and index == 2: # 是否需要在第二个数字后添加括号
                    calculates = str(calculates) + ' ' + str(sym_list[index - 1]) + "(" + str(numbers_list[index])
                    flag = 1 # 已添加括号
                    continue
                if flag == 1:
                    if str(sym_list[index - 1]) == '−': # 如果是减号，需要满足题目条件
                        if "'" in str(numbers_list[index]) and numbers_list[index] is not int: # 如果是真分数
                            num1 = realtomixed(str(numbers_list[index])) # 转换为假分数
                        else:
                            num1 = eval(str(numbers_list[index]))
                        if "'" in str(numbers_list[index - 1]) and numbers_list[index - 1] is not int: # 如果是真分数
                            num2 = realtomixed(str(numbers_list[index])) # 转换为假分数
                        else:
                            num2 = eval(str(numbers_list[index - 1]))
                        if (num1 >= num2): # num2-num1
                            if num2 <= 1:
                                num1 = 0
                            while num1 >= num2: # 直到生成num1<num2
                                num1 = random.randint(1, max_num)
                            numbers_list[index] = str(int(num1))
                    # 继续完成calculates表达式
                    calculates = str(calculates) + ' ' + str(sym_list[index - 1]) + ' ' + str(numbers_list[index]) + ")"
                    flag = 0
                # 没添加括号
                elif cumulate == index: # 需要添加括号
                    calculates = "(" + str(calculates) + ' ' + str(sym_list[index - 1]) + ' ' + str(numbers_list[index])
                    flag = 1
                elif cumulate == 2 and index == 1: # 需要添加括号
                    calculates = str(calculates) + ' ' + str(sym_list[index - 1]) + " ( " + str(numbers_list[index])
                    flag = 1
                elif cumulate == 3 and index == 2: # 需要添加括号
                    calculates = str(calculates) + ' ' + str(sym_list[index - 1]) + " ( " + str(numbers_list[index])
                    flag = 1
                else:
                    calculates = str(calculates) + ' ' + str(sym_list[index - 1]) + ' ' + str(numbers_list[index])
            # 添加“=”到表达式的末尾，以构建完整的数学题目。
            calculates = calculates + " = "
            # 检查生成的数学表达式结果是否大于等于0，如果结果小于0，则重新生成表达式，直到生成一个结果大于等于0的表达式
            if CalAnswers(calculates) >= 0:
                break
            else:
                calculates = None

        test_list.append(calculates)
    return test_list

# 生成答案
def get_answer(question):
    answer_list = []
    for i, ele in enumerate(question):
        answer_list.append(mixedtoreal(CalAnswers(ele)))
    return answer_list

# 保存程序生成的题目和答案
# 格式:
    # 1.。。。。
    # 2.。。。。
def save_as_file(qst_list, saved_path='Exercises.txt'):
    with open(saved_path, 'w' , encoding='utf-8') as f:
        for i in range(1, len(qst_list) + 1):
            f.write(str(i) + ". " + str(qst_list[i - 1]) + "\n")

# 假分数转换真分数
def mixedtoreal(num):
    num_str = str(num)
    if '/' in num_str:
        nume = int(num_str.split('/')[0])
        deno = int(num_str.split('/')[1])
        if deno < nume :
            former = nume // deno # 带分数的整数部分
            later = nume % deno # 带分数的分数部分
            mixed_fraction = str(former) + "'" + str(later) + "/" + str(deno)
            return mixed_fraction
        else:
            return num
    else:
        return num

# 真分数转换假分数
def realtomixed(num):
    num = num.split("'") # 分割
    if len(num) == 1:
        return eval(num[0])
    num2 = num[1].split('/') # 分割
    num1 = int(num[0]) * int(num2[1]) + int(num2[0])
    result = fractions.Fraction(num1, int(num2[1]))
    return result


if __name__ == '__main__':
    main()
