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

    def getNode_svg(self, node_height, node_width, margin_x, margin_y, node_font_size, sizeDataBox, node_radius):
        y = (self.step)*(node_height+2*margin_y) + margin_y
        x = self.pos*(node_width+2*margin_x) + margin_x + sizeDataBox

        rect = f'<rect x="{x}" y="{y}" width="{node_width}" height="{node_height}" rx="{node_radius}" ry="{node_radius}" style="fill:rgb(173,216,230);stroke-width:3;stroke:rgb(0,0,0)"\n/>'

        y_text_label = y+node_height/4

        text_label = f'<text x="{x+node_width/2}" y="{y_text_label}" font-size="{node_font_size}" text-anchor="middle" alignment-baseline="middle">label={self.label}</text>\n'

        y_text_items = y+node_height/4*3

        text_items = f'<text x="{x+node_width/2}" y="{y_text_items}" font-size="{node_font_size}" text-anchor="middle" alignment-baseline="middle">n_items={len(self.object.event_ids)}</text>\n'


        return rect+text_label+text_items

    def getLine_svg(self, node_height, node_width, margin_x, margin_y, node_font_size, sizeDataBox, rule_text):
        line_width = 20
        p_node = self.parent
        if p_node is None:
            return ""
        y1 = (self.step)*(node_height+2*margin_y) + margin_y
        y2 = y1 - 2*margin_y
        x1= self.pos*(node_width+2*margin_x) + margin_x + sizeDataBox + node_width/2
        x2 = p_node.pos*(node_width+2*margin_x) + margin_x + sizeDataBox + node_width/2

        lines_of_text = self.splitText(rule_text, line_width)

        line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:rgb(100,255,100);stroke-width:2" />\n'

        # precheck to prevent errors
        if self.parent and self.parent.parent:
            # check if parent is the same as grandparent --> no new rule was learned
            if self.parent.parent_label == self.parent_label: 
                rect_height = 1*node_font_size/2
                rect_width = line_width*node_font_size/3*0.925
                rect_x = (x1+x2)/2-rect_width/2
                rect_y = (y1+y2)/2-rect_height/2
                rect = f'<rect x="{rect_x}" y="{rect_y}" width="{rect_width}" height="{rect_height}" fill="grey" stroke="black" stroke-width="1" />\n'
                return line+rect

        rect_height = len(lines_of_text)*node_font_size/2
        rect_width = line_width*node_font_size/3*0.925
        rect_x = (x1+x2)/2-rect_width/2
        rect_y = (y1+y2)/2-rect_height/2
        rect = f'<rect x="{rect_x}" y="{rect_y}" width="{rect_width}" height="{rect_height}" fill="grey" stroke="black" stroke-width="1" />\n'
        texts=""
        for i, text_line in enumerate(lines_of_text):
            texts += f'<text x="{rect_x}" y="{rect_y+i*node_font_size/2}" alignment-baseline="hanging" font-size="{node_font_size/2}">{text_line}</text>\n'
        return line+rect+texts
    def splitText(self, text, n):
        # split text into words
        words = text.split(" ")
        lines = []
        i = 0
        curr_line = ""
        n_of_words = 0
        while i < len(words):
            if len(curr_line+" "+words[i]) <= n:
                curr_line += " "+words[i]
                i += 1
                n_of_words += 1
            elif n_of_words == 0:
                lines.append(words[i])
                i += 1
            else:
                lines.append(curr_line)
                curr_line = words[i]
                n_of_words = 1
                i+=1
        if curr_line != "":
            lines.append(curr_line)
        return lines
        

    def getWidth(self, last_level):
        if self.step == last_level:
            return 1
        return sum([child.getWidth(last_level) for child in self.children])

class TreePrinter():
    # variables for visualisation with SVG
    node_height = 40
    node_width = 100
    node_margin_x = 15
    node_margin_y = 35
    node_font_size = 10
    node_radius = 5
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
        root_el = {
           'dispersal': 0.,
            'impurity': 1.,
            'target': 0.,
            'score': 0.
        }
        if self.treeHistory[0]['score'] > 0:
            self.treeHistory.insert(0, root_el)

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
        self.svg_representation += f'<svg height="{self.height}" width="{self.width}" style="background-color:white">\n'
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
        self.svg_representation += f'  SVG not supported\n</svg>'

    # draw nodes
    def _drawNodes(self, node):
        if node.step != self.last_level:
            for child in node.children:
                self._drawNodes(child)
        self.svg_representation += node.getNode_svg(self.node_height, self.node_width,self.node_margin_x, self.node_margin_y, self.node_font_size, self.sizeDataBox, self.node_radius)

    # draw lines
    def _drawLines(self, node):
        if node.step != self.last_level:
            for child in node.children:
                self._drawLines(child)
        self.svg_representation += node.getLine_svg(self.node_height, self.node_width,self.node_margin_x, self.node_margin_y, self.node_font_size, self.sizeDataBox,str(node.object.step_rule))
    
    # add metrics
    def _addMetrics(self):
        for i, val in enumerate(self.treeHistory):
            dis = val['dispersal']
            imp = val['impurity']
            score = val['score']

            y_center = i*(self.node_height+2*self.node_margin_y)+self.node_margin_y+self.node_height/2

            newRule = self.treeHistory

            r1 = f'<text dominant-baseline = "central" font-size="{self.node_font_size}" style = "fill: rgb(0,0,255); " >'
            r2 = f'<tspan x = "10" y = "{y_center-18}"> step={i}\n </tspan>'
            r3 = f'<tspan x = "10" y = "{y_center-6}"> dis={dis:.5f}\n </tspan>'
            r4 = f'<tspan x = "10" y = "{y_center+6}" > imp={imp:.5f}\n </tspan>'
            r5 = f'<tspan x = "10" y = "{y_center+18}"> score={score:.5f}\n </tspan>'
            r6 = f'</text>'



            self.svg_representation += r1+r2+r3+r4+r5+r6
