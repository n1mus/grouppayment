"""
A bunch of friends payed for a bunch of things, and now we have to split the bills and
figure out who owes whom what, in a simplified number of transactions
"""

import sys
import argparse
import numpy as np



#############################################################
############################################################
class Graph:

    tol = 1e-4 # roundoff error

    def __init__(self, nodeNames, deposits):
        self.nodeNames = nodeNames
        self.deposits = deposits
        self.nNodes = len(nodeNames)
        self.nodes = []
        self.matrix = np.ndarray((self.nNodes, self.nNodes)) * np.nan
        self.originalMatrix = self.matrix.copy()

        self.__setupBidirectionalAdjMatrix()
        self.__consolidateBidirectionalAdjMatrix()

        self.__setupUnidirectionalGraph()

    def __setupBidirectionalAdjMatrix(self):
        """
        Split up each deposit into the number of people
        Every other person owes that much to the depositor
        For each owe, make arrow towards depositor with that split amount
        :return:
        """
        self.matrix = np.ndarray((self.nNodes,self.nNodes)) * 0

        for i in range(self.nNodes):
            for j in range(self.nNodes):
                if i == j:
                    self.matrix[i,j] = np.nan
                else:
                    self.matrix[i,j] = self.deposits[j]/self.nNodes


    def __consolidateBidirectionalAdjMatrix(self):
        """
        Given the bidirectional graph repped by adj matrix
        Simplify it by consolidating any two arrows between any two nodes
        :return:
        """
        for i in range(self.nNodes):
            for j in range(i+1,self.nNodes):
                difference = self.matrix[i,j] - self.matrix[j,i]
                self.matrix[i,j] = difference if difference > 0 else 0
                self.matrix[j,i] = -difference if difference < 0 else 0
        # save original adj matrix
        self.originalMatrix = self.matrix.copy()


    def __setupUnidirectionalGraph(self):
        """
        Given the unidirectional graph repped by adj matrix
        Turn it into node+edge ds
        :return:
        """
        for i in range(self.nNodes):
            self.nodes.append(Node(self.nodeNames[i],i))

        # create non-0 edges
        for i in range(self.nNodes):
            for j in range(self.nNodes):
                if i == j or self.matrix[i,j] == 0:
                    continue
                edge = Edge(self.nodes[i], self.nodes[j], self.matrix[i,j])
                self.nodes[i].addOutgoingEdge(edge)
                self.nodes[j].addIncomingEdge(edge)


    def deleteEdge(self, edge):
        edge.parent.deleteOutgoingEdge(edge)
        edge.child.deleteIncomingEdge(edge)


    def reverseEdge(self, edge):
        edge.reverse()


    def passOnTriangleOp(self):
        for primNode in self.nodes:
            for interimNode in primNode.getChildren():
                for tertNode in interimNode.getChildren():
                    if primNode.isConnected(tertNode):
                        moveWeight = primNode.getEdge(interimNode).weight
                        interimNode.getEdge(tertNode).changeWeight(-moveWeight)
                        self.deleteEdge(primNode.getEdge(interimNode))

                        if primNode.isParent(tertNode):
                            primNode.getEdge(tertNode).changeWeight(moveWeight)
                        elif primNode.isChild(tertNode):
                            primNode.getEdge(tertNode).changeWeight(-moveWeight)
                        else:
                            assert False

                        self.checkNegZeroEdges()

                        return True
        return False


    def passOnHigherPolygonOp(self):
        """
        TODO
        Prove necessary? Algo?
        Handle pass-ons in configurations more complicated than a triangle
        :return:
        """
        pass


    def checkNegZeroEdges(self):
        for node in self.nodes:
            for edge in node.outgoingEdges:
                if edge.weight == 0:
                    self.deleteEdge(edge)
                elif edge.weight < 0:
                    self.reverseEdge(edge)


    def __updateAdjMatrix(self):
        """
        Reset the internal adjacency matrix
        Use graph ds to repopulate
        :return:
        """
        self.matrix = self.matrix * 0
        for i in range(self.nNodes):
            for child in self.nodes[i].getChildren():
                self.matrix[i,child.id] = self.nodes[i].getEdge(child).weight


    def totalFlow(self, matrix, id):
        totalFlow = 0
        for k in range(self.nNodes):
            if k == id:
                continue
            totalFlow = totalFlow + matrix[id,k] - matrix[k,id]
        return totalFlow


    def verifyFinalGraph(self):
        # verify total flow is same before and after simplification
        for i in range(self.nNodes):
            originalFlow = self.totalFlow(self.originalMatrix,i)
            finalFlow = self.totalFlow(self.matrix,i)
            assert abs(originalFlow - finalFlow) <= self.tol, \
                "Node " + str(i) + ", Total flow original " + str(self.totalFlow(self.originalMatrix,i)) + "\n" + \
                "Node " + str(i) + ", Total flow simplified " + str(self.totalFlow(self.matrix,i))


    def print(self):
        self.__updateAdjMatrix()
        print(self.nodeNames)
        print(self.matrix)


    def prettyPrint(self):
        self.__updateAdjMatrix()
        print("\n")
        for i in range(self.nNodes):
            for j in range(self.nNodes):
                if self.matrix[i,j] > 0:
                    print(self.nodeNames[i], 'gives', self.nodeNames[j], str(self.matrix[i,j]))
                elif self.matrix[i,j] < 0:
                    assert False
        print('\n')

