from pygame import mixer
import os
import json
import numpy as np


PATH = os.path.dirname(__file__)


class Music():

    def __init__(self):
        self.active = [
            [False, False, False, False, False], [False, False, False, False, False]]
        mixer.init(channels=9)

        with open('utils/map_data.json', 'r') as file:
            self.current_map = json.load(file)
        
        print(self.current_map)
        with open('utils/notes.json', 'r') as file:
            data = json.load(file)
        self.note_dict = {}
        for instr in data:
            self.note_dict[instr] = {}
            for each in data[instr]:
                intr_name=["piano", "guitar", "violin", "xylophone", "drums"][int(instr)]
                self.note_dict[instr][each] = mixer.Sound(
                    "assets/tones/"+intr_name+"/"+each+".wav")
        #print(self.note_dict)

    def play(self, hand_index, index):
        from utils.selected_instrument import inst_indx
        tune=None
        channel_=mixer.Channel(0)
        if(index!=6 and index!=7 and  index!=0):
            try:
                tune=self.note_dict[str(inst_indx)][self.current_map[str(inst_indx)][hand_index][str(index)]]
                channel_=mixer.Channel(index-1) if hand_index==0 else mixer.Channel(4+index)
            except:
                pass


        if(index == 0):
            self.active[hand_index] = [False, False, False, False, False]
            pass
        elif(index == 1 and not self.active[hand_index][0] and tune):
            self.active[hand_index] = [True, False, False, False, False]
            channel_.play(tune)

        elif(index == 2 and not self.active[hand_index][1] and tune):
            channel_.play(tune)
            self.active[hand_index] = [False, True, False, False, False]

        elif(index == 3 and not self.active[hand_index][2] and tune):
            channel_.play(tune)
            self.active[hand_index] = [False, False, True, False, False]

        elif(index == 4 and not self.active[hand_index][3] and tune):
            channel_.play(tune)
            self.active[hand_index] = [False, False, False, True, False]

        elif(index == 5 and not self.active[hand_index][4] and tune):
            channel_.play(tune)
            self.active[hand_index] = [False, False, False, False, True]
