//#include "Common.h"
#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <string>
#include <cmath>
#include <ctime>
#include "myrand.h"

using namespace std;

struct Config{ //RB的参数 
    size_t n;
    double a,p,r;
};

struct Edge{
    public:
    int v1,v2;
    bool operator < (Edge const &temp) const 
    {
        return !((this->v1 == temp.v1) && (this->v2 == temp.v2));
    }
    
    Edge(Edge const &temp)
    {
        this->v1 = temp.v1;
        this->v2 = temp.v2;
    }
    
    Edge()
    {
        this->v1 = 0;
        this->v2 = 0;
    }
    
    Edge operator =(Edge const temp){
        this->v1 = temp.v1;
        this->v2 = temp.v2;
    }
};

inline int min(int a,int b)
{
    return (a > b) ? b : a;
}

vector<Edge> arrangeVertex(int n)
{
    vector<Edge> v;
    for(int i = 1 ; i <= n ; i++){
        for(int j = 1 ; j <= n ; j++){
            Edge e ;
            e.v1 = i;
            e.v2 = j;
            v.push_back(e);
        }
    }
    size_t size = v.size() ;
    while(size > 0){
        int_64 index = rand_int(10) % size;
        Edge e = v[index];
        v[index] = v[size - 1];
        v[size - 1] = e; 
        size--;
    }
    return v;
}

void RB_allowRepeat(Config const &conf,set<Edge> &res)//生成一个RB实例 
{
    size_t n = conf.n;
    double a = conf.a;
    double p = conf.p;
    double r = conf.r;
    int d = static_cast<int> (pow(n,a));
    int l1 = static_cast<int> (p * pow(n,2*a));
    int l2 = static_cast<int> (r * n * log(n) - 1);
    cout << d << "," << l1 << "," << l2 << endl;
    res.clear();
    for(int i = 0 ; i < l2 ; i++ ){
        int_64 n1 = rand_int(10) % n;
        int_64 n2 = rand_int(10) % n;
        while(n2 == n1){
            n2 = rand_int(10) % n;
        }
        vector<Edge> v = arrangeVertex(d);
        int size = min(v.size(),l1);
        for(int j = 0 ; j < size ; j++){
            Edge e;
            e.v1 = n1 * d + v[j].v1;
            e.v2 = n2 * d + v[j].v2;
            res.insert(e);
        }
    } 
    
}

int main(int argc,char **argv)
{
    string conffile = "rGraph_rb.conf";
    if(argc > 1){
        conffile = string(argv[1]);
    }
    srand(time(0));
    freopen(conffile.c_str(),"r",stdin);
    set<Edge> res;
    Config conf;
    char outfile[512];
    int num = 0;
    while(scanf("n=%d a=%lf p=%lf r=%lf\n",&conf.n,&conf.a,&conf.p,&conf.r) == 4){
        RB_allowRepeat(conf,res);
        sprintf(outfile,"rGraph_rb%d.out",num++);
        ofstream fout(outfile);
        int n = conf.n;
        int d = static_cast<int> (pow(n,conf.a) + 0.5);
        int size = d * conf.n;
        fout << "Size " << size << endl;
//        fout << "RB_d " << d << endl;
        /*for(int i = 0 ; i < n ; i++){ //输出团内的边 
            for(int j = 1 ; j <= d ; j++){
                for(int k = j + 1 ; k <= d ; k++ ){
                    fout << "e " <<i*d + j << " " << i*d + k << endl;
                }
            }
        } */
        set<Edge>::iterator it;
        for(it = res.begin() ; it != res.end() ; it++){ //输出团之间的边 
            fout << "e "<< it->v1 << " " << it->v2 << endl;
        }
    }
}