################################################################
#########################################################
class Node:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.outgoingEdges = []
        self.incomingEdges = []

    def addOutgoingEdge(self, edge):
        self.outgoingEdges.append(edge)

    def addIncomingEdge(self, edge):
        self.incomingEdges.append(edge)

    def deleteOutgoingEdge(self, edge):
        self.outgoingEdges.remove(edge)

    def deleteIncomingEdge(self, incomingEdge):
        self.incomingEdges.remove(incomingEdge)

    def getEdge(self, other):
        for edge in self.outgoingEdges:
            if edge.child == other:
                return edge
        for edge in self.incomingEdges:
            if edge.parent == other:
                return edge

    def sumOutgoing(self):
        sum = 0
        for outgoingEdge in self.outgoingEdges:
            sum = sum + outgoingEdge.weight
        return sum

    def sumIncoming(self):
        sum = 0
        for incomingEdge in self.incomingEdges:
            sum = sum + incomingEdge.weight
        return sum

    def totalFlow(self):
        return self.sumOutgoing() - self.sumIncoming()

    def reverseEdge(self, edge):
        if edge in self.outgoingEdges:
            self.outgoingEdges.remove(edge)
            self.incomingEdges.append(edge)
        elif edge in self.incomingEdges:
            self.incomingEdges.remove(edge)
            self.outgoingEdges.append(edge)


    def getChildren(self):
        children = []
        for edge in self.outgoingEdges:
            children.append(edge.child)
        return children

    def getParents(self):
        parents = []
        for edge in self.incomingEdges:
            parents.append(edge.parent)
        return parents

    def isConnected(self, other):
        if self.getChildren().count(other) + self.getParents().count(other) > 0:
            return True
        return False

    def isChild(self, other):
        return other in self.getParents()

    def isParent(self, other):
        return other in self.getChildren()

    def __eq__(self, other):
        return self.name == other.name


############################################################
#############################################################
class Edge:
    """
    Edge remembers both parent and child
    Edge is remembered by both parent and child
    """
    def __init__(self, parent, child, weight):
        self.parent = parent
        self.child = child
        self.weight = weight

    def __eq__(self, other):
        if self.weight != other.weight or self.parent != other.parent or self.child != other.child:
            return False
        return True

    def changeWeight(self, change):
        self.weight = self.weight + change

    def reverse(self):
        temp = self.parent
        self.parent = self.child
        self.child = temp
        self.weight = -self.weight

        self.child.reverseEdge(self)
        self.parent.reverseEdge(self)










def main(names = ["B","R","K","Je","Jo","S"],
         deposits = [1500,300,60,60,150,36]):



    graph = Graph(names,deposits)

    print("ORIGINAL UNIDIRECTIONAL GRAPH")
    graph.print()

    print('Working',end='')
    while graph.passOnTriangleOp():
        print('.',end='')
    print()

    print("SIMPLIFIED GRAPH")
    graph.print()
    graph.prettyPrint()

    graph.verifyFinalGraph()

















if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Names and deposits")

    parser.add_argument('--names', metavar='names', dest='names', type=str, nargs='+',
                        required=True, help='Names of people')
    parser.add_argument('--deposits', metavar='deposits', dest='deposits', type=float, nargs='+',
                        required=True, help='Deposits made by corresponding people')

    args = parser.parse_args()

    if len(args.names) != len(args.deposits):
        print("Error: Number of names must equal number of deposits")
        parser.print_help()
        sys.exit()


    print(args.names)
    print(args.deposits)


    main(args.names, args.deposits)
    print("\n\n\n----- done -----")


