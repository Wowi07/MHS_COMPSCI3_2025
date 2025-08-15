from tkinter import *
from functools import partial
import csv
import random

# get all the capital and country name from csv file
def get_all_cap():
    file = open("Capital_Quiz/country_capitals(Sheet1).csv","r")
    all_cap=list(csv.reader(file,delimiter=","))
    file.close()

    # remove first row
    all_cap.pop(0)

    return all_cap
# call get_all_cap to get the information needed
all_cap=get_all_cap()


def question_generating():
    """
    Random and return information about question
    :return: ans_list, country name for the question, real_ans_index
    """
    #save index of cap chosen
    cap_chosen=[]
    while len(cap_chosen) != 4:   # repeat until has enough amount of options
        random_cap = random.choice(all_cap)
        if (random_cap not in cap_chosen):  # make sure no option appears twice in one question
            cap_chosen.append(random_cap)   # if valid then append in

    ans_list=[]

    real_ans=random.choice(cap_chosen)    # random the correct out of 4 options
    # 0 and 1 indicate that option is wrong or correct
    for count,item in enumerate(cap_chosen):    # going through every option to put in the ans_list
        if item==real_ans:
            country=item[0]
            ans_list.append([item[1],1]) # indicates that this is the correct ans
            real_ans_index=count    # save the index of real answer. This is for changing its color later
            print(f"answer: {item[1]}") # testing purpose
        else:
            ans_list.append([item[1],0])

    # choose the question, correct ans
    return ans_list , country , real_ans_index

class StartGame:
    def __init__(self):
        """
        GUI for Start Game(choose number of question box)
        """
        # frame
        self.cap_frame=Frame(padx=10,pady=10)   
        self.cap_frame.grid()

        # heading
        self.cap_heading=Label(self.cap_frame,text="Capital Quiz",  
                               justify="center",font=("Arial","16","bold"),fg="#3a3a3a")    
        self.cap_heading.grid(row=0,pady=10)

        # introduction sentence
        intruction="How many capital do you know?\nAre you ready to challenge yourself?"
        self.cap_intro=Label(self.cap_frame,text=intruction,font=("Arial","14"),fg="#3a3a3a")
        self.cap_intro.grid(row=1,padx=5,pady=10)

        # Label to show instruction and error announcing
        self.cap_error=Label(self.cap_frame,font=("Arial","8"),fg="#32680B"
                             ,text="How many question you want to answer?")
        self.cap_error.grid(row=2,padx=5,pady=2)

        # create a frame here to put entry and play button in the same row
        self.entry_frame=Frame(self.cap_frame,padx=10,pady=4)
        self.entry_frame.grid(row=3)

        # entry box
        self.cap_entry=Entry(self.entry_frame,font=("Arial","20"),
                             width=11,justify="left",bg="#f8f8f8")
        self.cap_entry.grid(row=0,pady=5,column=0,padx=5)
        
        # play button
        self.play_button=Button(self.entry_frame,fg="#ffffff",bg="#6aa84f",text="Play",font=("Arial","16","bold"),width=9,command=self.check_round)
        self.play_button.grid(row=0,pady=5,padx=5,column=1)

    def check_round(self):
        """
        Check if what user entry is valid.
        If wrong, send straight to entry error function.
        If right, send to game play.
        """
        question_wanted=self.cap_entry.get()
        try:
            question_wanted=int(question_wanted)
            if(question_wanted<=0):
                self.entry_error()
            else:
                self.to_play(question_wanted)
        except ValueError:
            self.entry_error()
    

    def entry_error(self):
        """
        Change the color and text of instruction Label, also delete the invalid entry
        """
        error_text="Please enter valid integer greater than 0"
        self.cap_entry.delete(0,END)
        self.cap_error.config(text=error_text,fg="#ff0000")
        self.cap_entry.config(bg="#ffc0c0")

    def to_play(self,question_wanted):
        """
        Leads user to Game Play
        """
        root.withdraw() # hide get round box (not long show icon for it)
        Game_Play(self) # call Game_Play class, send its variable as prefix partner.

        # Reset everything. Left no crumb XD
        self.cap_entry.config(bg="#f8f8f8")
        self.cap_error.config(fg="#32680B",text="How many question you want to answer?")
        self.cap_entry.delete(0,END)


