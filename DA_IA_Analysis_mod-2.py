#!/usr/bin/env python
# coding: utf-8

# In[24]:


import random

#評価軸のリストを作成
DA_s_noenvy_sum = 0
IA_s_noenvy_sum = 0
DA_c_noenvy_sum = 0
IA_c_noenvy_sum = 0
DA_s_utility_sum = 0
IA_s_utility_sum = 0
DA_c_utility_sum = 0
IA_c_utility_sum = 0
DA_stability_sum = 0
IA_stability_sum = 0
DA_judging_sum = 0
IA_judging_sum = 0
DA_s_matched_num_sum = 0
IA_s_matched_num_sum = 0
DA_s_anmatched_num_sum = 0
IA_s_anmatched_num_sum = 0

#学生の人数
S = 561

#研究室の数
C = 44

#研究室１つあたりの定員
CP = [13]*C

#試行回数
T = 2

#学生の選好に関わる相関パラメータ
α = 0.5

#研究室の選好に関わる相関パラメータ
β = 0.7

#学生が実際に応募できる研究室の数
apply_num = 2

print('学生数: {} 研究室数: {} 研究室の定員: 各{}人 応募できる研究室の数: {}'.format(S,C,CP[0],apply_num))
print('α: {} β: {} 試行回数: {}回'.format(α, β, T))
print()

