import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 작업 디렉토리 지정
os.chdir('C:\\Users\\Msi\\Desktop\\공모전\\카드소비 프로젝트\\데이터')

# seaborn을 사용하여 그릴 때 배경을 바꿔준다.
# 배경을 바꾸게 되면 폰트가 초기화되기 때문에 폰트를 설정하기 전에 미리 설정해주도록 한다.
sns.set_style('darkgrid')

# 한글 폰트가 깨지기 때문에 폰트를 바꿔준다.
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

# 카드 소비데이터 가져오기 - PPT 12장 그림 1
pop = pd.read_csv('pop.csv')

jongno_name = ['청운효자동', '사직동', '삼청동', '부암동', '평창동', '무악동',
               '교남동', '가회동', '종로1.2.3.4가동', '종로5.6가동', '이화동',
               '혜화동', '창신1동', '창신2동', '창신3동', '숭인1동', '숭인2동']

nowon_name = ['월계1동', '월계2동', '월계3동', '공릉1동', '공릉2동', '하계1동',
              '하계2동', '중계본동', '중계1동', '중계4동', '중계2.3동', '상계1동',
              '상계2동', '상계3.4동', '상계5동', '상계6.7동', '상계8동', '상계9동', '상계10동']


mct_name = ['숙박(10)', '레저용품(20)', '레저업소(21)', '문화취미(22)', '가구(30)', '전기(31)', 
            '주방용구(32)', '연료판매(33)', '광학제품(34)', '가전(35)', '유통업(40)', '의복(42)',
            '직물(43)', '신변잡화(44)', '서적문구(50)', '사무통신(52)', '자동차판매(60)', '자동차정비(62)',
            '의료기관(70)', '보건위생(71)', '요식업소(80)', '음료식품(81)', '수리서비스(92)']

age_name = ['25세 미만', '25세~29세', '30세~34세', '35세~39세', '40세~44세',
            '45세~49세', '50세~54세', '55세~59세', '60세~64세', '65세 이상']

# 유동인구 데이터 이상치 확인
plt.figure(figsize=(12, 4))
sns.boxplot(x='DONG_CD', y='POP', data = pop)
plt.title('지역별 유동인구 boxplot', fontsize=17, position=(0.5, 1.05))
plt.axvline(x=16.5, color='r', linestyle='--')
plt.xlabel('종로구                                                          노원구', fontsize = 15)
plt.ylabel('유동인구', fontsize=15)
plt.xticks(rotation=60)
plt.show()

# 유동인구 데이터 이상치 확인 - PPT 17장 그림 1
plt.figure(figsize=(12, 4))
sns.boxplot(x='DONG_CD', y='POP', data = pop)
plt.title('지역별 유동인구 boxplot', fontsize=17, position=(0.5, 1.05))
plt.axvline(x=16.5, color='r', linestyle='--')
plt.xlabel('종로구                                                          노원구', fontsize = 15)
plt.ylabel('유동인구', fontsize=15)
plt.ylim(0, 15000)
plt.xticks(rotation=60)
plt.show()


dong_name = jongno_name + nowon_name

# 유동인구 이상치 제거 - PPT 18장 그림 1
pop_outlier = pd.DataFrame()
def pop_outlier_remove(dong_name):
    pop_dong = pop[pop['DONG_CD'] == dong_name]
    Q1 = pop_dong['POP'].quantile(q=0.25)
    Q3 = pop_dong['POP'].quantile(q=0.75)
    IQR = Q3 - Q1
    step = 1.5 * IQR
    outlier_remove = pop_dong[(pop_dong['POP'] > Q1 - step) & 
                              (pop_dong['POP'] < Q3 + step)]
    return outlier_remove

pop_outlier = pd.concat([pop_outlier_remove(i) for i in dong_name])

# 유동인구 이상치 제거 후 길이 비교 - PPT 18장 그림 2
plt.figure(figsize=(3, 4))
g = sns.barplot(['제거 전', '제거 후'], [len(pop), len(pop_outlier)])
g.annotate(len(pop), (g.patches[0].get_x() + g.patches[0].get_width() / 2., g.patches[0].get_height()), ha = 'center', va = 'center', xytext = (0, 4), textcoords = 'offset points')
g.annotate(len(pop_outlier), (g.patches[1].get_x() + g.patches[1].get_width() / 2., g.patches[1].get_height()), ha = 'center', va = 'center', xytext = (0, 4), textcoords = 'offset points')
plt.show()

# 유동인구 이상치 제거 후 데이터 저장
pop_outlier.to_csv('pop_outlier.csv', index=False)