class Game_Play:
    def __init__(self,partner):
        """
        Initial GUI for Game_Play with important variables.
        """

        # initial setting and values when user haven't answer any question
        self.answered=BooleanVar()  # to check have user answered the current question

        self.point_rush= IntVar()   # to save the current value of point rush
        self.point_rush.set(0)

        self.current_question_num = IntVar()    # hold the number of question answered. Other words, the current question number
        self.current_question_num.set(0)

        self.question_wanted=int(partner.cap_entry.get())   # get the question wanted from what user have entered before, put it back from partner. to self. so its easier to use

        self.current_point=IntVar() # current point user got. Initially 0.
        self.current_point.set(0)

        self.highest_streak=0   # highest streak point

        self.correct_num=0  # number of correct answer

        point_announce= f"| Point: {self.current_point.get()} |"    # Initial text for point_announcing

        #create a box on top
        self.play_box= Toplevel()
        self.play_box.protocol("WM_DELETE_WINDOW",root.destroy) # If user use X icon to close this box, they will close the whole thing
        
        # frame
        self.play_frame=Frame(self.play_box)
        self.play_frame.grid(padx=10,pady=10)
        
        # heading
        self.play_heading = Label(self.play_frame,
                                  font=("Arial","16","bold"),fg="#3a3a3a" )
        self.play_heading.grid(pady=6,padx=5,row=0)

        # point announcing
        self.play_point = Label(self.play_frame,
                                font=("Arial","10","bold"),fg="#3a3a3a",text=point_announce
                                )
        self.play_point.grid(pady=2,row=1)

        # question topic
        self.play_question = Label(self.play_frame,text="",
                                font=("Arial","15"),fg="#3a3a3a",wraplength=300)
        self.play_question.grid(row=2)
        

        # create ans frame
        self.ans_frame=Frame(self.play_frame)
        self.ans_frame.grid(row=3,padx=5,pady=5)

        # ans buttons
        self.ans_list_ref = []  # use list to refer it, so easier and more convenience
        #since all button is the same except the text, it is easier to create its button initially
        for count in range(0,4):
            self.ans_option=Button(self.ans_frame,
                                   font=("Arial","12","bold"),
                                   fg="#3a3a3a",
                                   bg="#b7b7b7",width=15)
            self.ans_option.grid(row=int(count/2),column=int(count%2),pady=5,padx=5)
            self.ans_list_ref.append(self.ans_option)
        
        # point rush announcement
        self.point_rush_annoucement = Label(self.play_frame,
                                            text=f"🔥 Point rush +{self.point_rush.get()} 🔥"
                                            ,font=("Arial","14","bold"),bg="#f0f0f0"    # f0f0f0 is lightest color for point rush
                                            ,fg="#cc0000", width=27)
        self.point_rush_annoucement.grid(row=4,padx=5,pady=5)
        
        # hint stats frame. Because I wanna put these together
        self.hint_stats_frame = Frame(self.play_frame)
        self.hint_stats_frame.grid(pady=5,padx=5,row=6)

        self.button_ref=[]
        # text | bg | row | column | command | width | frame it's in
        button_feature_list= [
            ["Next Round","#1155cc",5,None,self.new_round,27,self.play_frame],
            ["Help/Info","#e98e05",0,0,self.to_help,13,self.hint_stats_frame],  # row and column of help and stats in hint_stats_frame is different
            ["Stats","#434343",0,1,self.to_stats,13,self.hint_stats_frame],     # from the next round and end game
            ["End Game","#cc0000",7,None,self.close_play,27,self.play_frame]
        ]
        for item in (button_feature_list):
            self.button= Button(item[6],text=item[0],bg=item[1],
                                command=item[4],width=item[5],
                                font=("Arial","15","bold"),fg="#FFFFFF")
            self.button.grid(row=item[2],column=item[3],pady=2,padx=2)
            self.button_ref.append(self.button)

        self.new_round()    # call new round function

    def new_round(self):
        """
        Change(config) buttons and Label base on the information taken from other functions
        """
        # initially reset the color of answer options
        for item in (self.ans_list_ref):
            item.config(bg="#b7b7b7",disabledforeground="#717171")

        # get the current round and update by adding 1
        self.button_ref[0].config(state=DISABLED)   # disable next round button
        # reset the answered to False
        self.answered.set(True)
        self.buttons_state("NORMAL")


        # change the display for question annoncement etc...
        heading_text= f"Question {self.current_question_num.get()+1} of {self.question_wanted}"
        self.play_heading.config(text=heading_text)

        # ans_topic_list : the option name | correct or not(1 for correct, 0 for wrong)
        # country: name of the country
        # real_ans_index: the index of real answer in ans_list
        base_information = question_generating()
        ans_topic_list=base_information[0]
        country=base_information[1]
        self.real_ans_index=base_information[2]

        question = f"What is the capital of {country}?" # question based on information just got above

        # change text of button based on information got above
        # command of button is calling the check_ans, with the reference is if that option correct or not; and index of the button
        for count,item in enumerate(self.ans_list_ref):
            item.config(text=ans_topic_list[count][0],command=partial(self.check_ans,ans_topic_list[count][1],count))
        self.play_question.config(text=question)    # put question in

        
    def buttons_state(self,states):
        """
        disable or enable buttons.
        """
        if states == "DISABLED":
            for item in(self.button_ref):   #disable buttons like help/stats/end game...
                item.config(state=DISABLED)
            for item in(self.ans_list_ref): #disable answer options
                item.config(state=DISABLED)
        else:
            for item in(self.button_ref):
                item.config(state=NORMAL)
            # if statement to cover the boundary
            if self.answered.get(): # if they haven't answer the question
                self.button_ref[0].config(state=DISABLED)  # if havent answer then disable next round button still
                for item in(self.ans_list_ref): # enable other button
                    item.config(state=NORMAL)
        # if this is the last question, then always disable the next round button
        if self.current_question_num.get()==self.question_wanted:
            self.button_ref[0].config(state=DISABLED)  



    def check_ans(self,correct,button_chose_index):
        """
        Check if the question choose is correct or not.
        Update variables and GUI bases on the response.
        """
        self.current_question_num.set(self.current_question_num.get()+1)    # only update the number of question answered when user answered

        self.answered.set(False)    # when alr answer, set this variable to False to indicate

        # correct will be used as an if condition; 1 for correct, 0 for incorrect
        if correct==1:
            self.correct_num+=1  # count that user just answer one more question correct

            self.current_point.set(self.current_point.get()+100+self.point_rush.get())  # if answered correct, add points by +100(original point) + point rush
            self.point_rush.set(self.point_rush.get()+50)   # increase the point rush
            self.highest_streak=max(self.highest_streak,self.point_rush.get())    # get the highest streak point

            # Update point and point rush right away
            point_announce= f"| Point: {self.current_point.get()} |"       # update the display of point
            self.play_point.config(text=point_announce) 

            self.point_rush_annoucement.config(text=f"🔥 Point rush +{self.point_rush.get()} 🔥")   # update the display of point rush

            # changing color of point rush base how large is the streak
            if self.point_rush.get()==150:  # second state
                self.point_rush_annoucement.config(bg="#ffe599")
            elif self.point_rush.get()==300:    # third state
                self.point_rush_annoucement.config(bg="#ffca99")
            elif self.point_rush.get()==500:    # fourth state
                self.point_rush_annoucement.config(bg="#ffa899")

        else:   # if they answer wrong
            self.point_rush.set(0)  # reset point rush
            self.point_rush_annoucement.config(text=f"🔥 Point rush +{self.point_rush.get()} 🔥",bg="#f0f0f0")

        # disable the answer option buttons ONLY
        for item in(self.ans_list_ref):
            item.config(state=DISABLED)

        # enable next round button or not (use for the final round)
        if self.current_question_num.get()==self.question_wanted:
            self.button_ref[0].config(state=DISABLED)
        else:
            self.button_ref[0].config(state=NORMAL)

        # change color to indicate answer
        # logic: change color of what they choose first. If it is same as correct ans, the color of that button
        # will now be changed into green. If they choose wrong, then the real ans will be green and what they chose will be red.
        self.ans_list_ref[button_chose_index].config(bg="#ea9999",disabledforeground="#3a3a3a")
        self.ans_list_ref[self.real_ans_index].config(bg="#93c47d",disabledforeground="#3a3a3a")

    def to_help(self):
        """
        Send to help class
        """
        self.buttons_state("DISABLED")  # disable every button when open help
        Help(self)
    def to_stats(self):
        """
        Send to stats class
        """
        self.buttons_state("DISABLED")  # disable every button when open stats
        Stats(self)


    def close_play(self):   
        """
        Close the game play and return to question num choosing.
        Only trigger when use end game button, not X icon
        """
        root.deiconify()
        self.play_box.destroy()

