import tensorflow as tf
from keras.preprocessing import image
from .play_music import Music


class Predict():
    def __init__(self):
        """
        json_file = open("models/model-bw.json", "r")
        model_json = json_file.read()
        json_file.close()
        self.model=tf.keras.models.model_from_json(
            model_json, custom_objects=None
        )
        self.model.load_weights('models/model-bw.h5')"""
        self.interpreter = tf.lite.Interpreter(model_path="models/lite/model-online(class 8).tflite")
        self.interpreter.allocate_tensors()
        self.input_details,self.output_details = self.interpreter.get_input_details(),self.interpreter.get_output_details()
        self.music=Music()

        
    def predict(self,hand_index,img,verification_index):
        img = image.img_to_array(img)
        img= img.reshape(1,100,100,1)
        img = img/255
        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()
        proba = self.interpreter.get_tensor(self.output_details[0]['index'])
        proba= [round(each,5) for each in proba[0]]
        print(proba)
        top = max(proba)
        top_index=list(proba).index(top)
            
        class_name = ['Palm-Up', 'Thumb', 'Index Finger', 'Middle Finger',
                    'Ring Finger', 'Little Finger',"Down","Nothing"][top_index]
        if(top>0.97):
            if(verification_index not in [0,1,7,8,None]):
                if(verification_index==top_index):
                    self.music.play(hand_index,top_index)
                    return class_name
                else:
                    return "Nothing"
            else:
                self.music.play(hand_index,top_index)
                return class_name
        else:
            return "Nothing1"
