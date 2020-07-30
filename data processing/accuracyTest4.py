import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import signal

def find_error_score(y1, y2):
    n = len(y1)
    error_total = 0
    for i in range(len(y1)):
        error_total += abs(y1[i] - y2[i])
    return error_total/n

def lag_finder(y1, y2, sr, leftPhone, rightPhone):
    # n = len(y1)

    # corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])

    # delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    # delay = delay_arr[np.argmax(corr)]
    # print('y2 is ' + str(delay) + ' behind y1')
    # max_corr = np.amax(corr)
    # print('max correlation is: ' + str(max_corr))

    plt.figure(figsize=(20,10))
    plt.subplots_adjust(hspace=0.6)

    plt.subplot(5,1,1)
    plt.plot(leftPhone[:,0], color='orange', label='left')
    plt.plot(rightPhone[:,0], color='blue', label='right')
    error_score = find_error_score(leftPhone[:,0], rightPhone[:,0])
    plt.title("X error_score = " + str(error_score))
    plt.ylabel('G')

    # error_score = error_score(leftPhone, rightPhone)
    # print(error_score)

    plt.subplot(5,1,2)
    plt.plot(leftPhone[:,1], color='green', label='left')
    plt.plot(rightPhone[:,1], color='purple', label='right')
    error_score = find_error_score(leftPhone[:,1], rightPhone[:,1])
    plt.title("Y error_score = " + str(error_score))
    plt.ylabel('G')

    plt.subplot(5,1,3)
    plt.plot(leftPhone[:,2], color='orange', label='left')
    plt.plot(rightPhone[:,2], color='blue', label='right')
    error_score = find_error_score(leftPhone[:,2], rightPhone[:,2])
    plt.title("Z error_score = " + str(error_score))
    plt.ylabel('G')

    plt.subplot(5,1,4)
    plt.plot(y1, color='green', label='left')
    plt.plot(y2, color='purple', label='right')
    error_score = find_error_score(y1, y2)
    plt.title("Magnitudes error_score = " + str(error_score))
    plt.ylabel('G')

    # plt.subplot(5,1,5)
    # plt.plot(delay_arr, corr)
    # max_corr_title = 'max correlation is: ' + str(round(max_corr,2)*100) + '%'
    # plt.title('Lag: ' + str(np.round(delay, 3)) + ' s ' + max_corr_title)
    # plt.xlabel('Lag')
    # plt.ylabel('Correlation coeff')

    # plt.savefig('Figure_1.png')
    plt.show()

def syncSignals(leftPhone, rightPhone):
    # find which recording is longer
    leftPhoneShorter = True
    shorterRec = leftPhone
    longerRec = rightPhone
    if len(leftPhone) > len(rightPhone):
        leftPhoneShorter = False
        shorterRec = rightPhone
        longerRec = leftPhone

    lenShorterRec = len(shorterRec)
    lenLongerRec = len(longerRec)
    numSteps = lenLongerRec - lenShorterRec
    # take the error_score score at ever shift step
    error_scores = []
    for i in range(numSteps):
        start = i
        end = -(numSteps - i)
        error_scores.append(find_error_score(shorterRec, longerRec[start:end]))

    # print("error score", error_scores)
    summed_error_score = []
    for error in error_scores:
        sum = error[0] + error[1] + error[2]
        summed_error_score.append(sum)
    shiftAmount = np.argmin(summed_error_score)
    start = shiftAmount
    end = -(numSteps - shiftAmount)
    # print("start end num steps ", start, end, numSteps)
    longerRec = longerRec[start:end]

    # print(error_scores)
    # plt.figure(figsize=(20,10))
    # plt.subplots_adjust(hspace=0.6)

    # plt.subplot(5,1,1)
    # plt.plot(error_scores)
    # plt.title("X")
    # plt.ylabel('G')
    # plt.show()
    
    if leftPhoneShorter:
        return shorterRec, longerRec
    else:
        return longerRec, shorterRec
        



