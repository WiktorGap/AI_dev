#include <map>
#include <iostream>
#include <set>
#include <queue>
#include <vector> 
using namespace std;

int main()
{
    char actualPoint;
    char target = 'F'; 
    char start = 'A';  

    set<char> vistedPoints;
    map<char, vector<char>> graph;
    map<char, char> parent; 
    vector<char> childs;
    queue<char> q;

    graph['A'] = {'B', 'C'};
    graph['B'] = {'D', 'E'};
    graph['C'] = {'F'};
    graph['D'] = {};
    graph['E'] = {'F'};
    graph['F'] = {};

    q.push(start);
    vistedPoints.insert(start);

    bool found = false; 

    while (!q.empty())
    {
        actualPoint = q.front();
        q.pop();
        childs = graph[actualPoint];

        for (const char& child : childs)
        {
            if (vistedPoints.find(child) == vistedPoints.end())
            {
                parent[child] = actualPoint; 
                q.push(child);
                vistedPoints.insert(child);

                if (child == target)
                {
                    found = true;
                    break; 
                }
            }
        }
        if (found) break; 
    }


    if (found)
    {
        vector<char> path;
        char current = target;
        while (current != start)
        {
            path.push_back(current);
            current = parent[current];
        }
        path.push_back(start);

        cout << "Sciezka do " << target << ": ";
        for (int i = path.size() - 1; i >= 0; --i)
        {
            cout << path[i];
            if (i > 0) cout << " -> ";
        }
        cout << endl;
    }
    else
    {
        cout << "Nie znaleziono sciezki do " << target << endl;
    }

    return 0;
}