count = 0
while count < T:
    
    #学生の選好式　SU = αCVj+(1-α)PVij
    #研究室jの人気度
    CV = []
    for i in range(C):
        CV.append(random.random())
    
    #学生iの研究室jに対する好みの度合い
    PV = []
    for i in range(S):
        pv = [random.random() for j in range(C)]
        PV.append(pv)
    
    #学生iの研究室jに対する効用
    SU = []
    for i in range(S):
        su = [(CV[j]*α)+(PV[i][j]*(1-α)) for j in range(C)]
        SU.append(su)
        
    #学生の選好
    s_prefs = []
    
    #効用の低い順のインデックスに並び替える
    for i in range(S):
        s_prefs.append([j[0] for j in sorted(enumerate(SU[i]), key=lambda x:x[1])])
    
    #効用の高い順に変換
    for i in range(S):
        s_prefs[i].reverse()
    
    #リストの要素に+1して選好を作成
    for i in range(S):
        for j in range(C):
            s_prefs[i][j] += 1
            
    #応募できる研究室だけの選好を作成
    for i in range(S):
        del s_prefs[i][apply_num:C]
    
    #研究室の選好式　CU = βSVi+(1-β)QVji
    #学生iの人気度
    SV = []
    for i in range(S):
        SV.append(random.random())
        
    #研究室jの学生iに対する好みの度合い
    QV = []
    for i in range(C):
        qv = [random.random() for j in range(S)]
        QV.append(qv)
        
    #研究室jの学生iに対する効用
    CU = []
    for i in range(C):
        cu = [(SV[j]*β)+(QV[i][j]*(1-β)) for j in range(S)]
        CU.append(cu)
    
    #研究室の選好
    c_prefs = []
    
    #効用の低い順のインデックスに並び替える
    for i in range(C):
        c_prefs.append([j[0] for j in sorted(enumerate(CU[i]), key=lambda x:x[1])])

    #効用の高い順に変換
    for i in range(C):
        c_prefs[i].reverse()
    
    #リストの要素に+1して選好を作成
    for i in range(C):
        for j in range(S):
            c_prefs[i][j] += 1
        
    #研究室の選好をランクに変換
    c_rank = [[0]*S for i in range(C)]
    for i in range(C):
        for j in range(S):
            k = c_prefs[i][j]
            c_rank[i][k-1] = j+1
                
    capacity = CP
    
    DA_s_matched = [0]*(S+1)
    IA_s_matched = [0]*(S+1)
    
    DA_c_matched = [[0]*(S+1) for i in range(C)]
    IA_c_matched = [[0]*(S+1) for i in range(C)]
    
    DA_num_match = 0
    IA_num_match = 0
    
    DA_s_filled = [0]*(S+1)
    IA_s_filled = [0]*(S+1)
    
    DA_c_filled = [0]*C
    IA_c_filled = [0]*C
    
    DA_position = [0]*(S+1)
    IA_position = [0]*(S+1)
    
    step = [0]*(S+1)
    
    DA_judging = 0
    IA_judging = 0
    
    while DA_num_match < S:
        for i in range(S):
            if DA_s_filled[i]==0:
                j = s_prefs[i][DA_position[i]]-1
                DA_judging += 1
                if DA_c_filled[j]<capacity[j]:
                    DA_c_matched[j][i] = 1
                    DA_s_matched[i] = j
                    DA_s_filled[i] = 1
                    DA_c_filled[j] += 1
                    DA_num_match += 1
                else:
                    n = -1
                    rej = S
                    for k in range(S):
                        if DA_c_matched[j][k]==1:
                            if c_rank[j][i]<c_rank[j][k] and c_rank[j][k]>n:
                                DA_s_filled[rej] = 1
                                DA_position[rej] -= 1
                                DA_c_matched[j][rej] = 1
                                DA_s_matched[rej] = j
                                DA_s_filled[k] = 0
                                DA_position[k] += 1
                                rej = k
                                DA_c_matched[j][k] = 0
                                n = c_rank[j][k]
                    if n != -1:
                        DA_c_matched[j][i] = 1
                        DA_s_matched[i] = j
                        DA_s_filled[i] = 1
                        if DA_position[rej]==apply_num:
                            DA_s_matched[rej] = -1
                            DA_s_filled[rej] = 1
                            DA_num_match += 1
                    else:
                        DA_position[i] += 1
                        if DA_position[i]==apply_num:
                            DA_s_matched[i] = -1
                            DA_s_filled[i] = 1
                            DA_num_match += 1
    
    t = 1
    while IA_num_match < S:
        for i in range(S):
            if IA_s_filled[i] ==0:
                j = s_prefs[i][IA_position[i]]-1
                IA_judging += 1
                if IA_c_filled[j]<capacity[j]:
                    IA_c_matched[j][i] = 1
                    IA_s_matched[i] = j
                    IA_s_filled[i] = 1
                    step[i] = t
                    IA_c_filled[j] += 1
                    IA_num_match += 1
                else:
                    n = -1
                    rej = S
                    for k in range(S):
                        if IA_c_matched[j][k]==1 and step[k]==t:
                            if c_rank[j][i]<c_rank[j][k] and c_rank[j][k]>n:
                                IA_s_filled[rej] = 1
                                IA_position[rej] -= 1
                                IA_c_matched[j][rej] = 1
                                IA_s_matched[rej] = j
                                step[rej] = t
                                IA_s_filled[k] = 0
                                IA_position[k] += 1
                                rej = k
                                IA_c_matched[j][k] = 0
                                step[k] = 0
                                n = c_rank[j][k]
                    if n != -1:
                        IA_c_matched[j][i] = 1
                        IA_s_matched[i] = j
                        IA_s_filled[i] = 1
                        step[i] = t
                        if IA_position[rej]==apply_num:
                            IA_s_matched[rej] = -1
                            IA_s_filled[rej] = 1
                            IA_num_match += 1
                    else:
                        IA_position[i] += 1
                        step[i] = 0
                        if IA_position[i]==apply_num:
                            IA_s_matched[i] = -1
                            IA_s_filled[i] = 1
                            IA_num_match += 1
        t += 1
        
    #都合上それぞれのs_matchedの最後の要素を削除
    del DA_s_matched[S]
    del IA_s_matched[S]
    
    #マッチできた学生の数
    DA_s_matched_num = S-(DA_s_matched.count(-1))
    IA_s_matched_num = S-(IA_s_matched.count(-1))
    
    #どこにもマッチできなかった学生の数
    DA_s_anmatched_num = DA_s_matched.count(-1)
    IA_s_anmatched_num = IA_s_matched.count(-1)

    #第一希望にマッチした学生の数, The number of students getting their first choice
    DA_s_noenvy = 0
    for i in range(S):
        if DA_s_matched[i] == s_prefs[i][0]-1:
            DA_s_noenvy += 1
            
    IA_s_noenvy = 0
    for i in range(S):
        if IA_s_matched[i] == s_prefs[i][0]-1:
            IA_s_noenvy += 1
            
    #学生の効用, Utility of the students
    DA_s_utility = 0
    for i in range(S):
        for j in range(apply_num):
            if DA_s_matched[i]+1 == s_prefs[i][j]:
                DA_s_utility += C-j
                
    IA_s_utility = 0
    for i in range(S):
        for j in range(apply_num):
            if IA_s_matched[i]+1 == s_prefs[i][j]:
                IA_s_utility += C-j
    
    #都合上それぞれのc_matchedの最後の要素を削除
    for i in range(C):
        del DA_c_matched[i][S]
        
    for i in range(C):
        del IA_c_matched[i][S]
    
    #第一希望にマッチした研究室の数, The number of laboratories getting their first choice
    DA_c_noenvy = 0
    for i in range(C):
        k = [l for l, x in enumerate(DA_c_matched[i]) if x==1]
        if c_prefs[i][0]-1 in k:
            DA_c_noenvy += 1
    
    IA_c_noenvy = 0
    for i in range(C):
        k = [l for l, x in enumerate(IA_c_matched[i]) if x==1]
        if c_prefs[i][0]-1 in k:
            IA_c_noenvy += 1
        
    #研究室の効用, Utility of the laboratories
    DA_c_utility = 0
    for i in range(C):
        k = [l for l, x in enumerate(DA_c_matched[i]) if x==1]
        for j in range(len(k)):
            for m in range(S):
                if k[j]==c_prefs[i][m]-1:
                    DA_c_utility += S-m
                    
    IA_c_utility = 0
    for i in range(C):
        k = [l for l, x in enumerate(IA_c_matched[i]) if x==1]
        for j in range(len(k)):
            for m in range(S):
                if k[j]==c_prefs[i][m]-1:
                    IA_c_utility += S-m
    
        
    #安定性（ブロッキング・ペアの数）, Stability: The number of Brocking pairs
    DA_stability = 0
    for i in range(S):
        for j in range(apply_num):
            if DA_s_matched[i]==s_prefs[i][j]-1:
                break
            else:
                k=s_prefs[i][j]-1
                for m in range(capacity[k]):
                    l=[n for n, x in enumerate(DA_c_matched[k]) if x==1]
                    if c_rank[k][i]<c_rank[k][l[m]]:
                        DA_stability+=1
                        break
    
    IA_stability = 0
    for i in range(S):
        for j in range(apply_num):
            if IA_s_matched[i]==s_prefs[i][j]-1:
                break
            else:
                k=s_prefs[i][j]-1
                for m in range(capacity[k]):
                    l=[n for n, x in enumerate(IA_c_matched[k]) if x==1]
                    if c_rank[k][i]<c_rank[k][l[m]]:
                        IA_stability+=1
                        break
    
    #1マッチング毎に集計結果をリストへ追加
    DA_s_noenvy_sum += DA_s_noenvy
    IA_s_noenvy_sum += IA_s_noenvy
    DA_c_noenvy_sum += DA_c_noenvy
    IA_c_noenvy_sum += IA_c_noenvy
    DA_s_utility_sum += DA_s_utility
    IA_s_utility_sum += IA_s_utility
    DA_c_utility_sum += DA_c_utility
    IA_c_utility_sum += IA_c_utility
    DA_stability_sum += DA_stability
    IA_stability_sum += IA_stability
    DA_judging_sum += DA_judging
    IA_judging_sum += IA_judging
    DA_s_matched_num_sum += DA_s_matched_num
    IA_s_matched_num_sum += IA_s_matched_num
    DA_s_anmatched_num_sum += DA_s_anmatched_num
    IA_s_anmatched_num_sum += IA_s_anmatched_num

    count += 1
    
