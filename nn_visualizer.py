from numpy import linspace
import pdb

class Node:
    """
    Simple class representing the svg code for a single node
    """
    def __init__(self,cx,cy,r=3):
	    self.svg = f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'

class Line:
    """
    Simple class representing the svg code for a single line
    """
    def __init__(self,x1,y1,x2,y2,width):
        color = 'green' if width > 0 else 'red'
        self.svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


class NNVis:
    """
    Visualize a neural network. All you need are weights!
    """
    def __init__(self, weights='default'):
        if weights == 'default':
            weights = [
                        [[-120, 255, 0],
                         [140, -64, 99],
                         [64, 120, -32]],
                        [[120],
                         [-99],
                         [ 32]]
                    ]
        self.weights = weights

        node_counts = [len(w) for w in weights]
        node_counts.append(len(weights[-1][0]))

        #todo: introduce check to make sure valid weights are used

        maxweight = 0
        for w in weights:
            for row in w:
                maxweight = max(maxweight, max(row))
        self.maxweight = maxweight

        viewbox_height = 100
        viewbox_width = 100
        num_layers = len(weights)
        x_padding = 0
        y_padding = 10
        layer_width = viewbox_width / (num_layers + 1)

        cx_list = linspace(x_padding, viewbox_width-x_padding, num_layers+1)

        node_count_iter = iter(node_counts)
        nodes = []
        for cx in cx_list:
            cy_list = linspace(y_padding, viewbox_height-y_padding, next(node_count_iter))
            for cy in cy_list:
                nodes.append(Node(cx,cy))
        self.nodes = nodes

        lines = []
        cx_iter = iter(cx_list)
        node_count_iter = iter(node_counts)
        x1 = next(cx_iter)
        y_list_1 = linspace(y_padding, viewbox_height-y_padding, next(node_count_iter))
        for w in weights:
            x2 = next(cx_iter)
            y_list_2 = linspace(y_padding, viewbox_height-y_padding, next(node_count_iter))
            
            row_iter = iter(w)
            for y1 in y_list_1:
                weight_row = next(row_iter)
                for y2,weightval in zip(y_list_2, weight_row):
                    line_width = weightval / maxweight
                    lines.append(Line(x1,y1,x2,y2,line_width))
            x1 = x2
            y_list_1 = y_list_2
        self.lines = lines

    
    def visualize(self):
        print('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">')
        for line in self.lines:
            print(line.svg)
        for node in self.nodes:
            print(node.svg)
        print('</svg>')



if __name__ == "__main__":  
    nnvis = NNVis()
    nnvis.visualize()
