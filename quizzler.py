from os import path,mkdir,system
from time import sleep, time
from datetime import datetime
from random import *
import re
import json
#utility
def clear_screen() : system('cls')
def count_down(n,message = 'Get Ready'):
    for i in reversed(range(n)) :
        clear_screen()
        print(f'{message}'.center(100))
        print(f'\n\n{i}'.center(100))
        sleep(1)
    pass
#intro-Text
def banner() :
        print('Welcome To Quizzler !'.center(100,'-'))
        sleep(1)
        print("""
            creator@Mohammad_Ayan_Khan
            Enrollment@0157CS191104
            Version@1.0
            Date_Of_Creation@23-Oct-2021
            
            About -
                Quizzler
                Players can register with a username & password to login
                or they can choose to play anonymously.
                
                Registered users' past scores are saved and can be viewed after logging in.
                And all of the anonymous scores are also stored together.
                 
                usernames should be unique and password length should be greater than 2
                
                Quizzler requires a separate .json file for questions/answers
                Currently it conssist of 3 quizzies.
                (Programming language is python)
                1) miscellaneous1
                2) regular_expression2
                3) files_and_strings3
                
                Player has to choose number of question and type of quiz to play.
                Result is displayed once the quiz gets completed.
                Result consist of  percentage, number of correct answers, total time spent for quiz, and a score.
                (score is 10000 * 1/time spent for each question)
                All of this is stored with a timestamp locally.
                
                Players can also look at top scores of all other players.
                
            Instructions for playing -
                In Quizzler almost all of the question comes with 4 options,
                give any of one of these commands 1/2/3/4 to select your answer.
                
                
            Good Luck ;)
            
                Enter 'register' to register.
                Enter 'login' if you are already registered.
                Enter 'anonymous' to skip, Warning- scores will not get saved.
                
            """)
#authentification terminal 
def cmd_input():
    print("-"*100)
    cmd = input('cmd login/register/anonymous> ').strip().casefold() 
    
    if cmd == "login"  :
        name = login()
        print('Enter "start" to launch the quiz\nEnter "check_history" it display past Attempts\nEnter "top_score" to get a list of top players.\nEnter "quit" to exit.')
        return quiz_menu(name)
    elif cmd == "register"  :
        # if name is not unique /restart
        if register() :
            return cmd_input()
    elif cmd == "anonymous" :
        print('Enter "start" to launch the quiz\nEnter "check_history" it display past Attempts\nEnter "quit" to exit.')
        return quiz_menu('anonymous')
    else :
        print('Please try another option-- login/register/anonymous')
        return cmd_input()    
#Authentification
def login():
    clear_screen()
    print('Login')
    name     = input('name > ').strip()
    passwd   = input('password > ').strip()
    if record_checkout(name , passwd) == True :
        return name
    else :
        print("Wrong username or password !")
        return cmd_input() 
def register():
    clear_screen()
    print('Register a new Player')
    print('Password should be greater than 2 characters')
    name     = input('name > ').strip()
    passwd = input('password > ').strip()
    
    if len(passwd) < 3 :
        print('passwd is too short')
        return cmd_input
    
    if record_checkout(name,passwd) == False :
        record_add(name,passwd)
        
        return True
    else :
        print('User already exist')
        return cmd_input()
#file_handeling
def record_checkout(name = '',passwd = ''):
    try : 
        with open('record_quizzler_users.txt') as record :
            record = record.read()
    except FileNotFoundError :
        return False
        
    if len(name) > 0 and len(passwd) > 0 :
        s_name = re.search(f'(?<=_){name}+(?=_)',record)
        if s_name != None :
            if name == s_name.group() :
                s_passwd = re.search(f'(?<=_{name}_,\$).+(?=\$)',record)
                if s_passwd != None and passwd == s_passwd.group() :
                    return True
                else :
                    return 'wrong password'
        else :
            return False
        
    return False
def record_add(name,passwd):
    with open('record_quizzler_users.txt','a') as record :
        record.writelines('\n_'+name+'_'+','+'$'+passwd+'$\n')
def save_file_add(name,quiz_type,quiz_num_questions,correct_ans,quiz_score,quiz_completion_time):
    if path.isdir('saves/') == False : mkdir('saves')
    with open(f'saves/{name}_save.txt','a+') as save :
        save.writelines(f'\n' + '| Type : {quiz_type} | Number of Questions : {quiz_num_questions} | Score  : {quiz_score} | Percent : {correct_ans / quiz_num_questions * 100} | Time spent : {quiz_completion_time} | Time-Stamp : {datetime.now()}| '+'\n')
def save_file_checkout(name):
    if path.isdir('saves/') == False : mkdir('saves')
    try : 
        with open(f'saves/{name}_save.txt') as saveFile :
            saveFile = saveFile.read()
        print(saveFile)
    except FileNotFoundError :
        with open(f'saves/{name}_save.txt','w+') as saveFile :
            saveFile = saveFile.write('')
