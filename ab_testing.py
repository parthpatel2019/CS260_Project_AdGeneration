from tkinter import *
from PIL import ImageTk, Image
import scipy.stats
import random

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
"""
Class that runs A/B testing, polling the user to determine which image is preferred
in a Head-to-Head comparison. Used for a proof of concept - actual A/B testing would
have to be run on an ad engine.
"""
class ABTester:
    def __init__(self, base_image_pil, dream_booth_image_pil, total_particpants):
        self.base_image_selects = 0
        self.dream_booth_image_selects = 0
        self.score = 0
        self.base_image_pil = base_image_pil.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        self.dream_booth_image_pil = dream_booth_image_pil.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        self.total_participants = total_particpants

    """
    Run polling prompt to allow a user to pick/score one image over the other.
    """
    def run_polling_prompt(self):
        def handle_submit(root_tk, selection_variable):
            if selection_variable.get() == 1:
                self.base_image_selects += 1
                root_tk.destroy()
            elif selection_variable.get() == 2:
                self.dream_booth_image_selects += 1
                root_tk.destroy()

        # Randomize the placement of the advertisements on the screen.
        base_image_left = random.randint(0, 1) == 0
        base_image_relx = 0.25 if base_image_left else 0.75
        dream_booth_image_relx = 0.75 if base_image_left else 0.25

        # Set up TK
        root_tk = Tk()
        root_tk.title('A/B Testing Prompt - Pick Your Favorite Advertisement!')
        root_tk.attributes('-fullscreen', True)
        root_tk.bind('<Escape>', lambda _: root_tk.destroy())

        # Display both images.
        base_image = ImageTk.PhotoImage(self.base_image_pil)
        base_image_label = Label(image=base_image)
        base_image_label.place(relx=base_image_relx, rely=0.2, anchor=CENTER)

        dream_booth_image = ImageTk.PhotoImage(self.dream_booth_image_pil)
        dream_booth_image_label = Label(image=dream_booth_image)
        dream_booth_image_label.place(relx=dream_booth_image_relx, rely=0.2, anchor=CENTER)

        # Initial Question - (Binary Choice) Which Advertisement is preferred?
        selection_variable = IntVar(value=0)

        preferred_advertisement_question_prompt = Label(
            text='Which advertisement do you prefer?',
            font=('Comic Sans MS', 30, 'bold')
        )
        preferred_advertisement_question_prompt.pack(side=TOP, pady=(600, 0))

        prefer_base_image_radio = Radiobutton(
            text='The Advertisement on the Left.' if base_image_relx == 0.25 else 'The Advertisement on the Right.',
            font=('Comic Sans MS', 20),
            variable=selection_variable,
            value=1,
            command=(lambda: selection_variable.set(1))
        )
        prefer_base_image_radio.pack()

        prefer_dream_booth_image_radio = Radiobutton(
            text='The Advertisement on the Left.' if dream_booth_image_relx == 0.25 else 'The Advertisement on the Right.',
            font=('Comic Sans MS', 20),
            variable=selection_variable,
            value=2,
            command=(lambda: selection_variable.set(2))
        )
        prefer_dream_booth_image_radio.pack()

        submit_button = Button(
            text='Submit',
            font=('Comic Sans MS', 24, 'bold'),
            command=(lambda: handle_submit(root_tk, selection_variable))
        )
        submit_button.pack()


        root_tk.mainloop()

    """
    Run the class, performing A/B testing via manual input by allowing the participants
    to select one image over the other and score them.
    """
    def run(self):
        for _ in range(self.total_participants):
            self.run_polling_prompt()
        self.score = self.dream_booth_image_selects / self.total_participants
        return self.score
    """
    Run the class, performing simulated A/B testing via automatically generating the score
    given some mean and standard deviation (both in [0, 1]). Effectively bypasses true A/B testing for demo purposes.
    """
    def run_bypass(self, mean, std_dev):
        return scipy.stats.truncnorm.rvs(
          -mean / std_dev, mean / std_dev, loc=mean,scale=std_dev, size=1
        )[0]
