class TreeNode():
    def __init__(self, label, parent_label, object, step, parent, children):
        self.label = label
        self.parent_label = parent_label
        self.object = object
        self.step = step
        self.parent = parent
        self.children = children
    
    def __repr__(self):
        return f"TreeNode [{self.label}]"
    
    def append_child(self, child_node):
        self.children.append(child_node)
    
    def set_parent(self, parent_node):
        self.parent = parent_node

    def getNode_svg(self, node_height, node_width, margin_x, margin_y, node_font_size, sizeDataBox):
        y = (self.step)*(node_height+2*margin_y) + margin_y
        x = self.pos*(node_width+2*margin_x) + margin_x + sizeDataBox
        return f'<rect x="{x}" y="{y}" width="{node_width}" height="{node_height}" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />\n<text x="{x+node_width/2}" y="{y+node_height/2}" font-size="{node_font_size}" text-anchor="middle" alignment-baseline="middle">{self.label}</text>\n'

    def getLine_svg(self, node_height, node_width, margin_x, margin_y, node_font_size, sizeDataBox):
        p_node = self.parent
        if p_node is None:
            return ""
        y1 = (self.step)*(node_height+2*margin_y) + margin_y
        y2 = y1 - 2*margin_y
        x1= self.pos*(node_width+2*margin_x) + margin_x + sizeDataBox + node_width/2
        x2 = p_node.pos*(node_width+2*margin_x) + margin_x + sizeDataBox + node_width/2
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:rgb(100,255,100);stroke-width:2" />\n'

    def getWidth(self, last_level):
        if self.step == last_level:
            return 1
        return sum([child.getWidth(last_level) for child in self.children])

class TreePrinter():
    # variables for visualisation with SVG
    node_height = 20
    node_width = 30
    node_margin_x = 20
    node_margin_y = 10
    node_font_size = 10
    sizeDataBox = 100
    


    def __init__(self, root, last_level, treeHistory):
        self.root = root
        self._steps_taken_on_last_level = 0
        self.svg_representation = ""
        self.last_level = last_level
        self.width = root.getWidth(self.last_level)
        self.treeHistory = treeHistory
        #self.vertical = vertical

        # add first element to treeHistory
        #root_el = {
        #    'dispersal': 0.,
        #    'impurity': 1.,
        #    'target': 0.,
        #    'score': 1.
        #}
        #self.treeHistory.insert(0, root_el)

        # for vertical tree
        self.width = self.sizeDataBox + (2*self.node_margin_x + self.node_width) * self.width
        self.height = (2*self.node_margin_y +
                       self.node_height) * (last_level+1)

    def print_tree_svg(self):
        self._steps_taken_on_last_level = 0
        self.svg_representation = ""
        self._assignPos(self.root)
        self._getStartSVG()
        self._addMetrics()
        self._drawLines(self.root)
        self._drawNodes(self.root)
        self._getEndSVG()

        # save svg
        with open("tree.svg", "w") as f:
            f.write(self.svg_representation)
    # assign positions to nodes
    def _assignPos(self, node):
        if node.step == self.last_level:
            node.pos = self._steps_taken_on_last_level
            self._steps_taken_on_last_level += 1
            return
        for child in node.children:
            self._assignPos(child)
        if len(node.children)>1:
            node.pos = (node.children[0].pos + node.children[1].pos) / 2
        elif len(node.children)==1:
            node.pos = node.children[0].pos
        else:
            raise Exception("No children found")
    
    # get start of SVG
    def _getStartSVG(self):
        # header
        self.svg_representation += f'<!DOCTYPE html>\n<html>\n<body>\n<svg height="{self.height}" width="{self.width}">\n'
        self.svg_representation

        # structure
        # horizontal lines
        for i in range(self.last_level):
            y = (i+1)*(self.node_height+2*self.node_margin_y)
            self.svg_representation += f'<line x1="{0}" y1="{y}" x2="{self.width}" y2="{y}" style="stroke:rgb(255,100,100);stroke-width:2" />\n'

        # vertical line
        self.svg_representation += f'<line x1="{self.sizeDataBox}" y1="{0}" x2="{self.sizeDataBox}" y2="{self.height}" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        

    # get end of SVG
    def _getEndSVG(self):
        self.svg_representation += f'  SVG not supported\n</svg>\n</body>\n</html>'

    # draw nodes
    def _drawNodes(self, node):
        if node.step != self.last_level:
            for child in node.children:
                self._drawNodes(child)
        self.svg_representation += node.getNode_svg(self.node_height, self.node_width,self.node_margin_x, self.node_margin_y, self.node_font_size, self.sizeDataBox)

    # draw lines
    def _drawLines(self, node):
        if node.step != self.last_level:
            for child in node.children:
                self._drawLines(child)
        self.svg_representation += node.getLine_svg(self.node_height, self.node_width,self.node_margin_x, self.node_margin_y, self.node_font_size, self.sizeDataBox)
    
    # add metrics
    def _addMetrics(self):
        for i, val in enumerate(self.treeHistory):
            dis = val['dispersal']
            imp = val['impurity']
            score = val['score']

            y_center = i*(self.node_height+2*self.node_margin_y)+self.node_margin_y+self.node_height/2

            r1 = f'<text dominant-baseline = "central" font-size="{self.node_font_size}" style = "fill: rgb(0,0,255); " >'
            r2 = f'<tspan x = "0" y = "{y_center-12}"> dis={dis:.5f}\n </tspan>'
            r3 = f'<tspan x = "0" y = "{y_center}" > imp={imp:.5f}\n </tspan>'
            r4 = f'<tspan x = "0" y = "{y_center+12}"> score={score:.5f}\n </tspan>'
            r5 = f'</text>'



            self.svg_representation += r1+r2+r3+r4+r5
