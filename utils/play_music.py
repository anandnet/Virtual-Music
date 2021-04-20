from pygame import mixer
import os
import json


PATH = os.path.dirname(__file__)


class Music():

    def __init__(self):
        self.active = [
            [False, False, False, False, False], [False, False, False, False, False]]
        mixer.init(channels=9)

        with open('utils/map_data.json', 'r') as file:
            self.current_map = json.load(file)

        # print(self.current_map)
        with open('utils/notes.json', 'r') as file:
            data = json.load(file)
        self.note_dict = {}
        for instr in data:
            self.note_dict[instr] = {}
            #print(data[instr])
            for each in data[instr]:
                try:
                #intr_name=["piano", "guitar", "violin", "xylophone", "drums"][int(instr)]
                    self.note_dict[instr][each.split(".")[0]] = mixer.Sound("assets/tones/"+instr+"/"+each)
                except Exception as e:
                    print(e)
        #print(self.note_dict)

    def play(self, hand_index, index):
        from utils.selected_instrument import selected_instr
        tune = None
        channel_ = mixer.Channel(0)
        if(index != 6 and index != 7 and index != 0):
            try:
                tune = self.note_dict[selected_instr][self.current_map[selected_instr][hand_index][str(index)]]
                channel_ = mixer.Channel(
                    index-1) if hand_index == 0 else mixer.Channel(4+index)
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
