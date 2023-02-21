from numpy import matrix
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
        self.svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{abs(width)}"/>'


class NNVis:
    """
    Visualize a neural network. All you need are weights!
    """
    def __init__(self, weights = [
                        [[-120, 255, 0,111],
                         [140, -64, 99,50],
                         [64, 120, -32,-230]],
                        [[120, -99,32]]
                        ]):
            self.fromList(weights)
    def fromList(self,weights):
        #transposing the weights to make it easier to match them to lines later
        transposed_weights = [matrix(w).T.tolist() for w in weights]
        weights = transposed_weights
        self.weights = transposed_weights

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
        layer_width = (viewbox_width - 2 * x_padding) / (num_layers)
        cx_list =[x_padding + i * layer_width for i in range(num_layers+1)]


        node_count_iter = iter(node_counts)
        nodes = []
        cy_list_list = []
        node_gap_y = (viewbox_height - 2 * y_padding) / max(node_counts)
        for cx in cx_list:
            num_nodes = next(node_count_iter)

            node_col_height = num_nodes * node_gap_y - 2 * y_padding 
            y_start_point = (viewbox_height - node_col_height) / 2
            cy_list =[y_start_point + i * node_gap_y for i in range(num_nodes)]
            cy_list_list.append(cy_list)
            for cy in cy_list:
                nodes.append(Node(cx,cy))
        self.nodes = nodes

        lines = []
        cx_iter = iter(cx_list)
        cy_iter = iter(cy_list_list)
        node_count_iter = iter(node_counts)
        x1 = next(cx_iter)
        y_list_1 = next(cy_iter)
        for w in weights:
            x2 = next(cx_iter)
            y_list_2 = next(cy_iter)
            
            row_iter = iter(w)
            for y1 in y_list_1:
                weight_row = next(row_iter)
                for y2,weightval in zip(y_list_2, weight_row):
                    line_width = weightval / maxweight
                    lines.append(Line(x1,y1,x2,y2,line_width))
            x1 = x2
            y_list_1 = y_list_2
        self.lines = lines
    
        svg = '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        for line in self.lines:
            svg += line.svg
        for node in self.nodes:
            svg += node.svg
        svg += '</svg>'

        self.svg = svg

    def writeSvg(self,filepath='example.svg'):
        with open(filepath,'w') as f:
            f.write(self.svg)

if __name__ == "__main__":  
    nnvis = NNVis()
