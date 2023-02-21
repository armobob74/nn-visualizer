from nn_visualizer import NNVis

weights = [
    [[-120, 120],
     [64, 80],
     [-52, 85],
     [32, -70]],
    [
     [-120, -20, 140,32],
     ],
]
nnvis = NNVis(weights)
nnvis.writeSvg("example.svg")