def scoreboard_checkout():
    try :
        with open('scoreboard.txt','r') as file :
            record = file.readlines()
            record = [i.split(maxsplit=3)[1:] for i in record if i != '\n' ]
    except :
        with open('scoreboard.txt','w') as file :
            file.write('')
            record = []
        
    return record
def scoreboard_update(name , score ): 
    name = str(name).strip()
    record = scoreboard_checkout()
    record.append([name,score,str(datetime.now())])
    record.sort(reverse=True , key= lambda x : float(x[1]))
    
    with open('scoreboard.txt','a+') as file :
        file.seek(0)
        file.truncate()
        for idx,rec in enumerate(record[:100]) : #Just TOP 100 :)
            file.write(f'{idx + 1} ' + ' '.join(rec) + '\n')
#quiz
def quiz_question_count():
    n = input("Give number of questions You wish to attempt [5 to 10] > ")
    if n.isnumeric() : 
        n = int(n)
        if 4 < n < 11 :
            print(f'You Selected {n} questions !')
            return n
    clear_screen()
    print('Please enter a valid number...')
    return quiz_question_count()
def quiz_type() :
    print("""
          Few More Steps Left !
          Please select one of the following quizzes --
          1) Python miscellaneous
          2) Regular Expressions
          3) Strings and Files
          Or enter a random number to select a Truly random quiz.
          """)
    n = input('cmd 1/2/3 > ')
    if n.isnumeric() :
        n = int(n) 
        if n > 3 : n % 3 + 1
        clear_screen()
        return n
    else :
        clear_screen()
        return quiz_type()   
def quiz_import(n):
    try :
        with open('quiz.json',encoding='utf-8') as quiz :
            quiz = json.load(quiz)
            wordList = [quiz_type_json for quiz_type_json in quiz]
            print(wordList)
            for word in wordList :
                d = re.search(f'.*{n}',word)
                if d :
                    quiz = quiz[d.group()]
                    break
            
        return [quiz,d.group()]
    except :
        clear_screen()
        print("quiz.json NOT FOUND")
        sleep(3)
        return cmd_input()        
def quiz_menu(name) :
    cmd = input("cmd start/check_history/top_score/quit >").strip().casefold()
    if cmd == "start" :
        return quiz_start(name)
    elif cmd == "check_history" :
        clear_screen()
        print('History-->')
        save_file_checkout(name)
        print('\n\n\n')
        return quiz_menu(name)
    elif cmd == "top_score":
        clear_screen()
        print("Top Socres -->")
        print(*scoreboard_checkout(),sep='\n')
        print('\n\n\n')
        return quiz_menu(name)
    elif cmd == "quit" :
        from sys import exit
        exit()
    else :
        clear_screen()
        print("PLease give a valid command")
        return quiz_menu(name)
def quiz_start(name):
    clear_screen()
    print('WELCOME'.center(100))
    number_of_questions = quiz_question_count()
    type_of_quiz = quiz_type()
    quiz,quiz_type_name  = quiz_import(type_of_quiz)
    # start count down
    count_down(4)
    #quiz/result parameters
    max_question_number = len(quiz)
    questions = [ i % max_question_number + 1  for i in range(1,number_of_questions + 1)]
    shuffle(questions)
    total_time = 0
    score = 0
    correct = 0
    for flag,idx in enumerate(questions) :
        start = time()
        clear_screen()
        print('Author :',quiz[f'question{idx}']['author'])
        print(quiz[f'question{idx}']['ques'])
        for i in range(1,5):
            print(f'{i} :',quiz[f'question{idx}']['options'][f'{i}'])

        
        ans_key = input('cmd 1/2/3/4 > ').strip().casefold()
        end = time()
        
        if ans_key not in ['1','2','3','4'] : 
            count_down(3,message='Get ready for Next question, last questoin got marked as wrong.')
            continue
        #check answer
        if quiz[f'question{idx}']['options'][f'{ans_key}'] == quiz[f'question{idx}']['answer'] :
            correct += 1
            score += 10000 * (1 / (end - start))
            
        clear_screen()
        print('You spent' , end - start , 'seconds on this question.')
        total_time += end-start
        sleep(2)
        if flag != number_of_questions - 1 :
            count_down(3,message='Get ready for Next Question !')
        
    clear_screen()    
    print(f'Congratulations You Finished the quiz in {total_time / 60} minutes !')
    print(f'Your score was {score}')
    print(f'Your percentage was {correct / number_of_questions * 100}')
    print(f'Your {correct} answers were correct out of {number_of_questions}')
    #recording on scoreboard
    scoreboard_update(name,str(score))
    #saving result
    save_file_add(name,quiz_type_name,number_of_questions,correct,score,total_time/60)
    return quiz_menu(name)
#start script
def intro():
    banner()
    cmd_input()       
if __name__ == "__main__" :
    intro()
    
     
  
    

    