#include <bits/stdc++.h>
using namespace std;

map<string, int> ma;
int main()
{
    #ifndef  ONLINE_JUDGE
      freopen("tweet_links.txt", "r", stdin);
    #endif

    string st;
    int N, ans = 0, i;

    cin >> N;
    for(i=1; i<=N; i++)
    {
       cin >> st;
       if( !ma[st] )
       {
           ma[st] = 1;
           ans++;
       }
       else
       {
           cout << i << endl;
       }
    }
    cout << ans;

    return 0;
}