class Help:
    def __init__(self,partner):
        """
        GUI for help box
        """
        background = "#ffe8cf"
        text="Capital Quiz is a program that generates questions a" \
        "bout which is the capital of a specific country.\nPoint rush is a mechanism of cap quiz. Everytime you answer a question correct, the point you can earn in " \
        "the next question is added by 50." \
        " It is added until you answer wrong. \nEg. Q1: +100p, Q2: +150p, Q3: +200p"
        
        # create help box
        self.help_box = Toplevel()
        self.help_box.protocol("WM_DELETE_WINDOW",partial(self.close_help,partner))

        # put frame in box
        self.help_frame = Frame(self.help_box,bg=background)
        self.help_frame.grid()
        
        # heading
        self.help_heading = Label(self.help_frame,text="Help/Info",
                                  font=("Arial","15","bold"),
                                   fg="#3a3a3a",bg=background)
        self.help_heading.grid(pady=5,padx=5,row=0)
        
        # help text
        self.help_text = Label(self.help_frame,text=text,
                                  font=("Arial","11"),
                                   fg="#3a3a3a",wraplength=300,justify="left",
                                   bg=background
                                   )
        self.help_text.grid(row=1,pady=2,padx=5)

        # dissmiss button
        self.dismiss_button = Button(self.help_frame,text="Dismiss",
                                  font=("Arial","15","bold"),
                                   fg="#ffffff",bg="#e2954c"
                                   ,command=partial(self.close_help,partner),width=10)
        self.dismiss_button.grid(pady=5,padx=5,row=2)
        
    def close_help(self,partner):       
        """
        Close help box and return to game play. Trigger when both close by X icon or dismiss button
        """
        self.help_box.destroy()
        partner.buttons_state("NORMAL") # return buttons state to normal

