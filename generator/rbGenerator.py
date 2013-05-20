#!/usr/bin/env python


import sys
import math
import random
import getopt
import argparse

#put information at the header of the benchmark file
def print_comment(n, a, p, r):
    print "c graph  baced on rb Model"
    print "c parameter n=" + str(n) + " a=" + str(a) + " p=" + str(p) + " r=" + str(r)
    print "c "
    print "c by fang zhiwen(zhiwenf@gmail.com)"
    print "c "

#output the graph(vertices and edges)
#c comment
#c comment
#p edge V E 
#e v1 v2
#...
#e vi vj
#
def output_graph(n, d, edges):
    vnum = n * d
    enum = n * d * (d - 1) / 2
    for v1 in range(0, n):
        for v2 in range(v1+1,n):
            edges[v1][v2] = list(set(edges[v1][v2]))
            enum = enum + len(edges[v1][v2])
    # print the graph in dimacs graph formate
    # the vertex is indexed from 1,2,3,...,...
    print "p edge", vnum, enum
    for v1 in range(0, n):
        for x1 in range(0, d):
            for x2 in range(x1+1, d):
                print "e", v1*d + x1 + 1, v1*d + x2 + 1
        for v2 in range(v1, n):
            for e in edges[v1][v2]:
                print "e", v1*d+e[0] + 1, v2*d+e[1] + 1

#generate a graph baced on RB model without hiding optimum solution
#n, a, p, r are the paramters in RB model
def generate_without_hos(n, a, p, r):
    d = int(pow(n, a) + 0.5)
    l1 = int(p * pow(n, 2 * a) + 0.5)
    l2 = int(r * n * math.log(n) + 0.5)
    #print "d", d ,"l1",l1, "l2", l2
    edges=[[[] for v1 in range(0, n)] for v2 in range(0, n)]    
#random selecton a pair of variable for l2 times
    var_list = range(0, n)
    for ll2 in range(0, l2):
        v1, v2 = random.sample(var_list, 2)
        if v2 < v1:
            t = v1
            v1 = v2
            v2 = t

        for ll1 in range(0, l1):
            d1 = random.randint(0,d-1)
            d2 = random.randint(0, d-1)
            edges[v1][v2].append((d1, d2))
    print_comment(n, a, p, r)
    output_graph(n, d, edges)

#generate a solution in the graph random
#i.e keep a consistent assignment between each pair of variables
def hide_solution(n, d):
    sol = set()
    for v1 in range(0, n):
        for v2 in range(v1+1, n):
            x1 = random.randint(0, d-1)
            x2 = random.randint(0, d-1)
            sol.add((v1 * n + x1, v2 * n + x2))
    return sol

#generate a graph baced on RB model with hiding optimum solution
#n, a, p, r are the paramters in RB model    
def generate_with_hos(n, a, p, r):
    
    d = int(pow(n, a) + 0.5)
    
    l1 = int(p * pow(n, 2 * a) + 0.5)
    l2 = int(r * n * math.log(n) + 0.5)
    
    edges=[[[] for v1 in range(0, n)] for v2 in range(0, n)]    
#random selecton a pair of variable for l2 times
    var_list = range(0, n)
    sol = hide_solution(n, d)
    all_relation = []
    for x in range(0, d):
        for y in range(0, d):
            all_relation.append((x, y))

    for ll2 in range(0, l2):
        v1, v2 = random.sample(var_list, 2)
        if v2 < v1:
            t = v1
            v1 = v2
            v2 = t
        nogoods = random.sample(all_relation, l1+1)
        conflict_with_sol = False
        for e in nogoods[1:]:
            x1 = v1 * n + e[0]
            x2 = v2 * n + e[1]
            if (x1, v2) not in sol:
                edges[v1][v2].append(e)
            else:
                conflict_with_sol = True
        if conflict_with_sol:
            edges.append(nogoods[0])
    print_comment(n, a, p, r)
    output_graph(n, d, edges)
#generator an instance baced on RB
#hide: indicate to hide an optimum solution or not
#n, a, p, r: parameter in RB model
def generate(hide, n, a, p, r):
    if hide :
    #generate instance with hidden optimum solution
        generate_with_hos(n, a, p, r)
    else :
    #generate instance without hidded optimum solution
        generate_without_hos(n, a, p, r)
    
def main():
    #parse command parameters  
    parser = argparse.ArgumentParser(description="Generate graph baced on RB model")
    parser.add_argument('-n', metavar='integer', type=int,  help="integer N: the number of variable in RB model")
    parser.add_argument("-a", metavar='float', type=float, help="float a(alpha): the parameter a(alpha) in RB model")
    parser.add_argument("-p", metavar='float', type=float, help="float p: the parameter p in RB model")
    parser.add_argument("-r", metavar='float', type=float, help="float r: the parameter r in RB model")
    parser.add_argument('--hide', action='store_true', help="hide(default false):hide an optimum solution or not")
    parser.add_argument('-s', '--seed',metavar="int",  action='store', type=int, help="s(seed): seed for random number generator, default is current system time")
    args = vars(parser.parse_args())
    #all the parameters in RB model should be assigned a value
    if args["n"] == None:
        print "-n can not be empty"
        sys.exit(1)
    if args["a"] == None:
        print "-a can not be empty"
        sys.exit(1)
    if args["p"] == None:
        print "-p can not be empty"
        sys.exit(1)
    if args["r"] == None:
        print "-r can not be empty"
        sys.exit(1)
    random.seed(args["seed"]) # seed will be none if not using the -s(--seed) option
    generate(args["hide"], args["n"], args["a"], args["p"], args["r"])

if __name__ == "__main__":
    main()