def make_graph(leftPhone_str, rightPhone_str):
    leftPhone_json = json.loads(leftPhone_str)
    leftPhone = np.array(leftPhone_json)
    leftPhone = leftPhone[:,1:4].astype(np.float)

    rightPhone_json = json.loads(rightPhone_str)
    rightPhone = np.array(rightPhone_json)
    rightPhone = rightPhone[:,1:4].astype(np.float)

    # # print(leftPhone)
    # print(leftPhone[0])
    # print(rightPhone[0])

    # sync signals time wise
    leftPhone, rightPhone = syncSignals(leftPhone, rightPhone)

    leftPhone_mag = []
    rightPhone_mag = []
    for row in leftPhone:
        leftPhone_mag.append(abs(row[0]) + abs(row[1]) + abs(row[2]))
    for row in rightPhone:
        rightPhone_mag.append(abs(row[0]) + abs(row[1]) + abs(row[2]))


    # shorten longest recording
    shortest = len(leftPhone_mag)
    if len(rightPhone_mag) < shortest:
        shortest = len(rightPhone_mag)

    leftPhone_mag = leftPhone_mag[:shortest]
    rightPhone_mag = rightPhone_mag[:shortest]

    leftPhone = leftPhone[:shortest]
    rightPhone = rightPhone[:shortest]


    lag_finder(leftPhone_mag, rightPhone_mag, shortest, leftPhone, rightPhone)


# main
fileContents = {}
# fileName = "testDataArduino/armRecording.json"
# fileName = "testDataPhone/accuracyTestOneplusIpadZCorrected.json"
# fileName = "testDataPhone/derektestmovingbotharms.json"
fileName = "testDataPhone/accuracyTestIphone6sIphone6s.json"
# fileName = "testDataArduino/hw1hw2.json"

with open(fileName) as f:
    fileContents = json.load(f)
# print(fileContents)
make_graph(fileContents["data"]["leftPhone"], fileContents["data"]["rightPhone"])

