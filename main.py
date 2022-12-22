import tkinter
import csv
import random

# ---------------------------- CONSTANTS ------------------------------- #
WATERMARK_TEXT = "Watermark"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
LIGHT_GREEN = "#E8F3D6"
DARK_BLUE = "#1C658C"
YELLOW = "#f7f5dd"
GREY = "#CFD2CF"
FONT_NAME = "Courier"
# FONT_NAME = "Sans Serif"
TEST_TIME = 60

display = ""
char_count = 0
word_lengths = []
correct_count = 0
current_word = 0
board_words = []
time_out = True
last_word = 0
game_on = False
countdown = 5


# ------------------------------Functionalities-------------------------
def on_key_press(event):
    global char_count, current_word, correct_count, last_word, game_on

    if (not time_out) or (last_word > 0):
        if event.char == " ":
            current_word += 1
            char_count = 0
            for i in range(current_word):
                char_count += word_lengths[i] + 1
            # char_count += len(input_field.get("1.0", "end-1c"))
            # count correct letters
            typed_in = input_field.get("1.0", "end-1c")
            length = min(len(typed_in), word_lengths[current_word - 1])
            for i in range(length):
                if typed_in[i] == board_words[current_word - 1][i]:
                    correct_count += 1
            cpm_label.config(text=f"CPM: {correct_count}")
            wpm_label.config(text=f"WPM: {round(correct_count / 5)}")

            input_field.delete("1.0", "end")
            if char_count >= len(display) - 1:
                refresh_board()

            if time_out:
                last_word -= 1
                results_label.config(text=f"Character per Minute: {correct_count}, "
                                          f"Word per Minute: {round(correct_count / 5)}")
                timer_label.config(text="Time's Up!")
                print(correct_count)
                game_on = False
                start_button.config(text="Start")
        else:
            typed_in = input_field.get("1.0", "end-1c")
            curr_position = char_count + len(typed_in)
            rest = display[curr_position::]
            word_board.delete(f"1.{curr_position}")
            word_board.insert(f"1.{curr_position}", rest)

            if len(input_field.get("1.0", "end-1c")) > 0:
                if typed_in[len(typed_in) - 1] == display[curr_position - 1]:
                    letter = word_board.get(f"1.{curr_position - 1}")
                    word_board.delete(f"1.{curr_position - 1}")
                    word_board.insert(f"1.{curr_position - 1}", letter)
                    word_board.tag_add("green", f"1.{curr_position - 1}")
                    word_board.tag_config("green", foreground="green")
                else:
                    letter = word_board.get(f"1.{curr_position - 1}")
                    word_board.delete(f"1.{curr_position - 1}")
                    word_board.insert(f"1.{curr_position - 1}", letter)
                    word_board.tag_add("red", f"1.{curr_position - 1}")
                    word_board.tag_config("red", foreground="red")


def refresh_board():
    word_board.delete("1.0", "end")
    global char_count, current_word, word_lengths, board_words
    current_word = 0
    char_count = 0
    numbers = []
    for i in range(6):
        numbers.append(random.randint(0, 999))
    board_words = [words[number] for number in numbers]
    word_lengths = [len(word) for word in board_words]
    for board_word in board_words:
        word_board.insert("end", board_word + " ")
    global display
    display = word_board.get("1.0", "end")
    return


def timer():
    global time_out, countdown
    # print(countdown)
    if countdown <= 0:
        time_out = True
        timer_label.config(text="Finishing Up Final Word...")
    else:
        time_out = False
        timer_label.config(text="Countdown: %d" % countdown)
        countdown -= 1
        window.after(1000, timer)


def start_game():
    global time_out, last_word, game_on, display, char_count, word_lengths, correct_count, current_word, \
        board_words, countdown
    char_count = 0
    word_lengths = []
    correct_count = 0
    current_word = 0
    refresh_board()
    cpm_label.config(text=f"CPM: {correct_count}")
    wpm_label.config(text=f"WPM: {round(correct_count / 5)}")
    results_label.config(text="")
    input_field.delete("1.0", "end")
    input_field.focus_set()
    if game_on:
        display = ""
        board_words = []
        countdown = 0
        game_on = False
        window.after(1000, start_game)
    else:
        game_on = True
        start_button.config(text="Reset")
        countdown = TEST_TIME
        timer()
        time_out = False
        last_word = 1


with open('1000en.csv', newline='') as csvfile:
    words = list(csv.reader(csvfile))
    words = [word[0] for word in words]

# --------------------------UI setup----------------------------

window = tkinter.Tk()
window.title("Typing Speed Test")
window.config(pady=50, padx=50)

heading_label = tkinter.Label(
    text="Type When Ready",
    fg=DARK_BLUE, font=(FONT_NAME, 20, "bold")
)
heading_label.grid(column=0, row=0, columnspan=3)

cpm_label = tkinter.Label(text="CPM: 0")
cpm_label.config(pady=20)
cpm_label.grid(column=0, row=1)

wpm_label = tkinter.Label(text="WPM: 0")
wpm_label.config(pady=20)
wpm_label.grid(column=2, row=1)

timer_label = tkinter.Label(text="Countdown: 60", font=(FONT_NAME, 15))
timer_label.config(pady=20)
timer_label.grid(column=1, row=1)

window.bind('<KeyPress>', on_key_press)

word_board = tkinter.Text(window,
                          font=('sans serif', 20),
                          width=50,
                          height=1,
                          pady=10,
                          )
word_board.grid(column=0, row=2, columnspan=3, pady=20)

input_label = tkinter.Label(text="Type Here:", fg=DARK_BLUE, font=(FONT_NAME, 20))
input_label.grid(column=0, row=3)

input_field = tkinter.Text(window,
                           background=LIGHT_GREEN,
                           foreground='black',
                           font=('sans serif', 20),
                           width=30,
                           height=1,
                           )
input_field.grid(column=1, row=3, columnspan=2, pady=20)

results_label = tkinter.Label(
    text=f"",
    font=('sans serif', 20),
)
results_label.config(pady=20)
results_label.grid(column=0, row=4, columnspan=3)

start_button = tkinter.Button(text="Start", command=start_game, width=11, font=(FONT_NAME, 15))
start_button.grid(column=0, row=5, columnspan=3)

# ----------------------Let the storm rage on!-------------
# word_board.tag_add("highlight", f"1.0", f"1.{word_lengths[0]}")
# word_board.tag_config("highlight", background=PINK)
window.mainloop()
