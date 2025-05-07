#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <stack>
#include <algorithm>  

using namespace std;

map<char,vector<char>> graph;



void dfs(map<char,vector<char>> graph, char root, char target)
{
    vector<char> path;
    set<char> visited; 
    char actualPoint;
    stack<char> stack;
    vector<char> childs;
    map<char, char> parent; 

    stack.push(root);
    while(!stack.empty())
    {
        actualPoint = stack.top();
        stack.pop();

        if(visited.find(actualPoint) == visited.end())
        {
            visited.insert(actualPoint);

            if(actualPoint == target)
            {

                while(actualPoint != root)
                {
                    path.push_back(actualPoint);
                    actualPoint = parent[actualPoint];
                }
                path.push_back(root);
                reverse(path.begin(), path.end());

                cout << "Znaleziono ścieżkę: ";
                for(char c : path)
                    cout << c << " ";
                cout << endl;
                return;
            }

            childs = graph[actualPoint];
            for(const char& child : childs)
            {
                if(visited.find(child) == visited.end())
                {
                    parent[child] = actualPoint;
                    stack.push(child);
                }
            }
        }
    }

    cout << "Nie znaleziono ścieżki." << endl;
}

int main()
{
    graph['A'] = {'B', 'C'};
    graph['B'] = {'D', 'E'};
    graph['C'] = {'F'};
    graph['D'] = {};
    graph['E'] = {'F'};
    graph['F'] = {};

    dfs(graph, 'A', 'F'); 

    return 0;
}
