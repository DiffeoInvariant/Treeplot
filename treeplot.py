#!/usr/bin/python3

import matplotlib.pyplot as plt
from math import radians, sin, cos
import argparse
#from numba import njit

class TreePlotter(object):

    
    def __init__(self, **kwargs):

        self.lines = None
        self.hausdorff_dimension = None
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.title = None
        
        self.parser = None
        from_args = kwargs.get('from_args',False)

        self.plot_in_ctor = False
        if from_args:
            self._build_arg_parser()
            self._extract_args()
        else:
            self.line_width = kwargs.get('line_width',0.25)
            self.plot_width = kwargs.get('plot_width',10)
            self.plot_height = kwargs.get('plot_height',10)
            self.root_len = kwargs.get('root_len', 1.0)
            self.scale_factor = kwargs.get('scale_by',0.6)
            self.root_coord = kwargs.get('root', [0.5*self.plot_width, 0.0])
            self.left_angle = kwargs.get('left_angle', 90.0)
            self.right_angle = kwargs.get('right_angle', 90.0)
            self.tree_depth = kwargs.get('depth', 10)
            self.plot_in_ctor = kwargs.get('plot_from_options', False)

        self.ax.set_xlim([0,self.plot_width])
        self.ax.set_ylim([0,self.plot_height])

        #self.lines maps a Line to a tuple of two Lines, (left child, right child)
        # (basically a binary tree implemented with a hash table)
        self.lines = {'root' : self.Line(self.root_coord[0], self.root_coord[1],
                                    self.root_len, self.right_angle, True, True, True)}

        if self.plot_in_ctor:
            self.add_lines_to_depth()
            self.plot_all_lines()
            self.show()
        


    def add_lines_to_depth(self, depth=None, left_angle_deg=None, right_angle_deg=None):
        if depth is not None:
            self.tree_depth = depth

        for i in range(self.tree_depth - 1):
            self.add_lines_to_leaves(left_angle_deg, right_angle_deg)
            


    def plot_line(self, line):
        xs, ys = line.plot_coords()
        self.ax.plot(xs, ys, linewidth=self.line_width, color='black')

    def plot_lines_from(self, from_line):
        if from_line == 'root':
            ln = self.lines[from_line]
            self.plot_line(ln)
            self.plot_lines_from(ln)
            
            
        elif not from_line.is_leaf:
            left, right = self.lines[from_line]
            self.plot_line(left)
            self.plot_line(right)

            self.plot_lines_from(left)
            self.plot_lines_from(right)
            
              
    def plot_all_lines(self):
        self.plot_lines_from('root')
                

    def title(self, title=None):
        if title is not None:
            self.title = title
        self.ax.title(self.title)
        
    def show(self):
        plt.show()
        

    def get_child_lines(self, leaf_line, angle_degs_left=None, angle_degs_right=None):
        if angle_degs_left is None:
            angle_degs_left = self.left_angle
        if angle_degs_right is None:
            angle_degs_right = self.right_angle

        
        new_length = self.scale_factor * leaf_line.length
        new_startx, new_starty = leaf_line.midpoint()
        left = self.Line(new_startx, new_starty, new_length, angle_degs_left, False, True, not leaf_line.vertical)
        right = self.Line(new_startx, new_starty, new_length, angle_degs_right, True, True, not leaf_line.vertical)
        leaf_line.set_leaf(False)
        return left, right


    def add_lines_to_leaves(self, angle_degs_left=None, angle_degs_right=None):
        lines_to_add = []
        for (par, children) in self.lines.items():
            if isinstance(children, self.Line):
                if children.is_leaf:
                    lines_to_add.append((children, self.get_child_lines(children, angle_degs_left, angle_degs_right)))
            else:
                for child in children:
                    if child.is_leaf:
                        lines_to_add.append((child, self.get_child_lines(child, angle_degs_left, angle_degs_right)))
        for (p, c) in lines_to_add:
            self.lines[p] = c



    #def add_all_lines_to_plot(self):
    #    for 

    class FromFile(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            with values as fl:
                parser.parse_args(fl.read().split(), namespace)
                
    def _build_arg_parser(self):
        self.parser = argparse.ArgumentParser(description='Parse tree plot options')
        self.parser.add_argument('--depth', '-d',
                                 help='Tree depth to plot to', type=int)
        self.parser.add_argument('--left_angle', '-la',
                                 help='Angle to use for left/down lines in degrees',
                                 type=float)
        self.parser.add_argument('--right_angle','-ra',
                                 help='Angle to use for right/up lines in degrees',
                                 type=float)
        self.parser.add_argument('--plot_width', '-pw',
                                 help='plot width',
                                 type=float)
        self.parser.add_argument('--plot_height', '-ph',
                                 help='plot height',
                                 type=float)
        self.parser.add_argument('--root_length','-rl',
                                 help='length of root line',
                                 type=float)
        self.parser.add_argument('--scale_factor','-s',
                                 help='scale new line lengths by this factor',
                                 type=float)
        self.parser.add_argument('--root', '-r',
                                 help='coordinates to use for the root line',
                                 type=float, nargs=2)
        self.parser.add_argument('--file','-f',
                                 help='Filename to read options from',
                                 type=open, action=self.FromFile)
        self.parser.add_argument('--plot_from_options', '-p',
                                 help='generate the plot in the constructor from given options',
                                 action='store_true')
        self.parser.add_argument('--title', '-t',
                                 help='title for the plot', type=str)
        self.parser.add_argument('--line_width', '-lw',
                                 help='width of lines in plot',
                                 type=float)

    def _extract_args(self):
        args = self.parser.parse_args()
        if args.depth:
            self.tree_depth = args.depth
        if args.left_angle:
            self.left_angle = args.left_angle
        if args.right_angle:
            self.right_angle = args.right_angle
        if args.plot_width:
            self.plot_width = args.plot_width
        if args.plot_height:
            self.plot_height = args.plot_height
        if args.root_length:
            self.root_len = args.root_length
        if args.scale_factor:
            self.scale_factor = args.scale_factor
        if args.root:
            self.root_coord = args.root
        if args.plot_from_options:
            self.plot_in_ctor = True
        if args.title:
            self.title = args.title
        if args.line_width:
            self.line_width = args.line_width

    def to_options_file(self, filename):
        ops_string = f"--tree_depth {self.tree_depth} "\
                     f"--left_angle {self.left_angle} "\
                     f"--right_angle {self.right_angle} "\
                     f"--root_length {self.root_len} "\
                     f"--scale_factor {self.scale_factor} "\
                     f"--root {self.root_coord} "\
                     f"--plot_width {self.plot_width} "\
                     f"--plot_height {self.plot_height} "
        if self.plot_from_options:
            ops_string.join("--plot_from_options ")
        if self.title:
            ops_string.join(f"--title {self.title} ")
        
        with open(filename, 'w') as ops_file:
            ops_file.write(ops_string)
            

    
    class Line(object):
                 

        def __init__(self, startx=0.0, starty=0.0, length=1, angle_degree=0.0, is_right=True, is_leaf=False, vertical=False):

            self.vertical = vertical
                                     
            #convert angle to the standard reference frame (from the
            # measurements shown in the pset)
            if is_right:
                if self.vertical:
                    angle = angle_degree
                else:
                    angle = angle_degree - 90.0
            else:
                if self.vertical:
                    angle = -angle_degree
                else:
                    angle = 270.0 - angle_degree
                                     
            self.startpt = [startx, starty]
            self.endpt = [startx + length * cos(radians(angle)), starty + length * sin(radians(angle))]
            self.length = length
            self.angle = radians(angle)
            self.is_leaf = is_leaf
            


        def plot_coords(self):
            return [self.startpt[0], self.endpt[0]], [self.startpt[1], self.endpt[1]]


        def set_leaf(self, is_leaf=True):
            self.is_leaf = is_leaf

        def start(self):
            return self.startpt

        def end(self):
            return self.endpt

        def midpoint(self):
                 return [0.5*(self.startpt[0] + self.endpt[0]), 0.5*(self.startpt[1] + self.endpt[1])]

        def compute_endpoint(self, set_endpoint=True, return_endpoint=True):
            x = self.length * cos(self.angle)
            y = self.length * sin(self.angle)
            if set_endpoint:
                self.endpt = (x,y)

            if return_endpoint:
                return (x,y)

        def rotate(self, new_angle, is_degrees=True):
            if is_degrees:
                self.angle = radians(new_angle)
            else:
                self.angle = float(new_angle)

            self.compute_endpoint(True, False)
            
            



if __name__ == '__main__':
    tree_plotter = TreePlotter(from_args=True)