print('第一希望にマッチした学生の数, The number of students getting their first choice')
print('DA: {} 平均値: {} 学生全体における割合: {}% マッチした学生における割合: {}%'.format(DA_s_noenvy_sum, DA_s_noenvy_sum/T,((DA_s_noenvy_sum/T)/S)*100, ((DA_s_noenvy_sum/T)/(DA_s_matched_num_sum/T))*100))
print('IA: {} 平均値: {} 学生全体における割合: {}% マッチした学生における割合: {}%'.format(IA_s_noenvy_sum, IA_s_noenvy_sum/T,((IA_s_noenvy_sum/T)/S)*100, ((IA_s_noenvy_sum/T)/(IA_s_matched_num_sum/T))*100))
print()
print('どこにもマッチできなかった学生の数, The number of students not getting any laboratories')
print('DA: {} 平均値: {} 割合: {}%'.format(DA_s_anmatched_num_sum, DA_s_anmatched_num_sum/T, ((DA_s_anmatched_num_sum/T)/S)*100))
print('IA: {} 平均値: {} 割合: {}%'.format(IA_s_anmatched_num_sum, IA_s_anmatched_num_sum/T, ((IA_s_anmatched_num_sum/T)/S)*100))
print()
print('第一希望にマッチした研究室の数, The number of laboratories getting their first choice')
print('DA: {} 平均値: {} 割合: {}%'.format(DA_c_noenvy_sum, DA_c_noenvy_sum/T, ((DA_c_noenvy_sum/T)/C)*100))
print('IA: {} 平均値: {} 割合: {}%'.format(IA_c_noenvy_sum, IA_c_noenvy_sum/T, ((IA_c_noenvy_sum/T)/C)*100))
print()
print('学生の効用, Utility of the students')
print('DA: {} 平均値: {} 比較値: {}'.format(DA_s_utility_sum, DA_s_utility_sum/T, (DA_s_utility_sum/T)/(DA_s_matched_num_sum/T)))
print('IA: {} 平均値: {} 比較値: {}'.format(IA_s_utility_sum, IA_s_utility_sum/T, (IA_s_utility_sum/T)/(IA_s_matched_num_sum/T)))
print()
print('研究室の効用, Utility of the laboratories')
print('DA: {} 平均値: {} 比較値: {}'.format(DA_c_utility_sum, DA_c_utility_sum/T, (DA_c_utility_sum/T)/(DA_s_matched_num_sum/T)))
print('IA: {} 平均値: {} 比較値: {}'.format(IA_c_utility_sum, IA_c_utility_sum/T, (IA_c_utility_sum/T)/(IA_s_matched_num_sum/T)))
print()
print('安定性（ブロッキング・ペアの数）, Stability: The number of Brocking pairs')
print('DA: {} 平均値: {}'.format(DA_stability_sum, DA_stability_sum/T))
print('IA: {} 平均値: {}'.format(IA_stability_sum, IA_stability_sum/T))
print()
print('容易性（面接回数）, Easiness: The number of interviews')
print('DA: {} 平均値: {}'.format(DA_judging_sum, DA_judging_sum/T))
print('IA: {} 平均値: {}'.format(IA_judging_sum, IA_judging_sum/T))


# In[ ]:




