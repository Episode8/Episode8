from read_cal_check import *
import random
import fractions
import argparse

def main():
    # 接收并处理命令行参数
    operate = get_arguments()  # 包含操作数和参数

    # 模式：生成题目
    if operate.mode == 1:
        # 生成题目和答案
        question = get_question(operate)
        answer = get_answer(question)

        # 保存程序生成的题目和答案
        save_as_file(answer, operate.anssavepath)
        save_as_file(question,operate.qstsavepath)

    # 模式：改卷
    elif operate.mode == 2:
        question = readfile(operate.qstpath)
        answer = readfile(operate.anspath)
        check_results = check(question , answer)
        # 保存结果
        saveresult_as_file(check_results)


# 接收并处理命令行参数
def get_arguments():
    # 1.生成题目模式
    # 使用 -n 参数控制生成题目的个数
    # 使用 -r 参数控制题目中数值（自然数、真分数和真分数分母）的范围，该参数可以设置为1或其他自然数。该参数必须给定，否则程序报错并给出帮助信息。
    # 2.阅卷模式
    # 程序支持对给定的题目文件和答案文件，判定答案中的对错并进行数量统计，输入参数如下：
    # -e
    # -a
    # 例：main.py - e < exercisefile >.txt - a < answerfile >.txt
    parser = argparse.ArgumentParser(description='calculater')
    parser.add_argument('-r', dest='maxnumber', help='range of numbers', default=None, type=int)
    parser.add_argument('-n', dest='qstnumber', help='how much questions', default=None, type=int)
    parser.add_argument('-a', dest='anspath', help='path of answer file', default=None, type=str)
    parser.add_argument('-e', dest='qstpath', help='path of exercise file', default=None, type=str)
    parser.add_argument('-mode', dest='mode', help='path of answer file', default=None, type=int)
    parser.add_argument('-qstsavepath', dest='qstsavepath', help='path of saving questions', default='Exercises.txt', type=str)
    parser.add_argument('-anssavepath', dest='anssavepath', help='path of saving answers', default='Answers.txt', type=str)
    args = parser.parse_args()
    if args.qstnumber != None or args.maxnumber != None:
        assert args.qstnumber != None and args.maxnumber != None, "Error:生成题目模式缺少生成题目数量或者数字范围"
        args.mode = 1
        return args
    elif args.qstpath != None or args.anspath != None:
        assert args.qstpath != None, "Error:缺失题目文件路径"
        assert args.anspath != None, "Error:缺少答案文件路径"
        args.mode = 2
        return args
    else:
        assert False, "未输入命令行参数，无法运行"