# leftPhone_str = '[["8:45:38 PM.923",0.7578277587890625,0.963470458984375,-0.1989593505859375],["8:45:39 PM.24",0.636322021484375,0.6524658203125,0.1717681884765625],["8:45:39 PM.128",0.639801025390625,0.7425537109375,-0.1177215576171875],["8:45:39 PM.236",0.584716796875,0.57794189453125,0.079193115234375],["8:45:39 PM.333",0.7669219970703125,0.7337646484375,-0.0362548828125],["8:45:39 PM.435",0.9217071533203125,1.0575103759765625,-0.037750244140625],["8:45:39 PM.525",0.69561767578125,0.6256561279296875,-0.0250396728515625],["8:45:39 PM.635",0.5973968505859375,0.6930084228515625,-0.139495849609375],["8:45:39 PM.731",0.5237884521484375,0.547271728515625,-0.0575714111328125],["8:45:39 PM.831",0.596435546875,0.8303375244140625,-0.107452392578125],["8:45:39 PM.932",0.682647705078125,0.9236602783203125,-0.061065673828125],["8:45:40 PM.33",0.707122802734375,0.87469482421875,-0.2091064453125],["8:45:40 PM.130",0.6315460205078125,0.6484527587890625,0.110015869140625],["8:45:40 PM.222",0.5441436767578125,0.649566650390625,0.0097198486328125],["8:45:40 PM.336",0.6026153564453125,0.6825103759765625,-0.0190582275390625],["8:45:40 PM.424",0.80499267578125,0.750274658203125,0.002593994140625],["8:45:40 PM.532",1.021209716796875,1.0107879638671875,0.08245849609375],["8:45:40 PM.621",0.7463226318359375,0.5617523193359375,-0.0070037841796875],["8:45:40 PM.732",0.6147308349609375,0.7577056884765625,-0.13372802734375],["8:45:40 PM.820",0.5197906494140625,0.6105804443359375,-0.0854034423828125],["8:45:40 PM.931",0.549835205078125,0.825164794921875,-0.059814453125],["8:45:41 PM.20",0.7377166748046875,0.9894561767578125,0.0134124755859375],["8:45:41 PM.131",0.707000732421875,0.709381103515625,-0.179962158203125],["8:45:41 PM.219",0.6629791259765625,0.494232177734375,0.119049072265625],["8:45:41 PM.321",0.5894622802734375,0.5980377197265625,-0.07196044921875],["8:45:41 PM.421",0.72772216796875,0.619354248046875,-0.007537841796875],["8:45:41 PM.521",0.828094482421875,0.730804443359375,-0.079986572265625],["8:45:41 PM.620",0.9078216552734375,0.89373779296875,-0.097564697265625],["8:45:41 PM.720",0.72052001953125,0.748565673828125,0.006561279296875],["8:45:41 PM.817",0.5552215576171875,0.6125030517578125,-0.0700836181640625],["8:45:41 PM.917",0.5409698486328125,0.6555938720703125,-0.003509521484375],["8:45:42 PM.19",0.6669921875,0.9316253662109375,-0.1190338134765625],["8:45:42 PM.119",0.7091064453125,0.9773712158203125,-0.1338958740234375],["8:45:42 PM.216",0.631744384765625,0.6078643798828125,0.168609619140625],["8:45:42 PM.318",0.66717529296875,0.672119140625,0.0062103271484375],["8:45:42 PM.415",0.70489501953125,0.6399993896484375,0.0015411376953125],["8:45:42 PM.515",0.7320709228515625,0.7185516357421875,-0.002655029296875],["8:45:42 PM.615",0.8772735595703125,1.0036163330078125,-0.1153564453125],["8:45:42 PM.715",0.5130157470703125,0.8079833984375,0.09234619140625],["8:45:42 PM.814",0.3875579833984375,0.820587158203125,-0.101837158203125],["8:45:42 PM.914",0.4052886962890625,0.73345947265625,0.004241943359375],["8:45:43 PM.13",0.5171661376953125,0.90948486328125,-0.132720947265625],["8:45:43 PM.113",0.75341796875,1.0477447509765625,-0.0627288818359375],["8:45:43 PM.211",0.589630126953125,0.7214508056640625,-0.018646240234375],["8:45:43 PM.313",0.6416473388671875,0.7068939208984375,0.1392364501953125],["8:45:43 PM.411",0.6187591552734375,0.6065673828125,0.1495819091796875],["8:45:43 PM.510",0.638641357421875,0.7574615478515625,0.0273895263671875],["8:45:43 PM.610",0.642669677734375,0.848724365234375,-0.0487823486328125],["8:45:43 PM.711",0.6768035888671875,0.8422698974609375,-0.166168212890625],["8:45:43 PM.809",0.6055908203125,0.9166259765625,0.0193328857421875],["8:45:43 PM.909",0.478424072265625,0.7371673583984375,-0.0925140380859375],["8:45:44 PM.9",0.4732513427734375,0.6968536376953125,-0.00250244140625],["8:45:44 PM.109",0.6040496826171875,0.899444580078125,-0.092315673828125],["8:45:44 PM.208",0.840362548828125,1.143524169921875,-0.0435028076171875],["8:45:44 PM.308",0.6567535400390625,0.6137847900390625,-0.0130157470703125],["8:45:44 PM.408",0.6442413330078125,0.583526611328125,0.018707275390625],["8:45:44 PM.507",0.543121337890625,0.643463134765625,0.08843994140625],["8:45:44 PM.607",0.634674072265625,0.6902008056640625,-0.0187225341796875],["8:45:44 PM.707",0.838775634765625,0.91461181640625,-0.005706787109375],["8:45:44 PM.806",0.7969207763671875,0.76531982421875,-0.12176513671875],["8:45:44 PM.905",0.609710693359375,0.6892852783203125,0.0161590576171875],["8:45:45 PM.5",0.5013580322265625,0.676116943359375,-0.1343994140625],["8:45:45 PM.104",0.5350799560546875,0.685638427734375,-0.0387420654296875],["8:45:45 PM.204",0.66082763671875,0.9003448486328125,-0.0993804931640625],["8:45:45 PM.305",0.732208251953125,1.0260772705078125,-0.221527099609375],["8:45:45 PM.404",0.662872314453125,0.6577911376953125,0.2567291259765625],["8:45:45 PM.503",0.6202850341796875,0.6720123291015625,-0.0619049072265625],["8:45:45 PM.603",0.5766143798828125,0.673095703125,0.0965423583984375],["8:45:45 PM.703",0.786590576171875,0.7604522705078125,-0.0047760009765625],["8:45:45 PM.802",0.9748687744140625,1.0157623291015625,-0.0167388916015625],["8:45:45 PM.902",0.701690673828125,0.628936767578125,-0.03424072265625],["8:45:46 PM.2",0.6358795166015625,0.70111083984375,-0.0968475341796875],["8:45:46 PM.102",0.562347412109375,0.5825042724609375,-0.027557373046875],["8:45:46 PM.201",0.583709716796875,0.7913970947265625,-0.0748443603515625],["8:45:46 PM.301",0.8311767578125,1.06201171875,-0.0076751708984375],["8:45:46 PM.401",0.63665771484375,0.71112060546875,-0.10516357421875],["8:45:46 PM.500",0.6682586669921875,0.614593505859375,0.1214752197265625],["8:45:46 PM.600",0.6268310546875,0.628875732421875,-0.0912017822265625],["8:45:46 PM.660",0.6268310546875,0.628875732421875,-0.0912017822265625]]'
# rightPhone_str = '[["20:45:39.548",0.64799964427948,-0.6820005774497986,0.10400059819221497],["20:45:39.645",0.5579996109008789,-0.6300002336502075,-0.06999967992305756],["20:45:39.747",0.7179993391036987,-0.8160001039505005,-0.059999506920576096],["20:45:39.847",0.8499994874000549,-1.0019999742507935,-0.06599929928779602],["20:45:39.960",0.8279997110366821,-0.6500006318092346,-0.15999971330165863],["20:45:40.60",0.7159999012947083,-0.5240002274513245,-0.05200029909610748],["20:45:40.165",0.6980005502700806,-0.5560001730918884,-0.12799978256225586],["20:45:40.280",0.9220001101493835,-0.7240006923675537,0.010000176727771759],["20:45:40.380",1.0519993305206299,-0.8900001645088196,-0.030000530183315277],["20:45:40.488",0.8040005564689636,-0.5660003423690796,-0.03799973800778389],["20:45:40.586",0.6539994478225708,-0.7400006651878357,0.18799927830696106],["20:45:40.695",0.5219992995262146,-0.6820005774497986,0.015999972820281982],["20:45:40.798",0.6660006046295166,-0.7479998469352722,-0.06599929928779602],["20:45:40.900",0.9139993786811829,-0.9459993243217468,-0.23200036585330963],["20:45:40.999",0.7899999618530273,-0.6579998135566711,-0.004000382032245398],["20:45:41.106",0.8260003328323364,-0.5899995565414429,-0.03799973800778389],["20:45:41.206",0.64799964427948,-0.5020005106925964,-0.014000559225678444],["20:45:41.313",0.737999677658081,-0.6340006589889526,-0.05600067973136902],["20:45:41.418",1.023999810218811,-0.8420003056526184,-0.21600039303302765],["20:45:41.526",0.9499996900558472,-0.5880001187324524,0.09000003337860107],["20:45:41.626",0.7339993119239807,-0.6080005168914795,-0.042000122368335724],["20:45:41.728",0.6620001792907715,-0.5359998345375061,0.004000382032245398],["20:45:41.838",0.6360000371932983,-0.6739997863769531,-0.07999985665082932],["20:45:41.937",0.7899999618530273,-0.7639998197555542,-0.12199997901916504],["20:45:42.40",0.8940005898475647,-0.8260003328323364,0.16200068593025208],["20:45:42.146",0.9019997715950012,-0.5140000581741333,-0.18400046229362488],["20:45:42.251",0.663999617099762,-0.4960006773471832,0.008000764064490795],["20:45:42.350",0.753999650478363,-0.6219995021820068,-0.06399989128112793],["20:45:42.452",0.9779992699623108,-0.8859997987747192,-0.10799942165613174],["20:45:42.560",0.8539998531341553,-0.5280006527900696,0.024000735953450203],["20:45:42.661",0.7599994540214539,-0.6219995021820068,-0.0360003262758255],["20:45:42.761",0.7040002942085266,-0.6180006861686707,0.04799991473555565],["20:45:42.859",0.6780001521110535,-0.6660006046295166,-0.06800027191638947],["20:45:42.972",0.8699998259544373,-0.9939992427825928,-0.16200068593025208],["20:45:43.75",0.7520002126693726,-0.6080005168914795,0.030000530183315277],["20:45:43.179",0.7959997653961182,-0.5639994144439697,-0.1179995983839035],["20:45:43.290",0.7439994812011719,-0.5039998888969421,-0.16599951684474945],["20:45:43.394",0.7919993996620178,-0.6200000643730164,-0.033999357372522354],["20:45:43.505",1.0619995594024658,-0.9019997715950012,-0.12000057101249695],["20:45:43.612",0.8439996838569641,-0.5300000309944153,-0.014000559225678444],["20:45:43.720",0.785999596118927,-0.7219997048377991,0.08400024473667145],["20:45:43.816",0.6720004081726074,-0.6240004897117615,0.004000382032245398],["20:45:43.928",0.6140002608299255,-0.7260000705718994,-0.04799991473555565],["20:45:44.28",0.7479998469352722,-0.7680001854896545,-0.19600003957748413],["20:45:44.135",0.8100003600120544,-0.663999617099762,0],["20:45:44.241",0.9499996900558472,-0.6099998950958252,-0.07599947601556778],["20:45:44.351",0.7140005230903625,-0.4920003116130829,-0.05600067973136902],["20:45:44.448",0.7460004687309265,-0.6059995293617249,-0.11400077491998672],["20:45:44.556",0.9819996356964111,-0.7460004687309265,-0.07800044864416122],["20:45:44.666",1.0399997234344482,-0.7300004959106445,-0.015999972820281982],["20:45:44.778",0.7580000162124634,-0.6820005774497986,-0.14399975538253784],["20:45:44.865",0.6219995021820068,-0.6279993057250977,0.021999767050147057],["20:45:44.972",0.6300002336502075,-0.6200000643730164,-0.07400006800889969],["20:45:45.74",0.7179993391036987,-0.7479998469352722,-0.059999506920576096],["20:45:45.179",0.8379998803138733,-0.939999520778656,-0.02799956128001213],["20:45:45.279",0.7880005836486816,-0.5880001187324524,-0.12399939447641373],["20:45:45.381",0.7819992303848267,-0.5319994688034058,-0.10799942165613174],["20:45:45.488",0.7360002398490906,-0.5479994416236877,-0.13399957120418549],["20:45:45.594",0.8680004477500916,-0.6679999828338623,-0.010000176727771759],["20:45:45.694",1.1180001497268677,-0.939999520778656,0.001999413128942251],["20:45:45.799",0.7680001854896545,-0.5880001187324524,-0.1900002509355545],["20:45:45.903",0.7580000162124634,-0.6739997863769531,0.1460007131099701],["20:45:46.2",0.6219995021820068,-0.6520000100135803,0.04399953410029411],["20:45:46.112",0.6760007739067078,-0.7739999890327454,-0.06399989128112793],["20:45:46.210",0.8360005021095276,-0.9619992971420288,-0.10600000619888306],["20:45:46.310",0.7479998469352722,-0.6040000915527344,-0.13799995183944702],["20:45:46.410",0.7980007529258728,-0.5479994416236877,-0.10000021755695343],["20:45:46.538",0.7119995355606079,-0.5120006799697876,0.001999413128942251],["20:45:46.636",0.8520004749298096,-0.6219995021820068,-0.0940004214644432],["20:45:46.739",1.106000542640686,-0.9339997172355652,-0.09199944883584976],["20:45:46.854",0.8300006985664368,-0.5739995837211609,-0.18199948966503143],["20:45:47.199",0.7520002126693726,-0.7119995355606079,0.06999967992305756],["20:45:47.232",0.6140002608299255,-0.5660003423690796,-0.07400006800889969],["20:45:47.265",0.6140002608299255,-0.5660003423690796,-0.07400006800889969]]'
# make_graph(leftPhone_str, rightPhone_str)
