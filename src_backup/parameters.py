#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================
# @File   parameters.py
# @Date   Created on 2019/07/13
# @Author Hehesheng
# ==============================

strTitle = "Brain Wave Analyst"
strStatuBarColor = "#008200"
strStatuBarInit = "Ready"
strClearReceive = "Clear Receive"
strSend = "Send"
strSocketSettings = "Network"
strSocketAddress = "IP:"
strSocketDefaultAddress = "127.0.0.1"
strSocketPort = "Port:"
strSocketDefaultPort = "9999"
strSocketButtonStart = "Start"
strSocketButtonStop = "Stop"
strOneNETDeviceId = "dev id:"

strLearnSettings = "Learn"
strEmotionHappy = "happy"
strEmotionSad = "sad"
strEmotionRelax = "relax"
strEmotionAttention = "attention"
strEmotionAngry = "angry"
strEmotionScare = "scare"
strLearnButton = "Learn emotion"
strWaitting = "Waiting..."
strAnalysisButton = "Analysis"

strAlgorithmText = "algorithm"
strAlgorithmVector = "Vector"
strAlgorithmNN = "NN"
strAlgorithmRealTime = "real time"
strAlgorithmEmotion = "emotion"

strOnenetTgamName = "tgam_pack"
strOnenetAd59Name = "ad59_pack"

radioButtonDefault = "font: bold; font-size:30px;"
radioButtonSelected = "background-color: red;"

strTest1 = """
{
    "tick":	13959,
    "type":	"AD5933",
    "start":	1000,
    "end":	3000,
    "len":	10,
    "real":	[-3725, -145, -9366, 4197, -21410, -18089, 19280, 29000, 16448, -11977],
    "image":	[-15570, -30921, -21185, 19271, 22350, -16044, -31654, -27809, -7325, 28519]
}
"""

strTest2 = """
{
    "tick":	161419,
    "type":	"TGAM",
    "raw_data":	{
        "len":	512,
        "raw":	[16808, 32330, 12222, 30465, 18509, 19173, 9967, 26007, 2838, 25316, 23797, 17994, 15367, 28053, 28690, 18048, 4286, 17666, 2027, 27533, 1012, 2744, 17344, 26478, 25499, 29890, 12418, 27817, 19593, 1040, 14006, 15063, 5547, 27008, 26439, 15442, 4322, 4700, 19348, 9718, 30428, 11337, 5336, 30853, 17286, 27288, 11127, 23114, 13477, 13226, 2226, 17694, 24131, 12923, 7433, 28899, 11449, 12885, 16357, 12650, 31583, 14111, 25408, 13731, 17178, 7604, 3640, 20773, 15373, 16856, 11243, 22166, 30842, 19508, 21112, 25541, 27078, 16525, 21132, 6756, 4786, 14639, 31756, 11816, 30054, 9036, 5074, 16467, 15388, 757, 19411, 10908, 17676, 31409, 19147, 20697, 25355, 19906, 1773, 31561, 29578, 9976, 29454, 19587, 26454, 8403, 22004, 11242, 27613, 12685, 11286, 3294, 13944, 30628, 20404, 9057, 5357, 24062, 2997, 6645, 16603, 16622, 19459, 25577, 15470, 18883, 25860, 24713, 30077, 17737, 12065, 30356, 31451, 14123, 9692, 16996, 898, 10259, 6928, 948, 23541, 16210, 26805, 27964, 26747, 18651, 28437, 15062, 11952, 7985, 18381, 5759, 1936, 2848, 20437, 9852, 23426, 5583, 29300, 13249, 17986, 11157, 21324, 885, 23245, 22325, 20989, 1917, 9299, 30029, 3159, 12925, 1958, 16159, 16583, 10487, 12441, 2230, 28142, 27508, 26624, 24680, 7485, 30814, 28920, 12424, 15857, 24266, 7586, 24701, 17469, 11409, 26402, 32104, 32284, 17565, 20411, 22758, 23242, 21853, 26515, 20444, 16917, 11565, 7021, 25690, 28940, 1578, 1956, 13988, 286, 3848, 4386, 21729, 17877, 6514, 6895, 10982, 1970, 10360, 15716, 22107, 5640, 26425, 22906, 10970, 22481, 16366, 26809, 6086, 31139, 27015, 12195, 27533, 25266, 26818, 31658, 12304, 3356, 25590, 25563, 20102, 1084, 27385, 15052, 31211, 3465, 7787, 6598, 19762, 32737, 19977, 16099, 17544, 29464, 20068, 22024, 1068, 28300, 31427, 21528, 17018, 23874, 2719, 28778, 4532, 28565, 28091, 23746, 15568, 17854, 3394, 135, 10953, 24741, 21508, 25759, 17221, 543, 16279, 20585, 21807, 4403, 8992, 10335, 27798, 8411, 11062, 6639, 24228, 12070, 22988, 12820, 27320, 2988, 10282, 5694, 12489, 10450, 7003, 24708, 23423, 12551, 32643, 3967, 3883, 2823, 23014, 4895, 26763, 29008, 3922, 11460, 26001, 10983, 30349, 6108, 410, 6951, 6301, 14254, 568, 27456, 3966, 22067, 1757, 27044, 10728, 6502, 25047, 18166, 20650, 12250, 19463, 7819, 15013, 28391, 12147, 29204, 2176, 24033, 18611, 12778, 32515, 4034, 3285, 3397, 9539, 1586, 28042, 23076, 7845, 4218, 20523, 12625, 26723, 8170, 26308, 22432, 26792, 9996, 28189, 23132, 27404, 25982, 24238, 27430, 15756, 29176, 4780, 10198, 31450, 26917, 11984, 15849, 16382, 30667, 9309, 28839, 2611, 2464, 26600, 6544, 5393, 2197, 26284, 19439, 24662, 10893, 11789, 9712, 11517, 11106, 20787, 31235, 2489, 10935, 8150, 32661, 7505, 10772, 16199, 11646, 26964, 28213, 4460, 6368, 31487, 3319, 15476, 20859, 28640, 23692, 6453, 23089, 31848, 13417, 11558, 15567, 27169, 16189, 9669, 12805, 1492, 30373, 13695, 21759, 17278, 2469, 14382, 17014, 6772, 30450, 10201, 14651, 20547, 28326, 31396, 21417, 25320, 12321, 11638, 14171, 30282, 13697, 3337, 23887, 19522, 14108, 25778, 28039, 20869, 19167, 912, 28282, 5952, 16329, 25893, 3894, 31893, 5466, 9808, 5931, 28101, 29160, 10804, 21990, 3166, 2175, 23382, 9942, 23950, 14481, 11565, 304, 8813, 15684, 4776, 26919, 32048, 6342, 3617, 9734, 11174, 25982, 30342, 11711, 5787, 31919, 24099, 2377, 31163, 18145, 12301, 23513, 17490, 22327, 2492, 30747, 27550, 21220, 28347, 15414, 4616, 12461, 29188, 19374, 17026, 7669, 1799, 29151, 24892]
    },
    "pack_data":	{
        "sign":	200,
        "detal":	800610,
        "theta":	1402263,
        "low_alpha":	104155,
        "high_alpha":	714571,
        "low_beta":	184040,
        "high_beta":	547557,
        "low_gamma":	161083,
        "middle_gamma":	875607,
        "attention":	74,
        "relex":	23
    }
}
"""


class ParametersToSave:

    def __init__(self):
        return

    def __del__(self):
        return