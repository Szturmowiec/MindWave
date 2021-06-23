import threading
import numpy as np
import json
from NeuroSkyPy import NeuroSkyPy
import time
import os
from PIL import Image
from matplotlib import pyplot as plt


def display_image(filename):
    image = Image.open(filename)
    image_numpy = np.asarray(image)
    plt.imshow(image_numpy)
    plt.draw()
    plt.pause(2.1)
    plt.close('all')
    return


data = {}
neuropy = NeuroSkyPy.NeuroSkyPy("COM3", 57600)
neuropy.start()

while neuropy.attention == 0:
    print("waiting for measurement to begin...")
    time.sleep(1)

images_dir = os.path.abspath("images2")
for file in os.listdir(images_dir):
    image_data = {"attention": [], "meditation": [], "blinkStrength": [], "highAlpha": [], "lowAlpha": [],
                  "highBeta": [], "lowBeta": [], "delta": [], "lowGamma": [], "midGamma": [], "theta": []}
    image_path = os.path.join(images_dir, file)
    print("currently displayed image: " + file)
    image_thread = threading.Thread(target=display_image, args=(image_path,))
    image_thread.start()

    start = time.time()

    while time.time() - start < 2:
        image_data["attention"].append(neuropy.attention)
        image_data["meditation"].append(neuropy.meditation)
        image_data["blinkStrength"].append(neuropy.blinkStrength)
        image_data["highAlpha"].append(neuropy.highAlpha)
        image_data["lowAlpha"].append(neuropy.lowAlpha)
        image_data["highBeta"].append(neuropy.highBeta)
        image_data["lowBeta"].append(neuropy.lowBeta)
        image_data["delta"].append(neuropy.delta)
        image_data["theta"].append(neuropy.theta)
        image_data["lowGamma"].append(neuropy.lowGamma)
        image_data["midGamma"].append(neuropy.midGamma)
        time.sleep(0.2)

    data[file] = image_data
    image_thread.join()

neuropy.stop()
with open('brain_scan_2.json', 'w') as f:
    json.dump(data, f)

'''
def attention_callback(attention_value):
    """this function will be called everytime NeuroPy has a new value for attention"""
    print("Value of attention is: ", attention_value)
    return None


neuropy.setCallBack("attention", attention_callback)

try:
    while True:
        sleep(0.2)
        print(neuropy.attention)
finally:
    neuropy.stop()

sys.exit(0)


# Initializing the arrays required to store the data.
attention_values = np.array([])
meditation_values = np.array([])
delta_values = np.array([])
theta_values = np.array([])
lowAlpha_values = np.array([])
highAlpha_values = np.array([])
lowBeta_values = np.array([])
highBeta_values = np.array([])
lowGamma_values = np.array([])
highGamma_values = np.array([])
blinkStrength_values = np.array([])
time_array = np.array([])

tn = Telnet('127.0.0.1', 13854)

start = time.clock()

i = 0;
json_str = '{"enableRawOutput": true, "format": "Json"}'
tn.write(str.encode(json_str));

outfile = "null";
if len(sys.argv) > 1:
    outfile = sys.argv[len(sys.argv) - 1];
    outfptr = open(outfile, 'w');

eSenseDict = {'attention': 0, 'meditation': 0};
waveDict = {'lowGamma': 0, 'highGamma': 0, 'highAlpha': 0, 'delta': 0, 'highBeta': 0, 'lowAlpha': 0, 'lowBeta': 0,
            'theta': 0};
signalLevel = 0;

while time.clock() - start < 30:
    blinkStrength = 0;
    line = tn.read_until(str.encode('\r'));
    if len(line) > 20:
        timediff = time.clock() - start;
        line = line.decode("utf-8")
        dict = json.loads(str(line));
        if "poorSignalLevel" in dict:
            signalLevel = dict['poorSignalLevel'];
        if "blinkStrength" in dict:
            blinkStrength = dict['blinkStrength'];
        if "eegPower" in dict:
            waveDict = dict['eegPower'];
            eSenseDict = dict['eSense'];
        outputstr = str(timediff) + ", " + str(signalLevel) + ", " + str(blinkStrength) + ", " + str(
            eSenseDict['attention']) + ", " + str(eSenseDict['meditation']) + ", " + str(
            waveDict['lowGamma']) + ", " + str(waveDict['highGamma']) + ", " + str(waveDict['highAlpha']) + ", " + str(
            waveDict['delta']) + ", " + str(waveDict['highBeta']) + ", " + str(waveDict['lowAlpha']) + ", " + str(
            waveDict['lowBeta']) + ", " + str(waveDict['theta']);
        time_array = np.append(time_array, [timediff]);
        blinkStrength_values = np.append(blinkStrength_values, [blinkStrength]);
        lowGamma_values = np.append(lowGamma_values, [waveDict['lowGamma']]);
        highGamma_values = np.append(highGamma_values, [waveDict['highGamma']]);
        highAlpha_values = np.append(highAlpha_values, [waveDict['highAlpha']]);
        delta_values = np.append(delta_values, [waveDict['delta']]);
        lowBeta_values = np.append(lowBeta_values, [waveDict['lowBeta']]);
        highBeta_values = np.append(highBeta_values, [waveDict['highBeta']]);
        theta_values = np.append(theta_values, [waveDict['theta']]);
        lowAlpha_values = np.append(lowAlpha_values, [waveDict['lowAlpha']]);
        attention_values = np.append(attention_values, [eSenseDict['attention']]);
        meditation_values = np.append(meditation_values, [eSenseDict['meditation']]);
        print(outputstr);
        if outfile != "null":
            outfptr.write(outputstr + "\n");

person_name = input('Enter the name of the person: ')
blink_label = input('Enter left or right eye blink(1 for left, 2 for right): ')
time_starting = input('When does TGC start: ')
lefty_righty = input('Is the person left-handed or right-handed: ')
time_blinking = input('The time of the blink: ')

# Data Recorded for a single person
data_row = pd.DataFrame(
    {'Name': person_name, 'attention': [attention_values], 'meditation': [meditation_values], 'delta': [delta_values],
     'theta': [theta_values], 'lowAlpha': [lowAlpha_values], 'highAlpha': [highAlpha_values],
     'lowBeta': [lowBeta_values], 'highBeta': [highBeta_values],
     'lowGamma': [lowGamma_values], 'highGamma': [highGamma_values], 'blinkStrength': [blinkStrength_values],
     'time': [time_array], 'LOR': blink_label})

# Reading the data stored till now
dataset = pd.read_csv('data_eeg.csv')

from numpy import nan as Nan

dataset = dataset.append(pd.Series([blink_label, person_name, [attention_values], [blinkStrength_values], [delta_values]
                                       , [highAlpha_values], [highBeta_values], [highGamma_values], [lowAlpha_values],
                                    [lowBeta_values], [lowGamma_values], [meditation_values],
                                    [theta_values], [time_array], time_starting, lefty_righty, time_blinking],
                                   index=['LOR', 'Name', 'attention', 'blinkStrength', 'delta', 'highAlpha', 'highBeta',
                                          'highGamma', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'theta', 'time',
                                          'time_start', 'LTYRTY', 'time_blink']), ignore_index=True)

# Appending and storing the data in the same csv
# dataset.append(data_row)
dataset.to_csv('data_eeg.csv')

tn.close();
# outfptr.close();
'''
