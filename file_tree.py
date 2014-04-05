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
# @Revision:
# $Id: $
#
################################################################################
import os

#
# main: The main entry point for the file tree browser.
#
def main():
  """
  This function is the main entry point for the file tree browser.
  """

  #
  # Find all of the directories and their children.
  #
  root_dir = "foo"

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
#          print "path = " + path
#          print "child = " + child
#          print "parent = " + current
#          print "parent uid = " + uid
#          print
           children.append(path)
           node_to_name[uid] = children
           unvisited_nodes.append( path )
     visited_nodes.append(node)

  for node in visited_nodes:
     name_to_node[node[1]] = node[0]

  for name in name_to_node.keys():
    node = name_to_node[name]
    #
    #  Create drawing rules for nodes
    #
    # ___appstatII_CVS [shape=folder,label="CVS", fill=Green];
    print node + '[shape=folder,label="' + node + '", fill=Green];'
  for node in node_to_name:
    #print node + ":"
    current = node_to_name[node]
    for each in current:
    # print name_to_node[each]
      print node + "->" + name_to_node[each] + ";"
      #
      # Create rules for edges here
      #

#
# Invocation Check:
#
if __name__ == "__main__":
  main()