# 生成题目
def get_question(args):
    symbol = ['+', '−', '×', '÷'] # 四则运算
    number = args.qstnumber
    maxnum = args.maxnumber
    test_list = [] # 用于存储生成的数学题目
    for i in range(number):
        while True:
            calculates = ''
            mathnum = random.randint(2, 4)   # 随机生成2-4个数字
            symbolnum = mathnum - 1
            sym = [] # 运算符号
            numbers = [] # 运算数字
            question = []
            cumulate = 0 # 括号数
            brackets = 0
            if mathnum == 3:
                brackets = random.randint(0, 1)
            elif mathnum == 4:
                brackets = random.randint(0, 2)
            if brackets == 1:
                cumulate = random.randint(1, mathnum - 1)
            for j in range(symbolnum):
                iindex = random.randint(0, 3)
                sym.append(symbol[iindex])
            for w in range(mathnum):
                number_format = random.randint(1, 2)
                if number_format == 1: # 生成自然数
                    num = random.randint(1, maxnum - 1)
                elif number_format == 2: # 生成真分数
                    nume = random.randint(1, maxnum - 1)
                    deno = random.randint(1, maxnum - 1)
                    if nume < deno: # 真分数，不需要转换格式
                        num = str(nume) + '/' + str(deno)
                    elif nume == deno: # 等于1
                        num = str(1)
                    else: # 假分数，转换为正确格式
                        if nume % deno == 0:
                            num = str(int(nume / deno))
                        else:
                            sname = nume // deno
                            last = nume % deno
                            num = str(sname) + "'" + str(fractions.Fraction(last, deno))
                numbers.append(num)
            flag = 0 # 标记，是否需要添加括号：1为需要，0为不需要
            if cumulate == 1 or brackets == 2: # 需要添加括号
                calculates = "(" + str(numbers[0])
                flag = 1 # 已添加括号
            else:
                calculates = numbers[0]
            for index in range(1, mathnum): # 生成 mathnum 次number，并填入
                if brackets == 2 and index == 2: # 是否需要在第二个数字后添加括号
                    calculates = str(calculates) + ' ' + str(sym[index - 1]) + "(" + str(numbers[index])
                    flag = 1 # 已添加括号
                    continue
                if flag == 1:
                    if str(sym[index - 1]) == '−': # 如果是减号，需要满足题目条件
                        if "'" in str(numbers[index]) and numbers[index] is not int: # 如果是真分数
                            num1 = realtomixed(str(numbers[index])) # 转换为假分数
                        else:
                            num1 = eval(str(numbers[index]))
                        if "'" in str(numbers[index - 1]) and numbers[index - 1] is not int: # 如果是真分数
                            num2 = realtomixed(str(numbers[index])) # 转换为假分数
                        else:
                            num2 = eval(str(numbers[index - 1]))
                        if (num1 >= num2): # num2-num1
                            if num2 <= 1:
                                num1 = 0
                            while num1 >= num2: # 直到生成num1<num2
                                num1 = random.randint(1, maxnum)
                            numbers[index] = str(int(num1))
                    # 继续完成calculates表达式
                    calculates = str(calculates) + ' ' + str(sym[index - 1]) + ' ' + str(numbers[index]) + ")"

                    flag = 0
                # 没添加括号
                elif cumulate == index: # 需要添加括号
                    calculates = "(" + str(calculates) + ' ' + str(sym[index - 1]) + ' ' + str(numbers[index])
                    flag = 1
                elif cumulate == 2 and index == 1: # 需要添加括号
                    calculates = str(calculates) + ' ' + str(sym[index - 1]) + " ( " + str(numbers[index])
                    flag = 1
                elif cumulate == 3 and index == 2: # 需要添加括号
                    calculates = str(calculates) + ' ' + str(sym[index - 1]) + " ( " + str(numbers[index])
                    flag = 1
                else:

                    calculates = str(calculates) + ' ' + str(sym[index - 1]) + ' ' + str(numbers[index])
            calculates = calculates + " = " # 添加“=”到表达式的末尾，以构建完整的数学题目。
            # 检查生成的数学表达式结果是否大于等于0，如果结果小于0，则重新生成表达式，直到生成一个结果大于等于0的表达式
            if cal(calculates) >= 0:
                break
            else:
                calculates = None

        test_list.append(calculates)
    return test_list

# 生成答案
def get_answer(question):
    answer = []
    for i, ele in enumerate(question):
        answer.append(mixedtoreal(cal(ele)))
    return answer

# 假分数转换真分数
def mixedtoreal(num):
    num1 = str(num)
    if '/' in num1:
        nume = int(num1.split('/')[0])
        deno = int(num1.split('/')[1])
        if nume > deno:
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

# 保存程序生成的题目和答案
def save_as_file(qst, save_path='Exercises.txt'):
    # 格式:
    # 1.四则运算题目1
    # 2.四则运算题目2
    # 其中真分数在输入输出时采用如下格式，真分数五分之三表示为3/5，真分数二又八分之三表示为2’3/8。
    with open(save_path, "w", encoding='utf-8') as f:
        for i in range(1, len(qst) + 1):
            f.write(str(i) + ". " + str(qst[i - 1]) + "\n")

if __name__ == '__main__':
    main()