class Stats:
    def __init__(self,partner):
        """
        GUI for stats
        """
        question_answered=partner.current_question_num.get()    # get question answered

        # spacing and endline manually for the purpose of designing
        rounds_played = f"Rounds played: {question_answered}   \n\n"   
        total_score= f"Total Point: {partner.current_point.get()}   \n\n"

        # correct rate
        if question_answered==0:    # make sure the program don't divide anything by 0 T_T
            correct_rate = f"Correct rate: 0/0 (0%)         \n\n"
        else:
            correct_rate_num= int(partner.correct_num*100/question_answered)
            correct_rate = f"Correct rate: {partner.correct_num}/{question_answered} ({correct_rate_num}%)         \n\n"

        highest_point_rush= f"Highest point rush: +{partner.highest_streak}     \n"
        background = "#f3f3f3"
        text=rounds_played+total_score+correct_rate+highest_point_rush  # add everything together. Only need to call this to show every value

        # stat box
        self.stats_box = Toplevel()
        self.stats_box.protocol("WM_DELETE_WINDOW",partial(self.close_stats,partner))

        # frame
        self.stats_frame = Frame(self.stats_box,bg=background)
        self.stats_frame.grid()
        
        # heading
        self.stats_heading = Label(self.stats_frame,text="Statistics",
                                  font=("Arial","17","bold"),
                                   fg="#3a3a3a",bg=background)
        self.stats_heading.grid(pady=5,padx=40,row=0)
        
        # every main text in stats box
        self.stats_text = Label(self.stats_frame,text=text,
                                  font=("Arial","15"),
                                   fg="#434343",wraplength=600,justify="left",
                                   bg=background
                                   )
        self.stats_text.grid(row=1,pady=2,padx=40)
        
        # close button
        self.close_button = Button(self.stats_frame,text="Close",
                                  font=("Arial","15","bold"),
                                   fg="#ffffff",bg="#434343"
                                   ,command=partial(self.close_stats,partner),width=10)
        self.close_button.grid(pady=5,padx=40,row=2)

        
    def close_stats(self,partner):
        """
        Close stats box and return to game play. Trigger when both close by X icon or close button
        """
        self.stats_box.destroy()
        partner.buttons_state("NORMAL") # return buttons state to normal

# main
if __name__ == "__main__":
    root =Tk()
    root.title("Capital Quiz")
    StartGame()
    root.mainloop()
