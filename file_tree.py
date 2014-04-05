#!/usr/bin/python -B
################################################################################
# Copyright 2014 Phil Smith
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
################################################################################
# @Title: file_tree.py
#
# @Author: Phil Smith
#
# @Date: Fri, 04-Apr-14 08:50PM
#
# @Project: Scripts
#
# @Purpose: Create a 'dot' digraph of the folder tree rooted at the given
#           directory.
#
# Exit Codes:
# 1 - No root directory specified
# @Revision:
# $Id: $
#
################################################################################
import os
import sys
import argparse

#
# main: The main entry point for the file tree browser.
#{
def main( args ):
  """
  This function is the main entry point for the file tree browser.
  """
  
  #
  # Assign the parsed arguments.
  #
  if args.root:
    root_dir = args.root
    while '/' == root_dir[-1]:
      root_dir = root_dir[:-1]
  else:
    print "Starting directory must be specified with '-r or --root'"
    exit(1)

  # If no output is specified, assume ROOT + ".dot"
  if args.output:
    file_name = args.output
  else:
    file_name = root_dir + ".dot"

  # Default shape will be 'folder'
  # valid_shapes taken from: www.graphviz.org/doc/info/shapes.html
  valid_shapes = ["box", "ellipse", "circle", "point", "egg", "triangle",
                  "doublecircle", "house", "diamond", "plaintext", "none",
                  "hexagon", "octagon", "tab", "note"]
                   
  if args.shape in valid_shapes:
    shape = args.shape
  else:
    if args.shape != None:
      print "Unknown shape type: " + args.shape
    shape = "folder"
    print "Using default shape: " + shape

  unvisited_nodes = [root_dir]
  visited_nodes = []
  number = 0
  node_to_name = {}
  name_to_node = {}

  while( len(unvisited_nodes) > 0 ):
     current = unvisited_nodes.pop()
     uid = "node_" + str(number)
     number += 1

     # Create nodes in the tree.
     node = (uid, current)

     children = []
     for child in os.listdir(current):
        path = os.path.join(current, child)
        if os.path.isdir( path ):
           children.append(path)
           node_to_name[uid] = children
           unvisited_nodes.append( path )
     visited_nodes.append(node)

  for node in visited_nodes:
     name_to_node[node[1]] = node[0]

  out_file = open( file_name, 'w' )
#
# Write the opening graph information
#
  
  out_file.write( "digraph G\n{\n")
  for name in name_to_node.keys():
    #
    #  Create drawing rules for nodes
    #
    node = name_to_node[name]
    if name == root_dir:
      outline = "blue"
    else:
      outline = "black"
    
    label = os.path.split(name)[-1]
    out_file.write( node + '[shape=' + shape + 
                           ',color=' + outline +
                           ',label="' + label + '"];\n')

  for node in node_to_name:
    current = node_to_name[node]
    for each in current:
      #
      # Create rules for edges here
      #
      out_file.write( node + "->" + name_to_node[each] + ";\n")
#
# Write the closing graph information
#
  out_file.write("}\n")
  out_file.close()

#}
# End of main()
#

#
# Invocation Check:
#
if __name__ == "__main__":
  #
  # Parse the command line arguments
  # 
  descStr="""
  Create a file containing graph data formatted for the 'dot' utility.
  """
  progName = sys.argv[0]
  parser = argparse.ArgumentParser(prog=progName ,description=descStr)
  parser.add_argument('-r','--root', help='Folder from which to start the search.')
  parser.add_argument('-o','--output', help='Name of the output file.')
  parser.add_argument('-s','--shape', help='Shape used to represent the folders.')
  args = parser.parse_args()


  main( args )
